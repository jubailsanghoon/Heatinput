import streamlit as st

st.set_page_config(layout="centered")

# ======================================================
# CSS
# ======================================================
st.markdown("""
<style>
body { background-color:#F2F2F2; }

.main-container {
    max-width:650px;
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
    font-size:18px;
    font-weight:900;
    margin-top:15px;
    margin-bottom:8px;
}

/* Inline input row */
.inline-row {
    display:flex;
    align-items:center;
    justify-content:space-between;
    margin-bottom:8px;
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
# 1️⃣ Standard + Process
# ======================================================
left, space, right = st.columns([4,1,5])

with left:
    st.markdown('<div class="section-title">Standard Selection</div>', unsafe_allow_html=True)
    standard = st.radio("", ["AWS","ISO"], horizontal=True)

with right:
    st.markdown('<div class="section-title">Select Process</div>', unsafe_allow_html=True)
    process = st.radio("", ["SAW","FCAW","SMAW","GMAW"], horizontal=True)

# ======================================================
# 2️⃣ WPS Range (한 줄 정렬)
# ======================================================
st.markdown('<div class="section-title">WPS Range (kJ/mm)</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns([1,2,1,2])

with col1:
    st.markdown("**Min.**")
with col2:
    min_range = st.number_input("", step=0.01, format="%.2f", value=0.96)
with col3:
    st.markdown("**Max.**")
with col4:
    max_range = st.number_input("", step=0.01, format="%.2f", value=2.50)

# ======================================================
# 3️⃣ Input + Result
# ======================================================
left, gap, right = st.columns([5,1,4])

with left:
    st.markdown('<div class="section-title">Input Parameters</div>', unsafe_allow_html=True)

    def input_row(label, key, default):
        c1, c2 = st.columns([3,2])
        with c1:
            st.markdown(f"**{label}**")
        with c2:
            return st.number_input("", step=0.1, format="%.1f",
                                   value=default, key=key)

    voltage = input_row("Voltage (V)", "v", 30.0)
    current = input_row("Current (A)", "c", 300.0)
    length  = input_row("Length (mm)", "l", 5.0)
    time    = input_row("Time (sec)", "t", 1.0)

# ======================================================
# Calculation
# ======================================================
if standard == "AWS":
    k = 1.0
else:
    efficiency = {
        "SAW": 1.0,
        "GMAW": 0.8,
        "FCAW": 0.8,
        "SMAW": 0.8
    }
    k = efficiency.get(process, 0.8)

if length > 0 and time > 0:
    HI = (k * voltage * current * time) / (length * 1000)
else:
    HI = 0

# ======================================================
# Result
# ======================================================
with right:
    st.markdown('<div class="section-title">Live Result</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="result-box">{HI:.3f} kJ/mm</div>',
                unsafe_allow_html=True)

    if min_range <= HI <= max_range:
        st.markdown('<div class="pass">PASS</div>',
                    unsafe_allow_html=True)
    else:
        st.markdown('<div class="fail">FAIL</div>',
                    unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)