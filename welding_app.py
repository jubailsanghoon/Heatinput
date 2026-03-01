import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- 1. 페이지 설정 및 디자인 테마 ---
st.set_page_config(page_title="Welding Heat Master Pro", layout="wide")

brand_cream = "#FCF8F2"
brand_brown = "#4A3728"
brand_orange = "#FF6B00"
brand_green = "#28A745"

# CSS 주입: 레이아웃 및 반응형 디자인
st.markdown(f"""
    <style>
    /* 상부 여백 축소 */
    .block-container {{
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }}
    
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

    /* 사이드바 스타일링 */
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {{
        gap: 10px !important;
    }}
    
    section[data-testid="stSidebar"] .stRadio label {{
        background-color: white !important;
        border: 2px solid {brand_brown} !important;
        padding: 15px !important;
        border-radius: 10px !important;
    }}

    section[data-testid="stSidebar"] .stNumberInput input {{
        height: 80px !important;
        font-size: 28px !important;
        font-weight: 900 !important;
        color: {brand_orange} !important;
    }}

    /* 메인 프로세스 버튼: 균등 배분 및 한 줄 유지 */
    div[data-testid="stHorizontalBlock"] div[role="radiogroup"] {{
        display: flex !important;
        width: 100% !important;
        gap: 12px !important;
    }}
    
    div[data-testid="stHorizontalBlock"] div[role="radiogroup"] label {{
        background-color: white !important;
        border: 2px solid {brand_brown} !important;
        padding: 35px 10px !important;
        border-radius: 12px !important;
        flex: 1 1 0% !important; 
        min-height: 120px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }}
    
    div[role="radiogroup"] label p {{
        color: {brand_brown} !important;
        font-size: 22px !important;
        font-weight: 800;
        margin: 0 !important;
        white-space: nowrap !important;
    }}

    div[role="radiogroup"] label[data-checked="true"] {{
        background-color: {brand_brown} !important;
        border-color: {brand_orange} !important;
    }}
    
    div[role="radiogroup"] label[data-checked="true"] p {{
        color: white !important;
    }}

    /* 프로세스별 파스텔 배경 */
    div[role="radiogroup"] label:nth-child(1) {{ background-color: #E8F5E9 !important; }} 
    div[role="radiogroup"] label:nth-child(2) {{ background-color: #E1F5FE !important; }} 
    div[role="radiogroup"] label:nth-child(3) {{ background-color: #F3E5F5 !important; }} 
    div[role="radiogroup"] label:nth-child(4) {{ background-color: #FFF3E0 !important; }} 

    /* 숫자 입력창 */
    input[type="number"] {{
        font-size: 24px !important;
        height: 65px !important;
        font-weight: bold !important;
        border: 2px solid {brand_brown} !important;
    }}

    /* 라이브 결과 카드 */
    .result-card {{
        background-color: {brand_brown};
        color: white;
        padding: 15px 25px;
        border-radius: 15px;
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-around;
        height: 120px !important;
    }}
    
    .result-value {{
        color: {brand_orange} !important;
        font-size: 2.8rem; 
        font-weight: 900;
    }}

    /* 모바일 대응 미디어 쿼리 */
    @media (max-width: 768px) {{
        div[data-testid="stHorizontalBlock"] div[role="radiogroup"] label {{
            padding: 15px 2px !important;
            min-height: 80px !important;
        }}
        div[role="radiogroup"] label p {{
            font-size: 14px !important;
        }}
        .result-value {{
            font-size: 1.8rem !important;
        }}
        h1 {{
            font-size: 1.5rem !important;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. 데이터 관리 ---
if 'history' not in st.session_state:
    st.session_state.history = []

# --- 3. 사이드바 (설정 + 로고 + 이메일) ---
with st.sidebar:
    st.markdown(f"<h2 style='color:{brand_orange};'>📜 SELECT STANDARD</h2>", unsafe_allow_html=True)
    selected_std = st.radio("Standard", options=['ISO (Heat Input)', 'AWS (Arc Energy)'], label_visibility="collapsed")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='color:{brand_orange};'>⚙️ WPS STANDARDS</h2>", unsafe_allow_html=True)
    wps_min = st.number_input("Min Limit (kJ/mm)", value=1.0, step=0.1)
    wps_max = st.number_input("Max Limit (kJ/mm)", value=2.5, step=0.1)

    # [로고 및 이메일 삽입 위치]
    st.markdown("<br><hr>", unsafe_allow_html=True)
    
    # 로고 파일이 스크립트와 같은 폴더에 있어야 합니다.
    try:
        st.image("image_d9f201.jpg", width=80) 
    except:
        st.write("✔️")
    
    st.markdown(f"<p style='font-size: 13px; font-weight: bold; color: {brand_brown}; margin-top: -10px;'>jubail.sanghoon@gmail.com</p>", unsafe_allow_html=True)

# --- 4. 메인 UI 구성 ---
st.markdown(f"<h1><span style='color:{brand_orange};'>⚡</span> Welding Heat Master Pro</h1>", unsafe_allow_html=True)

col_left, col_right = st.columns([1.6, 1])

with col_left:
    st.markdown("### 🛠️ Step 1. Select Process")
    process_name = st.radio("Proc", options=['SAW', 'FCAW', 'SMAW', 'GMAW'], horizontal=True, label_visibility="collapsed")
    
    if 'ISO' in selected_std:
        k_map = {'SAW': 1.0, 'FCAW': 0.8, 'SMAW': 0.8, 'GMAW': 0.8}
        k = k_map[process_name]
        label_text = "Heat Input (ISO)"
    else:
        k = 1.0 
        label_text = "Arc Energy (AWS)"

with col_right:
    st.markdown(f"### 🎯 Step 3. {label_text}")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"### ⌨️ Step 2. Input Parameters (k={k})", unsafe_allow_html=True)
p_col1, p_col2 = st.columns(2)

with p_col1:
    v = st.number_input("Voltage (V)", value=28.0, step=0.5)
    a = st.number_input("Amperage (A)", value=220.0, step=5.0)
with p_col2:
    l_mm = st.number_input("Length (mm)", value=150.0, step=10.0)
    t_sec = st.number_input("Time (Sec)", value=120.0, step=1.0)

# 계산
hi = (k * v * a * t_sec) / (l_mm * 1000)
is_pass = wps_min <= hi <= wps_max
status = "PASS" if is_pass else "FAIL"
status_color = brand_green if is_pass else "#FF4B4B"

with col_right:
    st.markdown(f"""
        <div class="result-card">
            <div style="text-align:left;">
                <p style="margin:0; opacity:0.7; font-size:0.9rem;">{label_text}</p>
                <div class="result-value">{hi:.3f} <span style="font-size:1rem; color:white;">kJ/mm</span></div>
            </div>
            <h1 style="color:{status_color}; margin:0; font-size:2.8rem; font-weight:800;">{status}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    if st.button("💾 SAVE LOG DATA", use_container_width=True):
        st.session_state.history.insert(0, {
            "Time": datetime.now().strftime("%H:%M:%S"),
            "Std": "ISO" if "ISO" in selected_std else "AWS",
            "Proc": process_name,
            "HI (kJ/mm)": f"{hi:.3f}",
            "Status": status
        })
        st.toast("Success: Data Logged")

# --- 5. 히스토리 ---
st.markdown("<br><hr>", unsafe_allow_html=True)
if st.session_state.history:
    st.subheader("🕒 Recent Logs")
    st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True)