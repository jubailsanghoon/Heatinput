import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 페이지 설정 및 테마 ---
st.set_page_config(page_title="Heat Input Master", layout="wide")

color_bg = "#F2F2F2"
color_white = "#FFFFFF"
color_line = "#000000"
color_pass = "#28A745"
color_fail = "#DC3545"

if 'history' not in st.session_state: st.session_state.history = []

# --- 2. CSS 초정밀 레이아웃 (모바일 가독성 & +,- 버튼 고정) ---
st.markdown(f"""
    <style>
    /* 전체 배경 */
    .stApp {{ background-color: {color_bg}; color: {color_line}; }}
    
    /* [마스터] 기준 폰트 */
    .master-label {{
        font-size: 1.5rem !important; font-weight: normal !important; color: {color_line} !important;
        margin: 0 0 10px 0 !important; padding: 0 !important; line-height: 1.2 !important;
    }}

    /* [섹션 0] 상부 타이틀 */
    .header-logo img {{ mix-blend-mode: multiply; }}
    .header-container {{ display: flex; align-items: center; padding-top: 0px; margin-bottom: 0px; }}
    .black-divider {{ border-bottom: 5px solid {color_line}; margin-top: 5px; margin-bottom: 20px; width: 100%; }}
    .title-text {{ font-size: 2.3rem; font-weight: bold; margin-left: 15px; color: {color_line}; }}

    /* [섹션 2] Select Process (2x2 버튼 & 글자 크게) */
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] {{
        display: grid !important; grid-template-columns: repeat(2, 1fr) !important; 
        gap: 10px !important; margin-top: -5px !important;
    }}
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label {{
        height: 60px !important; border: 2px solid {color_line} !important; background-color: {color_white} !important;
        border-radius: 4px !important; justify-content: center !important; align-items: center !important;
        margin: 0 !important; padding: 0 !important;
    }}
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label p, 
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label span {{
        font-size: 1.5rem !important; font-weight: normal !important; margin: 0 !important;
    }}
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label[data-checked="true"] {{ background-color: {color_line} !important; }}
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label[data-checked="true"] p {{ color: {color_white} !important; }}

    /* [섹션 3] Input Parameters (+,- 버튼 좌우 강제 분리) */
    div[data-testid="stNumberInputContainer"] {{
        display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important;
        background-color: {color_white} !important; border: 2px solid {color_line} !important;
        border-radius: 4px !important; height: 60px !important; padding: 0 !important;
        align-items: center !important; justify-content: space-between !important;
    }}
    div[data-testid="stNumberInputContainer"] > button:first-of-type {{
        order: -1 !important; min-width: 55px !important; height: 100% !important; font-size: 1.5rem !important;
    }}
    div[data-testid="stNumberInputContainer"] input {{
        order: 2 !important; flex-grow: 1 !important; text-align: center !important; font-size: 1.5rem !important;
        background-color: transparent !important; border: none !important; width: 100% !important;
    }}
    div[data-testid="stNumberInputContainer"] > button:last-of-type {{
        order: 99 !important; min-width: 55px !important; height: 100% !important; font-size: 1.5rem !important;
    }}

    /* [섹션 4] Live Result & Save */
    .result-value-box {{
        background-color: {color_white}; border: 3px solid {color_line}; height: 75px !important; 
        display: flex; align-items: center; justify-content: center; font-size: 2.2rem; font-weight: bold;
        margin-bottom: 10px; border-radius: 4px;
    }}
    .result-status-box {{
        height: 60px !important; display: flex; align-items: center; justify-content: center; font-size: 1.8rem; font-weight: bold;
        border: 2px solid {color_line}; color: {color_white}; border-radius: 4px;
    }}
    .save-btn-container button {{
        height: 60px !important; font-size: 1.5rem !important; border: 2px solid {color_line} !important; 
        background-color: #E6E6E6 !important; color: {color_line} !important; margin-top: 10px !important;
    }}

    /* [모바일 전용 최적화] */
    @media (max-width: 768px) {{
        .title-text {{ font-size: 1.8rem; }}
        .master-label {{ font-size: 1.2rem !important; margin-top: 5px !important; }}
        div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label p {{ font-size: 1.2rem !important; }}
        div[data-testid="stNumberInputContainer"], 
        div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label {{ height: 50px !important; }}
        div[data-testid="stNumberInputContainer"] input {{ font-size: 1.3rem !important; }}
        .result-value-box {{ height: 60px !important; font-size: 1.8rem !important; }}
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. [상부 타이틀] ---
logo_url = "https://raw.githubusercontent.com/jubailsanghoon/Heatinput/main/db65c0d39f36f2dddc248ea0bf2e4efc.jpg"
st.markdown('<div class="header-container">', unsafe_allow_html=True)
c1, c2 = st.columns([1, 9])
with c1: st.markdown(f'<div class="header-logo"><img src="{logo_url}" width="80"></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<span class="title-text">Heat Input Master</span>', unsafe_allow_html=True)
st.markdown('</div><div class="black-divider"></div>', unsafe_allow_html=True)

# --- 4. [섹션 1] 사이드바 (Standard & WPS) ---
with st.sidebar:
    st.markdown("<div class='master-label'>Standard</div>", unsafe_allow_html=True)
    std_mode = st.radio("Std", options=['ISO', 'AWS'], label_visibility="collapsed")
    
    st.markdown("<br><div class='master-label'>WPS range</div>", unsafe_allow_html=True)
    w_min = st.number_input("Min", value=1.0, step=0.1, format="%.1f")
    w_max = st.number_input("Max", value=2.5, step=0.1, format="%.1f")
    
    st.markdown("<br><hr><div>Admin: jubail.sanghoon@gmail.com</div>", unsafe_allow_html=True)

# --- 5. 메인 레이아웃 (4개 섹션 조립) ---
col1, col2, col3 = st.columns([1.1, 1.3, 0.9], gap="medium")

# [섹션 2] Select Process
with col1:
    st.markdown("<div class='master-label'>Select Process</div>", unsafe_allow_html=True)
    proc = st.radio("P", options=['SAW', 'FCAW', 'SMAW', 'GMAW'], label_visibility="collapsed")
    # 열 효율 계수 k 설정
    k = 1.0 if std_mode == 'AWS' or proc == 'SAW' else 0.8

# [섹션 3] Input Parameters
with col2:
    st.markdown("<div class='master-label'>Input Parameters</div>", unsafe_allow_html=True)
    def param_row(label, val, step, key):
        c_l, c_i = st.columns([4.5, 5.5])
        with c_l: st.markdown(f"<div class='master-label' style='height: 60px; display: flex; align-items: center;'>{label}</div>", unsafe_allow_html=True)
        with c_i: return st.number_input(label, value=val, step=step, format="%.1f", label_visibility="collapsed", key=key)

    v = param_row("Voltage (V)", 28.0, 0.5, "v_in")
    a = param_row("Amperage (A)", 220.0, 5.0, "a_in")
    l = param_row("Length (mm)", 150.0, 10.0, "l_in")
    t = param_row("Time (Sec)", 120.0, 1.0, "t_in")

# [섹션 4] Live Result & Save
with col3:
    st.markdown("<div class='master-label'>Live Result</div>", unsafe_allow_html=True)
    # 입열량 공식: (k * V * A * t) / (L * 1000)
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
        st.toast("Saved Successfully!")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 6. 기록 로그 테이블 ---
if st.session_state.history:
    st.markdown("<hr style='margin-top:20px;'>", unsafe_allow_html=True)
    st.table(pd.DataFrame(st.session_state.history).head(10))