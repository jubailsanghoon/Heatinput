import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 페이지 설정 및 디자인 테마 ---
st.set_page_config(page_title="Heat Input Master", layout="wide")

color_bg = "#F2F2F2"      
color_white = "#FFFFFF"   
color_line = "#000000"    
color_orange = "#FF6B00"
color_pass = "#28A745"
color_fail = "#DC3545"

if 'history' not in st.session_state: st.session_state.history = []

# CSS 주입: '-' 버튼 왼쪽 배치 및 오렌지 윤곽선 정밀 시공
st.markdown(f"""
    <style>
    .stApp {{ background-color: {color_bg}; color: {color_line}; }}
    
    /* 타이틀 및 주황색 수평선 밀착 시공 */
    .header-container {{ padding-top: 5px; display: flex; align-items: center; margin-bottom: 0px; }}
    .orange-divider {{ border-bottom: 5px solid {color_orange}; margin-top: 2px; margin-bottom: 20px; width: 100%; }}
    .title-text {{ font-size: 2.3rem; font-weight: 900; margin-left: 15px; }}

    /* [요청 핵심] 숫자 입력창 내부 버튼 재배치 ([-] [Input] [+]) */
    div[data-testid="stNumberInputContainer"] {{
        background-color: #4A3728 !important; 
        border: 3px solid {color_orange} !important;
        border-radius: 8px !important;
        height: 55px !important;
        display: flex !important;
        align-items: center !important;
    }}
    
    /* 입력창 내부 숫자 스타일 */
    div[data-testid="stNumberInputContainer"] input {{
        color: {color_orange} !important;
        font-size: 1.4rem !important;
        font-weight: 900 !important;
        text-align: center !important;
        background-color: transparent !important;
        border: none !important;
    }}

    /* [-], [+] 버튼 크기 및 위치 조정 */
    button[data-testid="baseButton-secondary"] {{
        background-color: transparent !important;
        color: {color_orange} !important;
        border: none !important;
        font-size: 24px !important;
        font-weight: 900 !important;
        min-width: 45px !important;
    }}
    
    /* 사이드바 WPS 입력창 폭 60% */
    section[data-testid="stSidebar"] .stNumberInput {{ width: 85% !important; }}

    /* [공정 버튼] 2줄 그리드, 얇고 길게 (폭 200%, 높이 60%) */
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] {{
        display: flex !important;
        flex-wrap: wrap !important;
        gap: 10px !important;
    }}
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label {{
        flex: 0 0 calc(50% - 5px) !important;
        min-height: 42px !important;
        background-color: {color_white} !important;
        color: {color_line} !important;
        border: 2.5px solid {color_orange} !important;
        padding: 5px !important;
        border-radius: 8px !important;
    }}
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label[data-checked="true"] {{
        background-color: {color_line} !important;
    }}
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label[data-checked="true"] p {{
        color: {color_orange} !important;
    }}

    /* [입력창 밸런스] 라벨+입력창 1줄, 입력창 폭 60% */
    .input-row {{ display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }}

    /* [결과 박스] 높이 축소 (40%) 및 상하 분리 */
    .result-value-box {{
        background-color: {color_white};
        border: 3px solid {color_orange};
        height: 55px !important;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.8rem;
        font-weight: 900;
        margin-bottom: 8px;
    }}
    .result-status-box {{
        height: 48px !important;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.4rem;
        font-weight: 900;
        border: 2.5px solid {color_line};
        color: {color_white};
    }}

    .save-action-box {{ border: 2.5px solid {color_line}; padding: 12px; background-color: #E6E6E6; border-radius: 8px; margin-top: 15px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. 헤더 영역 (로고 및 타이틀) ---
logo_url = "https://raw.githubusercontent.com/jubailsanghoon/Heatinput/main/db65c0d39f36f2dddc248ea0bf2e4efc.jpg"

st.markdown('<div class="header-container">', unsafe_allow_html=True)
col_logo, col_title = st.columns([1, 8])
with col_logo:
    st.image(logo_url, width=80) 
with col_title:
    st.markdown(f'<span class="title-text">Heat Input Master</span>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="orange-divider"></div>', unsafe_allow_html=True)

# --- 3. 사이드바 (규격 및 WPS 설정) ---
with st.sidebar:
    st.markdown("### 📜 Standard Selection")
    # Standard 선택 버튼 크기를 Number Input과 동일하게 설정
    std_mode = st.radio("Std", options=['ISO', 'AWS'], label_visibility="collapsed")
    
    st.markdown("<br>### ⚙️ WPS range", unsafe_allow_html=True)
    w_min = st.number_input("Min", value=1.0, step=0.1, format="%.1f")
    w_max = st.number_input("Max", value=2.5, step=0.1, format="%.1f")
    
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.write("**Admin:** jubail.sanghoon@gmail.com")

# --- 4. 메인 대시보드 (3열 밸런스) ---
col1, col2, col3 = st.columns([1.1, 1.2, 0.9])

# [섹션 1] Select Process (2줄 그리드 슬림화)
with col1:
    st.markdown("### 1. Select Process")
    proc = st.radio("P", options=['SAW', 'FCAW', 'SMAW', 'GMAW'], horizontal=True, label_visibility="collapsed")
    k = 1.0 if std_mode == 'AWS' or proc == 'SAW' else 0.8

# [섹션 2] Input Parameters (1줄 평평한 정렬, 폭 60%)
with col2:
    st.markdown("### 2. Input Parameters")
    
    def render_row(label, val, step, key):
        r_c1, r_c2 = st.columns([5, 5])
        r_c1.markdown(f"<div style='margin-top:15px; font-weight:900;'>{label}</div>", unsafe_allow_html=True)
        return r_c2.number_input(label, value=val, step=step, format="%.1f", label_visibility="collapsed", key=key)

    v = render_row("Voltage (V)", 28.0, 0.5, "v_m")
    a = render_row("Amperage (A)", 220.0, 5.0, "a_m")
    l = render_row("Length (mm)", 150.0, 10.0, "l_m")
    t = render_row("Time (Sec)", 120.0, 1.0, "t_m")
    
    speed = (l / t) * 60 if t > 0 else 0

# [섹션 3] Live Result & Save
with col3:
    st.markdown("### 3. Live Result")
    hi = (k * v * a * t) / (l * 1000) if l > 0 else 0
    is_pass = w_min <= hi <= w_max
    
    st.markdown(f'<div class="result-value-box">{hi:.3f} kJ/mm</div>', unsafe_allow_html=True)
    st_bg = color_pass if is_pass else color_fail
    st.markdown(f'<div class="result-status-box" style="background-color:{st_bg};">{"PASS" if is_pass else "FAIL"}</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="save-action-box">', unsafe_allow_html=True)
    if st.button("💾 SAVE LOG DATA", use_container_width=True):
        st.session_state.history.insert(0, {
            "Time": datetime.now().strftime("%H:%M:%S"),
            "Proc": proc, "V": v, "A": a, "L": l, "T": t,
            "HI": f"{hi:.3f}", "Status": "PASS" if is_pass else "FAIL"
        })
        st.toast("Success: Logged")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. 히스토리 데이터 ---
if st.session_state.history:
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.table(pd.DataFrame(st.session_state.history).head(10))