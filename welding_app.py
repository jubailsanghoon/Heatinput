import streamlit as st

st.set_page_config(layout="centered")

# ======================================================
# CSS - 디자인 디테일 수정
# ======================================================
st.markdown("""
<style>
    /* 배경 및 기본 폰트 */
    body { background-color:#F2F2F2; }
    
    .main-container {
        max-width:700px;
        margin:auto;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Header */
    .header {
        display:flex;
        align-items:center;
        border-bottom:5px solid black;
        padding-bottom:10px;
        margin-bottom:20px;
    }
    .header img { height:50px; margin-right:15px; }
    .title { font-size:28px; font-weight:900; }

    /* Section Title */
    .section-title {
        font-size:18px;
        font-weight:900;
        margin-top:20px;
        margin-bottom:15px;
    }

    /* Result Box Styling */
    .result-box {
        font-size:24px;
        font-weight:900;
        padding:15px;
        background:#ffe5cc;
        border:3px solid black;
        text-align: center;
        margin-bottom: 10px;
    }

    .pass, .fail {
        font-size:24px;
        font-weight:900;
        padding:15px;
        border:3px solid black;
        text-align: center;
    }
    .pass { background:#00cc44; color:white; }
    .fail { background:#ff7f00; color:white; }

    /* 숫자 입력칸 사이 간격 조정 */
    div[data-testid="stHorizontalBlock"] {
        align-items: center;
    }
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
c_std, c_prc = st.columns([1, 1])
with c_std:
    st.markdown('<div class="section-title">Standard Selection</div>', unsafe_allow_html=True)
    standard = st.radio("Std", ["AWS","ISO"], horizontal=True, label_visibility="collapsed")
with c_prc:
    st.markdown('<div class="section-title">Select Process</div>', unsafe_allow_html=True)
    process = st.radio("Prc", ["SAW","FCAW","SMAW","GMAW"], horizontal=True, label_visibility="collapsed")

# ======================================================
# 2️⃣ WPS Range (두 번째 그림 레이아웃: 가로 한 줄 정렬)
# ======================================================
st.markdown('<div class="section-title">WPS Range (kJ/mm)</div>', unsafe_allow_html=True)
w1, w2, w3, w4, w5 = st.columns([1, 2, 1, 2, 3]) # 우측 여백을 위해 5분할

with w1: st.markdown("**Min.**")
with w2: min_range = st.number_input("min", value=0.96, step=0.01, format="%.2f", label_visibility="collapsed")
with w3: st.markdown("**Max.**")
with w4: max_range = st.number_input("max", value=2.50, step=0.01, format="%.2f", label_visibility="collapsed")

# ======================================================
# 3️⃣ Input + Result (두 번째 그림 레이아웃: 좌측 입력 / 우측 결과)
# ======================================================
st.write("") # 간격 조절
col_left, col_space, col_right = st.columns([5, 1, 4])

with col_left:
    st.markdown('<div class="section-title">Input Parameters</div>', unsafe_allow_html=True)
    
    # 두 번째 그림처럼 라벨과 입력창을 한 줄에 배치하는 함수
    def draw_input_row(label, value, key):
        r1, r2 = st.columns([2, 2])
        with r1: st.markdown(f"**{label}**")
        with r2: return st.number_input(label, value=value, step=0.1, format="%.1f", key=key, label_visibility="collapsed")

    voltage = draw_input_row("Voltage (V)", 30.0, "v")
    current = draw_input_row("Current (A)", 300.0, "c")
    length  = draw_input_row("Length (mm)", 5.0, "l")
    time    = draw_input_row("Time (sec)", 1.0, "t")

# 계산 로직
if standard == "AWS":
    k = 1.0
else:
    efficiency = {"SAW": 1.0, "GMAW": 0.8, "FCAW": 0.8, "SMAW": 0.8}
    k = efficiency.get(process, 0.8)

HI = (k * voltage * current * time) / (length * 1000) if length > 0 else 0

with col_right:
    st.markdown('<div class="section-title">Live Result</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="result-box">{HI:.3f} kJ/mm</div>', unsafe_allow_html=True)
    
    if min_range <= HI <= max_range:
        st.markdown('<div class="pass">PASS</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="fail">FAIL</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)