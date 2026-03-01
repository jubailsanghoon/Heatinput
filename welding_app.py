import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 페이지 설정 및 디자인 테마 ---
st.set_page_config(page_title="Heat Input Master", layout="wide")

# 모노톤 컬러 정의
color_bg = "#F2F2F2"      # 연회색 배경
color_white = "#FFFFFF"   # 흰색
color_line = "#000000"    # 검은색 실선
color_pass = "#28A745"    # 합격 녹색
color_fail = "#DC3545"    # 불합격 적색

if 'history' not in st.session_state: st.session_state.history = []

# CSS 주입: 폰트 크기 통일, 2x2 그리드, 여백 최소화 시공
st.markdown(f"""
    <style>
    .stApp {{ background-color: {color_bg}; color: {color_line}; }}
    
    /* 타이틀 영역 및 하단 검정 수평선 */
    .header-container {{
        padding-top: 5px;
        display: flex;
        align-items: center;
        background-color: transparent; /* 로고 배경 투명 */
    }}
    .black-divider {{
        border-bottom: 5px solid {color_line};
        margin-top: 2px;
        margin-bottom: 25px;
        width: 100%;
    }}
    .title-text {{ font-size: 2.3rem; font-weight: 900; margin-left: 15px; }}

    /* [통합 폰트 크기 설정] 'Select Process' 제목 크기와 동일하게 통일 (약 1.3rem) */
    .master-label, .stMarkdown h3, div[role="radiogroup"] label p, div.stNumberInput label p {{
        font-size: 1.3rem !important;
        font-weight: 800 !important;
        color: {color_line} !important;
    }}

    /* [공정 버튼] 2줄 배치 (SAW, FCAW / SMAW, GMAW) 및 높이/폭 조절 */
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] {{
        display: grid !important;
        grid-template-columns: 1fr 1fr !important; /* 2열 배치 */
        gap: 10px !important;
    }}
    
    div[role="radiogroup"] label {{
        background-color: {color_white} !important;
        border: 2px solid {color_line} !important;
        min-height: 50px !important;
        padding: 5px !important;
        border-radius: 4px !important;
        margin: 0 !important;
        justify-content: center !important;
    }}
    
    div[role="radiogroup"] label[data-checked="true"] {{
        background-color: {color_line} !important;
    }}
    div[role="radiogroup"] label[data-checked="true"] p {{
        color: {color_white} !important;
    }}

    /* [입력창] 숫자 입력창 내부 버튼 재배치 ([-] 왼쪽, [+] 오른쪽) 및 오렌지 배제 */
    div[data-testid="stNumberInputContainer"] {{
        background-color: {color_white} !important; 
        border: 2px solid {color_line} !important;
        border-radius: 4px !important;
        height: 55px !important;
    }}
    
    div[data-testid="stNumberInputContainer"] input {{
        color: {color_line} !important;
        font-size: 1.5rem !important;
        font-weight: 900 !important;
    }}
    
    button[data-testid="baseButton-secondary"] {{
        color: {color_line} !important;
        min-width: 50px !important;
    }}

    /* [여백 최소화] 라벨과 입력창 사이 간격 줄임 */
    div.stNumberInput {{
        margin-bottom: -15px !important;
    }}

    /* [Live Result] 2단 분리 레이아웃 */
    .result-value-box {{
        background-color: {color_white};
        border: 3px solid {color_line};
        height: 60px !important;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        font-weight: 900;
        margin-bottom: 10px;
    }}
    .result-status-box {{
        height: 50px !important;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        font-weight: 900;
        border: 2px solid {color_line};
        color: {color_white};
    }}
    
    /* 사이드바 폭 조절 */
    section[data-testid="stSidebar"] .stNumberInput {{ width: 85% !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. 헤더 영역 (로고 투명 배경 및 타이틀) ---
logo_url = "https://raw.githubusercontent.com/jubailsanghoon/Heatinput/main/db65c0d39f36f2dddc248ea0bf2e4efc.jpg"

st.markdown('<div class="header-container">', unsafe_allow_html=True)
col_logo, col_title = st.columns([1, 8])
with col_logo:
    st.image(logo_url, width=80) 
with col_title:
    st.markdown(f'<span class="title-text">Heat Input Master</span>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="black-divider"></div>', unsafe_allow_html=True)

# --- 3. 사이드바 (규격 및 WPS 설정) ---
with st.sidebar:
    st.markdown("### Standard")
    std_mode = st.radio("Std", options=['ISO', 'AWS'], label_visibility="collapsed")
    
    st.markdown("<br>### WPS range", unsafe_allow_html=True)
    w_min = st.number_input("Min", value=1.0, step=0.1, format="%.1f")
    w_max = st.number_input("Max", value=2.5, step=0.1, format="%.1f")
    
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.write("**Admin:** jubail.sanghoon@gmail.com")

# --- 4. 메인 대시보드 (3열 밸런스) ---
col1, col2, col3 = st.columns([1.1, 1.2, 0.9])

# [섹션 1] Select Process (2줄 2열 그리드)
with col1:
    st.markdown("### 1. Select Process")
    proc = st.radio("P", options=['SAW', 'FCAW', 'SMAW', 'GMAW'], horizontal=True, label_visibility="collapsed")
    k = 1.0 if std_mode == 'AWS' or proc == 'SAW' else 0.8

# [섹션 2] Input Parameters (1줄 평평한 정렬, 폰트 크기 통일)
with col2:
    st.markdown("### 2. Input Parameters")
    
    def render_row(label, val, step, key):
        r_c1, r_c2 = st.columns([5, 5])
        r_c1.markdown(f"<div style='margin-top:15px; font-weight:800; font-size:1.3rem;'>{label}</div>", unsafe_allow_html=True)
        return r_c2.number_input(label, value=val, step=step, format="%.1f", label_visibility="collapsed", key=key)

    v = render_row("Voltage (V)", 28.0, 0.5, "v_m")
    a = render_row("Amperage (A)", 220.0, 5.0, "a_m")
    l = render_row("Length (mm)", 150.0, 10.0, "l_m")
    t = render_row("Time (Sec)", 120.0, 1.0, "t_m")

# [섹션 3] Live Result & Status
with col3:
    st.markdown("### 3. Live Result")
    hi = (k * v * a * t) / (l * 1000) if l > 0 else 0
    is_pass = w_min <= hi <= w_max
    
    # 수치 박스
    st.markdown(f'<div class="result-value-box">{hi:.3f} kJ/mm</div>', unsafe_allow_html=True)
    
    # 상태 박스
    st_bg = color_pass if is_pass else color_fail
    st.markdown(f'<div class="result-status-box" style="background-color:{st_bg};">{"PASS" if is_pass else "FAIL"}</div>', unsafe_allow_html=True)
    
    # 별도 로그 저장 섹션
    st.markdown('<div style="margin-top:20px;">', unsafe_allow_html=True)
    if st.button("💾 SAVE LOG DATA", use_container_width=True):
        st.session_state.history.insert(0, {
            "Time": datetime.now().strftime("%H:%M:%S"),
            "Proc": proc, "V": v, "A": a, "L": l, "T": t,
            "HI": f"{hi:.3f}", "Status": "PASS" if is_pass else "FAIL"
        })
        st.toast("Data Saved")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. 히스토리 데이터 ---
if st.session_state.history:
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.table(pd.DataFrame(st.session_state.history).head(10))