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

# --- 2. CSS 초정밀 레이아웃 (60% 폭 & 모바일 가독성 최적화) ---
st.markdown(f"""
    <style>
    /* 전체 배경 */
    .stApp {{ background-color: {color_bg}; color: {color_line}; }}
    
    /* [마스터] 가변 폰트 시스템 */
    .master-label {{
        font-size: clamp(1.1rem, 2.5vw, 1.5rem) !important;
        font-weight: normal !important;
        color: {color_line} !important;
        margin-bottom: 5px !important;
        line-height: 1.2 !important;
    }}

    /* --- [섹션 3] 입력창 폭 60% 및 좌우 버튼 1/2/3 고정 --- */
    /* Input Parameters 컬럼 내의 입력창 너비 제한 */
    div[data-testid="column"]:nth-of-type(2) .stNumberInput {{
        width: 60% !important; 
        min-width: 220px !important; /* 모바일에서 지나친 축소 방지 */
    }}

    div[data-testid="stNumberInputContainer"] {{
        display: flex !important;
        flex-direction: row !important;
        height: 60px !important;
        background-color: {color_white} !important;
        border: 2px solid {color_line} !important;
        border-radius: 4px !important;
        overflow: hidden !important;
    }}

    /* 1번: 마이너스(-) 버튼 강제 왼쪽 */
    div[data-testid="stNumberInputContainer"] > button:first-of-type {{
        order: -1 !important; min-width: 60px !important; height: 100% !important; 
        font-size: 1.5rem !important; border-right: 1px solid #ddd !important;
        background: transparent !important;
    }}
    /* 2번: 숫자창 (가운데) */
    div[data-testid="stNumberInputContainer"] input {{
        order: 2 !important; flex-grow: 1 !important; text-align: center !important; 
        font-size: 1.5rem !important; font-weight: bold !important;
        background: transparent !important; border: none !important;
    }}
    /* 3번: 플러스(+) 버튼 강제 오른쪽 */
    div[data-testid="stNumberInputContainer"] > button:last-of-type {{
        order: 99 !important; min-width: 60px !important; height: 100% !important; 
        font-size: 1.5rem !important; border-left: 1px solid #ddd !important;
        background: transparent !important;
    }}

    /* [섹션 2] 공정 선택 버튼 글자 크기 동기화 */
    div[role="radiogroup"] label p, div[role="radiogroup"] label span {{
        font-size: clamp(1.1rem, 2.5vw, 1.5rem) !important;
    }}

    /* 결과 박스 스타일 */
    .result-value-box {{
        background: {color_white}; border: 3px solid {color_line}; height: 80px; 
        display: flex; align-items: center; justify-content: center; 
        font-size: clamp(1.5rem, 4vw, 2.2rem); font-weight: bold; margin-bottom: 10px;
    }}

    /* 📱 모바일 환경 전용 (Media Query) */
    @media (max-width: 768px) {{
        div[data-testid="column"]:nth-of-type(2) .stNumberInput {{
            width: 100% !important; /* 모바일은 가로폭 전체 활용 */
        }}
        .title-text {{ font-size: 1.8rem !important; }}
        div[data-testid="stNumberInputContainer"] {{ height: 50px !important; }}
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. 헤더 영역 (상부 타이틀) ---
logo_url = "https://raw.githubusercontent.com/jubailsanghoon/Heatinput/main/db65c0d39f36f2dddc248ea0bf2e4efc.jpg"
st.markdown(f"""
    <div style="display: flex; align-items: center; border-bottom: 5px solid black; padding-bottom: 10px; margin-bottom: 25px;">
        <img src="{logo_url}" width="70">
        <span class="title-text" style="font-size: 2.3rem; margin-left: 15px; font-weight: bold;">Heat Input Master</span>
    </div>
""", unsafe_allow_html=True)

# --- 4. 메인 레이아웃 (모듈형 3단 배치) ---
col1, col2, col3 = st.columns([1.1, 1.3, 0.9], gap="large")

# [섹션 1 & 2] 설정 및 공정 선택
with col1:
    with st.expander("🛠 Standard & WPS Range", expanded=True):
        std_mode = st.radio("Standard", ['ISO', 'AWS'], horizontal=True)
        w_min = st.number_input("WPS Min", 1.0, step=0.1, key="w_min")
        w_max = st.number_input("WPS Max", 2.5, step=0.1, key="w_max")
    
    st.markdown("<br><div class='master-label'>Select Process</div>", unsafe_allow_html=True)
    proc = st.radio("P", ['SAW', 'FCAW', 'SMAW', 'GMAW'], label_visibility="collapsed")
    # 열 효율 계수 k 자동 적용
    k = 1.0 if std_mode == 'AWS' or proc == 'SAW' else 0.8

# [섹션 3] Input Parameters (너비 60% 적용)
with col2:
    st.markdown("<div class='master-label'>Input Parameters</div>", unsafe_allow_html=True)
    def param_input(label, val, step, key):
        st.markdown(f"<div class='master-label' style='margin-top:15px;'>{label}</div>", unsafe_allow_html=True)
        return st.number_input(label, value=val, step=step, format="%.1f", label_visibility="collapsed", key=key)

    v = param_input("Voltage (V)", 28.0, 0.5, "v_val")
    a = param_input("Amperage (A)", 220.0, 5.0, "a_val")
    l = param_input("Length (mm)", 150.0, 10.0, "l_val")
    t = param_input("Time (Sec)", 120.0, 1.0, "t_val")

# [섹션 4] Live Result & Data Save
with col3:
    st.markdown("<div class='master-label'>Live Result</div>", unsafe_allow_html=True)
    hi = (k * v * a * t) / (l * 1000) if l > 0 else 0
    is_pass = w_min <= hi <= w_max
    
    st.markdown(f'<div class="result-value-box">{hi:.3f} kJ/mm</div>', unsafe_allow_html=True)
    
    st_bg = color_pass if is_pass else color_fail
    st.markdown(f"""
        <div style="background: {st_bg}; color: white; height: 60px; display: flex; align-items: center; justify-content: center; font-size: 1.8rem; font-weight: bold; border-radius: 4px; border: 2px solid black;">
            {"PASS" if is_pass else "FAIL"}
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("💾 SAVE LOG", use_container_width=True):
        st.session_state.history.insert(0, {
            "Time": datetime.now().strftime("%H:%M:%S"),
            "Proc": proc, "V": v, "A": a, "L": l, "T": t, 
            "HI": f"{hi:.3f}", "Status": "PASS" if is_pass else "FAIL"
        })
        st.toast("Data Saved!")

# --- 5. 데이터 로그 테이블 ---
if st.session_state.history:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.table(pd.DataFrame(st.session_state.history).head(10))