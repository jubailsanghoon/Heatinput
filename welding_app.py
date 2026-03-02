import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 페이지 설정 (모바일 규격 중앙 정렬) ---
st.set_page_config(page_title="Heat Input Master", layout="centered")

# --- 2. 세션 상태 초기화 (입력값 제어용) ---
if 'v' not in st.session_state: st.session_state.v = 28.0
if 'a' not in st.session_state: st.session_state.a = 220.0
if 'l' not in st.session_state: st.session_state.l = 150.0
if 't' not in st.session_state: st.session_state.t = 120.0
if 'history' not in st.session_state: st.session_state.history = []

# --- 3. CSS 초정밀 시공 (소장님 레이아웃 완벽 재현) ---
st.markdown(f"""
    <style>
    /* 전체 배경 및 중앙 450px 기둥 세우기 */
    .stApp {{
        background-color: #F2F2F2;
        max-width: 450px;
        margin: 0 auto;
        border-left: 1px solid #ddd;
        border-right: 1px solid #ddd;
    }}

    /* 모든 텍스트 검정색 및 굵기 고정 */
    * {{ color: #000000 !important; font-family: 'Inter', sans-serif; }}
    
    /* 섹션 제목 (라벨) */
    .section-title {{
        font-size: 1.2rem; font-weight: bold;
        margin-top: 25px; margin-bottom: 10px;
        border-left: 5px solid #000; padding-left: 10px;
    }}

    /* [섹션 1, 2] 라디오 버튼 그리드 (Standard, Process) */
    div[role="radiogroup"] {{ display: grid !important; gap: 8px !important; }}
    /* Standard: 2열 배치 */
    .std-box div[role="radiogroup"] {{ grid-template-columns: repeat(2, 1fr) !important; }}
    /* Process: 2열 배치 */
    .proc-box div[role="radiogroup"] {{ grid-template-columns: repeat(2, 1fr) !important; }}
    
    div[role="radiogroup"] label {{
        height: 55px !important; border: 2px solid #000 !important;
        background-color: #FFF !important; justify-content: center !important;
        font-weight: bold !important; border-radius: 4px !important;
    }}
    div[role="radiogroup"] label[data-checked="true"] {{ background-color: #000 !important; }}
    div[role="radiogroup"] label[data-checked="true"] p {{ color: #FFF !important; }}

    /* [섹션 3] 파라미터 입력창 (핵심: 라벨 - 버튼 - 숫자 - 버튼) */
    .param-container {{
        display: flex; align-items: center; justify-content: space-between;
        margin-bottom: 15px; width: 100%;
    }}
    .param-label {{ width: 35%; font-size: 1.1rem; font-weight: 600; }}
    
    /* 조작 버튼 (-) (+) */
    .stButton button {{
        width: 50px !important; height: 50px !important;
        font-size: 1.5rem !important; font-weight: bold !important;
        border: 2px solid #000 !important; background: #000 !important;
        color: #FFF !important; border-radius: 4px !important;
        display: flex; align-items: center; justify-content: center;
        padding: 0 !important;
    }}

    /* 숫자창 (가운데 콤팩트 박스) */
    .value-display {{
        width: 80px; height: 50px; border: 2px solid #000;
        background: #FFF; display: flex; align-items: center;
        justify-content: center; font-size: 1.3rem; font-weight: bold;
        border-radius: 4px;
    }}

    /* 결과창 */
    .result-value {{
        background: #FFF; border: 3px solid #000; height: 80px;
        display: flex; align-items: center; justify-content: center;
        font-size: 2.3rem; font-weight: bold; margin-top: 15px;
    }}
    .status-banner {{
        height: 60px; display: flex; align-items: center; justify-content: center;
        font-size: 1.8rem; font-weight: bold; border-radius: 4px;
        margin-top: 10px; border: 2px solid #000; color: #FFF !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. 헤더 영역 ---
st.markdown(f"""
    <div style="display: flex; align-items: center; border-bottom: 5px solid black; padding-bottom: 10px; margin-bottom: 10px;">
        <img src="https://raw.githubusercontent.com/jubailsanghoon/Heatinput/main/db65c0d39f36f2dddc248ea0bf2e4efc.jpg" width="60">
        <span style="font-size: 1.6rem; margin-left: 15px; font-weight: bold;">Heat Input Master</span>
    </div>
""", unsafe_allow_html=True)

# --- 5. 레이아웃 순서대로 배치 ---

# [섹션 1] Standard Selection
st.markdown('<div class="section-title">Standard Selection</div>', unsafe_allow_html=True)
st.markdown('<div class="std-box">', unsafe_allow_html=True)
std_mode = st.radio("Std", ['ISO Standard', 'AWS Standard'], horizontal=True, label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

# [섹션 2] WPS Range
st.markdown('<div class="section-title">WPS Range (kJ/mm)</div>', unsafe_allow_html=True)
col_min, col_max = st.columns(2)
with col_min: w_min = st.number_input("Min", value=1.0, step=0.1, format="%.1f")
with col_max: w_max = st.number_input("Max", value=2.5, step=0.1, format="%.1f")

# [섹션 3] Select Process
st.markdown('<div class="section-title">Select Process</div>', unsafe_allow_html=True)
st.markdown('<div class="proc-box">', unsafe_allow_html=True)
proc = st.radio("Proc", ['SAW', 'FCAW', 'SMAW', 'GMAW'], label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

# 효율 계수 k 로직
if std_mode == 'ISO Standard':
    k_val = 1.0 if proc == 'SAW' else 0.8
else:
    k_val = 1.0

# [섹션 4] Input Parameters (핵심: 증감 버튼 작동 로직)
st.markdown('<div class="section-title">Input Parameters</div>', unsafe_allow_html=True)

def manual_input_row(label, key, step):
    st.markdown(f'<div style="display:flex; align-items:center; margin-bottom:12px; width:100%;">', unsafe_allow_html=True)
    
    # 1. 라벨 (35%)
    st.markdown(f'<div class="param-label">{label}</div>', unsafe_allow_html=True)
    
    # 2. 버튼/입력 영역 (65%)
    c1, c2, c3 = st.columns([1, 1.8, 1])
    with c1:
        if st.button("－", key=f"minus_{key}"): 
            st.session_state[key] -= step
            st.rerun()
    with c2:
        st.markdown(f'<div class="value-display">{st.session_state[key]:.1f}</div>', unsafe_allow_html=True)
    with c3:
        if st.button("＋", key=f"plus_{key}"): 
            st.session_state[key] += step
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

manual_input_row("Voltage (V)", 'v', 0.5)
manual_input_row("Amperage (A)", 'a', 5.0)
manual_input_row("Length (mm)", 'l', 10.0)
manual_input_row("Time (Sec)", 't', 1.0)

# --- 6. 계산 및 결과 출력 ---
v, a, l, t = st.session_state.v, st.session_state.a, st.session_state.l, st.session_state.t
hi = (k_val * v * a * t) / (l * 1000) if l > 0 else 0
is_pass = w_min <= hi <= w_max

st.markdown('<div class="section-title">Live Result</div>', unsafe_allow_html=True)
st.markdown(f'<div class="result-value">{hi:.3f} kJ/mm</div>', unsafe_allow_html=True)

status_text = "PASS" if is_pass else "FAIL"
status_color = "#28A745" if is_pass else "#DC3545"
st.markdown(f'<div class="status-banner" style="background:{status_color};">{status_text} (k={k_val})</div>', unsafe_allow_html=True)

# --- 7. 저장 버튼 및 이력 ---
st.markdown("<br>", unsafe_allow_html=True)
if st.button("💾 SAVE LOG DATA", use_container_width=True):
    st.session_state.history.insert(0, {
        "Time": datetime.now().strftime("%H:%M:%S"),
        "Proc": proc, "HI": f"{hi:.3f}", "Status": status_text
    })
    st.toast("Saved!")

if st.session_state.history:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.table(pd.DataFrame(st.session_state.history).head(5))