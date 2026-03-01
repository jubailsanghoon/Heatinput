import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 페이지 설정 및 디자인 테마 ---
# Layout and Brand Colors
st.set_page_config(page_title="Welding Heat Master Pro", layout="wide")

brand_cream = "#FCF8F2"
brand_brown = "#4A3728"
brand_orange = "#FF6B00"
brand_green = "#28A745"

# CSS 주입: 모바일 고대비 시인성 및 보색 대비 강화
st.markdown(f"""
    <style>
    /* 상부 여백 축소 */
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
        font-size: 2rem !important;
    }}

    /* [핵심 수정] 프로세스 선택 버튼 가독성 강화 */
    div[data-testid="stHorizontalBlock"] div[role="radiogroup"] {{
        display: flex !important;
        width: 100% !important;
        gap: 10px !important;
    }}
    
    div[data-testid="stHorizontalBlock"] div[role="radiogroup"] label {{
        border: 3px solid {brand_brown} !important; /* 테두리 두껍게 */
        padding: 30px 5px !important;
        border-radius: 12px !important;
        flex: 1 1 0% !important; 
        min-height: 100px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.2s ease;
    }}

    /* 미선택 시: 파스텔 배경 + 진한 브라운 글자 (보색 대비) */
    div[role="radiogroup"] label p {{
        color: {brand_brown} !important; /* 미선택 시 글자색 */
        font-size: 20px !important;
        font-weight: 900 !important; /* 더 두껍게 */
        white-space: nowrap !important;
        text-align: center !important;
    }}

    /* [복구] 각 프로세스별 파스텔톤 배경색 */
    div[role="radiogroup"] label:nth-child(1) {{ background-color: #E8F5E9 !important; }} 
    div[role="radiogroup"] label:nth-child(2) {{ background-color: #E1F5FE !important; }} 
    div[role="radiogroup"] label:nth-child(3) {{ background-color: #F3E5F5 !important; }} 
    div[role="radiogroup"] label:nth-child(4) {{ background-color: #FFF3E0 !important; }} 

    /* 선택 시: 진한 브라운 배경 + 선명한 주황색 글자 (최강 보색 대비) */
    div[role="radiogroup"] label[data-checked="true"] {{
        background-color: {brand_brown} !important;
        border-color: {brand_orange} !important;
    }}
    
    div[role="radiogroup"] label[data-checked="true"] p {{
        color: {brand_orange} !important; /* 흰색 대신 보색인 주황색 적용 */
        font-size: 22px !important;
        text-shadow: 1px 1px 0px rgba(0,0,0,0.5); /* 입체감 추가 */
    }}

    /* 입력창 숫자 시인성 (전류/전압 등) */
    div.stNumberInput input {{
        height: 80px !important;
        font-size: 34px !important;
        font-weight: 900 !important;
        color: {brand_brown} !important;
        border: 4px solid {brand_brown} !important;
    }}
    
    div.stNumberInput label p {{
        font-size: 22px !important;
        font-weight: 900 !important;
        color: {brand_brown} !important;
    }}

    /* 라이브 결과 카드 */
    .result-card {{
        background-color: {brand_brown};
        color: white;
        padding: 15px 20px;
        border-radius: 15px;
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-around;
        height: 110px !important;
        border: 3px solid {brand_orange};
    }}
    
    .result-value {{
        color: {brand_orange} !important;
        font-size: 3rem; 
        font-weight: 900;
    }}

    /* 모바일 미디어 쿼리 정밀 최적화 */
    @media (max-width: 768px) {{
        div.stNumberInput input {{
            height: 70px !important;
            font-size: 30px !important;
        }}
        div.stNumberInput label p {{
            font-size: 20px !important;
        }}
        div[data-testid="stHorizontalBlock"] div[role="radiogroup"] label {{
            min-height: 80px !important;
            padding: 15px 2px !important;
            border-width: 2px !important;
        }}
        div[role="radiogroup"] label p {{ font-size: 16px !important; }}
        div[role="radiogroup"] label[data-checked="true"] p {{ font-size: 17px !important; }}
        .result-value {{ font-size: 2.2rem !important; }}
        h1 {{ font-size: 1.6rem !important; }}
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. 데이터 관리 ---
if 'history' not in st.session_state:
    st.session_state.history = []

# --- 3. 사이드바 (설정 + 브랜딩) ---
with st.sidebar:
    st.markdown(f"<h2 style='color:{brand_orange};'>📜 SELECT STANDARD</h2>", unsafe_allow_html=True)
    selected_std = st.radio("Standard Selection", options=['ISO (Heat Input)', 'AWS (Arc Energy)'], label_visibility="collapsed")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='color:{brand_orange};'>⚙️ WPS STANDARDS</h2>", unsafe_allow_html=True)
    wps_min = st.number_input("Min (kJ/mm)", value=1.0, step=0.1)
    wps_max = st.number_input("Max (kJ/mm)", value=2.5, step=0.1)

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
    
    if 'ISO' in selected_std:
        k_map = {'SAW': 1.0, 'FCAW': 0.8, 'SMAW': 0.8, 'GMAW': 0.8}
        k = k_map[process_name]
        label_text = "Heat Input (ISO)"
    else:
        k = 1.0 
        label_text = "Arc Energy (AWS)"

# 파라미터 입력
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"### ⌨️ Step 2. Input Parameters (k={k})")
p_col1, p_col2 = st.columns(2)

with p_col1:
    v = st.number_input("Voltage (V)", value=28.0, step=0.5)
    a = st.number_input("Amperage (A)", value=220.0, step=5.0)
with p_col2:
    l_mm = st.number_input("Length (mm)", value=150.0, step=10.0)
    t_sec = st.number_input("Time (Sec)", value=120.0, step=1.0)

# 계산 로직
hi = (k * v * a * t_sec) / (l_mm * 1000)
is_pass = wps_min <= hi <= wps_max
status = "PASS" if is_pass else "FAIL"
status_color = brand_green if is_pass else "#FF4B4B"

# 결과창 렌더링
with col_right:
    st.markdown(f"### 🎯 Step 3. {label_text}")
    st.markdown(f"""
        <div class="result-card">
            <div style="text-align:left;">
                <p style="margin:0; opacity:0.8; font-size:1rem;">{label_text}</p>
                <div class="result-value">{hi:.3f} <span style="font-size:1.2rem; color:white;">kJ/mm</span></div>
            </div>
            <h1 style="color:{status_color}; margin:0; font-size:3rem; font-weight:900;">{status}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("💾 SAVE LOG DATA", use_container_width=True):
        st.session_state.history.insert(0, {
            "Time": datetime.now().strftime("%H:%M:%S"),
            "Std": "ISO" if "ISO" in selected_std else "AWS",
            "Proc": process_name,
            "HI (kJ/mm)": f"{hi:.3f}",
            "Status": status
        })
        st.toast("Data Logged Successfully")

# 히스토리
st.markdown("<br><hr>", unsafe_allow_html=True)
if st.session_state.history:
    st.subheader("🕒 Recent Logs")
    st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True)