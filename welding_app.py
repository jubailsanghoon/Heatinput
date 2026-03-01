import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 페이지 설정 및 테마 ---
st.set_page_config(page_title="Heat Input Master", layout="wide")

color_bg = "#F2F2F2"
color_white = "#FFFFFF"
color_line = "#000000"
color_pass = "#28A745"
color_fail = "#DC3545"

if 'history' not in st.session_state: st.session_state.history = []

# --- 2. CSS 정밀 레이아웃 (가독성 보정) ---
st.markdown(f"""
    <style>
    /* 전체 배경 */
    .stApp {{ background-color: {color_bg}; color: {color_line}; }}
    
    /* [핵심] 가변 폰트 시스템: 화면 폭에 따라 글자 크기가 유연하게 변함 */
    :root {{
        --font-size-master: clamp(1rem, 4vw, 1.5rem);
        --font-size-result: clamp(1.4rem, 6vw, 2.2rem);
    }}

    .master-label {{
        font-size: var(--font-size-master) !important;
        font-weight: normal !important;
        color: {color_line} !important;
        margin-bottom: 5px !important;
        line-height: 1.2 !important;
    }}

    /* [섹션 0] 헤더 타이틀 */
    .title-text {{
        font-size: clamp(1.4rem, 5vw, 2.3rem);
        font-weight: bold;
        margin-left: 10px;
    }}

    /* [섹션 2] 공정 버튼 (2x2 그리드 & 가변 텍스트) */
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] {{
        display: grid !important; 
        grid-template-columns: repeat(2, 1fr) !important; 
        gap: 8px !important;
    }}
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label {{
        min-height: 50px !important;
        height: auto !important; /* 글자가 많아지면 늘어나게 설정 */
        border: 2px solid {color_line} !important;
        background-color: {color_white} !important;
        padding: 5px !important;
    }}
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label p, 
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label span {{
        font-size: var(--font-size-master) !important;
        text-align: center !important;
    }}

    /* [섹션 3] 입력창 (모바일 줄바꿈 방지 및 좌우 버튼 고정) */
    div[data-testid="stNumberInputContainer"] {{
        display: flex !important;
        flex-direction: row !important;
        height: 55px !important;
        background-color: {color_white} !important;
        border: 2px solid {color_line} !important;
        overflow: hidden !important;
    }}
    div[data-testid="stNumberInputContainer"] > button {{
        min-width: 45px !important;
        font-size: 1.2rem !important;
        border: none !important;
    }}
    div[data-testid="stNumberInputContainer"] input {{
        font-size: var(--font-size-master) !important;
        padding: 0 !important;
    }}

    /* [섹션 4] Live Result 가독성 극대화 */
    .result-value-box {{
        background-color: {color_white};
        border: 3px solid {color_line};
        min-height: 65px;
        display: flex; align-items: center; justify-content: center;
        font-size: var(--font-size-result);
        font-weight: bold;
        border-radius: 4px;
        padding: 5px;
    }}
    .result-status-box {{
        height: 50px !important;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.4rem;
        font-weight: bold;
        color: {color_white};
        border-radius: 4px;
    }}

    /* [모바일 전용] 여백 최적화 */
    @media (max-width: 768px) {{
        .stColumn {{ padding: 0 !important; margin-bottom: 20px !important; }}
        div[data-testid="stHorizontalBlock"] {{ gap: 0.5rem !important; }}
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. 헤더 영역 ---
st.markdown('<div class="header-container">', unsafe_allow_html=True)
c1, c2 = st.columns([1, 8])
with c1: st.image("https://raw.githubusercontent.com/jubailsanghoon/Heatinput/main/db65c0d39f36f2dddc248ea0bf2e4efc.jpg", width=60)
with c2: st.markdown(f'<span class="title-text">Heat Input Master</span>', unsafe_allow_html=True)
st.markdown('</div><div style="border-bottom: 3px solid black; margin-bottom: 20px;"></div>', unsafe_allow_html=True)

# --- 4. 사이드바 ---
with st.sidebar:
    st.markdown("<div class='master-label'>Standard</div>", unsafe_allow_html=True)
    std_mode = st.radio("Std", options=['ISO', 'AWS'], label_visibility="collapsed")
    st.markdown("<br><div class='master-label'>WPS range (kJ/mm)</div>", unsafe_allow_html=True)
    w_min = st.number_input("Min", value=1.0, step=0.1, format="%.1f")
    w_max = st.number_input("Max", value=2.5, step=0.1, format="%.1f")

# --- 5. 메인 레이아웃 (4개 섹션) ---
col1, col2, col3 = st.columns([1, 1.2, 0.8])

with col1:
    st.markdown("<div class='master-label'>Select Process</div>", unsafe_allow_html=True)
    proc = st.radio("P", options=['SAW', 'FCAW', 'SMAW', 'GMAW'], label_visibility="collapsed")
    k = 1.0 if std_mode == 'AWS' or proc == 'SAW' else 0.8

with col2:
    st.markdown("<div class='master-label'>Input Parameters</div>", unsafe_allow_html=True)
    def param_row(label, val, step, key):
        st.markdown(f"<div class='master-label'>{label}</div>", unsafe_allow_html=True)
        return st.number_input(label, value=val, step=step, format="%.1f", label_visibility="collapsed", key=key)

    v = param_row("Voltage (V)", 28.0, 0.5, "v_in")
    a = param_row("Amperage (A)", 220.0, 5.0, "a_in")
    l = param_row("Length (mm)", 150.0, 10.0, "l_in")
    t = param_row("Time (Sec)", 120.0, 1.0, "t_in")

with col3:
    st.markdown("<div class='master-label'>Live Result</div>", unsafe_allow_html=True)
    hi = (k * v * a * t) / (l * 1000) if l > 0 else 0
    is_pass = w_min <= hi <= w_max
    
    st.markdown(f'<div class="result-value-box">{hi:.3f} kJ/mm</div>', unsafe_allow_html=True)
    st_bg = color_pass if is_pass else color_fail
    st.markdown(f'<div class="result-status-box" style="background-color:{st_bg};">{"PASS" if is_pass else "FAIL"}</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("💾 SAVE LOG", use_container_width=True):
        st.session_state.history.insert(0, {"Time": datetime.now().strftime("%H:%M:%S"), "Proc": proc, "V": v, "A": a, "L": l, "T": t, "HI": f"{hi:.3f}", "Status": "PASS" if is_pass else "FAIL"})
        st.toast("Saved!")

# --- 6. 히스토리 데이터 ---
if st.session_state.history:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True)