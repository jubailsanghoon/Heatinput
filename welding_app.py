import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 페이지 설정 및 디자인 테마 ---
st.set_page_config(page_title="Welding Heat Master Pro", layout="wide")

brand_cream = "#FCF8F2"
brand_brown = "#4A3728"
brand_orange = "#FF6B00"
brand_green = "#28A745"  # PASS용 그린 컬러 추가

# CSS 주입: 상단 여백 축소 및 모바일 대응 반응형 CSS
st.markdown(f"""
    <style>
    /* 전체 상부 여백 50% 축소 (기본 6rem -> 2rem) */
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
        padding-bottom: 5px;
        margin-bottom: 15px;
        font-size: 2rem !important;
    }}

    /* 사이드바 스타일링 */
    section[data-testid="stSidebar"] .stNumberInput input {{
        height: 80px !important;
        font-size: 28px !important;
        font-weight: 900 !important;
    }}

    /* 프로세스 버튼: PC/모바일 가변 레이아웃 */
    div[data-testid="stHorizontalBlock"] div[role="radiogroup"] {{
        display: flex !important;
        width: 100% !important;
        gap: 8px !important;
    }}
    
    div[data-testid="stHorizontalBlock"] div[role="radiogroup"] label {{
        background-color: white !important;
        border: 2px solid {brand_brown} !important;
        padding: 25px 5px !important;
        border-radius: 12px !important;
        flex: 1 1 0% !important; 
        min-width: 0 !important;
        min-height: 100px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.2s ease;
    }}
    
    div[role="radiogroup"] label p {{
        font-size: 18px !important;
        font-weight: 800;
        white-space: nowrap !important;
    }}

    div[role="radiogroup"] label[data-checked="true"] {{
        background-color: {brand_brown} !important;
        border-color: {brand_orange} !important;
    }}
    
    div[role="radiogroup"] label[data-checked="true"] p {{
        color: white !important;
    }}

    /* 라이브 결과 카드 */
    .result-card {{
        background-color: {brand_brown};
        color: white;
        padding: 15px;
        border-radius: 15px;
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-around;
        height: 100px !important;
        margin-top: 10px;
    }}
    
    .result-value {{
        color: {brand_orange};
        font-size: 2.5rem; 
        font-weight: 900;
    }}

    /* 모바일 전용 미디어 쿼리 (@media) */
    @media (max-width: 768px) {{
        /* 모바일에서는 버튼 높이를 조금 줄여 화면 확보 */
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
        /* 모바일에서 컬럼이 수직으로 쌓일 때 여백 조절 */
        [data-testid="column"] {{
            margin-bottom: 15px;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. 데이터 관리 ---
if 'history' not in st.session_state:
    st.session_state.history = []

# --- 3. 사이드바 (규격 선택 + WPS 설정) ---
with st.sidebar:
    st.markdown(f"<h2 style='color:{brand_orange};'>📜 SELECT STANDARD</h2>", unsafe_allow_html=True)
    selected_std = st.radio("Standard Mode", options=['ISO (Heat Input)', 'AWS (Arc Energy)'], label_visibility="collapsed")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='color:{brand_orange};'>⚙️ WPS STANDARDS</h2>", unsafe_allow_html=True)
    wps_min = st.number_input("Min (kJ/mm)", value=1.0, step=0.1)
    wps_max = st.number_input("Max (kJ/mm)", value=2.5, step=0.1)

# --- 4. 메인 UI 구성 ---
st.markdown(f"<h1><span style='color:{brand_orange};'>⚡</span> Welding Heat Master Pro</h1>", unsafe_allow_html=True)

# 레이아웃: PC에서는 2열, 모바일에서는 자동으로 1열 전환됨
col_left, col_right = st.columns([1.6, 1])

with col_left:
    st.markdown("### 🛠️ Step 1. Select Process")
    process_name = st.radio("Proc", options=['SAW', 'FCAW', 'SMAW', 'GMAW'], horizontal=True, label_visibility="collapsed")
    
    # 규격 효율 계수(k) 로직
    if 'ISO' in selected_std:
        k_map = {'SAW': 1.0, 'FCAW': 0.8, 'SMAW': 0.8, 'GMAW': 0.8}
        k = k_map[process_name]
        label_text = "Heat Input (ISO)"
    else:
        k = 1.0 
        label_text = "Arc Energy (AWS)"

# 파라미터 입력부
st.markdown(f"### ⌨️ Step 2. Input Parameters (k={k})")
p_col1, p_col2 = st.columns(2)
with p_col1:
    v = st.number_input("Voltage (V)", value=28.0, step=0.5)
    a = st.number_input("Amperage (A)", value=220.0, step=5.0)
with p_col2:
    l_mm = st.number_input("Length (mm)", value=150.0, step=10.0)
    t_sec = st.number_input("Time (Sec)", value=120.0, step=1.0)

# 계산 공식
hi = (k * v * a * t_sec) / (l_mm * 1000)
is_pass = wps_min <= hi <= wps_max
status = "PASS" if is_pass else "FAIL"

# [핵심 요청 반영] PASS 시 그린 컬러 적용
status_color = brand_green if is_pass else "#FF4B4B"

# 결과창 렌더링
with col_right:
    st.markdown("### 🎯 Step 3. Live Result")
    st.markdown(f"""
        <div class="result-card">
            <div style="text-align:left;">
                <p style="margin:0; opacity:0.7; font-size:0.9rem;">{label_text}</p>
                <div class="result-value">{hi:.3f} <span style="font-size:1rem; color:white;">kJ/mm</span></div>
            </div>
            <h1 style="color:{status_color}; margin:0; font-size:2.8rem; font-weight:900;">{status}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    if st.button("💾 SAVE LOG DATA", use_container_width=True):
        st.session_state.history.insert(0, {
            "Time": datetime.now().strftime("%H:%M:%S"),
            "Std": "ISO" if "ISO" in selected_std else "AWS",
            "Proc": process_name,
            "HI": f"{hi:.3f}",
            "Status": status
        })
        st.toast("Saved!")

# --- 5. 히스토리 ---
st.markdown("<br><hr>", unsafe_allow_html=True)
if st.session_state.history:
    st.subheader("🕒 Recent Logs")
    st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True)