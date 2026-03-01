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

# --- 2. CSS 정밀 레이아웃 (모바일 Select Process 글자색 검정 고정) ---
st.markdown(f"""
    <style>
    /* 전체 배경 */
    .stApp {{ background-color: {color_bg}; color: {color_line}; }}
    
    /* [마스터] 가변 폰트 시스템 */
    :root {{
        --font-size-master: clamp(1rem, 4vw, 1.5rem);
    }}

    .master-label {{
        font-size: var(--font-size-master) !important;
        font-weight: normal !important;
        color: {color_line} !important;
        margin-bottom: 5px !important;
    }}

    /* --- [핵심 수정] Select Process (메인 화면 라디오 버튼) 글자색 검정 --- */
    /* 선택되지 않은 상태 포함 모든 텍스트를 검은색으로 강제 */
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label p {{
        color: {color_line} !important;
        font-size: var(--font-size-master) !important;
        opacity: 1 !important; /* 흐릿함 방지 */
        font-weight: 500 !important;
    }}

    /* 버튼 기본 스타일 */
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label {{
        min-height: 55px !important;
        border: 2px solid {color_line} !important;
        background-color: {color_white} !important;
        border-radius: 4px !important;
    }}

    /* 버튼 선택 시 스타일 (배경 검정, 글자 흰색으로 반전) */
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label[data-checked="true"] {{
        background-color: {color_line} !important;
    }}
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label[data-checked="true"] p {{
        color: {color_white} !important;
    }}

    /* --- [섹션 1] 사이드바 글자색 (이전 지시사항 유지: 흰색) --- */
    section[data-testid="stSidebar"] .master-label,
    section[data-testid="stSidebar"] div[role="radiogroup"] label p,
    section[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] p {{
        color: {color_white} !important;
        font-weight: bold !important;
    }}

    /* [섹션 3] 입력창 (PC 폭 60% 유지 / 모바일 100%) */
    @media (min-width: 769px) {{
        div[data-testid="column"]:nth-of-type(2) .stNumberInput {{ width: 60% !important; }}
    }}
    
    div[data-testid="stNumberInputContainer"] {{
        display: flex !important; flex-direction: row !important;
        background-color: {color_white} !important;
        border: 2px solid {color_line} !important;
        height: 60px !important;
    }}

    /* 숫자창 버튼 순서 고정: 1번[-] 2번[숫자] 3번[+] */
    div[data-testid="stNumberInputContainer"] > button:first-of-type {{ order: -1 !important; min-width: 55px !important; color: {color_line} !important; }}
    div[data-testid="stNumberInputContainer"] input {{ order: 2 !important; flex-grow: 1 !important; text-align: center !important; color: {color_line} !important; font-weight: bold !important; }}
    div[data-testid="stNumberInputContainer"] > button:last-of-type {{ order: 99 !important; min-width: 55px !important; color: {color_line} !important; }}

    /* 📱 모바일 전용 보정 */
    @media (max-width: 768px) {{
        div[data-testid="stNumberInputContainer"] {{ height: 50px !important; }}
        div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] {{
            grid-template-columns: repeat(2, 1fr) !important;
            gap: 5px !important;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. 헤더 영역 ---
logo_url = "https://raw.githubusercontent.com/jubailsanghoon/Heatinput/main/db65c0d39f36f2dddc248ea0bf2e4efc.jpg"
st.markdown(f"""
    <div style="display: flex; align-items: center; border-bottom: 5px solid black; padding-bottom: 10px; margin-bottom: 25px;">
        <img src="{logo_url}" width="60">
        <span style="font-size: clamp(1.4rem, 5vw, 2.3rem); margin-left: 15px; font-weight: bold;">Heat Input Master</span>
    </div>
""", unsafe_allow_html=True)

# --- 4. 사이드바 (Standard & WPS) ---
with st.sidebar:
    st.markdown("<div class='master-label'>Standard</div>", unsafe_allow_html=True)
    std_mode = st.radio("Standard", options=['ISO', 'AWS'], horizontal=False, label_visibility="collapsed")
    st.markdown("<br><div class='master-label'>WPS range (kJ/mm)</div>", unsafe_allow_html=True)
    w_min = st.number_input("Min", value=1.0, step=0.1, format="%.1f")
    w_max = st.number_input("Max", value=2.5, step=0.1, format="%.1f")

# --- 5. 메인 레이아웃 ---
col1, col2, col3 = st.columns([1.1, 1.3, 0.9], gap="medium")

with col1:
    st.markdown("<div class='master-label'>Select Process</div>", unsafe_allow_html=True)
    proc = st.radio("P", options=['SAW', 'FCAW', 'SMAW', 'GMAW'], label_visibility="collapsed")
    k = 1.0 if std_mode == 'AWS' or proc == 'SAW' else 0.8

with col2:
    st.markdown("<div class='master-label'>Input Parameters</div>", unsafe_allow_html=True)
    def param_row(label, val, step, key):
        st.markdown(f"<div class='master-label' style='margin-top:10px;'>{label}</div>", unsafe_allow_html=True)
        return st.number_input(label, value=val, step=step, format="%.1f", label_visibility="collapsed", key=key)

    v = param_row("Voltage (V)", 28.0, 0.5, "v_p")
    a = param_row("Amperage (A)", 220.0, 5.0, "a_p")
    l = param_row("Length (mm)", 150.0, 10.0, "l_p")
    t = param_row("Time (Sec)", 120.0, 1.0, "t_p")

with col3:
    st.markdown("<div class='master-label'>Live Result</div>", unsafe_allow_html=True)
    hi = (k * v * a * t) / (l * 1000) if l > 0 else 0
    is_pass = w_min <= hi <= w_max
    
    st.markdown(f'<div style="background:white; border:3px solid black; height:75px; display:flex; align-items:center; justify-content:center; font-size:2rem; font-weight:bold; margin-bottom:10px; color:black;">{hi:.3f} kJ/mm</div>', unsafe_allow_html=True)
    st_bg = color_pass if is_pass else color_fail
    st.markdown(f'<div style="background:{st_bg}; color:white; height:60px; display:flex; align-items:center; justify-content:center; font-size:1.8rem; font-weight:bold; border-radius:4px; border:2px solid black;">{"PASS" if is_pass else "FAIL"}</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("💾 SAVE LOG", use_container_width=True):
        st.session_state.history.insert(0, {"Time": datetime.now().strftime("%H:%M:%S"), "Proc": proc, "V": v, "A": a, "L": l, "T": t, "HI": f"{hi:.3f}", "Status": "PASS" if is_pass else "FAIL"})
        st.toast("Saved!")

# --- 6. 히스토리 ---
if st.session_state.history:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True)