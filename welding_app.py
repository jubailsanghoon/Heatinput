import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 페이지 설정 및 디자인 테마 ---
st.set_page_config(page_title="Welding Heat Master Pro", layout="wide")

brand_cream = "#FCF8F2"
brand_brown = "#4A3728"
brand_orange = "#FF6B00"

# CSS 주입: 버튼 및 결과창 높이 동기화 튜닝
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {brand_cream};
        color: {brand_brown};
    }}
    
    h1 {{
        color: {brand_brown};
        font-weight: 800;
        border-bottom: 3px solid {brand_orange};
        padding-bottom: 10px;
        margin-bottom: 25px;
    }}

    /* 사이드바 WPS 설정창 높이 유지 */
    section[data-testid="stSidebar"] .stNumberInput input {{
        height: 120px !important;
        font-size: 35px !important;
        font-weight: 900 !important;
        color: {brand_orange} !important;
    }}
    section[data-testid="stSidebar"] .stNumberInput label p {{
        font-size: 20px !important;
        font-weight: bold !important;
    }}

    /* Step 1. 프로세스 선택 버튼: 높이 70% 축소 및 폭 동일 */
    div[role="radiogroup"] {{
        display: flex !important;
        flex-direction: row !important;
        justify-content: space-between !important;
        width: 100% !important;
        gap: 12px !important;
    }}
    
    div[role="radiogroup"] label {{
        background-color: white !important;
        border: 2px solid {brand_brown} !important;
        padding: 35px 15px !important; /* 기존 50px에서 70% 수준인 35px로 축소 */
        border-radius: 12px !important;
        flex: 1 !important;
        text-align: center !important;
        white-space: nowrap !important;
        transition: all 0.2s ease;
        cursor: pointer;
        min-height: 110px !important; /* 높이 고정으로 결과창과 동기화 */
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }}

    /* 프로세스별 파스텔톤 배경 */
    div[role="radiogroup"] label:nth-child(1) {{ background-color: #E8F5E9 !important; }} 
    div[role="radiogroup"] label:nth-child(2) {{ background-color: #E1F5FE !important; }} 
    div[role="radiogroup"] label:nth-child(3) {{ background-color: #F3E5F5 !important; }} 
    div[role="radiogroup"] label:nth-child(4) {{ background-color: #FFF3E0 !important; }} 

    div[role="radiogroup"] label[data-checked="true"] {{
        background-color: {brand_brown} !important;
        border-color: {brand_orange} !important;
    }}
    
    div[role="radiogroup"] label[data-checked="true"] p {{
        color: white !important;
        font-size: 26px !important;
        font-weight: 900 !important;
    }}
    
    div[role="radiogroup"] label p {{
        color: {brand_brown} !important;
        font-size: 24px !important;
        font-weight: 800;
        margin: 0 !important;
    }}

    /* 숫자 입력창 스타일 */
    input[type="number"] {{
        font-size: 24px !important;
        height: 65px !important;
        font-weight: bold !important;
        border: 2px solid {brand_brown} !important;
    }}

    /* Step 3. 라이브 결과 카드: 프로세스 버튼과 높이 동일하게 조정 */
    .result-card {{
        background-color: {brand_brown};
        color: white;
        padding: 15px 25px !important;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
        display: flex;
        flex-direction: row; /* 가로 배열로 변경하여 높이 축소 대응 */
        align-items: center;
        justify-content: space-around;
        height: 110px !important; /* 프로세스 버튼 높이(min-height)와 동일하게 설정 */
    }}
    
    .result-value {{
        color: {brand_orange};
        font-size: 3rem; 
        font-weight: 900;
        margin: 0 15px;
    }}

    /* 로그 저장 버튼 */
    div.stButton > button {{
        height: 50px !important;
        background-color: {brand_orange} !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 10px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. 데이터 관리 ---
if 'history' not in st.session_state:
    st.session_state.history = []

# --- 3. 사이드바 (WPS 설정) ---
with st.sidebar:
    st.markdown(f"<h2 style='color:{brand_orange};'>⚙️ WPS STANDARDS</h2>", unsafe_allow_html=True)
    wps_min = st.number_input("Min Limit (kJ/mm)", value=1.0, step=0.1)
    wps_max = st.number_input("Max Limit (kJ/mm)", value=2.5, step=0.1)

# --- 4. 메인 UI 구성 ---
st.markdown(f"<h1><span style='color:{brand_orange};'>⚡</span> Welding Heat Master Pro</h1>", unsafe_allow_html=True)

# 레이아웃 구성
col_left, col_right = st.columns([1.6, 1])

with col_left:
    # Step 1. 프로세스 선택
    st.markdown("### 🛠️ Step 1. Select Process")
    process_name = st.radio("Proc", options=['SAW', 'FCAW', 'SMAW', 'GMAW'], horizontal=True, label_visibility="collapsed")
    k_map = {'SAW': 1.0, 'FCAW': 0.8, 'SMAW': 0.8, 'GMAW': 0.8}
    k = k_map[process_name]

with col_right:
    # Step 3. 라이브 결과 (버튼과 동일한 높이로 배치)
    st.markdown("### 🎯 Step 3. Live Result")
    # 계산 로직 (미리 수행)
    # 임시 기본값 설정을 위한 placeholder
    hi_placeholder = st.empty()

# 하단 파라미터 입력부
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"### ⌨️ Step 2. Input Parameters (Factor k={k})", unsafe_allow_html=True)
p_col1, p_col2, p_col3 = st.columns([1, 1, 0.6])

with p_col1:
    v = st.number_input("Voltage (V)", value=28.0, step=0.5)
    a = st.number_input("Amperage (A)", value=220.0, step=5.0)
with p_col2:
    l_mm = st.number_input("Length (mm)", value=150.0, step=10.0)
    t_sec = st.number_input("Time (Sec)", value=120.0, step=1.0)

# 실시간 계산
hi = (k * v * a * t_sec) / (l_mm * 1000)
is_pass = wps_min <= hi <= wps_max
status = "PASS" if is_pass else "FAIL"
status_color = brand_orange if is_pass else "#FF4B4B"

# 결과 카드 업데이트 (Step 3 위치에 렌더링)
with col_right:
    st.markdown(f"""
        <div class="result-card">
            <div style="text-align:left;">
                <p style="margin:0; opacity:0.7; font-size:0.9rem;">Heat Input</p>
                <div class="result-value">{hi:.3f} <span style="font-size:1rem; color:white;">kJ/mm</span></div>
            </div>
            <h1 style="color:{status_color}; margin:0; font-size:2.8rem; font-weight:800;">{status}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    if st.button("💾 SAVE LOG DATA", use_container_width=True):
        st.session_state.history.insert(0, {"Time": datetime.now().strftime("%H:%M:%S"), "Proc": process_name, "V/A": f"{v}/{a}", "HI": f"{hi:.3f}", "Status": status})
        st.session_state.history = st.session_state.history[:50]
        st.toast(f"Data Logged!")

# --- 5. 히스토리 ---
st.markdown("<br><hr>", unsafe_allow_html=True)
if st.session_state.history:
    st.subheader("🕒 Recent Logs (Last 50)")
    st.table(pd.DataFrame(st.session_state.history))