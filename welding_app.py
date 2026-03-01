import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 페이지 설정 및 디자인 테마 ---
st.set_page_config(page_title="Heat Input Master", layout="wide")

color_bg = "#F2F2F2"      # 연회색 배경
color_white = "#FFFFFF"   # 흰색 박스
color_line = "#000000"    # 검은색 실선
color_pass = "#28A745"
color_fail = "#DC3545"

if 'history' not in st.session_state: st.session_state.history = []

# CSS 주입: 절대 비율 고정 및 폰트 체급 통일
st.markdown(f"""
    <style>
    .stApp {{ background-color: {color_bg}; color: {color_line}; }}
    
    /* 로고 배경 투명화 및 타이틀 라인 */
    .header-logo img {{ mix-blend-mode: multiply; }}
    .header-container {{ padding-top: 5px; display: flex; align-items: center; margin-bottom: 0px; }}
    .black-divider {{ border-bottom: 5px solid {color_line}; margin-top: 2px; margin-bottom: 25px; width: 100%; }}
    .title-text {{ font-size: 2.3rem; font-weight: 900; margin-left: 15px; }}

    /* [비율 고정] 모든 핵심 타이틀 및 라벨 폰트 크기 통일 (1.5rem) */
    h3, .big-label {{
        font-size: 1.5rem !important;
        font-weight: 900 !important;
        color: {color_line} !important;
        margin-bottom: 12px !important;
        margin-top: 0px !important;
    }}

    /* [박스 크기 고정 1] ISO, AWS (폭 2배 꽉 차게) */
    section[data-testid="stSidebar"] div[role="radiogroup"] {{
        display: flex !important;
        gap: 10px !important;
    }}
    section[data-testid="stSidebar"] div[role="radiogroup"] label {{
        flex: 1 1 50% !important; /* 50%씩 정확히 분할 */
        min-height: 55px !important;
        border: 2px solid {color_line} !important;
        background-color: {color_white} !important;
        border-radius: 4px !important;
        justify-content: center !important;
        padding: 0 !important;
    }}

    /* [박스 크기 고정 2] Select Process 2x2 그리드 */
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] {{
        display: grid !important;
        grid-template-columns: repeat(2, 1fr) !important; /* 정확한 2열 균등 분할 */
        gap: 12px !important;
    }}
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label {{
        min-height: 60px !important; /* 버튼 높이 고정 */
        border: 2px solid {color_line} !important;
        background-color: {color_white} !important;
        border-radius: 4px !important;
        justify-content: center !important;
        margin: 0 !important;
    }}
    
    /* 버튼 텍스트 크기 통일 */
    div[role="radiogroup"] label p {{ font-size: 1.5rem !important; font-weight: 900 !important; }}
    
    /* 선택된 버튼 흑백 반전 */
    div[role="radiogroup"] label[data-checked="true"] {{ background-color: {color_line} !important; }}
    div[role="radiogroup"] label[data-checked="true"] p {{ color: {color_white} !important; }}

    /* [박스 크기 고정 3] Input Parameters (-) 왼쪽, (+) 오른쪽 분리 및 높이 유지 */
    div[data-testid="stNumberInputContainer"] {{
        background-color: {color_white} !important; 
        border: 2px solid {color_line} !important;
        border-radius: 4px !important;
        height: 55px !important; /* 높이 고정 */
        display: flex !important;
        justify-content: space-between !important; /* 버튼 양끝 배치 */
        align-items: center !important;
    }}
    div[data-testid="stNumberInputContainer"] input {{
        color: {color_line} !important;
        font-size: 1.5rem !important;
        font-weight: 900 !important;
        text-align: center !important;
    }}
    button[data-testid="baseButton-secondary"] {{
        color: {color_line} !important;
        min-width: 55px !important;
        height: 100% !important;
        font-size: 1.5rem !important;
    }}
    
    /* 파라미터 행 정렬: 라벨과 입력창 수평 맞춤 */
    .param-row {{ display: flex; align-items: center; margin-bottom: 15px; }}
    .param-label-col {{ width: 45%; }}
    .param-input-col {{ width: 55%; }}

    /* [박스 크기 고정 4] Live Result 비율 유지 */
    .result-value-box {{
        background-color: {color_white};
        border: 3px solid {color_line};
        height: 70px !important; /* 큰 수치 박스 */
        display: flex; align-items: center; justify-content: center;
        font-size: 2.2rem; font-weight: 900; margin-bottom: 10px;
        border-radius: 4px;
    }}
    .result-status-box {{
        height: 55px !important; /* 상태 박스 */
        display: flex; align-items: center; justify-content: center;
        font-size: 1.6rem; font-weight: 900; 
        border: 2px solid {color_line}; color: {color_white};
        border-radius: 4px;
    }}
    .save-action-box {{ 
        border: 2px solid {color_line}; padding: 15px; 
        background-color: #E6E6E6; margin-top: 15px; border-radius: 4px; 
    }}
    
    /* 사이드바 폭 가득 채우기 */
    section[data-testid="stSidebar"] .stNumberInput {{ width: 100% !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. 헤더 영역 ---
logo_url = "https://raw.githubusercontent.com/jubailsanghoon/Heatinput/main/db65c0d39f36f2dddc248ea0bf2e4efc.jpg"

st.markdown('<div class="header-container">', unsafe_allow_html=True)
col_logo, col_title = st.columns([1, 8])
with col_logo:
    st.markdown(f'<div class="header-logo"><img src="{logo_url}" width="80"></div>', unsafe_allow_html=True)
with col_title:
    st.markdown(f'<span class="title-text">Heat Input Master</span>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="black-divider"></div>', unsafe_allow_html=True)

# --- 3. 사이드바 (WPS 설정) ---
with st.sidebar:
    st.markdown("<div class='big-label'>Standard</div>", unsafe_allow_html=True)
    std_mode = st.radio("Std", options=['ISO', 'AWS'], horizontal=True, label_visibility="collapsed")
    
    st.markdown("<br><div class='big-label'>WPS range</div>", unsafe_allow_html=True)
    w_min = st.number_input("Min", value=1.0, step=0.1, format="%.1f")
    w_max = st.number_input("Max", value=2.5, step=0.1, format="%.1f")
    
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.write("**Admin:** jubail.sanghoon@gmail.com")

# --- 4. 메인 대시보드 (3열 구조: 비율 1 : 1.3 : 0.9 고정) ---
col1, col2, col3 = st.columns([1, 1.3, 0.9])

# [섹션 1] Select Process (2x2 그리드)
with col1:
    st.markdown("### Select Process")
    proc = st.radio("P", options=['SAW', 'FCAW', 'SMAW', 'GMAW'], label_visibility="collapsed")
    k = 1.0 if std_mode == 'AWS' or proc == 'SAW' else 0.8

# [섹션 2] Input Parameters (정렬 및 높이 유지)
with col2:
    st.markdown("### Input Parameters")
    
    def render_param(label, val, step, key):
        st.markdown(f"""
            <div class="param-row">
                <div class="param-label-col"><span class="big-label">{label}</span></div>
            </div>
            """, unsafe_allow_html=True)
        # 렌더링 타이밍 조절을 위해 컬럼 분리
        c1, c2 = st.columns([4.5, 5.5])
        with c1:
            st.markdown(f"<div class='big-label' style='margin-top:10px;'>{label}</div>", unsafe_allow_html=True)
        with c2:
            return st.number_input(label, value=val, step=step, format="%.1f", label_visibility="collapsed", key=key)

    v = render_param("Voltage (V)", 28.0, 0.5, "v_in")
    a = render_param("Amperage (A)", 220.0, 5.0, "a_in")
    l = render_param("Length (mm)", 150.0, 10.0, "l_in")
    t = render_param("Time (Sec)", 120.0, 1.0, "t_in")

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