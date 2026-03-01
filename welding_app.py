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
if 'step' not in st.session_state: st.session_state.step = 1

# CSS 주입: 규격/입력창 크기 통일 및 공정 버튼 2단 슬림화
st.markdown(f"""
    <style>
    .stApp {{ background-color: {color_bg}; color: {color_line}; }}
    
    /* 타이틀 및 주황색 수평선 여백 최소화 */
    .header-container {{ padding-top: 5px; display: flex; align-items: center; margin-bottom: 0px; }}
    .orange-divider {{ border-bottom: 5px solid {color_orange}; margin-top: 0px; margin-bottom: 20px; width: 100%; }}
    .title-text {{ font-size: 2.3rem; font-weight: 900; margin-left: 15px; }}

    /* [요청 1] Standard 선택 버튼을 WPS 입력창 크기와 동일하게 (높이 55px, 주황 테두리) */
    /* [요청 3] WPS range 및 모든 숫자 입력창 주황색 윤곽선 */
    div.stNumberInput input, div[role="radiogroup"] label {{
        background-color: #4A3728 !important; /* 고대비 다크 브라운 */
        color: {color_orange} !important;
        border: 3px solid {color_orange} !important;
        height: 55px !important; /* 높이 통일 */
        font-size: 1.2rem !important;
        font-weight: 900 !important;
        border-radius: 8px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }}
    
    /* [요청 2] 1. Select Process: 2줄로 얇고 길게, 글자 한 줄 유지 */
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] {{
        display: flex !important;
        flex-wrap: wrap !important;
        gap: 8px !important;
    }}
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label {{
        flex: 0 0 calc(50% - 5px) !important; /* 2열 배치 */
        min-height: 40px !important;           /* "얇게" 조절 */
        padding: 5px !important;
        background-color: {color_white} !important;
        color: {color_line} !important;
        border: 2px solid {color_orange} !important;
    }}
    /* 선택 시 반전 */
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label[data-checked="true"] {{
        background-color: {color_line} !important;
        border-color: {color_line} !important;
    }}
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label[data-checked="true"] p {{
        color: {color_orange} !important;
    }}
    div[role="radiogroup"] label p {{ white-space: nowrap !important; font-size: 1rem !important; }}

    /* [요청 5] Input Parameters 1줄 정렬 및 폭 60% */
    .input-row-container {{ display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; }}

    /* [요청 6] Live Result 박스 높이 40% 축소형 및 분리 */
    .result-value-box {{
        background-color: {color_white};
        border: 3px solid {color_orange};
        height: 55px !important; 
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.8rem;
        font-weight: 900;
        margin-bottom: 5px;
    }}
    .result-status-box {{
        height: 45px !important;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.3rem;
        font-weight: 900;
        border: 2px solid {color_line};
        color: {color_white};
    }}

    .save-box {{ border: 2px solid {color_line}; padding: 10px; background-color: #E0E0E0; border-radius: 8px; margin-top: 10px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. 타이틀 및 로고 (GitHub Raw 링크) ---
logo_url = "https://raw.githubusercontent.com/jubailsanghoon/Heatinput/main/db65c0d39f36f2dddc248ea0bf2e4efc.jpg"

st.markdown('<div class="header-container">', unsafe_allow_html=True)
col_l, col_t = st.columns([1, 8])
with col_l:
    st.image(logo_url, width=80) 
with col_t:
    st.markdown(f'<span class="title-text">Heat Input Master</span>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="orange-divider"></div>', unsafe_allow_html=True)

# --- 3. 사이드바 (WPS range) ---
with st.sidebar:
    st.markdown("### 📜 Standard")
    # Standard 버튼 크기를 Number Input과 동일하게 CSS로 처리됨
    std_mode = st.radio("Std", options=['ISO', 'AWS'], label_visibility="collapsed")
    
    st.markdown("<br>### ⚙️ WPS range", unsafe_allow_html=True)
    # 폭 60% 유지
    w_min = st.number_input("Min", value=1.0, step=0.1, format="%.1f")
    w_max = st.number_input("Max", value=2.5, step=0.1, format="%.1f")
    
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.write("**Contact:** jubail.sanghoon@gmail.com")
    mobile_mode = st.toggle("📱 Mobile Wizard Mode", value=False)

# --- 4. 메인 UI (3열 밸런스) ---
if not mobile_mode:
    c1, c2, c3 = st.columns([1, 1.2, 1])

    # 1. Select Process (2줄 얇고 길게)
    with c1:
        st.markdown("### 1. Select Process")
        proc = st.radio("P", options=['SAW', 'FCAW', 'SMAW', 'GMAW'], horizontal=True, label_visibility="collapsed")
        k = 1.0 if std_mode == 'AWS' or proc == 'SAW' else 0.8

    # 2. Input Parameters (1줄 평평하게, 폭 60%, 소수점 1자리)
    with c2:
        st.markdown("### 2. Input Parameters")
        def param_row(label, val, step, key):
            r1, r2 = st.columns([5, 5])
            r1.markdown(f"<div style='margin-top:15px; font-weight:900;'>{label}</div>", unsafe_allow_html=True)
            return r2.number_input(label, value=val, step=step, format="%.1f", label_visibility="collapsed", key=key)

        v = param_row("Voltage (V)", 28.0, 0.5, "v_pc")
        a = param_row("Amperage (A)", 220.0, 5.0, "a_pc")
        l = param_row("Length (mm)", 150.0, 10.0, "l_pc")
        t = param_row("Time (Sec)", 120.0, 1.0, "t_pc")
        speed = (l / t) * 60 if t > 0 else 0

    # 3. Live Result & Save
    with c3:
        st.markdown("### 3. Live Result")
        hi = (k * v * a * t) / (l * 1000) if l > 0 else 0
        is_pass = w_min <= hi <= w_max
        
        st.markdown(f'<div class="result-value-box">{hi:.3f} kJ/mm</div>', unsafe_allow_html=True)
        s_bg = color_pass if is_pass else color_fail
        st.markdown(f'<div class="result-status-box" style="background-color:{s_bg};">{"PASS" if is_pass else "FAIL"}</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="save-box">', unsafe_allow_html=True)
        if st.button("💾 SAVE LOG DATA", use_container_width=True):
            st.session_state.history.insert(0, {
                "Time": datetime.now().strftime("%H:%M:%S"),
                "Proc": proc, "V": f"{v:.1f}", "A": f"{a:.1f}",
                "HI": f"{hi:.3f}", "Status": "PASS" if is_pass else "FAIL"
            })
            st.toast("Data Saved")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 5. 상세 히스토리 ---
if st.session_state.history:
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.table(pd.DataFrame(st.session_state.history).head(10))