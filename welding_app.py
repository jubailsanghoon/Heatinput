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

/* 버튼 기본 */
.custom-btn button {
    width: 100%;
    height: 70px;
    font-size: 22px;
    font-weight: 900;
    border: 3px solid #000000;
    background-color: white;
    color: black;
}

/* 선택된 버튼 */
.active-btn button {
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
# Standard Selection (완전 버튼형 라디오)
# =====================================================
st.markdown('<div class="section-title">Standard Selection</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    container = st.container()
    if st.session_state.standard == "ISO":
        container.markdown('<div class="active-btn custom-btn">', unsafe_allow_html=True)
    else:
        container.markdown('<div class="custom-btn">', unsafe_allow_html=True)

    if container.button("ISO", key="iso_btn"):
        st.session_state.standard = "ISO"
        st.rerun()
    container.markdown('</div>', unsafe_allow_html=True)

with col2:
    container = st.container()
    if st.session_state.standard == "AWS":
        container.markdown('<div class="active-btn custom-btn">', unsafe_allow_html=True)
    else:
        container.markdown('<div class="custom-btn">', unsafe_allow_html=True)

    if container.button("AWS", key="aws_btn"):
        st.session_state.standard = "AWS"
        st.rerun()
    container.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# Select Process (4버튼 동일 크기 라디오)
# =====================================================
st.markdown('<div class="section-title">Select Process</div>', unsafe_allow_html=True)

p1, p2 = st.columns(2)
p3, p4 = st.columns(2)

def process_button(name, col):
    with col:
        container = st.container()
        if st.session_state.process == name:
            container.markdown('<div class="active-btn custom-btn">', unsafe_allow_html=True)
        else:
            container.markdown('<div class="custom-btn">', unsafe_allow_html=True)

        if container.button(name, key=f"{name}_btn"):
            st.session_state.process = name
            st.rerun()

        container.markdown('</div>', unsafe_allow_html=True)

process_button("SAW", p1)
process_button("FCAW", p2)
process_button("SMAW", p3)
process_button("GMAW", p4)