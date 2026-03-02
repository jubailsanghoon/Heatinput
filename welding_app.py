import streamlit as st

st.set_page_config(layout="centered")

# ======================================================
# CSS
# ======================================================
st.markdown("""
<style>
body { background-color:#F2F2F2; }

.main-container {
    max-width:520px;
    margin:auto;
}

/* Header */
.header {
    display:flex;
    align-items:center;
    border-bottom:5px solid black;
    padding-bottom:10px;
    margin-bottom:20px;
}
.header img { height:50px; margin-right:10px; }
.title { font-size:28px; font-weight:900; }

/* Section */
.section-title {
    font-size:20px;
    font-weight:900;
    margin-top:25px;
    margin-bottom:10px;
}

/* Radio Selected Color */
div[role="radiogroup"] > label > div:first-child {
    border:3px solid black;
}

input[type="radio"]:checked + div {
    background:#ff7f00 !important;
    color:white !important;
}

/* Input Layout */
.input-row {
    display:flex;
    align-items:center;
    margin-bottom:8px;
}
.input-label {
    width:37%;
    font-weight:900;
}
.input-gap {
    width:3%;
}
.input-box {
    width:60%;
}

/* Result */
.result-box {
    font-size:26px;
    font-weight:900;
    padding:15px;
    background:#ffe5cc;
    border:3px solid black;
    width:100%;
}

.pass, .fail {
    margin-top:5%;
    font-size:26px;
    font-weight:900;
    padding:15px;
    border:3px solid black;
    width:100%;
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
# 1️⃣ Standard Selection (완전 독립)
# ======================================================
st.markdown('<div class="section-title">Standard Selection</div>', unsafe_allow_html=True)

standard = st.radio(
    label="",
    options=["AWS", "ISO"],
    horizontal=True,
    key="standard_radio"
)

# ======================================================
# 2️⃣ WPS Range (kJ/mm)
# ======================================================
st.markdown('<div class="section-title">WPS Range (kJ/mm)</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    min_range = st.number_input("Min", step=0.1, format="%.1f", value=1.0)
with col2:
    max_range = st.number_input("Max", step=0.1, format="%.1f", value=2.5)

# ======================================================
# 3️⃣ Select Process (완전 독립)
# ======================================================
st.markdown('<div class="section-title">Select Process</div>', unsafe_allow_html=True)

process = st.radio(
    label="",
    options=["SAW", "FCAW", "SMAW", "GMAW"],
    horizontal=True,
    key="process_radio"
)

# ======================================================
# 4️⃣ Input + Result 같은 라인
# ======================================================
left, gap, right = st.columns([4,0.5,4])

with left:
    st.markdown('<div class="section-title">Input Parameters</div>', unsafe_allow_html=True)

    v_col1, v_gap, v_col2 = st.columns([0.37,0.03,0.60])
    with v_col1:
        st.markdown("**Voltage (V)**")
    with v_col2:
        voltage = st.number_input("", step=0.1, format="%.1f", key="v")

    c_col1, c_gap, c_col2 = st.columns([0.37,0.03,0.60])
    with c_col1:
        st.markdown("**Current (A)**")
    with c_col2:
        current = st.number_input("", step=0.1, format="%.1f", key="c")

    t_col1, t_gap, t_col2 = st.columns([0.37,0.03,0.60])
    with t_col1:
        st.markdown("**Travel Speed (mm)**")
    with t_col2:
        travel = st.number_input("", step=0.1, format="%.1f", key="t")

    time_col1, time_gap, time_col2 = st.columns([0.37,0.03,0.60])
    with time_col1:
        st.markdown("**Time (sec)**")
    with time_col2:
        time = st.number_input("", step=0.1, format="%.1f", key="time")

# ======================================================
# Calculation
# ======================================================
k = 1.0 if standard == "AWS" else (1.0 if process=="SAW" else 0.8)
HI = (k * voltage * current * time) / (travel * 1000) if travel != 0 else 0

with right:
    st.markdown('<div class="section-title">Live Result</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="result-box">{HI:.3f} kJ/mm</div>', unsafe_allow_html=True)

    if min_range <= HI <= max_range:
        st.markdown('<div class="pass">PASS</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="fail">FAIL</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)