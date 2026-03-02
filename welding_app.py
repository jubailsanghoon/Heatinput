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

/* Button */
.stButton > button {
    border:3px solid black;
    font-weight:900;
    background:white;
    padding:8px 0;
}
.selected {
    background:#ff7f00 !important;
    color:white !important;
}

/* Input Row */
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
# Session Init (완전 분리)
# ======================================================
if "standard" not in st.session_state:
    st.session_state.standard = "ISO"

if "process" not in st.session_state:
    st.session_state.process = "SAW"

# ======================================================
# 1️⃣ Standard Selection
# ======================================================
st.markdown('<div class="section-title">Standard Selection</div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:
    if st.button("AWS", key="std_aws", use_container_width=True):
        st.session_state.standard = "AWS"

with c2:
    if st.button("ISO", key="std_iso", use_container_width=True):
        st.session_state.standard = "ISO"

# 선택 색상 유지
if st.session_state.standard == "AWS":
    st.markdown("<style>button#std_aws{background:#ff7f00;color:white;}</style>", unsafe_allow_html=True)
elif st.session_state.standard == "ISO":
    st.markdown("<style>button#std_iso{background:#ff7f00;color:white;}</style>", unsafe_allow_html=True)

# ======================================================
# 2️⃣ Process Selection (완전 독립)
# ======================================================
st.markdown('<div class="section-title">Select Process</div>', unsafe_allow_html=True)

p1, p2 = st.columns(2)
p3, p4 = st.columns(2)

with p1:
    if st.button("SAW", key="proc_saw", use_container_width=True):
        st.session_state.process = "SAW"
with p2:
    if st.button("FCAW", key="proc_fcaw", use_container_width=True):
        st.session_state.process = "FCAW"
with p3:
    if st.button("SMAW", key="proc_smaw", use_container_width=True):
        st.session_state.process = "SMAW"
with p4:
    if st.button("GMAW", key="proc_gmaw", use_container_width=True):
        st.session_state.process = "GMAW"

# 선택 색상 유지
selected_map = {
    "SAW":"proc_saw",
    "FCAW":"proc_fcaw",
    "SMAW":"proc_smaw",
    "GMAW":"proc_gmaw"
}
selected_key = selected_map[st.session_state.process]
st.markdown(
    f"<style>button#{selected_key}{{background:#ff7f00;color:white;}}</style>",
    unsafe_allow_html=True
)

# ======================================================
# 3️⃣ Input + Live Result 같은 라인
# ======================================================
left, gap, right = st.columns([4,0.5,4])

with left:
    st.markdown('<div class="section-title">Input Parameters</div>', unsafe_allow_html=True)

    voltage = st.number_input("Voltage (V)", step=0.1, format="%.1f")
    current = st.number_input("Current (A)", step=0.1, format="%.1f")
    travel  = st.number_input("Travel Speed (mm)", step=0.1, format="%.1f")
    time    = st.number_input("Time (sec)", step=0.1, format="%.1f")

# Calculation
k = 1.0 if st.session_state.standard == "AWS" else (1.0 if st.session_state.process=="SAW" else 0.8)
HI = (k * voltage * current * time) / (travel * 1000) if travel != 0 else 0

with right:
    st.markdown('<div class="section-title">Live Result</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="result-box">{HI:.3f} kJ/mm</div>', unsafe_allow_html=True)

    if 1.0 <= HI <= 2.5:
        st.markdown('<div class="pass">PASS</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="fail">FAIL</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)