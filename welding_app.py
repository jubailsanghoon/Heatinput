import streamlit as st

st.set_page_config(layout="centered")

# ---------------------------
# CSS 스타일 (Field Spec.)
# ---------------------------
st.markdown("""
<style>
body {
    background-color: #F2F2F2;
}
.main-container {
    max-width: 460px;
    margin: auto;
}
.header {
    display:flex;
    align-items:center;
    border-bottom:5px solid black;
    padding-bottom:10px;
    margin-bottom:15px;
}
.header img {
    height:50px;
    margin-right:10px;
}
.title {
    font-size:28px;
    font-weight:900;
    color:black;
}
.big-button button {
    height:70px;
    font-size:20px;
    font-weight:bold;
    border:3px solid black;
}
.selected {
    background-color:#ff7f00 !important;
    color:white !important;
}
.section-title {
    font-size:20px;
    font-weight:900;
    margin-top:20px;
}
.result-box {
    font-size:26px;
    font-weight:900;
    padding:15px;
    background:#ffe5cc;
    text-align:center;
    border:3px solid black;
}
.pass {
    background-color:#00cc44;
    color:white;
    padding:10px;
    font-weight:900;
}
.fail {
    background-color:#ff7f00;
    color:white;
    padding:10px;
    font-weight:900;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-container">', unsafe_allow_html=True)

# ---------------------------
# Header
# ---------------------------
st.markdown("""
<div class="header">
<img src="https://raw.githubusercontent.com/jubailsanghoon/Heatinput/main/db65c0d39f36f2dddc248ea0bf2e4efc.jpg">
<div class="title">Heat Input Master</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------
# Session 초기화
# ---------------------------
defaults = {
    "standard": "ISO",
    "process": "SAW",
    "voltage": 30.0,
    "current": 300.0,
    "travel": 5.0,
    "time": 1.0,
    "min": 1.0,
    "max": 2.5
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------------------------
# S2 Standard Selection
# ---------------------------
st.markdown('<div class="section-title">Standard Selection</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

if col1.button("ISO", use_container_width=True):
    st.session_state.standard = "ISO"
    st.rerun()

if col2.button("AWS", use_container_width=True):
    st.session_state.standard = "AWS"
    st.rerun()

# ---------------------------
# S3 WPS Range
# ---------------------------
st.markdown('<div class="section-title">WPS Range (kJ/mm)</div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)
st.session_state.min = c1.number_input("Min", value=st.session_state.min)
st.session_state.max = c2.number_input("Max", value=st.session_state.max)

# ---------------------------
# S4 Select Process
# ---------------------------
st.markdown('<div class="section-title">Select Process</div>', unsafe_allow_html=True)

p1, p2 = st.columns(2)
if p1.button("SAW", use_container_width=True):
    st.session_state.process = "SAW"
    st.rerun()
if p2.button("FCAW", use_container_width=True):
    st.session_state.process = "FCAW"
    st.rerun()

p3, p4 = st.columns(2)
if p3.button("SMAW", use_container_width=True):
    st.session_state.process = "SMAW"
    st.rerun()
if p4.button("GMAW", use_container_width=True):
    st.session_state.process = "GMAW"
    st.rerun()

# ---------------------------
# Input Parameter Row 생성 함수
# ---------------------------
def input_row(label, key, step):
    c1, c2, c3, c4 = st.columns([3.5,1.5,3.5,1.5])

    c1.markdown(f"**{label}**")

    if c2.button("－", key=key+"_minus"):
        st.session_state[key] -= step
        st.rerun()

    st.session_state[key] = c3.number_input(
        "", value=st.session_state[key], key=key+"_input"
    )

    if c4.button("＋", key=key+"_plus"):
        st.session_state[key] += step
        st.rerun()

# ---------------------------
# S5 Input Parameters
# ---------------------------
st.markdown('<div class="section-title">Input Parameters</div>', unsafe_allow_html=True)

input_row("Voltage (V)", "voltage", 1.0)
input_row("Current (A)", "current", 10.0)
input_row("Travel Speed (mm)", "travel", 0.5)
input_row("Time (sec)", "time", 0.1)

# ---------------------------
# 계산 로직
# ---------------------------
if st.session_state.standard == "AWS":
    k = 1.0
else:
    if st.session_state.process == "SAW":
        k = 1.0
    else:
        k = 0.8

HI = (k * st.session_state.voltage *
      st.session_state.current *
      st.session_state.time) / (st.session_state.travel * 1000)

# ---------------------------
# Result
# ---------------------------
st.markdown('<div class="section-title">Live Result</div>', unsafe_allow_html=True)

st.markdown(f'<div class="result-box">{HI:.3f} kJ/mm</div>', unsafe_allow_html=True)

if st.session_state.min <= HI <= st.session_state.max:
    st.markdown('<div class="pass">PASS</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="fail">FAIL</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)