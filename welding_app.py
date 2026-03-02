import streamlit as st

st.set_page_config(page_title="Heat Input Master", layout="centered")

# -----------------------------
# CSS 강제 주입 (Layout 고정)
# -----------------------------
st.markdown("""
<style>
html, body, [class*="css"]  {
    font-family: Arial, Helvetica, sans-serif;
}

.main {
    background-color: #F2F2F2;
}

.block-container {
    max-width: 480px;
    padding-top: 10px;
    padding-bottom: 50px;
}

h1, h2, h3, label {
    color: #000000 !important;
    font-weight: 800 !important;
}

.stButton>button {
    width: 100%;
    height: 75px;
    font-size: 22px;
    font-weight: 900;
    border: 3px solid #000000;
    background-color: white;
    color: black;
}

.stButton>button:hover {
    background-color: black;
    color: white;
}

input {
    font-size: 20px !important;
    font-weight: 700 !important;
}

hr {
    border: 5px solid black;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Session State 초기화
# -----------------------------
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

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# -----------------------------
# Header
# -----------------------------
col1, col2 = st.columns([1,3])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/921/921347.png", width=60)
with col2:
    st.markdown("<h2>Heat Input Master</h2>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# -----------------------------
# S2 Standard Selection
# -----------------------------
st.markdown("### Standard Selection")

col1, col2 = st.columns(2)
with col1:
    if st.button("ISO"):
        st.session_state.standard = "ISO"
        st.rerun()

with col2:
    if st.button("AWS"):
        st.session_state.standard = "AWS"
        st.rerun()

# -----------------------------
# S3 WPS Range
# -----------------------------
st.markdown("### WPS Range (kJ/mm)")
col1, col2 = st.columns(2)
with col1:
    st.session_state.wps_min = st.number_input(
        "Min",
        value=st.session_state.wps_min,
        step=0.1
    )

with col2:
    st.session_state.wps_max = st.number_input(
        "Max",
        value=st.session_state.wps_max,
        step=0.1
    )

# -----------------------------
# S4 Process Selection
# -----------------------------
st.markdown("### Select Process")

row1 = st.columns(2)
row2 = st.columns(2)

with row1[0]:
    if st.button("SAW"):
        st.session_state.process = "SAW"
        st.rerun()

with row1[1]:
    if st.button("FCAW"):
        st.session_state.process = "FCAW"
        st.rerun()

with row2[0]:
    if st.button("SMAW"):
        st.session_state.process = "SMAW"
        st.rerun()

with row2[1]:
    if st.button("GMAW"):
        st.session_state.process = "GMAW"
        st.rerun()

# -----------------------------
# Input Row Component
# -----------------------------
def input_row(label, key, step):

    col1, col2, col3, col4 = st.columns([3.5,1.5,3.5,1.5])

    with col1:
        st.markdown(f"<p style='font-size:22px; font-weight:900;'>{label}</p>", unsafe_allow_html=True)

    with col2:
        if st.button("－", key=f"minus_{key}"):
            st.session_state[key] -= step
            st.rerun()

    with col3:
        st.session_state[key] = st.number_input(
            "",
            value=st.session_state[key],
            step=step,
            key=f"input_{key}",
            label_visibility="collapsed"
        )

    with col4:
        if st.button("＋", key=f"plus_{key}"):
            st.session_state[key] += step
            st.rerun()

# -----------------------------
# S5 Input Parameters
# -----------------------------
st.markdown("### Input Parameters")

input_row("Voltage (V)", "voltage", 1.0)
input_row("Current (A)", "current", 10.0)
input_row("Time (Sec)", "time", 1.0)
input_row("Length (mm)", "length", 10.0)

# -----------------------------
# Heat Input Calculation
# -----------------------------

# 열효율 k
if st.session_state.standard == "AWS":
    k = 1.0
else:
    if st.session_state.process == "SAW":
        k = 1.0
    else:
        k = 0.8

V = st.session_state.voltage
A = st.session_state.current
t = st.session_state.time
L = st.session_state.length

HI = (k * V * A * t) / (L * 1000)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(f"<h2>Heat Input: {HI:.3f} kJ/mm</h2>", unsafe_allow_html=True)

# -----------------------------
# WPS 판정
# -----------------------------
if HI < st.session_state.wps_min:
    st.error("Below WPS Minimum")
elif HI > st.session_state.wps_max:
    st.error("Above WPS Maximum")
else:
    st.success("Within WPS Range")