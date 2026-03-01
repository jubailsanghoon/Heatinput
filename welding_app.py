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

# --- 2. CSS 초정밀 레이아웃 (반응형 모바일 지원) ---
st.markdown(f"""
    <style>
    /* 전체 배경 */
    .stApp {{ background-color: {color_bg}; color: {color_line}; }}
    
    /* 헤더 및 타이틀 */
    .header-logo img {{ mix-blend-mode: multiply; }}
    .header-container {{ display: flex; align-items: center; padding-top: 0px; margin-bottom: 0px; }}
    .black-divider {{ border-bottom: 5px solid {color_line}; margin-top: 5px; margin-bottom: 20px; width: 100%; }}
    .title-text {{ font-size: 2.3rem; font-weight: normal; margin-left: 15px; color: {color_line}; }}
    
    /* PC 기준 마스터 폰트 (1.5rem) */
    .master-label {{
        font-size: 1.5rem !important; font-weight: normal !important; color: {color_line} !important;
        margin: 0 0 10px 0 !important; padding: 0 !important; line-height: 1.2 !important;
    }}

    /* Select Process 2x2 박스 그리드 */
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] {{
        display: grid !important; grid-template-columns: repeat(2, 1fr) !important; 
        gap: 10px !important; margin-top: -5px !important;
    }}
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label {{
        height: 60px !important; border: 2px solid {color_line} !important; background-color: {color_white} !important;
        border-radius: 4px !important; justify-content: center !important; align-items: center !important;
        margin: 0 !important; padding: 0 !important;
    }}
    
    /* 공정 버튼 텍스트 통일 */
    div[role="radiogroup"] label p, div[role="radiogroup"] label span, div[role="radiogroup"] label div {{
        font-size: 1.5rem !important; font-weight: normal !important; margin: 0 !important; 
    }}
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label[data-checked="true"] {{ background-color: {color_line} !important; }}
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label[data-checked="true"] p {{ color: {color_white} !important; }}

    /* --- [수정 핵심] 숫자 입력창 좌우 분리 (모바일 강제 적용) --- */
    div[data-testid="stNumberInputContainer"] {{
        display: flex !important;
        flex-direction: row !important; /* 모바일에서도 세로 쌓임 방지 */
        flex-wrap: nowrap !important;   /* 줄바꿈 방지 */
        background-color: {color_white} !important; 
        border: 2px solid {color_line} !important;
        border-radius: 4px !important;
        height: 60px !important; 
        padding: 0 !important;
        margin-bottom: 0px !important;
        align-items: center !important;
        justify-content: space-between !important;
    }}
    
    /* 1번: 마이너스(-) 버튼 강제 왼쪽 끝 */
    div[data-testid="stNumberInputContainer"] > button:first-of-type {{
        order: -1 !important; 
        min-width: 50px !important; 
        height: 100% !important;
        background-color: transparent !important;
        border-right: 1px solid #CCC !important;
        margin: 0 !important;
        color: {color_line} !important;
        font-size: 1.5rem !important;
    }}
    
    /* 2번: 숫자 입력 칸 가운데 */
    div[data-testid="stNumberInputContainer"] > div,
    div[data-testid="stNumberInputContainer"] input {{
        order: 2 !important;
        flex-grow: 1 !important;
        text-align: center !important;
        color: {color_line} !important;
        font-size: 1.5rem !important; 
        background-color: transparent !important;
        border: none !important;
        width: 100% !important; /* 모바일 입력창 찌그러짐 방지 */
    }}
    
    /* 3번: 플러스(+) 버튼 강제 오른쪽 끝 */
    div[data-testid="stNumberInputContainer"] > button:last-of-type {{
        order: 99 !important; 
        min-width: 50px !important;
        height: 100% !important;
        background-color: transparent !important;
        border-left: 1px solid #CCC !important;
        margin: 0 !important;
        color: {color_line} !important;
        font-size: 1.5rem !important;
    }}

    /* 컬럼 간 기본 여백 제거 */
    div[data-testid="column"]:nth-of-type(2) div[data-testid="stHorizontalBlock"] {{ gap: 0rem !important; }}
    div[data-testid="column"]:nth-of-type(2) div[data-testid="stHorizontalBlock"] div[data-testid="column"] {{ padding: 0 !important; }}
    .stNumberInput {{ margin-bottom: -10px !important; margin-left: 5px !important; }}
    
    /* 사이드바 설정 */
    section[data-testid="stSidebar"] div[role="radiogroup"] {{
        display: flex !important; flex-direction: column !important; align-items: flex-start !important; gap: 5px !important; margin-bottom: 15px !important;
    }}
    section[data-testid="stSidebar"] div.stNumberInput {{ width: 85% !important; margin-left: 0 !important; }}

    /* Live Result 박스 및 버튼 */
    .result-value-box {{
        background-color: {color_white}; border: 3px solid {color_line}; height: 75px !important; display: flex; align-items: center; justify-content: center;
        font-size: 2.2rem; margin-bottom: 10px; border-radius: 4px; margin-top: -5px;
    }}
    .result-status-box {{
        height: 60px !important; display: flex; align-items: center; justify-content: center; font-size: 1.8rem; 
        border: 2px solid {color_line}; color: {color_white}; border-radius: 4px;
    }}
    .save-btn-container button {{
        height: 60px !important; font-size: 1.5rem !important; border: 2px solid {color_line} !important; background-color: #E6E6E6 !important;
        color: {color_line} !important; border-radius: 4px !important; margin-top: 10px !important;
    }}

    /* --------------------------------------------------- */
    /* [모바일 전용 레이아웃] 화면 폭 768px 이하일 때 가독성 확보 */
    /* --------------------------------------------------- */
    @media (max-width: 768px) {{
        /* 글자 크기를 모바일 화면에 맞게 축소하여 잘림 방지 */
        .title-text {{ font-size: 1.8rem; }}
        .master-label {{ font-size: 1.1rem !important; height: auto !important; margin-top: 5px !important; }}
        
        div[role="radiogroup"] label p, 
        div[role="radiogroup"] label span, 
        div[role="radiogroup"] label div {{ font-size: 1.1rem !important; }}
        
        /* 입력창 및 박스 높이 축소 */
        div[data-testid="stNumberInputContainer"], 
        div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label {{ height: 50px !important; }}
        
        div[data-testid="stNumberInputContainer"] input {{ font-size: 1.2rem !important; }}
        
        /* 모바일에서 +,- 버튼 크기 재조정 */
        div[data-testid="stNumberInputContainer"] > button:first-of-type,
        div[data-testid="stNumberInputContainer"] > button:last-of-type {{
            min-width: 45px !important; font-size: 1.2rem !important;
        }}

        /* 결과창 크기 축소 */
        .result-value-box {{ height: 60px !important; font-size: 1.8rem !important; }}
        .result-status-box {{ height: 50px !important; font-size: 1.4rem !important; }}
        .save-btn-container button {{ height: 50px !important; font-size: 1.2rem !important; }}
        
        /* 모바일에서는 라벨과 입력창 사이의 숨구멍 여백 제거 */
        .stNumberInput {{ margin-left: 0 !important; }}
        section[data-testid="stSidebar"] div.stNumberInput {{ width: 100% !important; }}
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. 헤더 ---
logo_url = "https://raw.githubusercontent.com/jubailsanghoon/Heatinput/main/db65c0d39f36f2dddc248ea0bf2e4efc.jpg"

st.markdown('<div class="header-container">', unsafe_allow_html=True)
c_logo, c_title = st.columns([1, 9])
with c_logo:
    st.markdown(f'<div class="header-logo"><img src="{logo_url}" width="80"></div>', unsafe_allow_html=True)
with c_title:
    st.markdown(f'<span class="title-text">Heat Input Master</span>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="black-divider"></div>', unsafe_allow_html=True)

# --- 4. 사이드바 ---
with st.sidebar:
    st.markdown("<div class='master-label'>Standard</div>", unsafe_allow_html=True)
    std_mode = st.radio("Std", options=['ISO', 'AWS'], horizontal=False, label_visibility="collapsed")
    
    st.markdown("<br><div class='master-label'>WPS range</div>", unsafe_allow_html=True)
    w_min = st.number_input("Min", value=1.0, step=0.1, format="%.1f")
    w_max = st.number_input("Max", value=2.5, step=0.1, format="%.1f")
    
    st.markdown("<br><hr style='margin:10px 0;'>", unsafe_allow_html=True)
    st.markdown("<div>Admin: jubail.sanghoon@gmail.com</div>", unsafe_allow_html=True)

# --- 5. 메인 레이아웃 ---
col1, col2, col3 = st.columns([1.1, 1.3, 0.9], gap="medium")

with col1:
    st.markdown("<div class='master-label'>Select Process</div>", unsafe_allow_html=True)
    proc = st.radio("P", options=['SAW', 'FCAW', 'SMAW', 'GMAW'], label_visibility="collapsed")
    k = 1.0 if std_mode == 'AWS' or proc == 'SAW' else 0.8

with col2:
    st.markdown("<div class='master-label'>Input Parameters</div>", unsafe_allow_html=True)
    
    def param_row(label, val, step, key):
        c_lbl, c_inp = st.columns([4.5, 5.5])
        with c_lbl:
            st.markdown(f"<div class='master-label' style='display: flex; align-items: center; height: 100%; margin: 0 !important;'>{label}</div>", unsafe_allow_html=True)
        with c_inp:
            return st.number_input(label, value=val, step=step, format="%.1f", label_visibility="collapsed", key=key)

    v = param_row("Voltage (V)", 28.0, 0.5, "v_in")
    a = param_row("Amperage (A)", 220.0, 5.0, "a_in")
    l = param_row("Length (mm)", 150.0, 10.0, "l_in")
    t = param_row("Time (Sec)", 120.0, 1.0, "t_in")

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