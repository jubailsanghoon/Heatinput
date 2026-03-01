import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 페이지 설정 및 디자인 테마 ---
st.set_page_config(page_title="Heat Input Master", layout="wide")

# 모노톤 컬러 테마 (주황색 완전 배제)
color_bg = "#F2F2F2"      # 연회색 배경
color_white = "#FFFFFF"   # 흰색
color_line = "#000000"    # 검은색 실선
color_pass = "#28A745"
color_fail = "#DC3545"

if 'history' not in st.session_state: st.session_state.history = []

# CSS 주입: 로고 투명화, 2x2 그리드, 폰트 통일, 여백 최소화
st.markdown(f"""
    <style>
    .stApp {{ background-color: {color_bg}; color: {color_line}; }}
    
    /* [요청] 로고 배경색 투명화 특수 공법 (JPG의 흰색 배경을 투명하게 처리) */
    .header-logo img {{
        mix-blend-mode: multiply;
    }}
    
    .header-container {{ padding-top: 5px; display: flex; align-items: center; margin-bottom: 0px; }}
    .black-divider {{ border-bottom: 5px solid {color_line}; margin-top: 2px; margin-bottom: 25px; width: 100%; }}
    .title-text {{ font-size: 2.3rem; font-weight: 900; margin-left: 15px; }}

    /* [요청] h3 태그(Select Process 등) 폰트 크기 기준점 (1.5rem) */
    h3 {{
        font-size: 1.5rem !important;
        font-weight: 900 !important;
        color: {color_line} !important;
        margin-bottom: 15px !important;
    }}

    /* [요청] ISO, AWS 박스 폭 2배 확대 및 글자 크기 통일 */
    section[data-testid="stSidebar"] div[role="radiogroup"] {{
        display: flex !important;
        flex-direction: row !important; /* 가로로 넓게 꽉 채움 */
        gap: 10px !important;
    }}
    section[data-testid="stSidebar"] div[role="radiogroup"] label {{
        flex: 1 !important; /* 50%씩 차지하여 박스 폭 2배 효과 */
        min-height: 55px !important;
        border: 2px solid {color_line} !important;
        background-color: {color_white} !important;
        border-radius: 4px !important;
        justify-content: center !important;
        padding: 0 !important;
    }}
    section[data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] {{
        background-color: {color_line} !important;
    }}
    section[data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] p {{
        color: {color_white} !important;
    }}
    
    /* 라디오 버튼 안의 글자 크기를 h3(1.5rem)와 완벽히 통일 */
    div[role="radiogroup"] label p {{
        font-size: 1.5rem !important;
        font-weight: 900 !important;
    }}

    /* [요청] Select Process 2x2 그리드 배치 (SAW, FCAW / SMAW, GMAW) */
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] {{
        display: grid !important;
        grid-template-columns: 1fr 1fr !important; /* 정확한 2열 배열 */
        gap: 10px !important;
    }}
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label {{
        min-height: 55px !important;
        border: 2px solid {color_line} !important;
        background-color: {color_white} !important;
        border-radius: 4px !important;
        justify-content: center !important;
        padding: 5px !important;
        margin: 0 !important;
    }}
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label[data-checked="true"] {{
        background-color: {color_line} !important;
    }}
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label[data-checked="true"] p {{
        color: {color_white} !important;
    }}

    /* [요청] Voltage (V), WPS range 등 일반 텍스트 크기 통일 및 여백 최소화 */
    .big-label {{
        font-size: 1.5rem !important;
        font-weight: 900 !important;
        color: {color_line} !important;
        margin-top: 5px; /* 입력창과 높이를 맞추기 위한 미세 조정 */
    }}
    
    /* 입력창 디자인 (버튼 좌우 분리) */
    div[data-testid="stNumberInputContainer"] {{
        background-color: {color_white} !important; 
        border: 2px solid {color_line} !important;
        border-radius: 4px !important;
        height: 55px !important;
        margin-top: -5px !important; /* 라벨과의 여백 최소화 */
    }}
    div[data-testid="stNumberInputContainer"] input {{
        color: {color_line} !important;
        font-size: 1.5rem !important;
        font-weight: 900 !important;
    }}
    button[data-testid="baseButton-secondary"] {{
        color: {color_line} !important;
        min-width: 50px !important;
        font-size: 1.5rem !important;
    }}

    /* Live Result 박스 분리 */
    .result-value-box {{
        background-color: {color_white}; border: 3px solid {color_line};
        height: 60px !important; display: flex; align-items: center; justify-content: center;
        font-size: 2rem; font-weight: 900; margin-bottom: 8px;
    }}
    .result-status-box {{
        height: 50px !important; display: flex; align-items: center; justify-content: center;
        font-size: 1.5rem; font-weight: 900; border: 2px solid {color_line}; color: {color_white};
    }}
    .save-action-box {{ border: 2px solid {color_line}; padding: 12px; background-color: #E6E6E6; margin-top: 15px; border-radius: 4px; }}
    
    /* 사이드바 폭 */
    section[data-testid="stSidebar"] .stNumberInput {{ width: 100% !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. 헤더 영역 (투명 배경 로고) ---
logo_url = "https://raw.githubusercontent.com/jubailsanghoon/Heatinput/main/db65c0d39f36f2dddc248ea0bf2e4efc.jpg"

st.markdown('<div class="header-container">', unsafe_allow_html=True)
col_logo, col_title = st.columns([1, 8])
with col_logo:
    # CSS 클래스를 부여하여 multiply 효과 적용
    st.markdown(f'<div class="header-logo"><img src="{logo_url}" width="80"></div>', unsafe_allow_html=True)
with col_title:
    st.markdown(f'<span class="title-text">Heat Input Master</span>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="black-divider"></div>', unsafe_allow_html=True)

# --- 3. 사이드바 (규격 및 WPS 설정) ---
with st.sidebar:
    st.markdown("### Standard")
    # 가로 배치 및 버튼 2배 확대는 CSS(flex: 1)로 적용됨
    std_mode = st.radio("Std", options=['ISO', 'AWS'], horizontal=True, label_visibility="collapsed")
    
    st.markdown("<br><div class='big-label'>WPS range</div>", unsafe_allow_html=True)
    w_min = st.number_input("Min", value=1.0, step=0.1, format="%.1f")
    w_max = st.number_input("Max", value=2.5, step=0.1, format="%.1f")
    
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.write("**Admin:** jubail.sanghoon@gmail.com")

# --- 4. 메인 대시보드 (3열 밸런스) ---
col1, col2, col3 = st.columns([1.1, 1.3, 0.9])

# [섹션 1] Select Process (2x2 그리드 배열)
with col1:
    st.markdown("### Select Process")
    # CSS Grid를 통해 자동으로 2줄(SAW FCAW / SMAW GMAW)로 배치됨
    proc = st.radio("P", options=['SAW', 'FCAW', 'SMAW', 'GMAW'], label_visibility="collapsed")
    k = 1.0 if std_mode == 'AWS' or proc == 'SAW' else 0.8

# [섹션 2] Input Parameters (큰 폰트 및 여백 최소화)
with col2:
    st.markdown("### Input Parameters")
    
    def render_row(label, val, step, key):
        r_c1, r_c2 = st.columns([5, 5])
        # 라벨 폰트 크기를 h3(1.5rem)와 완벽히 통일
        r_c1.markdown(f"<div class='big-label'>{label}</div>", unsafe_allow_html=True)
        return r_c2.number_input(label, value=val, step=step, format="%.1f", label_visibility="collapsed", key=key)

    v = render_row("Voltage (V)", 28.0, 0.5, "v_m")
    a = render_row("Amperage (A)", 220.0, 5.0, "a_m")
    l = render_row("Length (mm)", 150.0, 10.0, "l_m")
    t = render_row("Time (Sec)", 120.0, 1.0, "t_m")

# [섹션 3] Live Result & Save
with col3:
    st.markdown("### Live Result")
    hi = (k * v * a * t) / (l * 1000) if l > 0 else 0
    is_pass = w_min <= hi <= w_max
    
    st.markdown(f'<div class="result-value-box">{hi:.3f} kJ/mm</div>', unsafe_allow_html=True)
    st_bg = color_pass if is_pass else color_fail
    st.markdown(f'<div class="result-status-box" style="background-color:{st_bg};">{"PASS" if is_pass else "FAIL"}</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="save-action-box">', unsafe_allow_html=True)
    if st.button("💾 SAVE LOG DATA", use_container_width=True):
        speed = (l / t) * 60 if t > 0 else 0
        st.session_state.history.insert(0, {
            "Time": datetime.now().strftime("%H:%M:%S"),
            "Proc": proc, "V": v, "A": a, "L": l, "T": t, "Speed": f"{speed:.1f}",
            "HI": f"{hi:.3f}", "Status": "PASS" if is_pass else "FAIL"
        })
        st.toast("Success: Data Saved")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. 히스토리 데이터 ---
if st.session_state.history:
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.table(pd.DataFrame(st.session_state.history).head(10))