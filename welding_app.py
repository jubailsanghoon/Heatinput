import streamlit as st

st.set_page_config(layout="centered")

# ======================================================
# CSS
# ======================================================
st.markdown("""
<style>
body { background-color:#F2F2F2; }

.main-container {
    max-width:480px;
    margin:auto;
}

/* ---------------- Header ---------------- */

.header {
    display:flex;
    align-items:center;
    border-bottom:5px solid black;
    padding-bottom:10px;
    margin-bottom:15px;
}
.header img { height:50px; margin-right:10px; }
.title { font-size:28px; font-weight:900; }

/* ---------------- Section ---------------- */

.section-title {
    font-size:20px;
    font-weight:900;
    margin-top:20px;
}

/* ---------------- Button Style ---------------- */

.stButton > button {
    border:3px solid black;
    font-weight:900;
    padding:8px 0;
    background:white;
}

.selected-btn {
    background:#ff7f00 !important;
    color:white !important;
}

/* ---------------- Input Width ---------------- */

div[data-testid="stNumberInput"] input {
    width:30% !important;
}

/* ---------------- Result ---------------- */

.result-box {
    font-size:26px;
    font-weight:900;
    padding:15px;
    background:#ffe5cc;
    border:3px solid black;
    width:100%;
    text-align:left;
}

.pass, .fail {
    font-size:26px;
    font-weight:900;
    padding:15px;
    border:3px solid black;
    width:100%;
    text-align:left;
}

.pass { background:#00cc44; color:white; }
.fail { background:#ff7f00; color:white; }

</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-container">', unsafe_allow_html=True)

# ======================================================
# Header
# ======================================================
st.markdown("""
<div class="header">
<img src="https://raw.githubusercontent.com/jubailsanghoon/Heatinput/main/db65c0d39f36f2dddc248ea0bf2e4efc.jpg">
<div class="title">Heat Input Master</div>
</div>
""", unsafe_allow_html=True)

# ======================================================
# Session Init
# ======================================================
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

# ======================================================
# Standard Selection
# ======================================================
st.markdown('<div class="section-title">Standard Selection</div>', unsafe_allow_html=True)

col1, col_gap, col2 = st.columns([3.5,1,3.5])

with col1:
    if st.button("AWS", use_container_width=True):
        st.session_state.standard = "AWS"

with col2:
    if st.button("ISO", use_container_width=True):
        st.session_state.standard = "ISO"

# 색상 유지
if st.session_state.standard == "AWS":
    st.markdown(
        "<style>button[kind='secondary']:first-child{background:#ff7f00!important;color:white!important;}</style>",
        unsafe_allow_html=True,
    )

# ======================================================
# WPS Range
# ======================================================
st.markdown('<div class="section-title">WPS Range (kJ/mm)</div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    st.session_state.min = st.number_input("Min", value=st.session_state.min)
with c2:
    st.session_state.max = st.number_input("Max", value=st.session_state.max)

# ======================================================
# Process Selection
# ======================================================
st.markdown('<div class="section-title">Select Process</div>', unsafe_allow_html=True)

p1, gap, p2 = st.columns([3.5,1,3.5])
with p1:
    if st.button("SAW", use_container_width=True):
        st.session_state.process = "SAW"
with p2:
    if st.button("FCAW", use_container_width=True):
        st.session_state.process = "FCAW"

p3, gap, p4 = st.columns([3.5,1,3.5])
with p3:
    if st.button("SMAW", use_container_width=True):
        st.session_state.process = "SMAW"
with p4:
    if st.button("GMAW", use_container_width=True):
        st.session_state.process = "GMAW"

# ======================================================
# Input Parameters + Live Result (Same Line)
# ======================================================
st.markdown('<div class="section-title">Input Parameters</div>', unsafe_allow_html=True)

left, spacer, right = st.columns([4,1,4])

# ---------- Input ----------
with left:
    st.session_state.voltage = st.number_input(
        "Voltage (V)", value=st.session_state.voltage, step=0.1, format="%.1f"
    )
    st.session_state.current = st.number_input(
        "Current (A)", value=st.session_state.current, step=0.1, format="%.1f"
    )
    st.session_state.travel = st.number_input(
        "Travel Speed (mm)", value=st.session_state.travel, step=0.1, format="%.1f"
    )
    st.session_state.time = st.number_input(
        "Time (sec)", value=st.session_state.time, step=0.1, format="%.1f"
    )

# ---------- Calculation ----------
if st.session_state.standard == "AWS":
    k = 1.0
else:
    k = 1.0 if st.session_state.process == "SAW" else 0.8

HI = (k *
      st.session_state.voltage *
      st.session_state.current *
      st.session_state.time) / (st.session_state.travel * 1000)

# ---------- Result ----------
with right:
    st.markdown('<div class="section-title">Live Result</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="result-box">{HI:.3f} kJ/mm</div>', unsafe_allow_html=True)

    if st.session_state.min <= HI <= st.session_state.max:
        st.markdown('<div class="pass">PASS</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="fail">FAIL</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)