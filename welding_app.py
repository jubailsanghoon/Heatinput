import streamlit as st

st.set_page_config(layout="centered")

# ---------------------------
# CSS (Field Spec Final)
# ---------------------------
st.markdown("""
<style>
body { background-color:#F2F2F2; }

.main-container {
    max-width:460px;
    margin:auto;
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

.section-title {
    font-size:20px;
    font-weight:900;
    margin-top:20px;
}

/* ---------- Radio Layout ---------- */

div[role="radiogroup"] {
    display:flex;
    gap:10px;
}

div[role="radiogroup"] label {
    flex:1;
    border:3px solid black;
    padding:18px 0;
    text-align:center;
    font-weight:900;
    font-size:20px;
    background:white;
    cursor:pointer;
}

div[role="radiogroup"] input {
    display:none;
}

div[role="radiogroup"] input:checked + div {
    background-color:#ff7f00 !important;
    color:white !important;
}

/* ---------- Result ---------- */

.result-box {
    font-size:26px;
    font-weight:900;
    padding:15px;
    background:#ffe5cc;
    text-align:center;
    border:3px solid black;
    width:75%;
    margin:auto;
}

/* ---------- PASS / FAIL ---------- */

.pass {
    background-color:#00cc44;
    color:white;
    padding:12px;
    font-weight:900;
    text-align:center;
    width:70%;
    margin:25px auto 0 auto;
}

.fail {
    background-color:#ff7f00;
    color:white;
    padding:12px;
    font-weight:900;
    text-align:center;
    width:70%;
    margin:25px auto 0 auto;
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
# Standard Selection (Radio)
# ---------------------------
st.markdown('<div class="section-title">Standard Selection</div>', unsafe_allow_html=True)

st.session_state.standard = st.radio(
    "",
    ["ISO", "AWS"],
    horizontal=True,
    index=["ISO","AWS"].index(st.session_state.standard)
)

# ---------------------------
# WPS Range
# ---------------------------
st.markdown('<div class="section-title">WPS Range (kJ/mm)</div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)
st.session_state.min = c1.number_input("Min", value=st.session_state.min)
st.session_state.max = c2.number_input("Max", value=st.session_state.max)

# ---------------------------
# Process Selection (Radio)
# ---------------------------
st.markdown('<div class="section-title">Select Process</div>', unsafe_allow_html=True)

st.session_state.process = st.radio(
    "",
    ["SAW", "FCAW", "SMAW", "GMAW"],
    horizontal=True,
    index=["SAW","FCAW","SMAW","GMAW"].index(st.session_state.process)
)

# ---------------------------
# Input Parameters
# ---------------------------
st.markdown('<div class="section-title">Input Parameters</div>', unsafe_allow_html=True)

st.session_state.voltage = st.number_input("Voltage (V)", value=st.session_state.voltage)
st.session_state.current = st.number_input("Current (A)", value=st.session_state.current)
st.session_state.travel  = st.number_input("Travel Speed (mm)", value=st.session_state.travel)
st.session_state.time    = st.number_input("Time (sec)", value=st.session_state.time)

# ---------------------------
# Calculation Logic
# ---------------------------
if st.session_state.standard == "AWS":
    k = 1.0
else:
    k = 1.0 if st.session_state.process == "SAW" else 0.8

HI = (k *
      st.session_state.voltage *
      st.session_state.current *
      st.session_state.time) / (st.session_state.travel * 1000)

# ---------------------------
# Live Result
# ---------------------------
st.markdown('<div class="section-title">Live Result</div>', unsafe_allow_html=True)

st.markdown(f'<div class="result-box">{HI:.3f} kJ/mm</div>', unsafe_allow_html=True)

if st.session_state.min <= HI <= st.session_state.max:
    st.markdown('<div class="pass">PASS</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="fail">FAIL</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)