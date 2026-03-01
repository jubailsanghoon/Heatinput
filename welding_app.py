import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 페이지 설정 및 디자인 테마 ---
st.set_page_config(page_title="Welding Heat Master Pro", layout="wide")

brand_cream = "#FCF8F2"
brand_brown = "#4A3728"
brand_orange = "#FF6B00"
brand_green = "#28A745"

# CSS 주입: 모바일 고대비 보색 시공 및 반응형 레이아웃
st.markdown(f"""
    <style>
    /* 상부 여백 축소 및 배경색 */
    .block-container {{
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
    }}
    .stApp {{
        background-color: {brand_cream};
        color: {brand_brown};
    }}
    
    h1 {{
        color: {brand_brown};
        font-weight: 900;
        border-bottom: 4px solid {brand_orange};
        padding-bottom: 10px;
        margin-bottom: 20px;
    }}

    /* [보색 시공 1] 사이드바 WPS 입력창 */
    section[data-testid="stSidebar"] .stNumberInput input {{
        background-color: {brand_brown} !important;
        color: {brand_orange} !important;
        height: 80px !important;
        font-size: 32px !important;
        font-weight: 900 !important;
        border: 3px solid {brand_orange} !important;
    }}

    /* [보색 시공 2] 메인 Step 2 모든 숫자 입력창 */
    div.stNumberInput input {{
        background-color: {brand_brown} !important;
        color: {brand_orange} !important;
        height: 85px !important;
        font-size: 36px !important;
        font-weight: 900 !important;
        border: 4px solid {brand_brown} !important;
        border-radius: 12px !important;
    }}
    
    div.stNumberInput label p {{
        font-size: 22px !important;
        font-weight: 900 !important;
        color: {brand_brown} !important;
    }}

    /* [공정 버튼] 파스텔 배경 및 고대비 텍스트 */
    div[data-testid="stHorizontalBlock"] div[role="radiogroup"] label {{
        border: 3px solid {brand_brown} !important;
        padding: 30px 5px !important;
        border-radius: 12px !important;
        min-height: 100px !important;
    }}
    
    div[role="radiogroup"] label:nth-child(1) {{ background-color: #E8F5E9 !important; }} 
    div[role="radiogroup"] label:nth-child(2) {{ background-color: #E1F5FE !important; }} 
    div[role="radiogroup"] label:nth-child(3) {{ background-color: #F3E5F5 !important; }} 
    div[role="radiogroup"] label:nth-child(4) {{ background-color: #FFF3E0 !important; }} 

    div[role="radiogroup"] label p {{
        color: {brand_brown} !important;
        font-size: 20px !important;
        font-weight: 900 !important;
        white-space: nowrap !important;
    }}

    /* 선택된 버튼 보색 반전 */
    div[role="radiogroup"] label[data-checked="true"] {{
        background-color: {brand_brown} !important;
    }}
    
    div[role="radiogroup"] label[data-checked="true"] p {{
        color: {brand_orange} !important;
        font-size: 22px !important;
    }}

    /* 결과 카드 및 PASS/FAIL */
    .result-card {{
        background-color: {brand_brown};
        color: white;
        padding: 20px;
        border-radius: 15px;
        border: 4px solid {brand_orange};
        height: 130px !important;
    }}
    
    .result-value {{
        color: {brand_orange} !important;
        font-size: 3.2rem; 
        font-weight: 900;
    }}

    /* 모바일 미디어 쿼리 */
    @media (max-width: 768px) {{
        div.stNumberInput input {{
            height: 75px !important;
            font-size: 30px !important;
        }}
        .result-value {{ font-size: 2.4rem !important; }}
        h1 {{ font-size: 1.6rem !important; }}
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. 데이터 관리 ---
if 'history' not in st.session_state:
    st.session_state.history = []

# --- 3. 사이드바 (WPS 설정 및 브랜딩) ---
with st.sidebar:
    st.markdown(f"<h2 style='color:{brand_orange};'>📜 STANDARD</h2>", unsafe_allow_html=True)
    selected_std = st.radio("Std", options=['ISO (Heat Input)', 'AWS (Arc Energy)'], label_visibility="collapsed")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='color:{brand_orange};'>⚙️ WPS LIMITS</h2>", unsafe_allow_html=True)
    wps_min = st.number_input("Min", value=1.0, step=0.1)
    wps_max = st.number_input("Max", value=2.5, step=0.1)

    st.markdown("<br><hr>", unsafe_allow_html=True)
    try:
        st.image("image_d9f201.jpg", width=80) 
    except:
        st.markdown("<h1 style='margin:0;'>✔️</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 14px; font-weight: 900; color: {brand_brown};'>jubail.sanghoon@gmail.com</p>", unsafe_allow_html=True)

# --- 4. 메인 UI 구성 ---
st.markdown(f"<h1><span style='color:{brand_orange};'>⚡</span> Welding Heat Master Pro</h1>", unsafe_allow_html=True)

col_left, col_right = st.columns([1.6, 1])

with col_left:
    st.markdown("### 🛠️ Step 1. Select Process")
    process_name = st.radio("Proc", options=['SAW', 'FCAW', 'SMAW', 'GMAW'], horizontal=True, label_visibility="collapsed")
    
    k = (1.0 if 'AWS' in selected_std or process_name == 'SAW' else 0.8)
    label_text = "Heat Input (ISO)" if 'ISO' in selected_std else "Arc Energy (AWS)"

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"### ⌨️ Step 2. Input Parameters (k={k})")
p_col1, p_col2 = st.columns(2)

with p_col1:
    v = st.number_input("Voltage (V)", value=28.0, step=0.5)
    a = st.number_input("Amperage (A)", value=220.0, step=5.0)
with p_col2:
    l_mm = st.number_input("Length (mm)", value=150.0, step=10.0)
    t_sec