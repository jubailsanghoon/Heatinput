import streamlit as st

st.set_page_config(layout="centered")

# ---------------------------
# CSS
# ---------------------------
st.markdown("""
<style>
body { background-color:#F2F2F2; }

.main-container {
    max-width:460px;
    margin:auto;
}

/* Header */
.header {
    display:flex;
    align-items:center;
    border-bottom:5px solid black;
    padding-bottom:10px;
    margin-bottom:15px;
}
.header img { height:50px; margin-right:10px; }
.title { font-size:28px; font-weight:900; }

.section-title {
    font-size:20px;
    font-weight:900;
    margin-top:20px;
}

/* ---------------- Standard ---------------- */

.standard-wrapper { margin-top:10px; }
.standard-row {
    display:flex;
    align-items:center;
}
.standard-left { width:10%; }
.standard-btn { width:35%; }
.standard-gap { width:10%; }

.standard-btn button {
    width:100%;
    border:3px solid black;
    font-weight:900;
    padding:8px 0;
    background:white;
}

.standard-btn button.selected {
    background:#ff7f00 !important;
    color:white !important;
}

/* ---------------- Process ---------------- */

.process-wrapper { margin:5% 0; }
.process-row {
    display:flex;
    align-items:center;
}
.process-left { width:10%; }
.process-btn { width:35%; }
.process-gap { width:10%; }

.process-btn button {
    width:100%;
    border:3px solid black;
    font-weight:900;
    padding:8px 0;
    background:white;
}

.process-btn button.selected {
    background:#ff7f00 !important;
    color:white !important;
}

/* ---------------- Input Width ---------------- */

.wps-row input { width:30% !important; }
.param-row input { width:40% !important; }

/* ---------------- Result ---------------- */

.result-box {
    font-size:26px;
    font-weight:900;
    padding:15px;
    background:#ffe5cc;
    border:3px solid black;
    width:75%;
    text-align:left;
}

.pass, .fail {
    font-size:26px;
    font-weight:900;
    padding:15px;
    border:3px solid black;
    width:75%;
    text-align:left;
    margin-top:10px;
}

.pass { background:#00cc44; color:white; }
.fail { background:#ff7f00; color:white; }

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
# Session Init
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
# Standard Selection
# ---------------------------
st.markdown('<div class="section-title">Standard Selection</div>', unsafe_allow_html=True)
st.markdown('<div class="standard-wrapper">', unsafe_allow_html=True)

col1, colgap, col2 = st.columns([3.5,1,3.5])

with col1:
    if st.button("AWS", use_container_width=True):
        st.session_state.standard = "AWS"

with col2:
    if st.button("ISO", use_container_width=True):
        st.session_state.standard = "ISO"

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# WPS Range
# ---------------------------
st.markdown('<div class="section-title">WPS Range (kJ/mm)</div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)
st.session_state.min = c1.number_input("Min", value=st.session_state.min)
st.session_state.max = c2.number_input("Max", value=st.session_state.max)

# ---------------------------
# Process Selection
# ---------------------------
st.markdown('<div class="section-title">Select Process</div>', unsafe_allow_html=True)

p1_left, p1_gap, p1_right = st.columns([3.5,1,3.5])
with p1_left:
    if st.button("SAW", use_container_width=True):
        st.session_state.process = "SAW"
with p1_right:
    if st.button("FCAW", use_container_width=True):
        st.session_state.process = "FCAW"

p2_left, p2_gap, p2_right = st.columns([3.5,1,3.5])
with p2_left:
    if st.button("SMAW", use_container_width=True):
        st.session_state.process = "SMAW"
with p2_right:
    if st.button("GMAW", use_container_width=True):
        st.session_state.process = "GMAW"

# ---------------------------
# Input Parameters
# ---------------------------
st.markdown('<div class="section-title">Input Parameters</div>', unsafe_allow_html=True)

st.session_state.voltage = st.number_input("Voltage (V)", value=st.session_state.voltage)
st.session_state.current = st.number_input("Current (A)", value=st.session_state.current)
st.session_state.travel  = st.number_input("Travel Speed (mm)", value=st.session_state.travel)
st.session_state.time    = st.number_input("Time (sec)", value=st.session_state.time)

# ---------------------------
# Calculation
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