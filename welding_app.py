import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 페이지 설정 (모바일 규격 고정) ---
st.set_page_config(page_title="Heat Input Master", layout="centered")

color_bg = "#F2F2F2"
color_white = "#FFFFFF"
color_line = "#000000"
color_pass = "#28A745"
color_fail = "#DC3545"

if 'history' not in st.session_state: st.session_state.history = []

# --- 2. CSS 초정밀 시공 ([-] 왼쪽 배치 및 순서 고정) ---
st.markdown(f"""
    <style>
    /* 전체 배경 및 중앙 정렬 */
    .stApp {{
        background-color: {color_bg};
        max-width: 480px;
        margin: 0 auto;
        border-left: 1px solid #ccc;
        border-right: 1px solid #ccc;
    }}
    
    * {{ color: {color_line} !important; font-family: 'Inter', sans-serif; }}

    .master-label {{
        font-size: 1.2rem !important;
        font-weight: bold !important;
        margin-top: 20px !important;
        margin-bottom: 8px !important;
        display: block;
    }}

    /* --- [핵심] 숫자 입력창 [-] [숫자] [+] 순서 강제 고정 --- */
    div[data-testid="stNumberInputContainer"] {{
        display: flex !important;
        flex-direction: row !important;
        height: 65px !important;
        background-color: {color_white} !important;
        border: 2px solid {color_line} !important;
        border-radius: 4px !important;
        padding: 0 !important;
        overflow: hidden !important;
    }}

    /* 1번: 마이너스(-) 버튼 - 무조건 맨 왼쪽 */
    div[data-testid="stNumberInputContainer"] > button:first-of-type {{
        order: 1 !important; 
        min-width: 70px !important; 
        height: 100% !important; 
        font-size: 1.8rem !important; 
        background: #F0F0F0 !important;
        border-right: 1px solid {color_line} !important;
        margin: 0 !important;
        border-radius: 0 !important;
    }}

    /* 2번: 숫자 입력 칸 - 무조건 가운데 */
    div[data-testid="stNumberInputContainer"] > div {{
        order: 2 !important;
        flex-grow: 1 !important;
    }}
    div[data-testid="stNumberInputContainer"] input {{
        height: 100% !important;
        font-size: 1.5rem !important; 
        font-weight: bold !important;
        text-align: center !important;
        border: none !important;
        background: transparent !important;
    }}

    /* 3번: 플러스(+) 버튼 - 무조건 맨 오른쪽 */
    div[data-testid="stNumberInputContainer"] > button:last-of-type {{
        order: 3 !important; 
        min-width: 70px !important; 
        height: 100% !important; 
        font-size: 1.8rem !important; 
        background: #F0F0F0 !important;
        border-left: 1px solid {color_line} !important;
        margin: 0 !important;
        border-radius: 0 !important;
    }}

    /* 버튼들 (Standard & Process) */
    div[role="radiogroup"] {{
        display: grid !important;
        gap: 10px !important;
    }}
    .std-container div[role="radiogroup"] {{ grid-template-columns: 1fr !important; }}
    .proc-container div[role="radiogroup"] {{ grid-template-columns: repeat(2, 1fr) !important; }}
    
    div[role="radiogroup"] label {{
        height: 60px !important;
        border: 2px solid {color_line} !important;
        background-color: {color_white} !important;
        justify-content: center !important;
        font-weight: bold !important;
    }}
    div[role="radiogroup"] label[data-checked="true"] {{ background-color: {color_line} !important; }}
    div[role="radiogroup"] label[data-checked="true"] p {{ color: {color_white} !important; }}

    /* 결과창 */
    .result-box {{
        background: {color_white}; border: 3px solid {color_line};
        height: 85px; display: flex; align-items: center; justify-content: center;
        font-size: 2.2rem; font-weight: bold; margin-top: 15px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. 헤더 ---
logo_url = "https://raw.githubusercontent.com/jubailsanghoon/Heatinput/main/db65c0d39f36f2dddc248ea0bf2e4efc.jpg"
st.markdown(f"""
    <div style="display: flex; align-items: center; border-bottom: 4px solid black; padding-bottom: 10px; margin-bottom: 20px;">
        <img src="{logo_url}" width="65">
        <span style="font-size: 1.7rem; margin-left: 15px; font-weight: bold;">Heat Input Master</span>
    </div>
""", unsafe_allow_html=True)

# --- 4. 메인 입력 영역 ---

# Standard (2줄)
st.markdown("<span class='master-label'>Standard Selection</span>", unsafe_allow_html=True)
st.markdown('<div class="std-container">', unsafe_allow_html=True)
std_mode = st.radio("Std", ['ISO Standard (0.8)', 'AWS Standard (1.0)'], label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)
k_val = 1.0 if "AWS" in std_mode else 0.8

# WPS Range
st.markdown("<span class='master-label'>WPS Range (kJ/mm)</span>", unsafe_allow_html=True)
c_min, c_max = st.columns(2)
with c_min: w_min = st.number_input("Min", value=1.0, step=0.1, format="%.1f", key="w_min")
with c_max: w_max = st.number_input("Max", value=2.5, step=0.1, format="%.1f", key="w_max")

# Select Process
st.markdown("<span class='master-label'>Select Process</span>", unsafe_allow_html=True)
st.markdown('<div class="proc-container">', unsafe_allow_html=True)
proc = st.radio("Proc", ['SAW', 'FCAW', 'SMAW', 'GMAW'], label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)
if "SAW" in proc: k_val = 1.0

# Input Parameters ([-] [숫자] [+] 고정형)
st.markdown("<span class='master-label'>Input Parameters</span>", unsafe_allow_html=True)
v = st.number_input("Voltage (V)", value=28.0, step=0.5, format="%.1f", key="v")
a = st.number_input("Amperage (A)", value=220.0, step=5.0, format="%.1f", key="a")
l = st.number_input("Length (mm)", value=150.0, step=10.0, format="%.1f", key="l")
t = st.number_input("Time (Sec)", value=120.0, step=1.0, format="%.1f", key="t")

# --- 5. 결과 및 저장 ---
hi = (k_val * v * a * t) / (l * 1000) if l > 0 else 0
is_pass = w_min <= hi <= w_max

st.markdown(f'<div class="result-box">{hi:.3f} kJ/mm</div>', unsafe_allow_html=True)
st_bg = color_pass if is_pass else color_fail
st.markdown(f'<div style="background:{st_bg}; color:white !important; height:60px; display:flex; align-items:center; justify-content:center; font-size:1.6rem; font-weight:bold; border-radius:4px; margin-top:10px; border:2px solid black;">{"PASS" if is_pass else "FAIL"}</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
if st.button("💾 SAVE LOG DATA", use_container_width=True):
    st.session_state.history.insert(0, {"Time": datetime.now().strftime("%H:%M:%S"), "Proc": proc, "HI": f"{hi:.3f}", "Status": "PASS" if is_pass else "FAIL"})
    st.toast("Saved!")

if st.session_state.history:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True)