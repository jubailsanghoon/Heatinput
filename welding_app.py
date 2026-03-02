import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 페이지 설정 (모바일 온리 규격) ---
st.set_page_config(page_title="Heat Input Master", layout="centered")

color_bg = "#F2F2F2"
color_white = "#FFFFFF"
color_line = "#000000"
color_pass = "#28A745"
color_fail = "#DC3545"

if 'history' not in st.session_state: st.session_state.history = []

# --- 2. CSS 정밀 보수 (입력창 폭 극소화 및 시인성 고정) ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {color_bg}; max-width: 480px; margin: 0 auto; }}
    * {{ color: {color_line} !important; font-family: 'Inter', sans-serif; }}

    /* 라디오 버튼 (Standard & Process) */
    div[role="radiogroup"] {{ display: grid !important; gap: 8px !important; }}
    .std-container div[role="radiogroup"] {{ grid-template-columns: repeat(2, 1fr) !important; }}
    .proc-container div[role="radiogroup"] {{ grid-template-columns: repeat(2, 1fr) !important; }}
    div[role="radiogroup"] label {{
        height: 55px !important; border: 2px solid {color_line} !important;
        background-color: {color_white} !important; justify-content: center !important; font-weight: bold !important;
    }}
    div[role="radiogroup"] label[data-checked="true"] {{ background-color: {color_line} !important; }}
    div[role="radiogroup"] label[data-checked="true"] p {{ color: {color_white} !important; }}

    /* [섹션 3] 입력창 레이아웃 - 콤팩트 시공 */
    .param-row {{
        display: flex !important; align-items: center !important;
        width: 100% !important; margin-bottom: 12px !important;
    }}
    .label-box {{ width: 35% !important; font-size: 1.1rem !important; font-weight: bold; }}
    
    /* 버튼 스타일 (검정 배경) */
    .calc-btn button {{
        width: 50px !important; height: 50px !important; font-size: 1.4rem !important;
        font-weight: bold !important; border: 2px solid {color_line} !important;
        background: {color_line} !important; color: {color_white} !important; border-radius: 4px !important;
        padding: 0 !important;
    }}
    
    /* 숫자 입력창 (매우 콤팩트하게) */
    .compact-input {{ width: 80px !important; margin: 0 5px !important; }}
    .compact-input input {{
        height: 50px !important; text-align: center !important; font-size: 1.3rem !important;
        font-weight: bold !important; border: 2px solid {color_line} !important; border-radius: 4px !important;
        padding: 0 !important;
    }}

    /* 결과 박스 */
    .result-box {{
        background: white; border: 3px solid black; height: 80px; 
        display: flex; align-items: center; justify-content: center; 
        font-size: 2.2rem; font-weight: bold; margin-top: 15px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. 헤더 영역 ---
logo_url = "https://raw.githubusercontent.com/jubailsanghoon/Heatinput/main/db65c0d39f36f2dddc248ea0bf2e4efc.jpg"
st.markdown(f'<div style="display:flex; align-items:center; border-bottom:4px solid black; padding-bottom:10px; margin-bottom:20px;"><img src="{logo_url}" width="55"><span style="font-size:1.6rem; margin-left:15px; font-weight:bold;">Heat Input Master</span></div>', unsafe_allow_html=True)

# --- 4. 메인 시공 ---

# [섹션 1] Standard - 지시하신 대로 계수 표기 삭제
st.markdown("### Standard Selection", unsafe_allow_html=True)
st.markdown('<div class="std-container">', unsafe_allow_html=True)
std_mode = st.radio("Std", ['ISO Standard', 'AWS Standard'], horizontal=True, label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

# [섹션 2] WPS Range
st.markdown("### WPS Range (kJ/mm)", unsafe_allow_html=True)
c_min, c_max = st.columns(2)
with c_min: w_min = st.number_input("Min", 1.0, step=0.1)
with c_max: w_max = st.number_input("Max", 2.5, step=0.1)

# [섹션 1'] Select Process
st.markdown("### Select Process", unsafe_allow_html=True)
st.markdown('<div class="proc-container">', unsafe_allow_html=True)
proc = st.radio("Proc", ['SAW', 'FCAW', 'SMAW', 'GMAW'], label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

# --- [k-factor 로직] 엔진 내부로 격리 ---
if std_mode == 'ISO Standard':
    if proc == 'SAW': k_val = 1.0
    elif proc in ['SMAW', 'GMAW', 'FCAW']: k_val = 0.8
    else: k_val = 0.8 # 기본값
else: # AWS Standard
    k_val = 1.0 # AWS는 전통적으로 Gross Heat Input 사용

# --- [섹션 3] Input Parameters (콤팩트 레이아웃) ---
st.markdown("### Input Parameters", unsafe_allow_html=True)

# Session State 초기화
for key, val in {'v':28.0, 'a':220.0, 'l':150.0, 't':120.0}.items():
    if key not in st.session_state: st.session_state[key] = val

def compact_welding_input(label, val_key, step):
    st.markdown('<div class="param-row">', unsafe_allow_html=True)
    c_label, c_minus, c_input, c_plus = st.columns([3.5, 1.5, 2.5, 1.5])
    
    with c_label: st.markdown(f'<div class="label-box">{label}</div>', unsafe_allow_html=True)
    with c_minus: 
        if st.button("-", key=f"{val_key}_m"): st.session_state[val_key] -= step
    with c_input:
        st.markdown(f'<div class="compact-input">', unsafe_allow_html=True)
        # 텍스트 입력을 통해 숫자창 폭을 좁게 유지
        st.text_input(label, value=f"{st.session_state[val_key]:.1f}", label_visibility="collapsed", key=f"{val_key}_disp")
        st.markdown('</div>', unsafe_allow_html=True)
    with c_plus:
        if st.button("+", key=f"{val_key}_p"): st.session_state[val_key] += step
    st.markdown('</div>', unsafe_allow_html=True)

compact_welding_input("Voltage (V)", "v", 0.5)
compact_welding_input("Amperage (A)", "a", 5.0)
compact_welding_input("Length (mm)", "l", 10.0)
compact_welding_input("Time (Sec)", "t", 1.0)

v, a, l, t = st.session_state.v, st.session_state.a, st.session_state.l, st.session_state.t

# --- 5. 결과 영역 ---
hi = (k_val * v * a * t) / (l * 1000) if l > 0 else 0
is_pass = w_min <= hi <= w_max

st.markdown(f'<div class="result-box">{hi:.3f} kJ/mm</div>', unsafe_allow_html=True)
st_bg = color_pass if is_pass else color_fail
st.markdown(f'<div style="background:{st_bg}; color:white !important; height:55px; display:flex; align-items:center; justify-content:center; font-size:1.5rem; font-weight:bold; border-radius:4px; margin-top:10px; border:2px solid black;">{"PASS" if is_pass else "FAIL"} (k={k_val})</div>', unsafe_allow_html=True)

st.button("💾 SAVE LOG DATA", use_container_width=True)
if st.session_state.history:
    st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True)