import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 페이지 설정 및 디자인 테마 ---
# Setup for layout and branding
st.set_page_config(page_title="Welding Heat Master Pro", layout="wide")

brand_cream = "#FCF8F2"
brand_brown = "#4A3728"
brand_orange = "#FF6B00"
brand_green = "#28A745"

# 세션 상태 초기화 (모바일 단계 및 모드 관리)
if 'step' not in st.session_state: st.session_state.step = 1
if 'history' not in st.session_state: st.session_state.history = []

# CSS 주입: PC/모바일 하이브리드 레이아웃 및 보색 대비
st.markdown(f"""
    <style>
    .block-container {{ padding-top: 1.5rem !important; }}
    .stApp {{ background-color: {brand_cream}; color: {brand_brown}; }}
    
    h1 {{ color: {brand_brown}; font-weight: 900; border-bottom: 4px solid {brand_orange}; padding-bottom: 5px; }}

    /* [보색 시공] 모든 숫자 입력창 (PC/모바일 공통 적용으로 시인성 통일) */
    div.stNumberInput input {{
        background-color: {brand_brown} !important;
        color: {brand_orange} !important;
        height: 80px !important;
        font-size: 32px !important;
        font-weight: 900 !important;
        border: 3px solid {brand_orange} !important;
        border-radius: 12px !important;
    }}
    div.stNumberInput label p {{ font-size: 20px !important; font-weight: 900 !important; color: {brand_brown} !important; }}

    /* 공정 버튼 스타일 */
    div[role="radiogroup"] label {{
        border: 3px solid {brand_brown} !important;
        padding: 25px 5px !important;
        border-radius: 12px !important;
        min-height: 90px !important;
        display: flex !important; align-items: center !important; justify-content: center !important;
    }}
    /* 미선택 파스텔 배경 */
    div[role="radiogroup"] label:nth-child(1) {{ background-color: #E8F5E9 !important; }} 
    div[role="radiogroup"] label:nth-child(2) {{ background-color: #E1F5FE !important; }} 
    div[role="radiogroup"] label:nth-child(3) {{ background-color: #F3E5F5 !important; }} 
    div[role="radiogroup"] label:nth-child(4) {{ background-color: #FFF3E0 !important; }} 

    div[role="radiogroup"] label p {{ color: {brand_brown} !important; font-size: 18px !important; font-weight: 900 !important; }}
    /* 선택 시 보색 반전 */
    div[role="radiogroup"] label[data-checked="true"] {{ background-color: {brand_brown} !important; }}
    div[role="radiogroup"] label[data-checked="true"] p {{ color: {brand_orange} !important; }}

    /* 결과 카드 */
    .result-card {{
        background-color: {brand_brown}; color: white; padding: 20px;
        border-radius: 15px; border: 4px solid {brand_orange};
    }}
    .result-value {{ color: {brand_orange} !important; font-size: 3rem; font-weight: 900; }}

    /* 모바일 위저드 버튼 */
    .stButton > button {{
        width: 100%; height: 60px !important;
        background-color: {brand_orange} !important; color: white !important;
        font-size: 20px !important; font-weight: 900 !important; border-radius: 12px !important;
    }}

    /* 모바일 환경에서의 미세 조정 */
    @media (max-width: 768px) {{
        div.stNumberInput input {{ font-size: 28px !important; height: 75px !important; }}
        .result-value {{ font-size: 2.2rem !important; }}
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. 사이드바 (PC에서는 여기서 설정, 모바일에서는 위저드가 우선) ---
with st.sidebar:
    st.markdown(f"<h2 style='color:{brand_orange};'>🖥️ DESKTOP SETUP</h2>", unsafe_allow_html=True)
    #
    pc_std = st.radio("Standard (PC)", options=['ISO (Heat Input)', 'AWS (Arc Energy)'])
    st.markdown(f"#### ⚙️ WPS range") # 명칭 변경 반영
    pc_min = st.number_input("Min (PC)", value=1.0, step=0.1)
    pc_max = st.number_input("Max (PC)", value=2.5, step=0.1)
    
    # 모바일 모드 강제 전환 스위치 (테스트용)
    mobile_mode = st.toggle("📱 Force Mobile Wizard View", value=False)
    
    st.markdown("<br><hr>", unsafe_allow_html=True)
    try: st.image("image_d9f201.jpg", width=60)
    except: st.markdown("✔️")
    st.markdown(f"<p style='font-size: 14px; font-weight: 900;'>jubail.sanghoon@gmail.com</p>", unsafe_allow_html=True)

# --- 3. 메인 로직 (반응형 분기) ---
st.markdown(f"<h1><span style='color:{brand_orange};'>⚡</span> Heat Master Pro</h1>", unsafe_allow_html=True)

# 모바일 위저드 레이아웃 (사용자가 토글을 켰거나 화면이 작을 때 - 여기서는 명시적 모드로 구현)
if mobile_mode:
    # [STEP 1] 모바일 통합 설정 (Standard + WPS range)
    if st.session_state.step == 1:
        st.markdown("### 🛠️ MOBILE STEP 1. CONFIG")
        m_std = st.radio("Select Standard", options=['ISO (Heat Input)', 'AWS (Arc Energy)'], key="m_std")
        st.markdown("#### ⚙️ WPS range")
        m_min = st.number_input("Min Limit", value=1.0, step=0.1, key="m_min")
        m_max = st.number_input("Max Limit", value=2.5, step=0.1, key="m_max")
        
        if st.button("START CALCULATOR ➔"):
            st.session_state.step = 2
            st.rerun()
    # [STEP 2] 모바일 계산기
    else:
        if st.button("⬅ BACK TO CONFIG"):
            st.session_state.step = 1
            st.rerun()
        
        # 모바일 설정값 사용
        curr_std, curr_min, curr_max = st.session_state.m_std, st.session_state.m_min, st.session_state.m_max
        
        process_name = st.radio("Process", options=['SAW', 'FCAW', 'SMAW', 'GMAW'], horizontal=True)
        k = (1.0 if 'AWS' in curr_std or process_name == 'SAW' else 0.8)
        
        p1, p2 = st.columns(2)
        v = p1.number_input("Volt", value=28.0)
        a = p1.number_input("Amp", value=220.0)
        l = p2.number_input("Length", value=150.0)
        t = p2.number_input("Time", value=120.0)
        
        hi = (k * v * a * t) / (l * 1000)
        status = "PASS" if curr_min <= hi <= curr_max else "FAIL"
        
        st.markdown(f"""<div class="result-card"><div class="result-value">{hi:.3f} kJ/mm</div>
                    <h1 style="color:{brand_green if status=='PASS' else '#FF4B4B'}; text-align:center;">{status}</h1></div>""", unsafe_allow_html=True)

# PC 전용 레이아웃 (All-in-one 대시보드)
else:
    st.info("💡 PC 전용 대시보드 모드입니다. 모바일 환경은 사이드바에서 'Mobile Wizard View'를 켜주세요.")
    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    with col1:
        st.markdown("### 🛠️ 1. Process")
        pc_proc = st.radio("Proc", options=['SAW', 'FCAW', 'SMAW', 'GMAW'], key="pc_proc")
        k_pc = (1.0 if 'AWS' in pc_std or pc_proc == 'SAW' else 0.8)
        
    with col2:
        st.markdown("### ⌨️ 2. Parameters")
        pv = st.number_input("Voltage", value=28.0, key="pv")
        pa = st.number_input("Amperage", value=220.0, key="pa")
        pl = st.number_input("Length", value=150.0, key="pl")
        pt = st.number_input("Time", value=120.0, key="pt")
        
    with col3:
        st.markdown("### 🎯 3. Result")
        hi_pc = (k_pc * pv * pa * pt) / (pl * 1000)
        st_pc = "PASS" if pc_min <= hi_pc <= pc_max else "FAIL"
        st.markdown(f"""<div class="result-card"><p>{pc_std[:10]}...</p>
                    <div class="result-value">{hi_pc:.3f}</div>
                    <h1 style="color:{brand_green if st_pc=='PASS' else '#FF4B4B'}; text-align:center;">{st_pc}</h1></div>""", unsafe_allow_html=True)
        if st.button("💾 SAVE"): st.toast("Logged!")