import streamlit as st

st.set_page_config(page_title="Heat Input Master", layout="centered")

# -----------------------------
# 🔥 DARK MODE + 600px Tablet 대응 CSS
# -----------------------------
st.markdown("""
<style>

/* 전체 배경 */
html, body, .main {
    background-color: #111111;
    color: white;
    font-family: Arial, Helvetica, sans-serif;
}

/* 중앙 고정 폭 (모바일 480 / 태블릿 600) */
.block-container {
    max-width: 480px;
    padding-top: 10px;
}

@media (min-width: 768px) {
    .block-container {
        max-width: 600px;
    }
}

/* 굵은 글씨 */
h1, h2, h3, label {
    font-weight: 900 !important;
}

/* 버튼 기본 */
.stButton>button {
    width: 100%;
    height: 75px;
    font-size: 22px;
    font-weight: 900;
    border: 3px solid white;
    background-color: #222222;
    color: white;
}

/* 버튼 hover */
.stButton>button:hover {
    background-color: white;
    color: black;
}

/* 🔥 활성화 버튼 */
.active-btn {
    background-color: white !important;
    color: black !important;
}

/* number_input 기본 스핀 제거 */
input[type=number]::-webkit-outer-spin-button,
input[type=number]::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
}
input[type=number] {
    -moz-appearance: textfield;
    width: 90px !important;
    text-align: center;
    font-size: 22px !important;
    font-weight: 900 !important;
}

/* 굵은 구분선 */
hr {
    border: 4px solid white;
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

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# -----------------------------
# Header
# -----------------------------
st.markdown("## 🔥 Heat Input Master")
st.markdown("<hr>", unsafe_allow_html=True)

# -----------------------------
# 🔥 Standard Selection (Active Highlight)
# -----------------------------
st.markdown("### Standard Selection")

col1, col2 = st.columns(2)

with col1:
    iso_class = "active-btn" if st.session_state.standard == "ISO" else ""
    if st.button("ISO"):
        st.session_state.standard = "ISO"
        st.rerun()
    st.markdown(f"<style>div[data-testid='column']:nth-of-type(1) .stButton>button {{}}</style>", unsafe_allow_html=True)

with col2:
    if st.button("AWS"):
        st.session_state.standard = "AWS"
        st.rerun()

# 버튼 강제 활성화 CSS 적용
if st.session_state.standard == "ISO":
    st.markdown("""
    <style>
    div[data-testid="stHorizontalBlock"] button:nth-child(1) {
        background-color: white !important;
        color: black !important;
    }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    div[data-testid="stHorizontalBlock"] button:nth-child(2) {
        background-color: white !important;
        color: black !important;
    }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------
# WPS Range
# -----------------------------
st.markdown("### WPS Range (kJ/mm)")
col1, col2 = st.columns(2)
with col1:
    st.session_state.wps_min = st.number_input("Min", value=st.session_state.wps_min, step=0.1)
with col2:
    st.session_state.wps_max = st.number_input("Max", value=st.session_state.wps_max, step=0.1)

# -----------------------------
# 🔥 Process Selection
# -----------------------------
st.markdown("### Select Process")

p1, p2 = st.columns(2)
p3, p4 = st.columns(2)

def process_btn(name, col):
    with col:
        if st.button(name):
            st.session_state.process = name
            st.rerun()

process_btn("SAW", p1)
process_btn("FCAW", p2)
process_btn("SMAW", p3)
process_btn("GMAW", p4)

# 활성 공정 버튼 강조
st.markdown(f"""
<style>
button:contains("{st.session_state.process}") {{
    background-color: white !important;
    color: black !important;
}}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Input Row
# -----------------------------
def input_row(label, key, step):
    c1, c2, c3, c4 = st.columns([3.5,1.5,3.5,1.5])

    with c1:
        st.markdown(f"### {label}")

    with c2:
        if st.button("－", key=f"minus_{key}"):
            st.session_state[key] -= step
            st.rerun()

    with c3:
        st.session_state[key] = st.number_input("", value=st.session_state[key], step=step, key=f"input_{key}", label_visibility="collapsed")

    with c4:
        if st.button("＋", key=f"plus_{key}"):
            st.session_state[key] += step
            st.rerun()

st.markdown("### Input Parameters")
input_row("Voltage (V)", "voltage", 1.0)
input_row("Current (A)", "current", 10.0)
input_row("Time (Sec)", "time", 1.0)
input_row("Length (mm)", "length", 10.0)

# -----------------------------
# Calculation
# -----------------------------
if st.session_state.standard == "AWS":
    k = 1.0
else:
    k = 1.0 if st.session_state.process == "SAW" else 0.8

V = st.session_state.voltage
A = st.session_state.current
t = st.session_state.time
L = st.session_state.length

HI = (k * V * A * t) / (L * 1000)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(f"## 🔥 Heat Input: {HI:.3f} kJ/mm")

if HI < st.session_state.wps_min:
    st.error("Below WPS Minimum")
elif HI > st.session_state.wps_max:
    st.error("Above WPS Maximum")
else:
    st.success("Within WPS Range")