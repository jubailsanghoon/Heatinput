import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 페이지 설정 및 테마 ---
st.set_page_config(page_title="Heat Input Master", layout="wide")

color_bg = "#F2F2F2"      # 연회색 배경
color_white = "#FFFFFF"   # 흰색 박스
color_line = "#000000"    # 검은색 실선
color_pass = "#28A745"
color_fail = "#DC3545"

if 'history' not in st.session_state: st.session_state.history = []

# --- 2. CSS 정밀 레이아웃 주입 ---
st.markdown(f"""
    <style>
    /* 전체 배경 및 폰트 강제 고정 */
    .stApp {{ background-color: {color_bg}; color: {color_line}; }}
    
    /* 헤더: 로고 투명화, 여백 최소화 */
    .header-logo img {{ mix-blend-mode: multiply; }}
    .header-container {{ display: flex; align-items: center; padding-top: 0px; margin-bottom: 0px; }}
    .black-divider {{ border-bottom: 5px solid {color_line}; margin-top: 5px; margin-bottom: 20px; width: 100%; }}
    
    /* 타이틀 텍스트 크기 고정 및 볼드 해제 */
    .title-text {{ font-size: 2.3rem; font-weight: normal; margin-left: 15px; color: {color_line}; }}
    
    /* [폰트] 모든 라벨 및 텍스트 1.5rem 고정 & 볼드 해제 (font-weight: normal) */
    .master-label {{
        font-size: 1.5rem !important;
        font-weight: normal !important;
        color: {color_line} !important;
        margin: 0 0 10px 0 !important;
        padding: 0 !important;
        line-height: 1.2 !important;
    }}

    /* ISO/AWS 박스 폭 통일, 높이 60px 고정 */
    section[data-testid="stSidebar"] div[role="radiogroup"] {{
        display: flex !important; width: 100% !important; gap: 10px !important; margin-bottom: 0px !important;
    }}
    section[data-testid="stSidebar"] div[role="radiogroup"] label {{
        flex: 1 1 50% !important; /* 폭 2배 꽉 채움 */
        height: 60px !important;  
        border: 2px solid {color_line} !important;
        background-color: {color_white} !important;
        border-radius: 4px !important;
        justify-content: center !important;
        margin: 0 !important; padding: 0 !important;
    }}

    /* Select Process 2x2 그리드, 높이 60px 고정 */
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] {{
        display: grid !important;
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 10px !important;
        margin-top: -5px !important;
    }}
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label {{
        height: 60px !important;
        border: 2px solid {color_line} !important;
        background-color: {color_white} !important;
        border-radius: 4px !important;
        justify-content: center !important;
        margin: 0 !important; padding: 0 !important;
    }}
    
    /* 라디오 버튼 텍스트 볼드 해제 및 선택 반전 */
    div[role="radiogroup"] label p {{ font-size: 1.5rem !important; font-weight: normal !important; margin: 0 !important; }}
    div[role="radiogroup"] label[data-checked="true"] {{ background-color: {color_line} !important; }}
    div[role="radiogroup"] label[data-checked="true"] p {{ color: {color_white} !important; }}

    /* 입력창 높이 60px 고정, (-)왼쪽 (+)오른쪽 배치 */
    div[data-testid="stNumberInputContainer"] {{
        background-color: {color_white} !important; 
        border: 2px solid {color_line} !important;
        border-radius: 4px !important;
        height: 60px !important; 
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        padding: 0 !important;
        margin-bottom: 0px !important;
    }}
    
    /* 입력창 숫자 볼드 해제 */
    div[data-testid="stNumberInputContainer"] input {{
        color: {color_line} !important;
        font-size: 1.5rem !important; 
        font-weight: normal !important;
        text-align: center !important;
    }}
    
    /* +,- 버튼 볼드 해제 */
    button[data-testid="baseButton-secondary"] {{
        color: {color_line} !important;
        min-width: 60px !important;
        height: 100% !important;
        font-size: 1.5rem !important; 
        font-weight: normal !important;
        background-color: transparent !important;
        border: none !important;
    }}

    /* 입력창 여백 최소화 */
    .stNumberInput {{ margin-bottom: -10px !important; }}
    
    /* [요청] WPS range 입력창 폭 축소 (Standard 박스와 유사한 비율로 조절) */
    section[data-testid="stSidebar"] div.stNumberInput {{
        width: 65% !important; 
    }}
    
    /* Live Result 박스 높이 고정 및 볼드 해제 */
    .result-value-box {{
        background-color: {color_white};
        border: 3px solid {color_line};
        height: 75px !important;
        display: flex; align-items: center; justify-content: center;
        font-size: 2.2rem; font-weight: normal; margin-bottom: 10px; border-radius: 4px;
        margin-top: -5px;
    }}
    .result-status-box {{
        height: 60px !important;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.8rem; font-weight: normal; 
        border: 2px solid {color_line}; color: {color_white}; border-radius: 4px;
    }}
    
    /* 저장 버튼 볼드 해제 */
    .save-btn-container button {{
        height: 60px !important;
        font-size: 1.5rem !important;
        font-weight: normal !important;
        border: 2px solid {color_line} !important;
        background-color: #E6E6E6 !important;
        color: {color_line} !important;
        border-radius: 4px !important;
        margin-top: 10px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. 헤더 (투명 로고 밀착) ---
logo_url = "https://raw.githubusercontent.com/jubailsanghoon/Heatinput/main/db65c0d39f36f2dddc248ea0bf2e4efc.jpg"

st.markdown('<div class="header-container">', unsafe_allow_html=True)
c_logo, c_title = st.columns([1, 9])
with c_logo:
    st.markdown(f'<div class="header-logo"><img src="{logo_url}" width="80"></div>', unsafe_allow_html=True)
with c_title:
    st.markdown(f'<span class="title-text">Heat Input Master</span>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="black-divider"></div>', unsafe_allow_html=True)

# --- 4. 사이드바 (WPS 폭 축소 적용) ---
with st.sidebar:
    st.markdown("<div class='master-label'>Standard</div>", unsafe_allow_html=True)
    std_mode = st.radio("Std", options=['ISO', 'AWS'], horizontal=True, label_visibility="collapsed")
    
    st.markdown("<br><div class='master-label'>WPS range</div>", unsafe_allow_html=True)
    # CSS width: 65% 적용됨
    w_min = st.number_input("Min", value=1.0, step=0.1, format="%.1f")
    w_max = st.number_input("Max", value=2.5, step=0.1, format="%.1f")
    
    st.markdown("<br><hr style='margin:10px 0;'>", unsafe_allow_html=True)
    st.write("Admin: jubail.sanghoon@gmail.com") # 텍스트 볼드 해제

# --- 5. 메인 레이아웃 (여백 깎아내기 및 칼정렬) ---
col1, col2, col3 = st.columns([1.1, 1.3, 0.9], gap="medium")

# [섹션 1] Select Process (2x2 그리드 높이 60px)
with col1:
    st.markdown("<div class='master-label'>Select Process</div>", unsafe_allow_html=True)
    proc = st.radio("P", options=['SAW', 'FCAW', 'SMAW', 'GMAW'], label_visibility="collapsed")
    k = 1.0 if std_mode == 'AWS' or proc == 'SAW' else 0.8

# [섹션 2] Input Parameters (1.5rem 통일 및 여백 밀착)
with col2:
    st.markdown("<div class='master-label'>Input Parameters</div>", unsafe_allow_html=True)
    
    def param_row(label, val, step, key):
        c_lbl, c_inp = st.columns([4.5, 5.5])
        with c_lbl:
            st.markdown(f"<div class='master-label' style='margin-top:10px !important;'>{label}</div>", unsafe_allow_html=True)
        with c_inp:
            return st.number_input(label, value=val, step=step, format="%.1f", label_visibility="collapsed", key=key)

    v = param_row("Voltage (V)", 28.0, 0.5, "v_in")
    a = param_row("Amperage (A)", 220.0, 5.0, "a_in")
    l = param_row("Length (mm)", 150.0, 10.0, "l_in")
    t = param_row("Time (Sec)", 120.0, 1.0, "t_in")

# [섹션 3] Live Result
with col3:
    st.markdown("<div class='master-label'>Live Result</div>", unsafe_allow_html=True)
    hi = (k * v * a * t) / (l * 1000) if l > 0 else 0
    is_pass = w_min <= hi <= w_max
    
    st.markdown(f'<div class="result-value-box">{hi:.3f} kJ/mm</div>', unsafe_allow_html=True)
    st_bg = color_pass if is_pass else color_fail
    st.markdown(f'<div class="result-status-box" style="background-color:{st_bg};">{"PASS" if is_pass else "FAIL"}</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="save-btn-container">', unsafe_allow_html=True)
    if st.button("💾 SAVE LOG", use_container_width=True):
        st.session_state.history.insert(0, {
            "Time": datetime.now().strftime("%H:%M:%S"),
            "Proc": proc, "V": v, "A": a, "L": l, "T": t, 
            "HI": f"{hi:.3f}", "Status": "PASS" if is_pass else "FAIL"
        })
        st.toast("Saved")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 6. 히스토리 ---
if st.session_state.history:
    st.markdown("<hr style='margin-top:20px; margin-bottom:10px;'>", unsafe_allow_html=True)
    st.table(pd.DataFrame(st.session_state.history).head(10))