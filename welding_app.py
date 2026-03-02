import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 페이지 설정 (중앙 정렬 규격 고정) ---
st.set_page_config(page_title="Heat Input Master", layout="centered")

color_bg = "#F2F2F2"
color_white = "#FFFFFF"
color_line = "#000000"
color_pass = "#28A745"
color_fail = "#DC3545"

if 'history' not in st.session_state: st.session_state.history = []

# --- 2. CSS 초정밀 시공 (소장님 레이아웃 도면 반영) ---
st.markdown(f"""
    <style>
    /* 전체 배경 및 중앙 정렬 (최대폭 500px 확보) */
    .stApp {{
        background-color: {color_bg};
        max-width: 500px;
        margin: 0 auto;
        border-left: 1px solid #ccc;
        border-right: 1px solid #ccc;
    }}
    
    * {{ color: {color_line} !important; font-family: 'Inter', sans-serif; }}

    /* [섹션 0] 헤더 */
    .header-logo {{ mix-blend-mode: multiply; }}
    .header-text {{ font-size: 1.8rem; font-weight: bold; margin-left: 15px; }}

    /* [마스터 라벨] */
    .master-label {{
        font-size: 1.3rem !important;
        font-weight: bold !important;
        margin-top: 25px !important;
        margin-bottom: 10px !important;
    }}

    /* --- [섹션 1 & 2] 버튼들 (Standard & Process) --- */
    div[role="radiogroup"] {{ display: grid !important; gap: 10px !important; }}
    .std-container div[role="radiogroup"] {{ grid-template-columns: 1fr !important; }}
    .proc-container div[role="radiogroup"] {{ grid-template-columns: repeat(2, 1fr) !important; }}
    
    div[role="radiogroup"] label {{
        height: 60px !important;
        border: 2px solid {color_line} !important;
        background-color: {color_white} !important;
        justify-content: center !important; font-weight: bold !important;
    }}
    div[role="radiogroup"] label[data-checked="true"] {{ background-color: {color_line} !important; }}
    div[role="radiogroup"] label[data-checked="true"] p {{ color: {color_white} !important; }}

    /* --- [핵심 수정] [섹션 3] Input Parameters 정밀 타설 --- */
    /* 라벨, 버튼, 입력창을 한 줄에 나열 (Flexbox) */
    .param-row-container {{
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        justify-content: space-between !important;
        margin-bottom: 12px !important;
        width: 100% !important;
    }}
    
    /* A: 라벨 (Voltage 등) - 폭 45% 확보 */
    .param-label {{
        font-size: 1.1rem !important;
        width: 45% !important;
        text-align: left !important;
    }}

    /* B: [+] 버튼 - 폭 15% (큼직하게) */
    .plus-btn button {{
        width: 15% !important;
        min-width: 60px !important;
        height: 55px !important;
        font-size: 1.8rem !important;
        font-weight: bold !important;
        background: {color_line} !important;
        color: {color_white} !important;
        border: 2px solid {color_line} !important;
        border-radius: 4px !important;
    }}

    /* C: 숫자 입력창 - 폭 30% (콤팩트하게) */
    .input-box {{
        width: 30% !important;
        min-width: 110px !important;
        height: 55px !important;
        border: 2px solid {color_line} !important;
        background-color: {color_white} !important;
        border-radius: 4px !important;
        display: flex; align-items: center; justify-content: center;
    }}
    .input-box input {{
        width: 100% !important;
        height: 100% !important;
        border: none !important;
        text-align: center !important;
        font-size: 1.5rem !important;
        font-weight: bold !important;
        padding: 0 !important;
    }}

    /* [섹션 4] 결과창 */
    .result-box {{
        background: {color_white}; border: 3px solid {color_line};
        height: 85px; display: flex; align-items: center; justify-content: center;
        font-size: 2.2rem; font-weight: bold; margin-top: 15px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. [섹션 0] 헤더 ---
logo_url = "https://raw.githubusercontent.com/jubailsanghoon/Heatinput/main/db65c0d39f36f2dddc248ea0bf2e4efc.jpg"
st.markdown(f"""
    <div style="display: flex; align-items: center; border-bottom: 4px solid black; padding-bottom: 10px; margin-bottom: 20px;">
        <img src="{logo_url}" width="65">
        <span class="header-text">Heat Input Master</span>
    </div>
""", unsafe_allow_html=True)

# --- 4. 메인 시공 ---

# [섹션 1] Standard Selection
st.markdown("<div class='master-label'>Standard Selection</div>", unsafe_allow_html=True)
st.markdown('<div class="std-container">', unsafe_allow_html=True)
std_mode = st.radio("Std", ['ISO Standard (0.8)', 'AWS Standard (1.0)'], label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)
k_val = 1.0 if "AWS" in std_mode else 0.8

# [섹션 2] WPS Range (Min/Max 대칭)
st.markdown("<div class='master-label'>WPS Range (kJ/mm)</div>", unsafe_allow_html=True)
c_min, c_max = st.columns(2)
with c_min: w_min = st.number_input("Min", 1.0, step=0.1, key="w_min")
with c_max: w_max = st.number_input("Max", 2.5, step=0.1, key="w_max")

# [섹션 1' (추가)] Select Process
st.markdown("<div class='master-label'>Select Process</div>", unsafe_allow_html=True)
st.markdown('<div class="proc-container">', unsafe_allow_html=True)
proc = st.radio("Proc", ['SAW', 'FCAW', 'SMAW', 'GMAW'], label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)
if "SAW" in proc: k_val = 1.0

# --- [핵심 2] [섹션 3] Input Parameters (소장님 도면 반영) ---
st.markdown("<div class='master-label'>Input Parameters</div>", unsafe_allow_html=True)

# 콤팩트 입력 함수 정의
if 'v' not in st.session_state: st.session_state.v = 28.0
if 'a' not in st.session_state: st.session_state.a = 220.0
if 'l' not in st.session_state: st.session_state.l = 150.0
if 't' not in st.session_state: st.session_state.t = 120.0

def compact_input(label, val_key, step):
    st.markdown(f'<div class="param-row-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="param-label">{label}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="plus-btn">', unsafe_allow_html=True)
    if st.button("+", key=f"{val_key}_plus"):
        st.session_state[val_key] += step
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="input-box">', unsafe_allow_html=True)
    st.text_input(label, value=f"{st.session_state[val_key]:.1f}", label_visibility="collapsed", key=f"{val_key}_input")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 4개 파라미터 타설
compact_input("Voltage (V)", "v", 0.5)
compact_input("Amperage (A)", "a", 5.0)
compact_input("Length (mm)", "l", 10.0)
compact_input("Time (Sec)", "t", 1.0)

# 값 동기화
v = float(st.session_state.v_input) if st.session_state.v_input else 0.0
a = float(st.session_state.a_input) if st.session_state.a_input else 0.0
l = float(st.session_state.l_input) if st.session_state.l_input else 0.0
t = float(st.session_state.t_input) if st.session_state.t_input else 0.0

# --- 5. 결과 및 저장 ---
hi = (k_val * v * a * t) / (l * 1000) if l > 0 else 0
is_pass = w_min <= hi <= w_max

st.markdown(f'<div class="result-box">{hi:.3f} kJ/mm</div>', unsafe_allow_html=True)
st_bg = color_pass if is_pass else color_fail
st.markdown(f'<div style="background:{st_bg}; color:white !important; height:60px; display:flex; align-items:center; justify-content:center; font-size:1.6rem; font-weight:bold; border-radius:4px; margin-top:10px; border:2px solid black;">{"PASS" if is_pass else "FAIL"}</div>', unsafe_allow_html=True)

if st.button("💾 SAVE LOG DATA", use_container_width=True):
    st.session_state.history.insert(0, {"Time": datetime.now().strftime("%H:%M:%S"), "Proc": proc, "HI": f"{hi:.3f}", "Status": "PASS" if is_pass else "FAIL"})
    st.toast("Saved!")

if st.session_state.history:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True)