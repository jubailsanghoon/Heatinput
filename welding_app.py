import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 페이지 설정 및 디자인 테마 ---
st.set_page_config(page_title="Welding Heat Master Pro", layout="wide")

brand_cream = "#FCF8F2"
brand_brown = "#4A3728"
brand_orange = "#FF6B00"
brand_green = "#28A745"

# 세션 상태 초기화 (슬라이드 단계 관리)
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'selected_std' not in st.session_state:
    st.session_state.selected_std = "ISO (Heat Input)"

# CSS 주입: 모바일 고대비 보색 및 슬라이드 UI 튜닝
st.markdown(f"""
    <style>
    .block-container {{
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
    }}
    .stApp {{
        background-color: {brand_cream};
        color: {brand_brown};
    }}
    
    /* 큰 타이틀 */
    h1 {{
        color: {brand_brown};
        font-weight: 900;
        border-bottom: 4px solid {brand_orange};
        padding-bottom: 5px;
        margin-bottom: 20px;
        font-size: 1.8rem !important;
    }}

    /* [보색 시공] 모든 숫자 입력창 (WPS 및 파라미터) */
    div.stNumberInput input {{
        background-color: {brand_brown} !important;
        color: {brand_orange} !important;
        height: 80px !important;
        font-size: 32px !important;
        font-weight: 900 !important;
        border: 3px solid {brand_orange} !important;
        border-radius: 12px !important;
    }}
    
    div.stNumberInput label p {{
        font-size: 20px !important;
        font-weight: 900 !important;
        color: {brand_brown} !important;
    }}

    /* [공정 버튼] 파스텔 배경 및 선택 시 보색 반전 */
    div[data-testid="stHorizontalBlock"] div[role="radiogroup"] label {{
        border: 3px solid {brand_brown} !important;
        padding: 25px 5px !important;
        border-radius: 12px !important;
        min-height: 90px !important;
    }}
    
    /* 미선택 시 파스텔톤 */
    div[role="radiogroup"] label:nth-child(1) {{ background-color: #E8F5E9 !important; }} 
    div[role="radiogroup"] label:nth-child(2) {{ background-color: #E1F5FE !important; }} 
    div[role="radiogroup"] label:nth-child(3) {{ background-color: #F3E5F5 !important; }} 
    div[role="radiogroup"] label:nth-child(4) {{ background-color: #FFF3E0 !important; }} 

    div[role="radiogroup"] label p {{
        color: {brand_brown} !important;
        font-size: 18px !important;
        font-weight: 900 !important;
    }}

    /* 선택 시 보색 반전 */
    div[role="radiogroup"] label[data-checked="true"] {{
        background-color: {brand_brown} !important;
    }}
    div[role="radiogroup"] label[data-checked="true"] p {{
        color: {brand_orange} !important;
        font-size: 20px !important;
    }}

    /* 결과 카드 */
    .result-card {{
        background-color: {brand_brown};
        color: white;
        padding: 20px;
        border-radius: 15px;
        border: 4px solid {brand_orange};
    }}
    .result-value {{
        color: {brand_orange} !important;
        font-size: 3rem; 
        font-weight: 900;
    }}

    /* 다음/이전 버튼 커스텀 */
    div.stButton > button {{
        width: 100%;
        height: 60px !important;
        background-color: {brand_orange} !important;
        color: white !important;
        font-size: 20px !important;
        font-weight: 900 !important;
        border-radius: 12px !important;
        border: none !important;
    }}

    @media (max-width: 768px) {{
        h1 {{ font-size: 1.5rem !important; }}
        div.stNumberInput input {{ font-size: 28px !important; height: 70px !important; }}
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. 사이드바 (브랜딩 고정) ---
with st.sidebar:
    st.markdown(f"<h2 style='color:{brand_orange};'>⚙️ SETTINGS</h2>", unsafe_allow_html=True)
    wps_min = st.number_input("WPS Min", value=1.0, step=0.1)
    wps_max = st.number_input("WPS Max", value=2.5, step=0.1)
    st.markdown("<br><hr>", unsafe_allow_html=True)
    try:
        st.image("image_d9f201.jpg", width=80) 
    except:
        st.markdown("<h1 style='margin:0;'>✔️</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 14px; font-weight: 900; color: {brand_brown};'>jubail.sanghoon@gmail.com</p>", unsafe_allow_html=True)

# --- 3. 메인 로직 (슬라이드 위저드) ---
st.markdown(f"<h1><span style='color:{brand_orange};'>⚡</span> Heat Master Pro</h1>", unsafe_allow_html=True)

# STEP 1: 규격 선택 슬라이드
if st.session_state.step == 1:
    st.markdown("### 📜 STEP 1. SELECT STANDARD")
    st.write("작업 규격을 선택해 주세요.")
    
    # 규격 선택을 큼직한 버튼처럼 배치
    std_choice = st.radio(
        "Standard", 
        options=['ISO (Heat Input)', 'AWS (Arc Energy)'], 
        label_visibility="collapsed"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("NEXT (계산기 시작) ➔"):
        st.session_state.selected_std = std_choice
        st.session_state.step = 2
        st.rerun()

# STEP 2: 계산기 슬라이드
else:
    if st.button("⬅ BACK (규격 재선택)"):
        st.session_state.step = 1
        st.rerun()
        
    st.markdown(f"### 🎯 MODE: {st.session_state.selected_std}")
    
    col_left, col_right = st.columns([1.6, 1])
    
    with col_left:
        st.markdown("#### 🛠️ 1. Process")
        process_name = st.radio("Proc", options=['SAW', 'FCAW', 'SMAW', 'GMAW'], horizontal=True, label_visibility="collapsed")
        
        k = (1.0 if 'AWS' in st.session_state.selected_std or process_name == 'SAW' else 0.8)
        
        st.markdown("#### ⌨️ 2. Parameters")
        p_col1, p_col2 = st.columns(2)
        with p_col1:
            v = st.number_input("Voltage (V)", value=28.0, step=0.5)
            a = st.number_input("Amperage (A)", value=220.0, step=5.0)
        with p_col2:
            l_mm = st.number_input("Length (mm)", value=150.0, step=10.0)
            t_sec = st.number_input("Time (Sec)", value=120.0, step=1.0)

    # 계산 결과
    hi = (k * v * a * t_sec) / (l_mm * 1000)
    is_pass = wps_min <= hi <= wps_max
    status = "PASS" if is_pass else "FAIL"
    status_color = brand_green if is_pass else "#FF4B4B"

    with col_right:
        st.markdown("#### 🎯 3. Result")
        st.markdown(f"""
            <div class="result-card">
                <p style="margin:0; opacity:0.8; font-size:1.1rem;">{st.session_state.selected_std[:10]}...</p>
                <div class="result-value">{hi:.3f} <span style="font-size:1.2rem; color:white;">kJ/mm</span></div>
                <h1 style="color:{status_color}; margin:0; font-size:3.5rem; font-weight:900; text-align:center;">{status}</h1>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💾 SAVE LOG"):
            if 'history' not in st.session_state: st.session_state.history = []
            st.session_state.history.insert(0, {"Time": datetime.now().strftime("%H:%M:%S"), "HI": f"{hi:.3f}", "Status": status})
            st.toast("Data Logged!")

    # 히스토리
    if 'history' in st.session_state and st.session_state.history:
        with st.expander("🕒 Recent Logs"):
            st.table(pd.DataFrame(st.session_state.history))