st.markdown("""
<style>

/* ---------- Radio Button Layout Fix ---------- */

div[role="radiogroup"] {
    display:flex;
    gap:10px;
}

div[role="radiogroup"] > label {
    flex:1;
    border:3px solid black;
    padding:18px 0;
    text-align:center;
    font-weight:900;
    font-size:20px;
    cursor:pointer;
    background:white;
}

/* 동그라미 숨김 */
div[role="radiogroup"] input {
    display:none;
}

/* 선택된 경우 */
div[role="radiogroup"] input:checked + div {
    background-color:#ff7f00 !important;
    color:white !important;
}

/* ---------- PASS / FAIL Layout ---------- */

.pass {
    background-color:#00cc44;
    color:white;
    padding:12px;
    font-weight:900;
    text-align:center;
    width:70%;
    margin:20px auto 0 auto;
}

.fail {
    background-color:#ff7f00;
    color:white;
    padding:12px;
    font-weight:900;
    text-align:center;
    width:70%;
    margin:20px auto 0 auto;
}

</style>
""", unsafe_allow_html=True)