import streamlit as st

st.set_page_config(page_title="Heat Input Master", layout="centered")

# =====================================================
# 🔥 MOBILE OPTIMIZED CSS
# =====================================================
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
    border-bottom: 3px solid black;
    margin-top: 18px;
    margin-bottom: 10px;
}

/* 버튼 기본 */
.stButton>button {
    width: 100%;
    height: 55px;
    font-size: 18px;
    font-weight: 900;
    border: 2px solid black;
    background-color: white;
    color: black;
}

/* 활성 버튼 */
.active {
    background-color: black !important;
    color: white !important;
}

/* number_input 기본 + - 제거 */
input[type=number]::-webkit-outer-spin-button,
input[type=number]::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
}

input[type=number] {
    -moz-appearance: textfield;
    width: 90px !important;
    text-align: center;
    font-weight: 800 !important;
    font-size: 16px !important;
}

/* 결과 박스 */
.result-box {
    border: 3px solid black;
    padding: 10px;
    margin-top: 8px;
    font-size: 18px;
    font-weight: 900;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# Session State
# =====================================================
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

# =====================================================
# 1️⃣ Standard Selection
# =====================================================
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

# 활성 표시
if st.session_state.standard == "ISO":
    st.markdown("""
    <style>
    div[data-testid="stHorizontalBlock"] button:nth-child(1){
        background:black !important;
        color:white !important;
    }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    div[data-testid="stHorizontalBlock"] button:nth-child(2){
        background:black !important;
        color:white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# =====================================================
# 2️⃣ WPS Range
# =====================================================
st.markdown('<div class="section-title">WPS Range</div>', unsafe_allow_html=True)

w1, w2 = st.columns([3,1])
with w1:
    st.session_state.wps_min = st.number_input("Min.", value=st.session_state.wps_min, step=0.1)
with w2:
    st.write("kJ/mm")

w3, w4 = st.columns([3,1])
with w3:
    st.session_state.wps_max = st.number_input("Max.", value=st.session_state.wps_max, step=0.1)
with w4:
    st.write("kJ/mm")

# =====================================================
# 3️⃣ Process Selection
# =====================================================
st.markdown('<div class="section-title">Select Process</div>', unsafe_allow_html=True)

p1, p2 = st.columns(2)
p3, p4 = st.columns(2)

def process_btn(name, col):
    with col:
        if st.button(name):
            st.session_state.process = name
            st.rerun()

process_btn("SAW", p1)
process_btn("FCAW", p2)
process_btn("SMAW", p3)
process_btn("GMAW", p4)

# =====================================================
# 4️⃣ Input Parameters
# =====================================================
st.markdown('<div class="section-title">Input Parameters</div>', unsafe_allow_html=True)

def input_row(label, key, step):

    l, m, v, p = st.columns([2.5,1,2,1])

    with l:
        st.markdown(f"**{label}**")

    with m:
        if st.button("-", key=f"minus_{key}"):
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
        if st.button("+", key=f"plus_{key}"):
            st.session_state[key] += step
            st.rerun()

input_row("Voltage (V)", "voltage", 1.0)
input_row("Amperage (A)", "current", 10.0)
input_row("Length (mm)", "length", 10.0)
input_row("Time (Sec)", "time", 1.0)

# =====================================================
# 5️⃣ Calculation
# =====================================================
if st.session_state.standard == "AWS":
    k = 1.0
else:
    k = 1.0 if st.session_state.process == "SAW" else 0.8

V = st.session_state.voltage
A = st.session_state.current
t = st.session_state.time
L = st.session_state.length

HI = (k * V * A * t) / (L * 1000)

# =====================================================
# 6️⃣ Live Result
# =====================================================
st.markdown('<div class="section-title">Live Result</div>', unsafe_allow_html=True)

st.markdown(f'<div class="result-box">kJ/mm : {HI:.3f}</div>', unsafe_allow_html=True)

if HI < st.session_state.wps_min:
    status = "Below Min"
elif HI > st.session_state.wps_max:
    status = "Above Max"
else:
    status = "Pass"

st.markdown(f'<div class="result-box">{status}</div>', unsafe_allow_html=True)

# =====================================================
# 7️⃣ Save Data
# =====================================================
if st.button("Save Data"):
    st.success("Saved (Demo)")