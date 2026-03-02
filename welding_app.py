import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 페이지 설정 (중앙 정렬을 위해 Wide 모드 해제) ---
st.set_page_config(page_title="Heat Input Master", layout="centered")

color_bg = "#F2F2F2"      # 연회색 바탕
color_white = "#FFFFFF"   # 흰색 박스
color_line = "#000000"    # 검정 선/글자
color_pass = "#28A745"
color_fail = "#DC3545"

if 'history' not in st.session_state: st.session_state.history = []

# --- 2. CSS 초정밀 시공 (모바일 전용 규격 고정) ---
st.markdown(f"""
    <style>
    /* 전체 배경 및 폭 고정 (450px) */
    .stApp {{
        background-color: {color_bg};
        max-width: 450px;
        margin: 0 auto;  /* PC 접속 시 중앙 정렬 */
        border-left: 1px solid #ddd;
        border-right: 1px solid #ddd;
    }}
    
    /* 모든 텍스트 검정색 강제 및 가독성 확보 */
    * {{ color: {color_line} !important; font-family: 'Inter', sans-serif; }}

    /* 라벨 스타일 */
    .master-label {{
        font-size: 1.1rem !important;
        font-weight: bold !important;
        margin-top: 15px !important;
        margin-bottom: 5px !important;
        display: block;
    }}

    /* 숫자 입력창 [-] 1번, [숫자] 2번, [+] 3번 고정 */
    div[data-testid="stNumberInputContainer"] {{
        display: flex !important;
        flex-direction: row !important;
        height: 60px !important;
        background-color: {color_white} !important;
        border: 2px solid {color_line} !important;
        border-radius: 4px !important;
        overflow: hidden !important;
    }}
    /* 버튼들 */
    div[data-testid="stNumberInputContainer"] button {{
        min-width: 60px !important; height: 100% !important; 
        font-size: 1.5rem !important; background: #eee !important;
    }}
    /* 입력 숫자 */
    div[data-testid="stNumberInputContainer"] input {{
        font-size: 1.3rem !important; font-weight: bold !important;
        text-align: center !important;
    }}

    /* 공정 선택 2x2 그리드 */
    div[role="radiogroup"] {{
        display: grid !important;
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 8px !important;
    }}
    div[role="radiogroup"] label {{
        height: 60px !important;
        border: 2px solid {color_line} !important;
        background-color: {color_white} !important;
        border-radius: 4px !important;
        justify-content: center !important;
    }}
    /* 선택된 버튼 반전 효과 */
    div[role="radiogroup"] label[data-checked="true"] {{
        background-color: {color_line} !important;
    }}
    div[role="radiogroup"] label[data-checked="true"] p {{
        color: {color_white} !important;
    }}

    /* 결과창 및 버튼 */
    .result-box {{
        background: {color_white}; border: 3px solid {color_line};
        height: 80px; display: flex; align-items: center; justify-content: center;
        font-size: 2rem; font-weight: bold; margin-top: 10px;
    }}
    .status-box {{
        height: 55px; display: flex; align-items: center; justify-content: center;
        font-size: 1.5rem; font-weight: bold; color: white !important;
        border-radius: 4px; margin-top: 10px; border: 2px solid {color_line};
    }}
    .stButton button {{
        height: 60px !important; font-size: 1.2rem !important;
        font-weight: bold !important; border: 2px solid {color_line} !important;
        background: #E6E6E6 !important; margin-top: 10px;
    }}

    /* 사이드바는 모바일에서 메뉴로 숨김 처리되므로 기본 스타일 유지 */
    </style>
    """, unsafe_allow_html=True)

# --- 3. 헤더 (상부 타이틀) ---
logo_url = "https://raw.githubusercontent.com/jubailsanghoon/Heatinput/main/db65c0d39f36f2dddc248ea0bf2e4efc.jpg"
st.markdown(f"""
    <div style="display: flex; align-items: center; border-bottom: 5px solid black; padding-bottom: 10px; margin-bottom: 20px;">
        <img src="{logo_url}" width="60">
        <span style="font-size: 1.6rem; margin-left: 12px; font-weight: bold;">Heat Input Master</span>
    </div>
""", unsafe_allow_html=True)

# --- 4. 메인 입력 영역 (수직 배치) ---
with st.sidebar:
    st.markdown("<span class='master-label'>Standard</span>", unsafe_allow_html=True)
    std_mode = st.radio("Std", ['ISO', 'AWS'], label_visibility="collapsed")
    st.markdown("<span class='master-label'>WPS Range</span>", unsafe_allow_html=True)
    w_min = st.number_input("Min", 1.0, step=0.1)
    w_max = st.number_input("Max", 2.5, step=0.1)

st.markdown("<span class='master-label'>Select Process</span>", unsafe_allow_html=True)
proc = st.radio("Proc", ['SAW', 'FCAW', 'SMAW', 'GMAW'], label_visibility="collapsed")
k = 1.0 if std_mode == 'AWS' or proc == 'SAW' else 0.8

st.markdown("<span class='master-label'>Input Parameters</span>", unsafe_allow_html=True)
def input_group(label, val, step, key):
    st.markdown(f"<div style='font-size:1rem; margin-bottom:5px;'>{label}</div>", unsafe_allow_html=True)
    return st.number_input(label, value=val, step=step, format="%.1f", label_visibility="collapsed", key=key)

v = input_group("Voltage (V)", 28.0, 0.5, "v")
a = input_group("Amperage (A)", 220.0, 5.0, "a")
l = input_group("Length (mm)", 150.0, 10.0, "l")
t = input_group("Time (Sec)", 120.0, 1.0, "t")

# --- 5. 결과 및 저장 ---
hi = (k * v * a * t) / (l * 1000) if l > 0 else 0
is_pass = w_min <= hi <= w_max

st.markdown(f'<div class="result-box">{hi:.3f} kJ/mm</div>', unsafe_allow_html=True)
st_bg = color_pass if is_pass else color_fail
st.markdown(f'<div class="status-box" style="background:{st_bg};">{"PASS" if is_pass else "FAIL"}</div>', unsafe_allow_html=True)

if st.button("💾 SAVE LOG", use_container_width=True):
    st.session_state.history.insert(0, {"Time": datetime.now().strftime("%H:%M:%S"), "Proc": proc, "HI": f"{hi:.3f}", "Status": "PASS" if is_pass else "FAIL"})
    st.toast("Saved!")

if st.session_state.history:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True)