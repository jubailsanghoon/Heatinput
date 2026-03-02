import streamlit as st

st.set_page_config(page_title="Heat Input Master", layout="centered")

# ==============================
# CSS
# ==============================
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

/* Header */
.header-title {
    font-size: 26px;
    font-weight: 900;
}

/* Section Title */
.section-title {
    font-size: 22px;
    font-weight: 900;
    border-bottom: 5px solid #000000;
    margin-top: 20px;
    margin-bottom: 10px;
}

/* Radio as Button */
div[role="radiogroup"] > label {
    width: 100%;
}

div[role="radiogroup"] label div {
    width: 100% !important;
    height: 70px !important;
    border: 3px solid #000000 !important;
    background-color: white !important;
    color: black !important;
    font-weight: 900 !important;
    font-size: 22px !important;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* 선택된 Radio */
div[role="radiogroup"] input:checked + div {
    background-color: #FF7A00 !important;
    color: white !important;
}

/* number_input 스핀 제거 */
input[type=number]::-webkit-outer-spin-button,
input[type=number]::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
}

input[type=number] {
    -moz-appearance: textfield;
    font-weight: 900 !important;
    font-size: 18px !important;
}

/* Result Box */
.result-hi {
    font-size: 24px;
    font-weight: 900;
    padding: 12px;
    background-color: #FFE5CC;
    border: 3px solid #000000;
}

.result-pass {
    font-size: 20px;
    font-weight: 900;
    padding: 10px;
    background-color: #00AA00;
    color: white;
    border: 3px solid #000000;
}

.result-fail {
    font-size: 20px;
    font-weight: 900;
    padding: 10px;
    background-color: #FF7A00;
    color: white;
    border: 3px solid #000000;
}

</style>
""", unsafe_allow_html=True)

# ==============================
# Session State
# ==============================
if "standard" not in st.session_state:
    st.session_state.standard = "ISO"

if "process" not in st.session_state:
    st.session_state.process = "SAW"

# ==============================
# Header
# ==============================
col1, col2 = st.columns([1,4])

with col1:
    st.image("https://raw.githubusercontent.com/jubailsanghoon/Heatinput/main/db65c0d39f36f2dddc248ea0bf2e4efc.jpg", width=60)

with col2:
    st.markdown('<div class="header-title">Heat Input Master</div>', unsafe_allow_html=True)

st.markdown('<div style="border-bottom:5px solid #000000;margin-top:10px;"></div>', unsafe_allow_html=True)

# ==============================
# Standard Selection
# ==============================
st.markdown('<div class="section-title">Standard Selection</div>', unsafe_allow_html=True)

st.session_state.standard = st.radio(
    "",
    ["ISO", "AWS"],
    horizontal=True,
    key="standard_radio"
)

# ==============================
# WPS Range
# ==============================
st.markdown('<div class="section-title">WPS Range (kJ/mm)</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns([1,2,1,2])

with col1:
    st.markdown("**Min.**")

with col2:
    wps_min = st.number_input("", value=1.0, step=0.1)

with col3:
    st.markdown("**Max.**")

with col4:
    wps_max = st.number_input("", value=2.5, step=0.1)

# ==============================
# Select Process
# ==============================
st.markdown('<div class="section-title">Select Process</div>', unsafe_allow_html=True)

st.session_state.process = st.radio(
    "",
    ["SAW", "FCAW", "SMAW", "GMAW"],
    horizontal=True,
    key="process_radio"
)

# ==============================
# Input Parameters (수동 입력만)
# ==============================
st.markdown('<div class="section-title">Input Parameters</div>', unsafe_allow_html=True)

voltage = st.number_input("Voltage (V)", value=30.0, step=1.0)
current = st.number_input("Current (A)", value=300.0, step=10.0)
time = st.number_input("Time (Sec)", value=10.0, step=1.0)
length = st.number_input("Length (mm)", value=100.0, step=10.0)

# ==============================
# Calculation
# ==============================
if st.session_state.standard == "AWS":
    k = 1.0
else:
    k = 1.0 if st.session_state.process == "SAW" else 0.8

HI = (k * voltage * current * time) / (length * 1000)

# ==============================
# Live Result
# ==============================
st.markdown('<div class="section-title">Live Result</div>', unsafe_allow_html=True)

st.markdown(f'<div class="result-hi">kJ/mm : {HI:.3f}</div>', unsafe_allow_html=True)

if HI < wps_min or HI > wps_max:
    st.markdown('<div class="result-fail">Fail</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="result-pass">Pass</div>', unsafe_allow_html=True)