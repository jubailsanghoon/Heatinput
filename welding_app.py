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
input[type="radio"]:checked + div {
    background:#ff7f00 !important;
    color:white !important;
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
# 1️⃣ Standard Selection
# ======================================================
st.markdown('<div class="section-title">Standard Selection</div>', unsafe_allow_html=True)

standard = st.radio(
    "",
    ["AWS", "ISO"],
    horizontal=True,
    key="standard_radio"
)

# ======================================================
# 2️⃣ WPS Range (kJ/mm)  🔥 수정 부분
# ======================================================
st.markdown('<div class="section-title">WPS Range (kJ/mm)</div>', unsafe_allow_html=True)

wps_col1, wps_gap, wps_col2 = st.columns([0.47,0.06,0.47])

with wps_col1:
    label1, gap1, input1 = st.columns([0.47,0.03,0.50])
    with label1:
        st.markdown("**Min.**")
    with input1:
        min_range = st.number_input(
            "",
            step=0.01,
            format="%.2f",
            value=1.00,
            key="min"
        )

with wps_col2:
    label2, gap2, input2 = st.columns([0.47,0.03,0.50])
    with label2:
        st.markdown("**Max.**")
    with input2:
        max_range = st.number_input(
            "",
            step=0.01,
            format="%.2f",
            value=2.50,
            key="max"
        )

# ======================================================
# 3️⃣ Select Process
# ======================================================
st.markdown('<div class="section-title">Select Process</div>', unsafe_allow_html=True)

process = st.radio(
    "",
    ["SAW", "FCAW", "SMAW", "GMAW"],
    horizontal=True,
    key="process_radio"
)

# ======================================================
# 4️⃣ Input + Result
# ======================================================
left, gap, right = st.columns([4,0.5,4])

with left:
    st.markdown('<div class="section-title">Input Parameters</div>', unsafe_allow_html=True)

    def input_row(label, key):
        col1, col_gap, col2 = st.columns([0.37,0.03,0.60])
        with col1:
            st.markdown(f"**{label}**")
        with col2:
            return st.number_input("", step=0.1, format="%.1f", key=key)

    voltage = input_row("Voltage (V)", "v")
    current = input_row("Current (A)", "c")
    travel  = input_row("Travel Speed (mm)", "t")
    time    = input_row("Time (sec)", "time")

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