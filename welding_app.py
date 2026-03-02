import streamlit as st

st.set_page_config(page_title="Heat Input Master", layout="centered")

# =====================================================
# CSS
# =====================================================
st.markdown("""
<style>

html, body, .main {
    background-color: #F2F2F2;
    font-family: Arial, Helvetica, sans-serif;
}

.block-container {
    max-width: 480px;
    padding-top: 10px;
}

/* Header */
.header-title {
    font-size: 26px;
    font-weight: 900;
}

/* Section Title */
.section-title {
    font-size: 22px;
    font-weight: 900;
    border-bottom: 5px solid #000000;
    margin-top: 20px;
    margin-bottom: 12px;
}

/* 버튼 공통 */
.stButton > button {
    width: 100%;
    height: 70px;
    font-size: 22px;
    font-weight: 900;
    border: 3px solid #000000;
    background-color: white;
    color: black;
}

/* 선택 상태 */
.selected > div > button {
    background-color: #FF7A00 !important;
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# Session State
# =====================================================
if "standard" not in st.session_state:
    st.session_state.standard = "ISO"

if "process" not in st.session_state:
    st.session_state.process = "SAW"

# =====================================================
# Header
# =====================================================
col1, col2 = st.columns([1,4])

with col1:
    st.image(
        "https://raw.githubusercontent.com/jubailsanghoon/Heatinput/main/db65c0d39f36f2dddc248ea0bf2e4efc.jpg",
        width=60
    )

with col2:
    st.markdown('<div class="header-title">Heat Input Master</div>', unsafe_allow_html=True)

st.markdown('<div style="border-bottom:5px solid #000000;margin-top:10px;"></div>', unsafe_allow_html=True)

# =====================================================
# Standard Selection (라디오 버튼형)
# =====================================================
st.markdown('<div class="section-title">Standard Selection</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    wrapper = st.container()
    if st.session_state.standard == "ISO":
        wrapper.markdown('<div class="selected">', unsafe_allow_html=True)
    if wrapper.button("ISO"):
        st.session_state.standard = "ISO"
        st.rerun()
    if st.session_state.standard == "ISO":
        wrapper.markdown('</div>', unsafe_allow_html=True)

with col2:
    wrapper = st.container()
    if st.session_state.standard == "AWS":
        wrapper.markdown('<div class="selected">', unsafe_allow_html=True)
    if wrapper.button("AWS"):
        st.session_state.standard = "AWS"
        st.rerun()
    if st.session_state.standard == "AWS":
        wrapper.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# Select Process (4버튼 라디오형)
# =====================================================
st.markdown('<div class="section-title">Select Process</div>', unsafe_allow_html=True)

p1, p2 = st.columns(2)
p3, p4 = st.columns(2)

def process_button(name, column):
    with column:
        wrapper = st.container()
        if st.session_state.process == name:
            wrapper.markdown('<div class="selected">', unsafe_allow_html=True)
        if wrapper.button(name):
            st.session_state.process = name
            st.rerun()
        if st.session_state.process == name:
            wrapper.markdown('</div>', unsafe_allow_html=True)

process_button("SAW", p1)
process_button("FCAW", p2)
process_button("SMAW", p3)
process_button("GMAW", p4)