import streamlit as st
import pandas as pd
from datetime import datetime

# 페이지 설정
st.set_page_config(layout="centered", page_title="Heat Input Master")

# ======================================================
# CSS - 간격 최소화 및 버튼 사이즈 완벽 일치화
# ======================================================
st.markdown("""
<style>
    body { background-color:#F2F2F2; }
    .main-container { max-width:750px; margin:auto; font-family: 'Segoe UI', sans-serif; }

    /* Header */
    .header { display:flex; align-items:center; border-bottom:5px solid black; padding-bottom:10px; margin-bottom:20px; }
    .header img { height:50px; margin-right:15px; }
    .title { font-size:28px; font-weight:900; }

    /* Section Title */
    .section-title { font-size:18px; font-weight:900; margin-top:15px; margin-bottom:10px; }

    /* Result Boxes */
    .result-box { font-size:26px; font-weight:900; padding:15px; background:#ffe5cc; border:3px solid black; text-align: center; margin-bottom: 10px; }
    .pass, .fail { font-size:26px; font-weight:900; padding:15px; border:3px solid black; text-align: center; margin-bottom: 15px; }
    .pass { background:#00cc44; color:white; }
    .fail { background:#ff7f00; color:white; }

    /* ★버튼 크기 일치화 (Export 버튼 작아짐 방지)★ */
    .stButton, .stDownloadButton { width: 100% !important; }
    .stButton > button, .stDownloadButton > button {
        width: 100% !important;
        height: 72px !important;
        font-size: 18px !important;
        font-weight: 900 !important;
        background-color: #E0E0E0 !important;
        color: black !important;
        border: 3px solid black !important;
        border-radius: 0px !important;
        padding: 0px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        background-color: #CCCCCC !important;
        border-color: #000000 !important;
    }

    /* 수평 중앙 정렬 (항목명과 입력창 높이 맞춤) */
    div[data-testid="stHorizontalBlock"] { align-items: center; }
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'history' not in st.session_state:
    st.session_state.history = []

st.markdown('<div class="main-container">', unsafe_allow_html=True)

# ======================================================
# Header
# ======================================================
st.markdown(f"""
<div class="header">
<img src="https://raw.githubusercontent.com/jubailsanghoon/Heatinput/main/db65c0d39f36f2dddc248ea0bf2e4efc.jpg">
<div class="title">Heat Input Master</div>
</div>
""", unsafe_allow_html=True)

# ======================================================
# 1️⃣ Standard & Process Selection
# ======================================================
c_std, c_prc = st.columns([1, 1.2])
with c_std:
    st.markdown('<div class="section-title">Standard Selection</div>', unsafe_allow_html=True)
    standard = st.radio("Std", ["AWS","ISO"], horizontal=True, label_visibility="collapsed")
with c_prc:
    st.markdown('<div class="section-title">Select Process</div>', unsafe_allow_html=True)
    process = st.radio("Prc", ["SAW","FCAW","SMAW","GMAW"], horizontal=True, label_visibility="collapsed")

# ======================================================
# 2️⃣ WPS Range (이미지 2번: 항목-입력창 여백 최소화)
# ======================================================
st.markdown('<div class="section-title">WPS Range (kJ/mm)</div>', unsafe_allow_html=True)
# [항목명](0.4) + [여백5%](0.05) + [입력창](1.8) + [여백10%](0.5) + [항목명](0.4) + [여백5%](0.05) + [입력창](1.8)
w_cols = st.columns([0.4, 0.05, 1.8, 0.5, 0.4, 0.05, 1.8, 1.2])

with w_cols[0]: st.markdown("**Min.**")
with w_cols[2]: min_range = st.number_input("min", value=0.96, step=0.01, format="%.2f", label_visibility="collapsed")
with w_cols[4]: st.markdown("**Max.**")
with w_cols[6]: max_range = st.number_input("max", value=2.50, step=0.01, format="%.2f", label_visibility="collapsed")

# ======================================================
# 3️⃣ Input Parameters & Live Result (이미지 2번: 수평 정렬)
# ======================================================
st.write("") 
col_left, col_space, col_right = st.columns([5, 0.8, 4.2])

with col_left:
    st.markdown('<div class="section-title">Input Parameters</div>', unsafe_allow_html=True)
    def draw_input_row(label, value, key):
        # [항목명](1.5) + [여백5%](0.05) + [입력창](2)
        r_cols = st.columns([1.5, 0.05, 2])
        with r_cols[0]: st.markdown(f"**{label}**")
        with r_cols[2]: return st.number_input(label, value=value, step=0.1, format="%.1f", key=key, label_visibility="collapsed")

    voltage = draw_input_row("Voltage (V)", 30.0, "v")
    current = draw_input_row("Current (A)", 300.0, "c")
    length  = draw_input_row("Length (mm)", 5.0, "l")
    time    = draw_input_row("Time (sec)", 1.0, "t")

k = 1.0 if standard == "AWS" else {"SAW": 1.0, "GMAW": 0.8, "FCAW": 0.8, "SMAW": 0.8}.get(process, 0.8)
HI = (k * voltage * current * time) / (length * 1000) if length > 0 else 0
status = "PASS" if min_range <= HI <= max_range else "FAIL"

with col_right:
    st.markdown('<div class="section-title">Live Result</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="result-box">{HI:.3f} kJ/mm</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="{status.lower()}">{status}</div>', unsafe_allow_html=True)

# ======================================================
# 4️⃣ 버튼 구역 (독립된 행에서 45:5:45 오른쪽 맞춤)
# ======================================================
btn_row_left, btn_row_space, btn_row_right = st.columns([5, 0.8, 4.2])

with btn_row_right:
    # 4.2 너비 구역 안에서: [여백5%](0.5) + [Save(45%)](4.5) + [여백5%](0.5) + [Export(45%)](4.5)
    b_cols = st.columns([0.5, 4.5, 0.5, 4.5])
    
    with b_cols[1]:
        if st.button("Save Data"):
            new_entry = {"Time": datetime.now().strftime("%H:%M:%S"), "Std": standard, "Process": process, "HI": round(HI, 3), "Result": status, "V": voltage, "A": current, "L": length, "T": time}
            st.session_state.history.insert(0, new_entry)
            if len(st.session_state.history) > 50: st.session_state.history.pop()
            st.rerun()

    with b_cols[3]:
        if st.session_state.history:
            csv = pd.DataFrame(st.session_state.history).to_csv(index=False).encode('utf-8-sig')
            st.download_button(label="Export", data=csv, file_name=f"HeatInput_{datetime.now().strftime('%m%d_%H%M')}.csv", mime="text/csv")
        else:
            st.button("Export", disabled=True)

# ======================================================
# 5️⃣ 히스토리 테이블
# ======================================================
if st.session_state.history:
    st.markdown('<div class="section-title">Recent History (Max 50)</div>', unsafe_allow_html=True)
    st.table(pd.DataFrame(st.session_state.history))

st.markdown('</div>', unsafe_allow_html=True)