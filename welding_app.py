import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 페이지 설정 및 테마 ---
st.set_page_config(page_title="Heat Input Master", layout="wide")

color_bg = "#F2F2F2"
color_white = "#FFFFFF"
color_line = "#000000"

if 'history' not in st.session_state: st.session_state.history = []

# --- 2. CSS 정밀 레이아웃 (폭 60% 고정 시공) ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {color_bg}; color: {color_line}; }}
    
    /* [마스터 라벨] */
    .master-label {{
        font-size: clamp(1rem, 4vw, 1.5rem) !important;
        font-weight: normal !important;
        color: {color_line} !important;
    }}

    /* --- [핵심 수정] 입력창 폭 60% 제한 --- */
    /* 섹션 3(Input Parameters) 내부의 모든 숫자 입력 박스 너비 조절 */
    div[data-testid="column"]:nth-of-type(2) .stNumberInput {{
        width: 60% !important;  /* 전체 폭의 60%만 사용 */
        margin-right: auto !important; /* 왼쪽 정렬 유지 */
    }}

    /* 입력창 내부 [-] [숫자] [+] 레이아웃 유지 */
    div[data-testid="stNumberInputContainer"] {{
        display: flex !important;
        flex-direction: row !important;
        height: 55px !important;
        background-color: {color_white} !important;
        border: 2px solid {color_line} !important;
        border-radius: 4px !important;
    }}
    
    /* 버튼 및 입력 폰트 크기 */
    div[data-testid="stNumberInputContainer"] button {{ min-width: 45px !important; font-size: 1.2rem !important; }}
    div[data-testid="stNumberInputContainer"] input {{ font-size: 1.2rem !important; }}

    /* 모바일 반응형 대응 (폭 60%가 너무 작을 경우 모바일에서만 80~90%로 유동적 조절 가능) */
    @media (max-width: 768px) {{
        div[data-testid="column"]:nth-of-type(2) .stNumberInput {{
            width: 85% !important; /* 모바일은 화면이 좁으므로 다시 85%로 확장 */
        }}
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. 헤더 영역 (생략) ---
st.markdown(f"<h2 style='text-align: center;'>Heat Input Master</h2>", unsafe_allow_html=True)

# --- 4. 메인 레이아웃 ---
col1, col2, col3 = st.columns([1, 1.3, 0.9])

# [섹션 2] Select Process
with col1:
    st.markdown("<div class='master-label'>Select Process</div>", unsafe_allow_html=True)
    proc = st.radio("P", options=['SAW', 'FCAW', 'SMAW', 'GMAW'], label_visibility="collapsed")

# [섹션 3] Input Parameters (폭 60% 적용 구역)
with col2:
    st.markdown("<div class='master-label'>Input Parameters</div>", unsafe_allow_html=True)
    
    def param_row(label, val, step, key):
        # 라벨을 먼저 출력하고 아래에 60% 폭의 입력창 배치
        st.markdown(f"<div class='master-label' style='margin-top:10px;'>{label}</div>", unsafe_allow_html=True)
        return st.number_input(label, value=val, step=step, format="%.1f", label_visibility="collapsed", key=key)

    v = param_row("Voltage (V)", 28.0, 0.5, "v_in")
    a = param_row("Amperage (A)", 220.0, 5.0, "a_in")
    l = param_row("Length (mm)", 150.0, 10.0, "l_in")
    t = param_row("Time (Sec)", 120.0, 1.0, "t_in")

# [섹션 4] Live Result (생략)
with col3:
    st.markdown("<div class='master-label'>Live Result</div>", unsafe_allow_html=True)
    # 계산 로직 및 저장 버튼...