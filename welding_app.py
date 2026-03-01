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

# --- 2. CSS 정밀 레이아웃 (웹 동결 + 모바일 글자색 보정) ---
st.markdown(f"""
    <style>
    /* 전체 배경 */
    .stApp {{ background-color: {color_bg}; color: {color_line}; }}
    
    /* [마스터] 가변 폰트 */
    .master-label {{
        font-size: clamp(1.1rem, 2.5vw, 1.5rem) !important;
        font-weight: normal !important;
        color: {color_line} !important;
        margin-bottom: 5px !important;
        line-height: 1.2 !important;
    }}

    /* --- [섹션 3] 입력창 폭 60% 및 좌우 버튼 고정 (웹 전용) --- */
    @media (min-width: 769px) {{
        div[data-testid="column"]:nth-of-type(2) .stNumberInput {{
            width: 60% !important; 
            min-width: 220px !important;
        }}
    }}

    div[data-testid="stNumberInputContainer"] {{
        display: flex !important;
        flex-direction: row !important;
        height: 60px !important;
        background-color: {color_white} !important;
        border: 2px solid {color_line} !important;
        border-radius: 4px !important;
        overflow: hidden !important;
    }}

    /* 버튼 및 숫자창 순서 고정 (1-2-3) */
    div[data-testid="stNumberInputContainer"] > button:first-of-type {{ order: -1 !important; min-width: 60px !important; font-size: 1.5rem !important; background: transparent !important; color: {color_line} !important; }}
    div[data-testid="stNumberInputContainer"] input {{ order: 2 !important; flex-grow: 1 !important; text-align: center !important; font-size: 1.5rem !important; font-weight: bold !important; color: {color_line} !important; }}
    div[data-testid="stNumberInputContainer"] > button:last-of-type {{ order: 99 !important; min-width: 60px !important; font-size: 1.5rem !important; background: transparent !important; color: {color_line} !important; }}

    /* --- [모바일 핵심 수정] 라디오 버튼 글자색 강제 검정색 --- */
    div[role="radiogroup"] label p, 
    div[role="radiogroup"] label span,
    div[role="radiogroup"] label div {{
        color: {color_line} !important; 
        font-size: clamp(1.1rem, 2.5vw, 1.5rem) !important;
        opacity: 1 !important;
    }}

    /* 공정 선택 버튼 배경 및 테두리 */
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label {{
        height: 60px !important; 
        border: 2px solid {color_line} !important;
        background-color: {color_white} !important;
        justify-content: center !important; align-items: center !important;
    }}
    
    /* 선택 시 색상 반전 */
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label[data-checked="true"] {{ background-color: {color_line} !important; }}
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label[data-checked="true"] p,
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label[data-checked="true"] span {{
        color: {color_white} !important; 
    }}

    /* 📱 모바일 전용 보정 */
    @media (max-width: 768px) {{
        div[data-testid="column"]:nth-of-type(2) .stNumberInput {{
            width: 100% !important; 
        }}
        div[data-testid="stNumberInputContainer"] {{ height: 50px !important; }}
        section[data-testid="stSidebar"] div[role="radiogroup"] label p {{
            color: {color_line} !important;
            font-weight: bold !important;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. 헤더 영역 ---
logo_url = "https://raw.githubusercontent.com/jubailsanghoon/Heatinput/main/db65c0d39f36f2dddc248ea0bf2e4efc.jpg"
st.markdown(f"""
    <div style="display: flex; align-items: center; border-bottom: 5px solid black; padding-bottom: 10px; margin-bottom: 25px;">
        <img src="{logo_url}" width="70">
        <span class="title-text" style="font-size: 2.3rem; margin-left: 15px; font-weight: bold;">Heat Input Master</span>
    </div>
""", unsafe_allow_html=True)

# --- 4. 메인 레이아웃 ---
col1, col2, col3 = st.columns([1.1, 1.3, 0.9], gap="large")

with col1:
    with st.sidebar:
        st.markdown("<div class='master-label'>Standard</div>", unsafe_allow_html=True)
        std_mode = st.radio("Standard", ['ISO', 'AWS'], horizontal=False, label_visibility="collapsed")
        st.markdown("<br><div class='master-label'>WPS range (kJ/mm)</div>", unsafe_allow_html=True)
        w_min = st.number_input("Min", 1.0, step=0.1)
        w_max = st.number_input("Max", 2.5, step=0.1)
    
    st.markdown("<div class='master-label'>Select Process</div>", unsafe_allow_html=True)
    proc = st.radio("P", ['SAW', 'FCAW', 'SMAW', 'GMAW'], label_visibility="collapsed")
    k = 1.0 if std_mode == 'AWS' or proc == 'SAW' else 0.8

with col2:
    st.markdown("<div class='master-label'>Input Parameters</div>", unsafe_allow_html=True)
    def param_input(label, val, step, key):
        st.markdown(f"<div class='master-label' style='margin-top:15px;'>{label}</div>", unsafe_allow_html=True)
        return st.number_input(label, value=val, step=step, format="%.1f", label_visibility="collapsed", key=key)

    v = param_input("Voltage (V)", 28.0, 0.5, "v")
    a = param_input("Amperage (A)", 220.0, 5.0, "a")
    l = param_input("Length (mm)", 150.0, 10.0, "l")
    t = param_input("Time (Sec)", 120.0, 1.0, "t")

with col3:
    st.markdown("<div class='master-label'>Live Result</div>", unsafe_allow_html=True)
    hi = (k * v * a * t) / (l * 1000) if l > 0 else 0
    is_pass = w_min <= hi <= w_max
    st.markdown(f'<div style="background:white; border:3px solid black; height:80px; display:flex; align-items:center; justify-content:center; font-size:2.2rem; font-weight:bold; margin-bottom:10px;">{hi:.3f} kJ/mm</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="background:{color_pass if is_pass else color_fail}; color:white; height:60px; display:flex; align-items:center; justify-content:center; font-size:1.8rem; font-weight:bold; border-radius:4px; border:2px solid black;">{"PASS" if is_pass else "FAIL"}</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("💾 SAVE LOG", use_container_width=True):
        st.session_state.history.insert(0, {"Time": datetime.now().strftime("%H:%M:%S"), "Proc": proc, "V": v, "A": a, "L": l, "T": t, "HI": f"{hi:.3f}", "Status": "PASS" if is_pass else "FAIL"})
        st.toast("Saved!")

if st.session_state.history:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.table(pd.DataFrame(st.session_state.history).head(10))