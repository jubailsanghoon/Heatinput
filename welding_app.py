import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 페이지 설정 ---
st.set_page_config(page_title="Heat Input Master", layout="centered")

# --- 2. 데이터 세션 관리 (수동 입력 및 버튼 연동) ---
if 'v' not in st.session_state: st.session_state.v = 28.0
if 'a' not in st.session_state: st.session_state.a = 220.0
if 'l' not in st.session_state: st.session_state.l = 150.0
if 't' not in st.session_state: st.session_state.t = 120.0
if 'history' not in st.session_state: st.session_state.history = []

# --- 3. CSS 정밀 시공 (글자 크기 및 버튼 위치 고정) ---
st.markdown("""
<style>
    .stApp { background-color: #F2F2F2; max-width: 480px; margin: 0 auto; }
    * { color: #000000 !important; font-family: 'Inter', sans-serif; }

    /* ISO, AWS 큰 글씨 시인성 확보 */
    .big-std-text { font-size: 1.8rem !important; font-weight: 900 !important; }

    /* 섹션 제목 */
    .section-title { font-size: 1.3rem; font-weight: 800; margin: 20px 0 10px 0; border-left: 6px solid #000; padding-left: 10px; }

    /* 라디오 버튼 (ISO, AWS) */
    div[role="radiogroup"] { display: grid !important; grid-template-columns: 1fr 1fr !important; gap: 10px !important; }
    div[role="radiogroup"] label {
        height: 70px !important; border: 3px solid #000 !important; background: #FFF !important;
        justify-content: center !important; border-radius: 6px !important;
    }
    div[role="radiogroup"] label[data-checked="true"] { background: #000 !important; }
    div[role="radiogroup"] label[data-checked="true"] p { color: #FFF !important; font-size: 1.8rem !important; font-weight: 900 !important; }
    div[role="radiogroup"] label p { font-size: 1.8rem !important; font-weight: 900 !important; }

    /* [핵심] 파라미터 입력 레이아웃 */
    .param-row { display: flex; align-items: center; width: 100%; margin-bottom: 10px; }
    
    /* 버튼 스타일 (검은색 대신 시인성 좋은 회색/흰색 조합 가능하지만, 지시에 따라 색상 조정) */
    .stButton button {
        width: 100% !important; height: 50px !important; 
        background: #E0E0E0 !important; color: #000 !important; /* 버튼 배경 연하게 조정 */
        font-size: 1.8rem !important; font-weight: bold !important;
        border: 2px solid #000 !important; border-radius: 4px !important;
    }

    /* 숫자 입력창 (수동 입력 가능하게 유지) */
    .stNumberInput input {
        height: 50px !important; font-size: 1.4rem !important; font-weight: 800 !important;
        text-align: center !important; border: 2px solid #000 !important; background: #FFF !important;
    }
    
    /* 결과창 */
    .result-display { background: #FFF; border: 4px solid #000; height: 90px; display: flex; align-items: center; justify-content: center; font-size: 2.5rem; font-weight: 900; }
    .status-banner { height: 65px; display: flex; align-items: center; justify-content: center; font-size: 2rem; font-weight: bold; border-radius: 6px; margin-top: 10px; border: 3px solid #000; color: #FFF !important; }
</style>
""", unsafe_allow_html=True)

# --- 4. 상단 타이틀 ---
st.markdown(f'<div style="border-bottom:5px solid #000; padding-bottom:10px; margin-bottom:20px;"><img src="https://raw.githubusercontent.com/jubailsanghoon/Heatinput/main/db65c0d39f36f2dddc248ea0bf2e4efc.jpg" width="60"><span style="font-size:1.8rem; font-weight:900; margin-left:15px;">Heat Input Master</span></div>', unsafe_allow_html=True)

# --- 5. 레이아웃 배치 ---

# [섹션 1] Standard (ISO / AWS 크게)
st.markdown('<div class="section-title">Standard</div>', unsafe_allow_html=True)
std_mode = st.radio("Std", ['ISO', 'AWS'], horizontal=True, label_visibility="collapsed")

# [섹션 2] WPS Range (제한 해제)
st.markdown('<div class="section-title">WPS Range (kJ/mm)</div>', unsafe_allow_html=True)
col_min, col_max = st.columns(2)
with col_min: 
    # min_value를 None으로 설정하여 제한 해제
    w_min = st.number_input("Min", value=1.0, step=0.1, format="%.1f")
with col_max: 
    w_max = st.number_input("Max", value=2.5, step=0.1, format="%.1f")

# [섹션 3] Process
st.markdown('<div class="section-title">Select Process</div>', unsafe_allow_html=True)
proc = st.radio("Proc", ['SAW', 'FCAW', 'SMAW', 'GMAW'], horizontal=True, label_visibility="collapsed")

# [핵심] [섹션 4] Input Parameters (Label - Minus - Input - Plus)
st.markdown('<div class="section-title">Input Parameters</div>', unsafe_allow_html=True)

def build_welding_row(label, key, step_val):
    # 소장님 지시: [라벨] [-] [입력창] [+]
    c_label, c_minus, c_input, c_plus = st.columns([3.5, 1.5, 3.5, 1.5])
    
    with c_label:
        st.markdown(f"<div style='padding-top:12px; font-weight:bold; font-size:1.1rem;'>{label}</div>", unsafe_allow_html=True)
    
    with c_minus:
        if st.button("－", key=f"btn_m_{key}"):
            st.session_state[key] = round(st.session_state[key] - step_val, 2)
            st.rerun()
            
    with c_input:
        # 수동 입력 가능하도록 st.number_input 사용하되 화살표 제거
        val = st.number_input(label, value=st.session_state[key], step=0.01, format="%.1f", label_visibility="collapsed", key=f"num_{key}")
        st.session_state[key] = val # 수동 입력값 동기화
        
    with c_plus:
        if st.button("＋", key=f"btn_p_{key}"):
            st.session_state[key] = round(st.session_state[key] + step_val, 2)
            st.rerun()

build_welding_row("Voltage (V)", 'v', 0.5)
build_welding_row("Amperage (A)", 'a', 5.0)
build_welding_row("Length (mm)", 'l', 10.0)
build_welding_row("Time (Sec)", 't', 1.0)

# --- 6. 계산 및 결과 ---
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