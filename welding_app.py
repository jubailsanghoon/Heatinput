import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 페이지 초기 설정 ---
st.set_page_config(page_title="Heat Input Master", layout="centered")

# 데이터 동기화 (버튼 작동용 세션 관리)
for k, v in {'v': 28.0, 'a': 220.0, 'l': 150.0, 't': 120.0}.items():
    if k not in st.session_state: st.session_state[k] = v
if 'history' not in st.session_state: st.session_state.history = []

# --- 2. CSS 정밀 타설 (레이아웃 강제 고정) ---
st.markdown("""
<style>
    /* 전체 배경 및 폭 고정 (450px) */
    .stApp { background-color: #F2F2F2; max-width: 450px; margin: 0 auto; }
    * { color: #000000 !important; font-family: 'Inter', sans-serif; }

    /* 헤더 스타일 */
    .header-box { display: flex; align-items: center; border-bottom: 5px solid #000; padding-bottom: 10px; margin-bottom: 20px; }
    
    /* 섹션 제목 */
    .section-title { font-size: 1.2rem; font-weight: 800; margin: 25px 0 12px 0; border-left: 6px solid #000; padding-left: 10px; }

    /* 라디오 버튼 (Standard, Process) - 2열 그리드 고정 */
    div[role="radiogroup"] { display: grid !important; grid-template-columns: 1fr 1fr !important; gap: 10px !important; }
    div[role="radiogroup"] label {
        height: 60px !important; border: 2px solid #000 !important; background: #FFF !important;
        justify-content: center !important; font-weight: bold !important; border-radius: 4px !important;
    }
    div[role="radiogroup"] label[data-checked="true"] { background: #000 !important; }
    div[role="radiogroup"] label[data-checked="true"] p { color: #FFF !important; }

    /* [핵심] 파라미터 행 - 폭 비율 강제 고정 */
    /* 라벨(35%) | 마이너스(15%) | 숫자(35%) | 플러스(15%) */
    .param-row { display: flex; align-items: center; width: 100%; margin-bottom: 15px; }
    .label-area { width: 35%; font-size: 1.1rem; font-weight: bold; }
    
    /* 버튼 스타일 */
    .stButton button {
        width: 100% !important; height: 55px !important; 
        background: #000 !important; color: #FFF !important;
        font-size: 1.8rem !important; font-weight: bold !important;
        border: none !important; border-radius: 4px !important;
    }
    
    /* 숫자 표시 칸 (중앙 콤팩트 박스) */
    .value-box {
        width: 90px; height: 55px; background: #FFF; border: 2px solid #000;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.4rem; font-weight: 900; border-radius: 4px; margin: 0 5px;
    }

    /* 결과창 */
    .result-display { background: #FFF; border: 4px solid #000; height: 90px; display: flex; align-items: center; justify-content: center; font-size: 2.3rem; font-weight: 900; margin-top: 15px; }
    .pass-fail { height: 60px; display: flex; align-items: center; justify-content: center; font-size: 1.8rem; font-weight: bold; border-radius: 4px; margin-top: 10px; border: 2px solid #000; color: #FFF !important; }
</style>
""", unsafe_allow_html=True)

# --- 3. 상부 타이틀 ---
st.markdown('<div class="header-box"><img src="https://raw.githubusercontent.com/jubailsanghoon/Heatinput/main/db65c0d39f36f2dddc248ea0bf2e4efc.jpg" width="60"><span style="font-size: 1.6rem; margin-left: 15px; font-weight: 900;">Heat Input Master</span></div>', unsafe_allow_html=True)

# --- 4. 레이아웃 순차 배치 ---

# [섹션 1] Standard Selection
st.markdown('<div class="section-title">Standard Selection</div>', unsafe_allow_html=True)
std_mode = st.radio("Std", ['ISO Standard', 'AWS Standard'], horizontal=True, label_visibility="collapsed")

# [섹션 2] WPS Range
st.markdown('<div class="section-title">WPS Range (kJ/mm)</div>', unsafe_allow_html=True)
col_min, col_max = st.columns(2)
with col_min: w_min = st.number_input("Min", 1.0, step=0.1, format="%.1f")
with col_max: w_max = st.number_input("Max", 2.5, step=0.1, format="%.1f")

# [섹션 3] Select Process
st.markdown('<div class="section-title">Select Process</div>', unsafe_allow_html=True)
proc = st.radio("Proc", ['SAW', 'FCAW', 'SMAW', 'GMAW'], horizontal=True, label_visibility="collapsed")

# [k-factor 로직]
k_val = 1.0 if std_mode == 'AWS Standard' or proc == 'SAW' else 0.8

# [섹션 4] Input Parameters (증감 버튼 로직 고정)
st.markdown('<div class="section-title">Input Parameters</div>', unsafe_allow_html=True)

def build_row(label, key, step):
    # CSS 비율에 맞춰 컬럼 분할 (라벨 4 : 마이너스 1.5 : 숫자 2.5 : 플러스 1.5)
    c_lab, c_min, c_val, c_plus = st.columns([4, 1.5, 2.5, 1.5])
    with c_lab: st.markdown(f'<div style="padding-top:15px; font-weight:bold;">{label}</div>', unsafe_allow_html=True)
    with c_min: 
        if st.button("－", key=f"m_{key}"): 
            st.session_state[key] = round(st.session_state[key] - step, 1)
            st.rerun()
    with c_val: st.markdown(f'<div class="value-box">{st.session_state[key]:.1f}</div>', unsafe_allow_html=True)
    with c_plus: 
        if st.button("＋", key=f"p_{key}"): 
            st.session_state[key] = round(st.session_state[key] + step, 1)
            st.rerun()

build_row("Voltage (V)", 'v', 0.5)
build_row("Amperage (A)", 'a', 5.0)
build_row("Length (mm)", 'l', 10.0)
build_row("Time (Sec)", 't', 1.0)

# --- 5. 결과 산출 및 로그 ---
v, a, l, t = st.session_state.v, st.session_state.a, st.session_state.l, st.session_state.t
hi = (k_val * v * a * t) / (l * 1000) if l > 0 else 0
is_pass = w_min <= hi <= w_max

st.markdown('<div class="section-title">Live Result</div>', unsafe_allow_html=True)
st.markdown(f'<div class="result-display">{hi:.3f} kJ/mm</div>', unsafe_allow_html=True)

res_color = "#28A745" if is_pass else "#DC3545"
st.markdown(f'<div class="pass-fail" style="background:{res_color};">{"PASS" if is_pass else "FAIL"}</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
if st.button("💾 SAVE LOG DATA", use_container_width=True):
    st.session_state.history.insert(0, {"Time": datetime.now().strftime("%H:%M:%S"), "Proc": proc, "HI": f"{hi:.3f}", "Status": "PASS" if is_pass else "FAIL"})
    st.toast("Saved!")

if st.session_state.history:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.table(pd.DataFrame(st.session_state.history).head(5))