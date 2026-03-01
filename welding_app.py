import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 페이지 설정 및 디자인 테마 ---
st.set_page_config(page_title="Heat Input Master", layout="wide")

# UI 컬러 가이드: 주황색 완전 배제
color_bg = "#F2F2F2"      # 연회색 배경
color_white = "#FFFFFF"   # 흰색
color_line = "#000000"    # 검은색 라인
color_pass = "#28A745"    # 합격(녹색)
color_fail = "#DC3545"    # 불합격(적색)

if 'history' not in st.session_state: st.session_state.history = []

# CSS 주입: 모노톤 테마 및 버튼 좌우 분리 시공
st.markdown(f"""
    <style>
    .stApp {{ background-color: {color_bg}; color: {color_line}; }}
    
    /* 타이틀 및 상단 검은색 수평선 */
    .header-container {{ padding-top: 5px; display: flex; align-items: center; margin-bottom: 0px; }}
    .black-divider {{ border-bottom: 5px solid {color_line}; margin-top: 2px; margin-bottom: 25px; width: 100%; }}
    .title-text {{ font-size: 2.3rem; font-weight: 900; margin-left: 15px; }}

    /* [요청] 숫자 입력창 내부 버튼 재배치 ([-] 왼쪽, [+] 오른쪽) */
    div[data-testid="stNumberInputContainer"] {{
        background-color: {color_white} !important; 
        border: 2px solid {color_line} !important; /* 검은색 라인으로 변경 */
        border-radius: 4px !important;
        height: 55px !important;
        display: flex !important;
        align-items: center !important;
    }}
    
    div[data-testid="stNumberInputContainer"] input {{
        color: {color_line} !important;
        font-size: 1.4rem !important;
        font-weight: 900 !important;
        text-align: center !important;
        background-color: transparent !important;
    }}

    /* 사이드바 및 입력창 버튼 스타일 */
    button[data-testid="baseButton-secondary"] {{
        color: {color_line} !important;
        font-size: 24px !important;
        font-weight: 900 !important;
        min-width: 45px !important;
    }}
    
    section[data-testid="stSidebar"] .stNumberInput {{ width: 85% !important; }}

    /* [공정 버튼] 2줄 그리드, 얇고 길게 (Black & White) */
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] {{
        display: flex !important;
        flex-wrap: wrap !important;
        gap: 10px !important;
    }}
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label {{
        flex: 0 0 calc(50% - 5px) !important;
        min-height: 42px !important;
        background-color: {color_white} !important;
        border: 2px solid {color_line} !important;
        padding: 5px !important;
        border-radius: 4px !important;
    }}
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label[data-checked="true"] {{
        background-color: {color_line} !important;
    }}
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label[data-checked="true"] p {{
        color: {color_white} !important;
    }}

    /* [입력창 밸런스] 라벨+입력창 1줄 */
    .input-row {{ display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }}

    /* [결과 박스] 모노톤 박스 분리 */
    .result-value-box {{
        background-color: {color_white};
        border: 3px solid {color_line};
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
        border: 2px solid {color_line};
        color: {color_white};
    }}

    .save-action-box {{ border: 2px solid {color_line}; padding: 12px; background-color: #E6E6E6; margin-top: 15px; }}
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
st.markdown('<div class="black-divider"></div>', unsafe_allow_html=True) # 주황색 대신 검은색 선

# --- 3. 사이드바 (규격 및 WPS 설정) ---
with st.sidebar:
    st.markdown("### 📜 Standard Selection")
    std_mode = st.radio("Std", options=['ISO', 'AWS'], label_visibility="collapsed")
    
    st.markdown("<br>### ⚙️ WPS range", unsafe_allow_html=True)
    w_min = st.number_input("Min", value=1.0, step=0.1, format="%.1f")
    w_max = st.number_input("Max", value=2.5, step=0.1, format="%.1f")
    
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.write("**Admin:** jubail.sanghoon@gmail.com")

# --- 4. 메인 대시보드 (3열 밸런스) ---
col1, col2, col3 = st.columns([1.1, 1.2, 0.9])

# [섹션 1] Select Process (모노톤 그리드)
with col1:
    st.markdown("### 1. Select Process")
    proc = st.radio("P", options=['SAW', 'FCAW', 'SMAW', 'GMAW'], horizontal=True, label_visibility="collapsed")
    k = 1.0 if std_mode == 'AWS' or proc == 'SAW' else 0.8

# [섹션 2] Input Parameters (1줄 정렬, 소수점 1자리)
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
        st.toast("Logged")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. 히스토리 데이터 ---
if st.session_state.history:
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.table(pd.DataFrame(st.session_state.history).head(10))