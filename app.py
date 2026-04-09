import streamlit as st
import pandas as pd
import datetime
import re
import io

# PAGE CONFIG
st.set_page_config(
    page_title="RegDarpan",
    layout="wide"
)

# UI STYLE
st.markdown("""
<style>

html, body, [class*="css"] {
font-family: 'Inter', sans-serif;
}

.stApp {
background-color: #f4f7fb;
}

/* Glass panels */

.glass {
background: rgba(255,255,255,0.6);
backdrop-filter: blur(12px);
border-radius: 14px;
padding: 20px;
box-shadow: 0 4px 20px rgba(0,0,0,0.08);
border:1px solid rgba(255,255,255,0.5);
}

/* Dashboard cards */

.card {
background:white;
border-radius:12px;
padding:18px;
text-align:center;
box-shadow:0 2px 10px rgba(0,0,0,0.06);
}

.card h2{
margin:0;
color:#003087;
}

.card p{
font-size:12px;
color:#6b7280;
margin:0;
}

.big-title{
font-size:28px;
font-weight:700;
color:#003087;
}

.subtitle{
color:#6b7280;
font-size:14px;
}

</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("""
<div class="glass">
<div class="big-title">RegDarpan</div>
<div class="subtitle">AI-powered CDSCO regulatory review assistant</div>
</div>
""", unsafe_allow_html=True)

st.markdown("")

# DASHBOARD
c1,c2,c3,c4 = st.columns(4)

with c1:
    st.markdown("""
    <div class="card">
    <h2>4</h2>
    <p>Urgent SAE Cases</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="card">
    <h2>11</h2>
    <p>Hospitalisation Reports</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="card">
    <h2>7</h2>
    <p>Incomplete Applications</p>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="card">
    <h2>2</h2>
    <p>Duplicate Reports</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ANONYMISATION ENGINE
def anonymise(text):

    tokens = []
    step1 = text

    def replace(pattern,label):
        nonlocal step1
        matches = re.findall(pattern, step1)
        for i,m in enumerate(matches):
            token=f"[{label}-{i+1:03d}]"
            tokens.append((token,m))
            step1=step1.replace(m,token)

    replace(r'\b[6-9]\d{9}\b',"PHONE")
    replace(r'#\d{4,6}',"HOSP_REC")
    replace(r'\b\d{1,2}[-/]\w+[-/]\d{2,4}\b',"DATE")
    replace(r'\b[A-Z]{2,}-[A-Z]{2,}-\d+\b',"PATIENT")

    step2 = step1

    step2 = re.sub(r'\[DATE-\d+\]','[YEAR-ONLY]',step2)

    return step1,step2,tokens

# FILE UPLOAD
st.markdown("### Upload Document")

uploaded = st.file_uploader("Upload Word / PDF / TXT",type=["txt"])

text=""

if uploaded:
    text = uploaded.read().decode("utf-8")

text = st.text_area("Or paste text",text,height=200)

if st.button("Run Anonymisation"):

    if not text:
        st.warning("Please upload or paste text")
    else:

        step1,step2,tokens = anonymise(text)

        st.markdown("## Anonymisation Result")

        col1,col2 = st.columns(2)

        with col1:
            st.markdown("### Original Document")
            st.text_area("",text,height=300)

        with col2:
            st.markdown("### Final Anonymised Output")
            st.text_area("",step2,height=300)

        st.markdown("### Token Map")

        df = pd.DataFrame(tokens,columns=["Token","Original"])
        st.dataframe(df,use_container_width=True)

        st.markdown("### Download Reports")

        pseudo_report = f"""
PSEUDONYMISED REPORT
Generated: {datetime.datetime.now()}

{text}

Pseudonymised Output
{step1}
"""

        final_report = f"""
FULLY ANONYMISED REPORT
Generated: {datetime.datetime.now()}

{step2}
"""

        d1,d2 = st.columns(2)

        with d1:
            st.download_button(
                "Download Pseudonymised Report",
                pseudo_report,
                file_name="pseudonymised_report.txt"
            )

        with d2:
            st.download_button(
                "Download Fully Anonymised Report",
                final_report,
                file_name="anonymised_report.txt"
            )
