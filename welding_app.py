import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 페이지 설정 및 초기화 ---
st.set_page_config(page_title="Heat Input Master", layout="centered")

# 핵심 파라미터 메모리(State) 관리
params_config = {'v': 28.0, 'a': 220.0, 'l': 150.0, 't': 120.0}
for k, v in params_config.items():
    if k not in st.session_state: st.session_state[k] = v
if 'history' not in st.session_state: st.session_state.history = []

# --- 2. CSS 정밀 시공 (라벨-마이너스-입력-플러스) ---
st.markdown("""
<style>
    .stApp { background-color: #F2F2F2; max-width: 480px; margin: 0 auto; }
    * { color: #000000 !important; font-family: 'Inter', sans-serif; }

    /* ISO / AWS 큰 글씨 */
    div[role="radiogroup"] label p { font-size: 2.2rem !important; font-weight: 900 !important; }
    div[role="radiogroup"] label[data-checked="true"] { background: #000 !important; }
    div[role="radiogroup"] label[data-checked="true"] p { color: #FFF !important; }

    /* 섹션 타이틀 */
    .section-title { font-size: 1.3rem; font-weight: 900; margin: 20px 0 10px 0; border-left: 8px solid #000; padding-left: 12px; }

    /* 증감 버튼 (회색 배경 + 검정 테두리) */
    .stButton button {
        width: 100% !important; height: 50px !important; 
        background-color: #E0E0E0 !important; color: #000 !important;
        font-size: 1.8rem !important; font-weight: bold !important;
        border: 2px solid #000 !important; border-radius: 4px !important;
    }

    /* 숫자 입력창 (수동 입력 최적화) */
    .stNumberInput input {
        height: 50px !important; font-size: 1.4rem !important; font-weight: 900 !important;
        text-align: center !important; border: 2px solid #000 !important; background: #FFF !important;
    }

    /* 결과창 디자인 */
    .result-display { background: #FFF; border: 4px solid #000; height: 90px; display: flex; align-items: center; justify-content: center; font-size: 2.5rem; font-weight: 900; }
    .status-banner { height: 65px; display: flex; align-items: center; justify-content: center; font-size: 2rem; font-weight: 900; border-radius: 6px; margin-top: 10px; border: 3px solid #000; color: #FFF !important; }
</style>
""", unsafe_allow_html=True)

# --- 3. 헤더 ---
st.markdown('<div style="border-bottom:6px solid #000; padding-bottom:10px; margin-bottom:20px;"><img src="https://raw.githubusercontent.com/jubailsanghoon/Heatinput/main/db65c0d39f36f2dddc248ea0bf2e4efc.jpg" width="65"><span style="font-size:1.8rem; font-weight:900; margin-left:15px;">Heat Input Master</span></div>', unsafe_allow_html=True)

# --- 4. 레이아웃 배치 ---

# [섹션 1] Standard (ISO / AWS)
st.markdown('<div class="section-title">Standard</div>', unsafe_allow_html=True)
std_mode = st.radio("Std", ['ISO', 'AWS'], horizontal=True, label_visibility="collapsed")

# [섹션 2] WPS Range
st.markdown('<div class="section-title">WPS Range (kJ/mm)</div>', unsafe_allow_html=True)
c_min, c_max = st.columns(2)
with c_min: w_min = st.number_input("Min", value=1.0, step=0.1)
with c_max: w_max = st.number_input("Max", value=2.5, step=0.1)

# [섹션 3] Process
st.markdown('<div class="section-title">Select Process</div>', unsafe_allow_html=True)
proc = st.radio("Proc", ['SAW', 'FCAW', 'SMAW', 'GMAW'], horizontal=True, label_visibility="collapsed")

# [핵심] [섹션 4] Input Parameters (작동 검증 로직)
st.markdown('<div class="section-title">Input Parameters</div>', unsafe_allow_html=True)

def validated_row(label, key, step_val):
    # 컬럼 배치: [라벨] [－] [입력창] [＋]
    c_lab, c_btn_m, c_input, c_btn_p = st.columns([3.5, 1.5, 3.5, 1.5])
    
    with c_lab:
        st.markdown(f"<div style='padding-top:12px; font-weight:900; font-size:1.1rem;'>{label}</div>", unsafe_allow_html=True)
    
    with c_btn_m:
        if st.button("－", key=f"m_{key}"):
            st.session_state[key] = round(st.session_state[key] - step_val, 2)
            st.rerun() # 즉시 반영
            
    with c_input:
        # 수동 입력 시 session_state와 즉시 동기화
        typed_val = st.number_input(label, value=st.session_state[key], step=0.0, format="%.1f", label_visibility="collapsed", key=f"in_{key}")
        if typed_val != st.session_state[key]:
            st.session_state[key] = typed_val
        
    with c_btn_p:
        if st.button("＋", key=f"p_{key}"):
            st.session_state[key] = round(st.session_state[key] + step_val, 2)
            st.rerun() # 즉시 반영

validated_row("Voltage (V)", 'v', 0.5)
validated_row("Amperage (A)", 'a', 5.0)
validated_row("Length (mm)", 'l', 10.0)
validated_row("Time (Sec)", 't', 1.0)

# --- 5. 결과 산출 및 로그 ---
k_val = 1.0 if std_mode == 'AWS' or proc == 'SAW' else 0.8
v, a, l, t = st.session_state.v, st.session_state.a, st.session_state.l, st.session_state.t
hi = (k_val * v * a * t) / (l * 1000) if l > 0 else 0
is_pass = w_min <= hi <= w_max

st.markdown('<div class="section-title">Live Result</div>', unsafe_allow_html=True)
st.markdown(f'<div class="result-display">{hi:.3f} kJ/mm</div>', unsafe_allow_html=True)

res_color = "#28A745" if is_pass else "#DC3545"
st.markdown(f'<div class="status-banner" style="background:{res_color};">{"PASS" if is_pass else "FAIL"}</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
if st.button("💾 SAVE LOG DATA", use_container_width=True):
    st.session_state.history.insert(0, {"Time": datetime.now().strftime("%H:%M:%S"), "Proc": proc, "HI": f"{hi:.3f}", "Status": "PASS" if is_pass else "FAIL"})
    st.toast("Saved!")

if st.session_state.history:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.table(pd.DataFrame(st.session_state.history).head(5))