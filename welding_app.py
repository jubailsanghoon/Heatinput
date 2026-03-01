import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 페이지 설정 및 테마 ---
st.set_page_config(page_title="Heat Input Master", layout="wide")

color_bg = "#F2F2F2"
color_white = "#FFFFFF"
color_line = "#000000"

if 'history' not in st.session_state: st.session_state.history = []

# --- 2. CSS 정밀 레이아웃 (공정 버튼 크기 보정) ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {color_bg}; color: {color_line}; }}
    
    /* [마스터] 기준 폰트 크기 설정 */
    .master-label {{
        font-size: 1.5rem !important; 
        font-weight: normal !important;
        color: {color_line} !important;
    }}

    /* --- [핵심 수정] Select Process 버튼 글자 크기 동기화 --- */
    /* 버튼 내부의 모든 p, span, div 요소를 추적하여 1.5rem 강제 주입 */
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label p,
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label span,
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label div {{
        font-size: 1.5rem !important; /* Input Parameters 라벨과 동일하게 설정 */
        font-weight: normal !important;
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1 !important;
    }}

    /* 2x2 그리드 레이아웃 고정 */
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] {{
        display: grid !important;
        grid-template-columns: repeat(2, 1fr) !important; 
        gap: 10px !important;
    }}
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label {{
        height: 60px !important; 
        border: 2px solid {color_line} !important;
        background-color: {color_white} !important;
        border-radius: 4px !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }}
    
    /* 선택된 버튼 색상 반전 */
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label[data-checked="true"] {{ background-color: {color_line} !important; }}
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label[data-checked="true"] p {{ color: {color_white} !important; }}

    /* --- [수정] 숫자 입력창 좌우 분리 (-) [숫자] (+) --- */
    div[data-testid="stNumberInputContainer"] {{
        display: flex !important;
        flex-direction: row !important;
        background-color: {color_white} !important; 
        border: 2px solid {color_line} !important;
        border-radius: 4px !important;
        height: 60px !important; 
        align-items: center !important;
        justify-content: space-between !important;
    }}
    div[data-testid="stNumberInputContainer"] > button:first-of-type {{ order: -1 !important; min-width: 60px !important; height: 100% !important; font-size: 1.5rem !important; }}
    div[data-testid="stNumberInputContainer"] input {{ order: 2 !important; flex-grow: 1 !important; text-align: center !important; font-size: 1.5rem !important; }}
    div[data-testid="stNumberInputContainer"] > button:last-of-type {{ order: 99 !important; min-width: 60px !important; height: 100% !important; font-size: 1.5rem !important; }}

    /* 모바일 반응형 대응 */
    @media (max-width: 768px) {{
        .master-label, 
        div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label p {{
            font-size: 1.2rem !important; /* 모바일에서는 가독성을 위해 살짝 축소 */
        }}
        div[data-testid="stNumberInputContainer"], 
        div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label {{ height: 50px !important; }}
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. 헤더 ---
st.markdown(f"<h1 style='text-align: center;'>Heat Input Master</h1>", unsafe_allow_html=True)
st.markdown("<hr style='border: 2px solid black;'>", unsafe_allow_html=True)

# --- 4. 메인 레이아웃 (4개 섹션 모듈화 준비) ---
col1, col2, col3 = st.columns([1.1, 1.3, 0.9], gap="medium")

# [섹션 2] Select Process (이제 글자가 큼직해졌습니다)
with col1:
    st.markdown("<div class='master-label'>Select Process</div>", unsafe_allow_html=True)
    proc = st.radio("P", options=['SAW', 'FCAW', 'SMAW', 'GMAW'], label_visibility="collapsed")

# [섹션 3] Input Parameters
with col2:
    st.markdown("<div class='master-label'>Input Parameters</div>", unsafe_allow_html=True)
    def param_row(label, val, step, key):
        c_lbl, c_inp = st.columns([4.5, 5.5])
        with c_lbl: st.markdown(f"<div class='master-label' style='height: 60px; display: flex; align-items: center;'>{label}</div>", unsafe_allow_html=True)
        with c_inp: return st.number_input(label, value=val, step=step, format="%.1f", label_visibility="collapsed", key=key)

    v = param_row("Voltage (V)", 28.0, 0.5, "v")
    a = param_row("Amperage (A)", 220.0, 5.0, "a")
    l = param_row("Length (mm)", 150.0, 10.0, "l")
    t = param_row("Time (Sec)", 120.0, 1.0, "t")

# [섹션 4] 결과 (생략 - 레이아웃 확인용)
with col3:
    st.markdown("<div class='master-label'>Live Result</div>", unsafe_allow_html=True)
    st.markdown("<div style='height:75px; border:3px solid black; display:flex; align-items:center; justify-content:center; font-size:2rem;'>0.000 kJ/mm</div>", unsafe_allow_html=True)