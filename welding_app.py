import streamlit as st
import pandas as pd
from datetime import datetime

# 페이지 설정
st.set_page_config(layout="centered", page_title="Heat Input Master")

# ======================================================
# CSS - 디자인 디테일 및 버튼 스타일
# ======================================================
st.markdown("""
<style>
    body { background-color:#F2F2F2; }
    .main-container { max-width:700px; margin:auto; font-family: 'Segoe UI', sans-serif; }

    /* Header */
    .header { display:flex; align-items:center; border-bottom:5px solid black; padding-bottom:10px; margin-bottom:20px; }
    .header img { height:50px; margin-right:15px; }
    .title { font-size:28px; font-weight:900; }

    /* Section Title */
    .section-title { font-size:18px; font-weight:900; margin-top:20px; margin-bottom:15px; }

    /* Result & Button Boxes */
    .result-box { font-size:24px; font-weight:900; padding:15px; background:#ffe5cc; border:3px solid black; text-align: center; margin-bottom: 10px; }
    .pass, .fail { font-size:24px; font-weight:900; padding:15px; border:3px solid black; text-align: center; margin-bottom: 10px; }
    .pass { background:#00cc44; color:white; }
    .fail { background:#ff7f00; color:white; }

    /* Save Data Button Styling (Customizing Streamlit Button) */
    div.stButton > button {
        width: 100%;
        height: 65px;
        font-size: 24px !important;
        font-weight: 900 !important;
        background-color: #E0E0E0 !important; /* 연회색 */
        color: black !important;
        border: 3px solid black !important;
        border-radius: 0px !important;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #CCCCCC !important;
        border-color: black !important;
    }
</style>
""", unsafe_allow_html=True)

# 데이터 저장용 session_state 초기화
if 'history' not in st.session_state:
    st.session_state.history = []

st.markdown('<div class="main-container">', unsafe_allow_html=True)

# ======================================================
# Header
# ======================================================
st.markdown(f"""
<div class="header">
<img src="https://raw.githubusercontent.com/jubailsanghoon/Heatinput/main/db65c0d39f36f2dddc248ea0bf2e4efc.jpg">
<div class="title">Heat Input Master</div>
</div>
""", unsafe_allow_html=True)

# ======================================================
# 1️⃣ Standard + Process Selection
# ======================================================
c_std, c_prc = st.columns([1, 1])
with c_std:
    st.markdown('<div class="section-title">Standard Selection</div>', unsafe_allow_html=True)
    standard = st.radio("Std", ["AWS","ISO"], horizontal=True, label_visibility="collapsed")
with c_prc:
    st.markdown('<div class="section-title">Select Process</div>', unsafe_allow_html=True)
    process = st.radio("Prc", ["SAW","FCAW","SMAW","GMAW"], horizontal=True, label_visibility="collapsed")

# ======================================================
# 2️⃣ WPS Range
# ======================================================
st.markdown('<div class="section-title">WPS Range (kJ/mm)</div>', unsafe_allow_html=True)
w1, w2, w3, w4, w5 = st.columns([1, 2, 1, 2, 3])
with w1: st.markdown("**Min.**")
with w2: min_range = st.number_input("min", value=0.96, step=0.01, format="%.2f", label_visibility="collapsed")
with w3: st.markdown("**Max.**")
with w4: max_range = st.number_input("max", value=2.50, step=0.01, format="%.2f", label_visibility="collapsed")

# ======================================================
# 3️⃣ Input + Result Layout
# ======================================================
st.write("") 
col_left, col_space, col_right = st.columns([5, 1, 4])

with col_left:
    st.markdown('<div class="section-title">Input Parameters</div>', unsafe_allow_html=True)
    def draw_input_row(label, value, key):
        r1, r2 = st.columns([2, 2])
        with r1: st.markdown(f"**{label}**")
        with r2: return st.number_input(label, value=value, step=0.1, format="%.1f", key=key, label_visibility="collapsed")

    voltage = draw_input_row("Voltage (V)", 30.0, "v")
    current = draw_input_row("Current (A)", 300.0, "c")
    length  = draw_input_row("Length (mm)", 5.0, "l")
    time    = draw_input_row("Time (sec)", 1.0, "t")

# Calculation Logic
if standard == "AWS":
    k = 1.0
else:
    efficiency = {"SAW": 1.0, "GMAW": 0.8, "FCAW": 0.8, "SMAW": 0.8}
    k = efficiency.get(process, 0.8)

HI = (k * voltage * current * time) / (length * 1000) if length > 0 else 0
status = "PASS" if min_range <= HI <= max_range else "FAIL"

with col_right:
    st.markdown('<div class="section-title">Live Result</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="result-box">{HI:.3f} kJ/mm</div>', unsafe_allow_html=True)
    
    # PASS / FAIL Display
    st.markdown(f'<div class="{status.lower()}">{status}</div>', unsafe_allow_html=True)

    # Save Data Button
    if st.button("Save Data"):
        new_data = {
            "Time": datetime.now().strftime("%H:%M:%S"),
            "Std": standard,
            "Process": process,
            "HI (kJ/mm)": round(HI, 3),
            "Result": status,
            "V": voltage, "A": current, "L": length, "T": time
        }
        # 50개까지만 저장 (최신 데이터가 위로)
        st.session_state.history.insert(0, new_data)
        if len(st.session_state.history) > 50:
            st.session_state.history.pop()

# ======================================================
# 4️⃣ History Table (저장된 데이터 보기)
# ======================================================
if st.session_state.history:
    st.markdown('<div class="section-title">Recent History (Max 50)</div>', unsafe_allow_html=True)
    df = pd.DataFrame(st.session_state.history)
    st.table(df) # 혹은 st.dataframe(df) 사용 가능

st.markdown('</div>', unsafe_allow_html=True)