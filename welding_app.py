import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 페이지 설정 및 디자인 테마 ---
st.set_page_config(page_title="Heat Input Master", layout="wide")

# UI 색상 정의
color_bg = "#F2F2F2"      
color_white = "#FFFFFF"   
color_line = "#000000"    
color_orange = "#FF6B00"  # 메인 주황색 라인
color_pass = "#28A745"
color_fail = "#DC3545"

if 'history' not in st.session_state: st.session_state.history = []

# CSS 주입: 요청사항(여백 최소화, 오렌지 라인, 버튼 통일) 정밀 반영
st.markdown(f"""
    <style>
    .stApp {{ background-color: {color_bg}; color: {color_line}; }}
    
    /* [요청 1] 타이틀 영역 및 주황색 수평선 여백 최소화 */
    .header-container {{
        padding-top: 5px;
        display: flex;
        align-items: center;
        margin-bottom: 0px; /* 여백 제거 */
    }}
    .orange-divider {{
        border-bottom: 5px solid {color_orange};
        margin-top: 0px;     /* 타이틀과의 간격 최소화 */
        margin-bottom: 20px; /* 아래 섹션과의 최소 간격 */
        width: 100%;
    }}
    .title-text {{ font-size: 2.3rem; font-weight: 900; margin-left: 15px; }}

    /* [요청 3] 프로세스 버튼: 크기 통일, 상하 여백, 주황색 윤곽선 */
    div[role="radiogroup"] label {{
        border: 3px solid {color_orange} !important; /* 윤곽선 주황색 */
        background-color: {color_white} !important;
        min-height: 55px !important;  /* 높이 통일 */
        padding: 15px 10px !important; /* 상하 여백 추가 */
        border-radius: 8px !important;
        margin-right: 10px !important;
        flex: 1 1 0% !important;      /* 모든 버튼 크기 동일하게 통일 */
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }}
    div[role="radiogroup"] label[data-checked="true"] {{ 
        background-color: {color_line} !important; 
        border-color: {color_line} !important;
    }}
    div[role="radiogroup"] label[data-checked="true"] p {{ color: {color_orange} !important; }}
    div[role="radiogroup"] label p {{ font-weight: 900 !important; font-size: 1.2rem !important; }}

    /* [요청 4, 5] Input Parameters 및 WPS range: 주황색 윤곽선 및 1줄 정렬 */
    div.stNumberInput input {{
        background-color: {color_brown if 'color_brown' in locals() else "#4A3728"} !important; 
        background-color: #4A3728 !important; /* 고대비 유지 */
        color: {color_orange} !important;
        border: 3px solid {color_orange} !important; /* 윤곽선 주황색 */
        height: 55px !important;
        font-size: 1.3rem !important;
        font-weight: 900 !important;
        border-radius: 8px !important;
    }}
    
    /* 사이드바 WPS range 폭 조정 */
    section[data-testid="stSidebar"] .stNumberInput {{ width: 85% !important; }}

    /* [요청 6] Live Result 박스 높이 40% 축소형 */
    .result-value-box {{
        background-color: {color_white};
        border: 3px solid {color_orange}; /* 여기도 오렌지 포인트 */
        height: 60px !important; 
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        font-weight: 900;
        margin-bottom: 5px;
    }}
    .result-status-box {{
        height: 50px !important;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        font-weight: 900;
        border: 3px solid {color_line};
        color: {color_white};
    }}

    .save-box {{
        border: 2px solid {color_line};
        padding: 10px;
        background-color: #E0E0E0;
        margin-top: 10px;
        border-radius: 8px;
    }}
    
    /* 텍스트 통일성 */
    label p {{ font-size: 16px !important; font-weight: 900 !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. 타이틀 및 로고 (GitHub Raw 링크 반영) ---
# [요청 2] 로고파일 링크 업데이트 (GitHub Raw URL 사용)
logo_url = "https://raw.githubusercontent.com/jubailsanghoon/Heatinput/main/db65c0d39f36f2dddc248ea0bf2e4efc.jpg"

st.markdown('<div class="header-container">', unsafe_allow_html=True)
col_l, col_t = st.columns([1, 8])
with col_l:
    st.image(logo_url, width=80) # 원본 비율 유지하며 폭 조정
with col_t:
    st.markdown(f'<span class="title-text">Heat Input Master</span>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="orange-divider"></div>', unsafe_allow_html=True)

# --- 3. 사이드바 (WPS range) ---
with st.sidebar:
    st.markdown("### 📜 Standard")
    std_mode = st.radio("Std", options=['ISO', 'AWS'], label_visibility="collapsed")
    
    st.markdown("<br>### ⚙️ WPS range", unsafe_allow_html=True)
    w_min = st.number_input("Min", value=1.0, step=0.1, format="%.1f")
    w_max = st.number_input("Max", value=2.5, step=0.1, format="%.1f")
    
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.write("**Contact:** jubail.sanghoon@gmail.com")

# --- 4. 메인 UI (3열 밸런스 조정) ---
c1, c2, c3 = st.columns([1.1, 1.2, 0.9])

# 1. Select Process (크기 통일 & 오렌지 윤곽선)
with c1:
    st.markdown("### 1. Select Process")
    proc = st.radio("P", options=['SAW', 'FCAW', 'SMAW', 'GMAW'], horizontal=True, label_visibility="collapsed")
    k = 1.0 if std_mode == 'AWS' or proc == 'SAW' else 0.8

# 2. Input Parameters (윤곽선 오렌지 & 1줄 정렬)
with c2:
    st.markdown("### 2. Input Parameters")
    
    def param_row(label, val, step, key):
        row_c1, row_c2 = st.columns([5, 5])
        row_c1.markdown(f"<div style='margin-top:15px; font-weight:900;'>{label}</div>", unsafe_allow_html=True)
        return row_c2.number_input(label, value=val, step=step, format="%.1f", label_visibility="collapsed", key=key)

    v = param_row("Voltage (V)", 28.0, 0.5, "v_main")
    a = param_row("Amperage (A)", 220.0, 5.0, "a_main")
    l = param_row("Length (mm)", 150.0, 10.0, "l_main")
    t = param_row("Time (Sec)", 120.0, 1.0, "t_main")
    
    speed = (l / t) * 60 if t > 0 else 0

# 3. Live Result & Save
with c3:
    st.markdown("### 3. Live Result")
    hi = (k * v * a * t) / (l * 1000) if l > 0 else 0
    is_pass = w_min <= hi <= w_max
    
    # 상단 수치 박스 (오렌지 윤곽선)
    st.markdown(f'<div class="result-value-box">{hi:.3f} kJ/mm</div>', unsafe_allow_html=True)
    
    # 하단 상태 박스
    s_bg = color_pass if is_pass else color_fail
    st.markdown(f'<div class="result-status-box" style="background-color:{s_bg};">{"PASS" if is_pass else "FAIL"}</div>', unsafe_allow_html=True)
    
    # 별도 분리된 Save 박스
    st.markdown('<div class="save-box">', unsafe_allow_html=True)
    if st.button("💾 SAVE LOG DATA", use_container_width=True):
        st.session_state.history.insert(0, {
            "Time": datetime.now().strftime("%H:%M:%S"),
            "Proc": proc,
            "V": f"{v:.1f}", "A": f"{a:.1f}",
            "L": f"{l:.1f}", "T": f"{t:.1f}",
            "HI": f"{hi:.3f}", "Status": "PASS" if is_pass else "FAIL"
        })
        st.toast("Data Logged")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. 히스토리 데이터 ---
if st.session_state.history:
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.table(pd.DataFrame(st.session_state.history).head(10))