import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 페이지 설정 및 디자인 테마 ---
st.set_page_config(page_title="Heat Input Master", layout="wide")

# UI 색상 정의 (연회색, 흰색, 검은색 라인)
color_bg = "#F2F2F2"      # 연회색
color_white = "#FFFFFF"   # 흰색
color_line = "#000000"    # 검은색 라인
color_orange = "#FF6B00"  # 주황색 포인트
color_pass = "#28A745"
color_fail = "#DC3545"

if 'history' not in st.session_state: st.session_state.history = []

# CSS 주입: 비율 및 시인성 정밀 조정
st.markdown(f"""
    <style>
    .stApp {{ background-color: {color_bg}; color: {color_line}; }}
    
    /* 타이틀 및 주황색 수평선 */
    .header-container {{
        border-bottom: 4px solid {color_orange};
        padding-bottom: 5px;
        margin-bottom: 25px;
        display: flex;
        align-items: center;
    }}
    .title-text {{ font-size: 2.2rem; font-weight: 900; margin-left: 15px; }}

    /* [요청 3] WPS range 입력창 폭 60% 및 버튼 확대 */
    section[data-testid="stSidebar"] .stNumberInput {{ width: 60% !important; }}
    section[data-testid="stSidebar"] button {{ height: 45px !important; width: 45px !important; }}

    /* [요청 3] 프로세스 버튼: 높이 60% 축소, 폭 200% 확대 (비율 조정) */
    div[role="radiogroup"] label {{
        border: 1.5px solid {color_line} !important;
        background-color: {color_white} !important;
        min-height: 35px !important; /* 기존 대비 약 60% */
        padding: 5px 20px !important; /* 가로 폭 확대 효과 */
        border-radius: 0px !important;
        margin-right: 10px !important;
    }}
    div[role="radiogroup"] label[data-checked="true"] {{ background-color: {color_line} !important; }}
    div[role="radiogroup"] label[data-checked="true"] p {{ color: {color_white} !important; }}

    /* [요청 5] Input Parameters 1줄 평평하게 및 폭 60% */
    .input-row {{
        display: flex;
        align-items: center;
        margin-bottom: 8px;
    }}
    .input-label {{ width: 40%; font-weight: bold; font-size: 1rem; }}
    .input-field {{ width: 60%; }}

    /* [요청 6] Live Result 박스 높이 40% 및 상하 분리 */
    .result-value-box {{
        background-color: {color_white};
        border: 1.5px solid {color_line};
        height: 55px !important; /* 높이 대폭 축소 */
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
        border: 1.5px solid {color_line};
        color: {color_white};
    }}

    /* [요청 6] Save Log 별도 박스 */
    .save-box {{
        border: 1.5px solid {color_line};
        padding: 10px;
        background-color: #EAEAEA;
        margin-top: 15px;
    }}
    
    /* 폰트 통일성 */
    * {{ font-size: 15px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. 타이틀 및 로고 (원본 파일 사용) ---
st.markdown('<div class="header-container">', unsafe_allow_html=True)
col_l, col_t = st.columns([1, 8])
with col_l:
    st.image("image_d9f201.jpg") # 원본 크기 그대로 사용
with col_t:
    st.markdown(f'<span class="title-text">Heat Input Master</span>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- 3. 사이드바 (WPS range) ---
with st.sidebar:
    st.markdown("### Standard")
    std_mode = st.radio("Std", options=['ISO', 'AWS'], label_visibility="collapsed")
    st.markdown("### WPS range")
    w_min = st.number_input("Min", value=1.0, format="%.1f")
    w_max = st.number_input("Max", value=2.5, format="%.1f")
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.write("jubail.sanghoon@gmail.com")

# --- 4. 메인 레이아웃 (3열 밸런스) ---
c1, c2, c3 = st.columns([1, 1.2, 1])

# 1. Select Process
with c1:
    st.markdown("### 1. Select Process")
    proc = st.radio("P", options=['SAW', 'FCAW', 'SMAW', 'GMAW'], horizontal=True, label_visibility="collapsed")
    k = 1.0 if std_mode == 'AWS' or proc == 'SAW' else 0.8

# 2. Input Parameters (소수점 1자리, 1줄 구성, 폭 60%)
with c2:
    st.markdown("### 2. Input Parameters")
    
    def input_row(label, val, step, key):
        col_la, col_in = st.columns([5, 5])
        col_la.markdown(f"<div style='margin-top:10px; font-weight:bold;'>{label}</div>", unsafe_allow_html=True)
        return col_in.number_input(label, value=val, step=step, format="%.1f", label_visibility="collapsed", key=key)

    v = input_row("Voltage (V)", 28.0, 0.5, "v")
    a = input_row("Amperage (A)", 220.0, 5.0, "a")
    l = input_row("Length (mm)", 150.0, 10.0, "l")
    t = input_row("Time (Sec)", 120.0, 1.0, "t")
    
    # 속도 계산 (Log 포함용)
    speed = (l / t) * 60 if t > 0 else 0

# 3. Live Result (높이 40% 축소 및 상하 분리)
with c3:
    st.markdown("### 3. Live Result")
    hi = (k * v * a * t) / (l * 1000) if l > 0 else 0
    is_pass = w_min <= hi <= w_max
    
    # 상단 수치 박스
    st.markdown(f'<div class="result-value-box">{hi:.3f} kJ/mm</div>', unsafe_allow_html=True)
    
    # 하단 상태 박스
    s_bg = color_pass if is_pass else color_fail
    st.markdown(f'<div class="result-status-box" style="background-color:{s_bg};">{"PASS" if is_pass else "FAIL"}</div>', unsafe_allow_html=True)
    
    # Save Log 별도 박스
    st.markdown('<div class="save-box">', unsafe_allow_html=True)
    if st.button("💾 SAVE LOG DATA", use_container_width=True):
        st.session_state.history.insert(0, {
            "Time": datetime.now().strftime("%H:%M:%S"),
            "Std": std_mode,
            "Proc": proc,
            "Volt(V)": f"{v:.1f}",
            "Amp(A)": f"{a:.1f}",
            "Length(mm)": f"{l:.1f}",
            "Time(s)": f"{t:.1f}",
            "Speed(mm/min)": f"{speed:.1f}",
            "HI(kJ/mm)": f"{hi:.3f}",
            "Status": "PASS" if is_pass else "FAIL"
        })
        st.toast("Data Saved")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. 상세 히스토리 (모든 정보 포함) ---
st.markdown("<br><hr>", unsafe_allow_html=True)
if st.session_state.history:
    st.subheader("🕒 Detailed Welding Logs")
    st.table(pd.DataFrame(st.session_state.history))