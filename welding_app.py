import streamlit as st

st.set_page_config(page_title="Heat Input Master", layout="centered")

# =========================================================
# 🔥 CSS (모바일 480px 고정 + 고대비 + 오렌지 활성화)
# =========================================================
st.markdown("""
<style>

html, body, .main {
    background-color: #F2F2F2;
    font-family: Arial, Helvetica, sans-serif;
}

.block-container {
    max-width: 480px;
    padding-top: 10px;
}

/* 제목 */
.section-title {
    font-size: 22px;
    font-weight: 900;
    border-bottom: 5px solid #000000;
    margin-top: 20px;
    margin-bottom: 12px;
}

/* Header */
.header-title {
    font-size: 26px;
    font-weight: 900;
}

/* 대형 버튼 */
.stButton>button {
    width: 100%;
    height: 72px;
    font-size: 22px;
    font-weight: 900;
    border: 3px solid #000000;
    background-color: white;
    color: black;
}

/* 선택된 버튼 */
.active-btn {
    background-color: #FF7A00 !important;
    color: white !important;
    border: 3px solid #000000 !important;
}

/* number_input 기본 +/- 제거 */
input[type=number]::-webkit-outer-spin-button,
input[type=number]::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
}

input[type=number] {
    -moz-appearance: textfield;
    width: 90px !important;
    text-align: center;
    font-weight: 900 !important;
    font-size: 18px !important;
}

/* 결과 박스 */
.result-box {
    border: 3px solid #000000;
    padding: 12px;
    font-size: 20px;
    font-weight: 900;
    margin-top: 8px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# Session State 초기화
# =========================================================
defaults = {
    "standard": "ISO",
    "process": "SAW",
    "voltage": 30.0,
    "current": 300.0,
    "time": 10.0,
    "length": 100.0,
    "wps_min": 1.0,
    "wps_max": 2.5
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# =========================================================
# S1 Header
# =========================================================
col1, col2 = st.columns([1,4])

with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/921/921347.png", width=50)

with col2:
    st.markdown('<div class="header-title">Heat Input Master</div>', unsafe_allow_html=True)

st.markdown('<div style="border-bottom:5px solid #000000;margin-top:10px;"></div>', unsafe_allow_html=True)

# =========================================================
# S2 Standard Selection
# =========================================================
st.markdown('<div class="section-title">Standard Selection</div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:
    if st.button("ISO"):
        st.session_state.standard = "ISO"
        st.rerun()

with c2:
    if st.button("AWS"):
        st.session_state.standard = "AWS"
        st.rerun()

# 활성화 표시
if st.session_state.standard == "ISO":
    st.markdown("""
    <style>
    div[data-testid="stHorizontalBlock"] button:nth-child(1){
        background:#FF7A00 !important;
        color:white !important;
    }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    div[data-testid="stHorizontalBlock"] button:nth-child(2){
        background:#FF7A00 !important;
        color:white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# =========================================================
# S3 WPS Range
# =========================================================
st.markdown('<div class="section-title">WPS Range (kJ/mm)</div>', unsafe_allow_html=True)

w1, w2 = st.columns(2)

with w1:
    st.session_state.wps_min = st.number_input("Min", value=st.session_state.wps_min, step=0.1)

with w2:
    st.session_state.wps_max = st.number_input("Max", value=st.session_state.wps_max, step=0.1)

# =========================================================
# S4 Process Selection
# =========================================================
st.markdown('<div class="section-title">Select Process</div>', unsafe_allow_html=True)

p1, p2 = st.columns(2)
p3, p4 = st.columns(2)

def process_button(name, col):
    with col:
        if st.button(name):
            st.session_state.process = name
            st.rerun()

process_button("SAW", p1)
process_button("FCAW", p2)
process_button("SMAW", p3)
process_button("GMAW", p4)

# =========================================================
# S5 Input Parameters
# =========================================================
st.markdown('<div class="section-title">Input Parameters</div>', unsafe_allow_html=True)

def input_row(label, key, step):

    l, m, v, p = st.columns([3.5,1.5,3.5,1.5])  # 35/15/35/15

    with l:
        st.markdown(f"<div style='font-weight:900;font-size:18px;'>{label}</div>", unsafe_allow_html=True)

    with m:
        if st.button("－", key=f"minus_{key}"):
            st.session_state[key] -= step
            st.rerun()

    with v:
        st.session_state[key] = st.number_input(
            "",
            value=st.session_state[key],
            step=step,
            key=f"input_{key}",
            label_visibility="collapsed"
        )

    with p:
        if st.button("＋", key=f"plus_{key}"):
            st.session_state[key] += step
            st.rerun()

input_row("Voltage (V)", "voltage", 1.0)
input_row("Current (A)", "current", 10.0)
input_row("Time (Sec)", "time", 1.0)
input_row("Length (mm)", "length", 10.0)

# =========================================================
# Calculation Logic
# =========================================================
if st.session_state.standard == "AWS":
    k = 1.0
else:
    k = 1.0 if st.session_state.process == "SAW" else 0.8

V = st.session_state.voltage
A = st.session_state.current
t = st.session_state.time
L = st.session_state.length

HI = (k * V * A * t) / (L * 1000)

# =========================================================
# Live Result
# =========================================================
st.markdown('<div class="section-title">Live Result</div>', unsafe_allow_html=True)

st.markdown(f'<div class="result-box">kJ/mm : {HI:.3f}</div>', unsafe_allow_html=True)

if HI < st.session_state.wps_min:
    status = "Below WPS Min"
elif HI > st.session_state.wps_max:
    status = "Above WPS Max"
else:
    status = "Pass"

st.markdown(f'<div class="result-box">{status}</div>', unsafe_allow_html=True)