import streamlit as st
import pandas as pd
from datetime import datetime

# ==========================================
# ⚙️ [기본 설정] 페이지 셋업 및 테마
# ==========================================
st.set_page_config(page_title="Heat Input Master", layout="wide")

color_bg = "#F2F2F2"      # 배경색
color_white = "#FFFFFF"   # 박스색
color_line = "#000000"    # 폰트 및 테두리(블랙)
color_pass = "#28A745"    # 합격(그린)
color_fail = "#DC3545"    # 불합격(레드)

if 'history' not in st.session_state: st.session_state.history = []

# ==========================================
# 🏗️ [CSS 코어] 완벽 격리된 모듈형 CSS & 모바일 반응형
# ==========================================
st.markdown(f"""
    <style>
    /* -----------------------------------
       공통 베이스 (전체 배경 및 폰트)
       ----------------------------------- */
    .stApp {{ background-color: {color_bg}; color: {color_line}; }}
    
    .master-label {{
        font-size: 1.5rem !important; font-weight: normal !important; color: {color_line} !important;
        margin: 0 0 10px 0 !important; padding: 0 !important; line-height: 1.2 !important;
    }}

    /* -----------------------------------
       [모듈 0] 상부 타이틀 (헤더)
       ----------------------------------- */
    .header-logo img {{ mix-blend-mode: multiply; }}
    .header-container {{ display: flex; align-items: center; padding-top: 0px; margin-bottom: 0px; }}
    .black-divider {{ border-bottom: 5px solid {color_line}; margin-top: 5px; margin-bottom: 20px; width: 100%; }}
    .title-text {{ font-size: 2.3rem; font-weight: bold; margin-left: 15px; color: {color_line}; }}

    /* -----------------------------------
       [모듈 1] 첫 번째 섹션 (사이드바 - Standard & WPS)
       ----------------------------------- */
    section[data-testid="stSidebar"] div[role="radiogroup"] {{
        display: flex !important; flex-direction: column !important; align-items: flex-start !important; 
        gap: 8px !important; margin-bottom: 15px !important;
    }}
    section[data-testid="stSidebar"] div[role="radiogroup"] label p {{
        font-size: 1.5rem !important; font-weight: normal !important; color: {color_line} !important; margin: 0 !important;
    }}
    section[data-testid="stSidebar"] div.stNumberInput {{ width: 85% !important; margin-left: 0 !important; }}

    /* -----------------------------------
       [모듈 2] 두 번째 섹션 (Select Process 2x2 버튼)
       ----------------------------------- */
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] {{
        display: grid !important; grid-template-columns: repeat(2, 1fr) !important; 
        gap: 10px !important; margin-top: -5px !important;
    }}
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label {{
        height: 60px !important; border: 2px solid {color_line} !important; background-color: {color_white} !important;
        border-radius: 4px !important; justify-content: center !important; align-items: center !important;
        margin: 0 !important; padding: 0 !important; cursor: pointer;
    }}
    /* 글자 크기 1.5rem 강제 동기화 및 선택 시 색상 반전 */
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label * {{ font-size: 1.5rem !important; font-weight: normal !important; margin: 0 !important; }}
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label[data-checked="true"] {{ background-color: {color_line} !important; }}
    div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label[data-checked="true"] * {{ color: {color_white} !important; }}

    /* -----------------------------------
       [모듈 3] 세 번째 섹션 (Input Parameters)
       ----------------------------------- */
    /* [-] [숫자] [+] 완벽 좌우 분리 */
    div[data-testid="stNumberInputContainer"] {{
        display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important;
        background-color: {color_white} !important; border: 2px solid {color_line} !important;
        border-radius: 4px !important; height: 60px !important; padding: 0 !important;
        align-items: center !important; justify-content: space-between !important; overflow: hidden !important;
    }}
    /* (-) 버튼 왼쪽 고정 */
    div[data-testid="stNumberInputContainer"] > button:first-of-type {{
        order: -1 !important; min-width: 60px !important; height: 100% !important; background-color: transparent !important;
        border-right: 1px solid #CCC !important; margin: 0 !important; color: {color_line} !important; font-size: 1.5rem !important;
    }}
    /* 가운데 숫자창 */
    div[data-testid="stNumberInputContainer"] > div, div[data-testid="stNumberInputContainer"] input {{
        order: 2 !important; flex-grow: 1 !important; text-align: center !important; color: {color_line} !important;
        font-size: 1.5rem !important; font-weight: bold !important; background-color: transparent !important; border: none !important; width: 100% !important;
    }}
    /* (+) 버튼 오른쪽 고정 */
    div[data-testid="stNumberInputContainer"] > button:last-of-type {{
        order: 99 !important; min-width: 60px !important; height: 100% !important; background-color: transparent !important;
        border-left: 1px solid #CCC !important; margin: 0 !important; color: {color_line} !important; font-size: 1.5rem !important;
    }}
    /* 스트림릿 기본 여백 박살 */
    div[data-testid="column"]:nth-of-type(2) div[data-testid="stHorizontalBlock"] {{ gap: 0rem !important; }}
    div[data-testid="column"]:nth-of-type(2) div[data-testid="stHorizontalBlock"] div[data-testid="column"] {{ padding: 0 !important; }}
    .stNumberInput {{ margin-bottom: -10px !important; }}

    /* -----------------------------------
       [모듈 4] 네 번째 섹션 (Live Result)
       ----------------------------------- */
    .result-value-box {{
        background-color: {color_white}; border: 3px solid {color_line}; height: 75px !important; 
        display: flex; align-items: center; justify-content: center; font-size: 2.2rem; font-weight: bold; 
        margin-bottom: 10px; border-radius: 4px; margin-top: -5px;
    }}
    .result-status-box {{
        height: 60px !important; display: flex; align-items: center; justify-content: center; font-size: 1.8rem; font-weight: bold;
        border: 2px solid {color_line}; color: {color_white}; border-radius: 4px;
    }}
    .save-btn-container button {{
        height: 60px !important; font-size: 1.5rem !important; font-weight: bold !important; border: 2px solid {color_line} !important; 
        background-color: #E6E6E6 !important; color: {color_line} !important; border-radius: 4px !important; margin-top: 10px !important;
    }}

    /* ==========================================
       📱 [모바일 최적화 스위치] 화면 폭 768px 이하 감지
       ========================================== */
    @media (max-width: 768px) {{
        /* 1. 글자 찌그러짐 방지 (전체적으로 폰트 다운사이징) */
        .title-text {{ font-size: 1.8rem !important; }}
        .master-label {{ font-size: 1.1rem !important; height: auto !important; margin-bottom: 5px !important; }}
        
        /* 2. 라디오 버튼 텍스트 최적화 */
        section[data-testid="stSidebar"] div[role="radiogroup"] label p {{ font-size: 1.2rem !important; }}
        div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label * {{ font-size: 1.1rem !important; }}
        
        /* 3. 박스 높이 다이어트 (60px -> 50px) */
        div[data-testid="stNumberInputContainer"], 
        div[data-testid="column"]:nth-of-type(1) div[role="radiogroup"] label,
        .result-status-box, .save-btn-container button {{ 
            height: 50px !important; 
        }}
        
        /* 4. 터치 버튼 최적화 (+, - 버튼 크기를 모바일 손가락에 맞춤) */
        div[data-testid="stNumberInputContainer"] > button:first-of-type,
        div[data-testid="stNumberInputContainer"] > button:last-of-type {{
            min-width: 45px !important; font-size: 1.3rem !important;
        }}
        div[data-testid="stNumberInputContainer"] input {{ font-size: 1.3rem !important; }}
        
        /* 5. 결과창 밸런스 조정 */
        .result-value-box {{ height: 60px !important; font-size: 1.8rem !important; }}
        
        /* 6. 모바일 여백 100% 활용 */
        section[data-testid="stSidebar"] div.stNumberInput {{ width: 100% !important; }}
        div[data-testid="stNumberInputContainer"] {{ margin-left: 0 !important; }}
    }}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 🏗️ [모듈 0] 상부 타이틀 (헤더)
# ==========================================
logo_url = "https://raw.githubusercontent.com/jubailsanghoon/Heatinput/main/db65c0d39f36f2dddc248ea0bf2e4efc.jpg"
st.markdown('<div class="header-container">', unsafe_allow_html=True)
c_logo, c_title = st.columns([1, 9])
with c_logo: st.markdown(f'<div class="header-logo"><img src="{logo_url}" width="80"></div>', unsafe_allow_html=True)
with c_title: st.markdown(f'<span class="title-text">Heat Input Master</span>', unsafe_allow_html=True)
st.markdown('</div><div class="black-divider"></div>', unsafe_allow_html=True)

# ==========================================
# 🏗️ [모듈 1] 왼쪽 첫 번째 섹션 (사이드바)
# ==========================================
with st.sidebar:
    st.markdown("<div class='master-label'>Standard</div>", unsafe_allow_html=True)
    std_mode = st.radio("Std", options=['ISO', 'AWS'], horizontal=False, label_visibility="collapsed")
    
    st.markdown("<br><div class='master-label'>WPS range</div>", unsafe_allow_html=True)
    w_min = st.number_input("Min", value=1.0, step=0.1, format="%.1f")
    w_max = st.number_input("Max", value=2.5, step=0.1, format="%.1f")
    
    st.markdown("<br><hr style='margin:10px 0;'>", unsafe_allow_html=True)
    st.markdown("<div>Admin: jubail.sanghoon@gmail.com</div>", unsafe_allow_html=True)

# ==========================================
# 메인 3단 배열 (PC: 가로 배치 / 모바일: 세로 자동 적재)
# ==========================================
col1, col2, col3 = st.columns([1.1, 1.3, 0.9], gap="medium")

# 🏗️ [모듈 2] 두 번째 섹션 (Select Process)
with col1:
    st.markdown("<div class='master-label'>Select Process</div>", unsafe_allow_html=True)
    proc = st.radio("P", options=['SAW', 'FCAW', 'SMAW', 'GMAW'], label_visibility="collapsed")
    k = 1.0 if std_mode == 'AWS' or proc == 'SAW' else 0.8

# 🏗️ [모듈 3] 세 번째 섹션 (Input Parameters)
with col2:
    st.markdown("<div class='master-label'>Input Parameters</div>", unsafe_allow_html=True)
    def param_row(label, val, step, key):
        c_lbl, c_inp = st.columns([4.5, 5.5])
        # PC에서는 높이를 맞추고, 모바일에서는 높이를 풀어주어 자동 줄바꿈 대응
        with c_lbl: st.markdown(f"<div class='master-label' style='display: flex; align-items: center; min-height: 60px; margin: 0 !important;'>{label}</div>", unsafe_allow_html=True)
        with c_inp: return st.number_input(label, value=val, step=step, format="%.1f", label_visibility="collapsed", key=key)

    v = param_row("Voltage (V)", 28.0, 0.5, "v_in")
    a = param_row("Amperage (A)", 220.0, 5.0, "a_in")
    l = param_row("Length (mm)", 150.0, 10.0, "l_in")
    t = param_row("Time (Sec)", 120.0, 1.0, "t_in")

# 🏗️ [모듈 4] 네 번째 섹션 (Live Result & Save)
with col3:
    st.markdown("<div class='master-label'>Live Result</div>", unsafe_allow_html=True)
    hi = (k * v * a * t) / (l * 1000) if l > 0 else 0
    is_pass = w_min <= hi <= w_max
    
    st.markdown(f'<div class="result-value-box">{hi:.3f} kJ/mm</div>', unsafe_allow_html=True)
    st_bg = color_pass if is_pass else color_fail
    st.markdown(f'<div class="result-status-box" style="background-color:{st_bg};">{"PASS" if is_pass else "FAIL"}</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="save-btn-container">', unsafe_allow_html=True)
    if st.button("💾 SAVE LOG", use_container_width=True):
        st.session_state.history.insert(0, {
            "Time": datetime.now().strftime("%H:%M:%S"),
            "Proc": proc, "V": v, "A": a, "L": l, "T": t, 
            "HI": f"{hi:.3f}", "Status": "PASS" if is_pass else "FAIL"
        })
        st.toast("Saved")
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 📊 [히스토리 데이터]
# ==========================================
if st.session_state.history:
    st.markdown("<hr style='margin-top:20px; margin-bottom:10px;'>", unsafe_allow_html=True)
    st.table(pd.DataFrame(st.session_state.history).head(10))