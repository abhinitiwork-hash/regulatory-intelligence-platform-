import streamlit as st
import re
import datetime
import difflib
import pandas as pd

st.set_page_config(
    page_title="CDSCO Regulatory Intelligence Platform",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── GLOBAL CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Hide default streamlit chrome */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Page background */
.stApp {
    background: #f0f4f8;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #001f5b 0%, #003087 60%, #004db3 100%);
    border-right: none;
}
section[data-testid="stSidebar"] * {
    color: white !important;
}
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown span {
    color: rgba(255,255,255,0.85) !important;
}

/* Sidebar compliance badges */
.comp-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 20px;
    padding: 5px 12px;
    font-size: 12px;
    font-weight: 500;
    color: white !important;
    margin: 3px 0;
    width: 100%;
}
.comp-badge.green { border-color: #4ade80; color: #4ade80 !important; }

/* Main header */
.platform-header {
    background: linear-gradient(135deg, #001f5b 0%, #003087 50%, #0052cc 100%);
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 4px 24px rgba(0,48,135,0.18);
}
.platform-header h1 {
    color: white;
    font-size: 26px;
    font-weight: 700;
    margin: 0;
    letter-spacing: -0.3px;
}
.platform-header p {
    color: rgba(255,255,255,0.7);
    margin: 4px 0 0;
    font-size: 13px;
    font-weight: 400;
}
.header-badge {
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 10px;
    padding: 8px 16px;
    text-align: center;
}
.header-badge .num {
    color: #7dd3fc;
    font-size: 22px;
    font-weight: 700;
    display: block;
    line-height: 1;
}
.header-badge .lbl {
    color: rgba(255,255,255,0.65);
    font-size: 11px;
    margin-top: 2px;
    display: block;
}

/* Stat cards row */
.stat-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin-bottom: 24px;
}
.stat-card {
    background: white;
    border-radius: 12px;
    padding: 18px 20px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    border-left: 4px solid #003087;
}
.stat-card.teal  { border-left-color: #0f766e; }
.stat-card.purple{ border-left-color: #6d28d9; }
.stat-card .s-val{ font-size: 28px; font-weight: 700; color: #1e293b; line-height:1; }
.stat-card .s-lbl{ font-size: 12px; color: #64748b; margin-top: 4px; }

/* Feature cards on home */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-top: 8px;
}
.feature-card {
    background: white;
    border-radius: 14px;
    padding: 22px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    border-top: 3px solid #003087;
    transition: box-shadow 0.2s;
}
.feature-card:hover { box-shadow: 0 4px 16px rgba(0,48,135,0.12); }
.feature-card.f2 { border-top-color: #0f766e; }
.feature-card.f3 { border-top-color: #6d28d9; }
.feature-card.f4 { border-top-color: #b45309; }
.feature-card.f5 { border-top-color: #0369a1; }
.feature-card.f6 { border-top-color: #be185d; }
.feature-card .fc-num { font-size: 11px; font-weight: 600; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.08em; }
.feature-card .fc-title { font-size: 15px; font-weight: 600; color: #1e293b; margin: 6px 0 4px; }
.feature-card .fc-desc  { font-size: 12px; color: #64748b; line-height: 1.5; }
.feature-card .fc-icon  { font-size: 28px; margin-bottom: 10px; }

/* Tab container */
.stTabs [data-baseweb="tab-list"] {
    background: white;
    border-radius: 12px;
    padding: 4px;
    gap: 2px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    font-size: 13px;
    font-weight: 500;
    color: #64748b;
    padding: 8px 14px;
}
.stTabs [aria-selected="true"] {
    background: #003087 !important;
    color: white !important;
}

/* Section headers inside tabs */
.section-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 20px;
    padding-bottom: 14px;
    border-bottom: 1px solid #e2e8f0;
}
.section-header .icon {
    width: 44px; height: 44px;
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px;
    flex-shrink: 0;
}
.icon.blue   { background: #dbeafe; }
.icon.teal   { background: #ccfbf1; }
.icon.purple { background: #ede9fe; }
.icon.amber  { background: #fef3c7; }
.icon.sky    { background: #e0f2fe; }
.icon.pink   { background: #fce7f3; }
.section-header h2 { font-size: 18px; font-weight: 600; color: #1e293b; margin: 0; }
.section-header p  { font-size: 12px; color: #64748b; margin: 2px 0 0; }

/* Input areas */
.stTextArea textarea {
    border: 1.5px solid #e2e8f0 !important;
    border-radius: 10px !important;
    font-size: 13px !important;
    font-family: 'Inter', sans-serif !important;
    background: #fafbfc !important;
    transition: border-color 0.2s !important;
}
.stTextArea textarea:focus {
    border-color: #003087 !important;
    background: white !important;
    box-shadow: 0 0 0 3px rgba(0,48,135,0.08) !important;
}
.stTextInput input {
    border: 1.5px solid #e2e8f0 !important;
    border-radius: 8px !important;
    font-size: 13px !important;
}
.stTextInput input:focus {
    border-color: #003087 !important;
    box-shadow: 0 0 0 3px rgba(0,48,135,0.08) !important;
}
.stSelectbox > div > div {
    border: 1.5px solid #e2e8f0 !important;
    border-radius: 8px !important;
}

/* Primary button */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #003087, #0052cc) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 10px 22px !important;
    box-shadow: 0 2px 8px rgba(0,48,135,0.25) !important;
    transition: all 0.2s !important;
}
.stButton > button[kind="primary"]:hover {
    box-shadow: 0 4px 16px rgba(0,48,135,0.35) !important;
    transform: translateY(-1px) !important;
}

/* Result cards */
.result-card {
    background: white;
    border-radius: 12px;
    padding: 20px 24px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    margin: 12px 0;
    border-left: 4px solid #003087;
}
.result-card.success { border-left-color: #16a34a; background: #f0fdf4; }
.result-card.warning { border-left-color: #d97706; background: #fffbeb; }
.result-card.danger  { border-left-color: #dc2626; background: #fef2f2; }
.result-card.info    { border-left-color: #0284c7; background: #f0f9ff; }

/* Token / audit table wrapper */
.table-wrapper {
    background: white;
    border-radius: 12px;
    padding: 4px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    margin: 12px 0;
}

/* Step pills */
.step-pill {
    display: inline-flex; align-items: center; gap: 6px;
    background: #003087; color: white;
    border-radius: 20px; padding: 4px 14px;
    font-size: 12px; font-weight: 600;
    margin-bottom: 10px;
}
.step-pill.step2 { background: #0f766e; }

/* RAG badge */
.rag-green  { background:#dcfce7; color:#15803d; border-radius:6px; padding:2px 10px; font-size:12px; font-weight:600; }
.rag-amber  { background:#fef9c3; color:#a16207; border-radius:6px; padding:2px 10px; font-size:12px; font-weight:600; }
.rag-red    { background:#fee2e2; color:#b91c1c; border-radius:6px; padding:2px 10px; font-size:12px; font-weight:600; }

/* Severity badge */
.sev-death  { background:#fee2e2; color:#991b1b; border-radius:8px; padding:6px 16px; font-size:14px; font-weight:700; display:inline-block; }
.sev-disab  { background:#ffedd5; color:#9a3412; border-radius:8px; padding:6px 16px; font-size:14px; font-weight:700; display:inline-block; }
.sev-hosp   { background:#fef9c3; color:#92400e; border-radius:8px; padding:6px 16px; font-size:14px; font-weight:700; display:inline-block; }
.sev-other  { background:#dbeafe; color:#1e40af; border-radius:8px; padding:6px 16px; font-size:14px; font-weight:700; display:inline-block; }

/* Dataframe overrides */
.stDataFrame { border-radius: 10px; overflow: hidden; }

/* Divider */
.divider { border: none; border-top: 1px solid #e2e8f0; margin: 20px 0; }

/* Download button */
.stDownloadButton > button {
    border-radius: 8px !important;
    border: 1.5px solid #003087 !important;
    color: #003087 !important;
    font-weight: 500 !important;
    font-size: 13px !important;
}

/* Metric overrides */
[data-testid="stMetricValue"] { font-size: 26px !important; font-weight: 700 !important; }
[data-testid="stMetricLabel"] { font-size: 12px !important; color: #64748b !important; }
</style>
""", unsafe_allow_html=True)


# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 16px 0 8px;'>
        <div style='font-size:36px;'>⚕️</div>
        <div style='font-weight:700; font-size:15px; color:white; margin-top:6px;'>CDSCO RIP</div>
        <div style='font-size:11px; color:rgba(255,255,255,0.55); margin-top:2px;'>Regulatory Intelligence Platform</div>
    </div>
    <hr style='border-color:rgba(255,255,255,0.15); margin:12px 0;'>
    """, unsafe_allow_html=True)

    st.markdown("<div style='font-size:11px; font-weight:600; color:rgba(255,255,255,0.5); text-transform:uppercase; letter-spacing:0.08em; margin-bottom:8px;'>Compliance</div>", unsafe_allow_html=True)
    for label in ["✅  DPDP Act 2023", "✅  ICMR Guidelines 2017", "✅  CDSCO Schedule Y", "✅  MeitY AI Ethics"]:
        st.markdown(f"<div class='comp-badge green'>{label}</div>", unsafe_allow_html=True)

    st.markdown("<hr style='border-color:rgba(255,255,255,0.15); margin:16px 0;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:11px; font-weight:600; color:rgba(255,255,255,0.5); text-transform:uppercase; letter-spacing:0.08em; margin-bottom:8px;'>Public Datasets</div>", unsafe_allow_html=True)
    for ds in ["FDA FAERS", "CDSCO CT-04/05/06", "ClinicalTrials.gov", "CTRI India"]:
        st.markdown(f"<div style='font-size:12px; color:rgba(255,255,255,0.7); padding:3px 0;'>• {ds}</div>", unsafe_allow_html=True)

    st.markdown("<hr style='border-color:rgba(255,255,255,0.15); margin:16px 0;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:11px; color:rgba(255,255,255,0.5); line-height:1.6;'>This tool assists regulatory officers. All final decisions must be made by qualified human reviewers.</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:10px; color:rgba(255,255,255,0.3); margin-top:12px; text-align:center;'>Stage 1 · CDSCO AI Hackathon 2026</div>", unsafe_allow_html=True)


# ── HEADER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="platform-header">
  <div>
    <h1>⚕️ Regulatory Intelligence Platform</h1>
    <p>AI-powered workflow automation for CDSCO regulatory processes · Stage 1 Demo</p>
  </div>
  <div style="display:flex; gap:12px;">
    <div class="header-badge"><span class="num">6</span><span class="lbl">AI Features</span></div>
    <div class="header-badge"><span class="num">20</span><span class="lbl">Schedule Y Fields</span></div>
    <div class="header-badge"><span class="num">3</span><span class="lbl">Source Types</span></div>
  </div>
</div>
""", unsafe_allow_html=True)


# ── TABS ─────────────────────────────────────────────────────────────────────
tab0, tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏠  Home",
    "🔒  Anonymisation",
    "📄  Summarisation",
    "✅  Completeness",
    "🏷️  Classification",
    "🔍  Comparison",
    "📋  Inspection Report"
])


# ── TAB 0 — HOME ─────────────────────────────────────────────────────────────
with tab0:
    st.markdown("""
    <div class="feature-grid">
      <div class="feature-card">
        <div class="fc-icon">🔒</div>
        <div class="fc-num">Feature 01</div>
        <div class="fc-title">AI Data Anonymisation</div>
        <div class="fc-desc">Two-step PII/PHI redaction. Pseudonymisation tokens + irreversible generalisation. DPDP Act 2023 compliant audit log.</div>
      </div>
      <div class="feature-card f2">
        <div class="fc-icon">📄</div>
        <div class="fc-num">Feature 02</div>
        <div class="fc-title">Document Summarisation</div>
        <div class="fc-desc">Handles SAE narrations, SUGAM checklists, and meeting transcripts. Structured output for reviewer consumption.</div>
      </div>
      <div class="feature-card f3">
        <div class="fc-icon">✅</div>
        <div class="fc-num">Feature 03</div>
        <div class="fc-title">Completeness Assessment</div>
        <div class="fc-desc">Verifies 20 mandatory Schedule Y fields. RAG status dashboard. Flags missing and incomplete items with recommendations.</div>
      </div>
      <div class="feature-card f4">
        <div class="fc-icon">🏷️</div>
        <div class="fc-num">Feature 04</div>
        <div class="fc-title">SAE Classification</div>
        <div class="fc-desc">ICD-10 keyword-based severity classification: Death, Disability, Hospitalisation, Others. Duplicate detection. Priority queue.</div>
      </div>
      <div class="feature-card f5">
        <div class="fc-icon">🔍</div>
        <div class="fc-num">Feature 05</div>
        <div class="fc-title">Document Comparison</div>
        <div class="fc-desc">Semantic diff between filing versions. Highlights substantive vs administrative changes. Downloadable change report.</div>
      </div>
      <div class="feature-card f6">
        <div class="fc-icon">📋</div>
        <div class="fc-num">Feature 06</div>
        <div class="fc-title">Inspection Report</div>
        <div class="fc-desc">Converts raw site observations into formal CDSCO GCP inspection reports. Critical / Major / Minor classification with deadlines.</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="result-card info">
      <b>How to use:</b> Select any feature tab above. Paste your document content. Click the action button. Download results.
      All processing is local — no data leaves this platform.
    </div>
    """, unsafe_allow_html=True)


# ── TAB 1 — ANONYMISATION ────────────────────────────────────────────────────
with tab1:
    st.markdown("""
    <div class="section-header">
      <div class="icon blue">🔒</div>
      <div>
        <h2>AI-Powered Data Anonymisation</h2>
        <p>Two-step process · Pseudonymisation → Irreversible Anonymisation · DPDP Act 2023 compliant</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    input_text = st.text_area("Paste regulatory document content", height=240,
        placeholder="Paste SAE report, clinical trial document, or any regulatory text containing PII/PHI...",
        key="anon_input")

    col1, col2, col3 = st.columns([1,1,3])
    with col1:
        run_anon = st.button("🔒 Run Anonymisation", type="primary", use_container_width=True)

    if run_anon and input_text.strip():
        INDIAN_FIRST = ["Rajesh","Priya","Suresh","Anita","Vikram","Sunita","Amit","Kavita",
                        "Ravi","Deepa","Mohit","Pooja","Arjun","Neha","Sanjay","Meera",
                        "Rahul","Divya","Anil","Rekha","Vijay","Smita","Ramesh","Geeta",
                        "Ashok","Usha","Manoj","Seema","Vinod","Lata"]
        INDIAN_LAST  = ["Sharma","Patel","Singh","Kumar","Mehta","Gupta","Verma","Joshi",
                        "Nair","Rao","Iyer","Reddy","Bose","Das","Malhotra","Kapoor",
                        "Agarwal","Pandey","Mishra","Tiwari"]

        token_map = []
        audit_log = []
        processed = input_text
        counters  = {"PATIENT":0,"INVESTIGATOR":0,"DATE":0,"SITE":0,"ID":0,"PHONE":0,"AADHAAR":0}
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        def next_token(kind):
            counters[kind] += 1
            return f"[{kind}-{counters[kind]:03d}]"

        aadhaar_re = re.compile(r'\b\d{4}[-\s]\d{4}[-\s]\d{4}\b')
        for m in aadhaar_re.finditer(processed):
            tok = next_token("AADHAAR")
            token_map.append({"Token":tok,"Original Value":m.group(),"Entity Type":"Aadhaar Number","Step":"Step 1"})
            audit_log.append({"Timestamp":ts,"Action":"Pseudonymised","Entity Type":"Aadhaar","Token":tok,"Reversible":"Yes"})
            processed = processed.replace(m.group(), tok, 1)

        phone_re = re.compile(r'\b[6-9]\d{9}\b')
        for m in phone_re.finditer(processed):
            tok = next_token("PHONE")
            token_map.append({"Token":tok,"Original Value":m.group(),"Entity Type":"Phone Number","Step":"Step 1"})
            audit_log.append({"Timestamp":ts,"Action":"Pseudonymised","Entity Type":"Phone","Token":tok,"Reversible":"Yes"})
            processed = processed.replace(m.group(), tok, 1)

        id_re = re.compile(r'\b(PT|SITE|IND|CT|SUBJ|INV)[-]\w+[-]\w+\b')
        for m in id_re.finditer(processed):
            original = m.group()
            if original.startswith(("PT","SUBJ")):
                tok = next_token("PATIENT"); etype = "Patient ID"
            elif original.startswith("SITE"):
                tok = next_token("SITE"); etype = "Site Number"
            elif original.startswith("INV"):
                tok = next_token("INVESTIGATOR"); etype = "Investigator ID"
            else:
                tok = next_token("ID"); etype = "Regulatory ID"
            token_map.append({"Token":tok,"Original Value":original,"Entity Type":etype,"Step":"Step 1"})
            audit_log.append({"Timestamp":ts,"Action":"Pseudonymised","Entity Type":etype,"Token":tok,"Reversible":"Yes"})
            processed = processed.replace(original, tok, 1)

        date_patterns = [
            re.compile(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b'),
            re.compile(r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b', re.IGNORECASE),
            re.compile(r'\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b', re.IGNORECASE),
        ]
        for pat in date_patterns:
            for m in pat.finditer(processed):
                tok = next_token("DATE")
                token_map.append({"Token":tok,"Original Value":m.group(),"Entity Type":"Date","Step":"Step 1"})
                audit_log.append({"Timestamp":ts,"Action":"Pseudonymised","Entity Type":"Date","Token":tok,"Reversible":"Yes"})
                processed = processed.replace(m.group(), tok, 1)

        name_re = re.compile(r'\b(?:Dr\.?\s+)?(' + '|'.join(INDIAN_FIRST) + r')\s+(?:\w+\s+)?(' + '|'.join(INDIAN_LAST) + r')\b')
        for m in name_re.finditer(processed):
            full_name = m.group()
            if "Dr" in full_name:
                tok = next_token("INVESTIGATOR"); etype = "Investigator Name"
            else:
                tok = next_token("PATIENT"); etype = "Patient Name"
            token_map.append({"Token":tok,"Original Value":full_name,"Entity Type":etype,"Step":"Step 1"})
            audit_log.append({"Timestamp":ts,"Action":"Pseudonymised","Entity Type":etype,"Token":tok,"Reversible":"Yes"})
            processed = processed.replace(full_name, tok, 1)

        st.markdown('<div class="step-pill">✓ Step 1 Complete — Pseudonymisation</div>', unsafe_allow_html=True)
        st.text_area("Step 1 Output", processed, height=160, key="step1_out")

        if token_map:
            st.markdown("**Token Mapping Table**")
            st.markdown('<div class="table-wrapper">', unsafe_allow_html=True)
            st.dataframe(pd.DataFrame(token_map), use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="result-card info">No PII/PHI patterns detected. Try pasting a document with Indian names, dates, phone numbers, or structured IDs.</div>', unsafe_allow_html=True)

        step2 = processed
        age_re = re.compile(r'\b(\d{2})\s*(?:years?|yrs?)\s*(?:old)?\b', re.IGNORECASE)
        step2 = age_re.sub(lambda m: f"{(int(m.group(1))//5)*5}-{(int(m.group(1))//5)*5+4} years", step2)
        step2 = re.compile(r'\[DATE-\d+\]').sub('[YEAR-GENERALISED]', step2)
        step2 = re.compile(r'\b(\d{2,3})\s*kg\b', re.IGNORECASE).sub(
            lambda m: f"{(int(m.group(1))//10)*10}-{(int(m.group(1))//10)*10+9} kg", step2)

        audit_log.append({"Timestamp":ts,"Action":"Irreversible Generalisation","Entity Type":"All Dates","Token":"[YEAR-GENERALISED]","Reversible":"No"})
        audit_log.append({"Timestamp":ts,"Action":"Irreversible Generalisation","Entity Type":"Ages","Token":"Age Range","Reversible":"No"})
        audit_log.append({"Timestamp":ts,"Action":"Irreversible Generalisation","Entity Type":"Weight","Token":"Weight Range","Reversible":"No"})

        st.markdown('<br><div class="step-pill step2">✓ Step 2 Complete — Irreversible Anonymisation</div>', unsafe_allow_html=True)
        st.text_area("Final Anonymised Output", step2, height=160, key="step2_out")

        st.markdown("**Audit Log**")
        st.markdown('<div class="table-wrapper">', unsafe_allow_html=True)
        df_audit = pd.DataFrame(audit_log)
        st.dataframe(df_audit, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

        download_text = f"=== STEP 1: PSEUDONYMISED ===\n{processed}\n\n=== STEP 2: FINAL ANONYMISED ===\n{step2}\n\n=== TOKEN MAP ===\n{pd.DataFrame(token_map).to_string()}\n\n=== AUDIT LOG ===\n{df_audit.to_string()}"
        st.download_button("⬇ Download Anonymisation Report", download_text, file_name="anonymisation_report.txt", mime="text/plain")

    elif run_anon:
        st.markdown('<div class="result-card warning">Please paste document content before running anonymisation.</div>', unsafe_allow_html=True)


# ── TAB 2 — SUMMARISATION ────────────────────────────────────────────────────
with tab2:
    st.markdown("""
    <div class="section-header">
      <div class="icon teal">📄</div>
      <div>
        <h2>Document Summarisation</h2>
        <p>Handles 3 distinct source types: SAE Case Narration · Application Checklist · Meeting Transcript</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    doc_type = st.selectbox("Select document type", [
        "SAE Case Narration","Application Checklist (SUGAM)","Meeting Transcript / Audio Transcript"])
    sum_input = st.text_area("Paste document content", height=240, key="sum_input")

    col1, col2, col3 = st.columns([1,1,3])
    with col1:
        run_sum = st.button("📄 Summarise Document", type="primary", use_container_width=True)

    if run_sum and sum_input.strip():
        text = sum_input.lower()
        st.markdown('<hr class="divider">', unsafe_allow_html=True)

        if doc_type == "SAE Case Narration":
            priority = "URGENT" if any(w in text for w in ["death","fatal","died","disability","permanent"]) else \
                       "STANDARD" if any(w in text for w in ["hospitalised","admitted","icu","inpatient"]) else "LOW"
            causality = "Possibly Related" if "possibly" in text else \
                        "Probably Related" if "probably" in text else \
                        "Unrelated" if "unrelated" in text else \
                        "Definitely Related" if "definitely" in text else "Under Assessment"
            outcome = "Fatal" if any(w in text for w in ["died","death","fatal"]) else \
                      "Recovering" if any(w in text for w in ["recovering","improving"]) else \
                      "Recovered" if "recovered" in text else "Ongoing"
            p_color = "#dc2626" if priority=="URGENT" else "#d97706" if priority=="STANDARD" else "#16a34a"
            card_cls = "danger" if priority=="URGENT" else "warning" if priority=="STANDARD" else "success"
            st.markdown(f'<div class="result-card {card_cls}"><b>Priority: {priority}</b> — {causality} · Outcome: {outcome}</div>', unsafe_allow_html=True)
            c1,c2,c3 = st.columns(3)
            c1.metric("Causality", causality)
            c2.metric("Outcome", outcome)
            c3.metric("Priority", priority)
            summary_txt = f"Causality: {causality}\nOutcome: {outcome}\nPriority: {priority}\nRecommended Action: {'Immediate escalation to DCGI' if priority=='URGENT' else 'Standard review queue'}"
            st.download_button("⬇ Download SAE Summary", summary_txt, file_name="sae_summary.txt")

        elif doc_type == "Application Checklist (SUGAM)":
            lines = [l.strip() for l in sum_input.split('\n') if l.strip()]
            complete   = sum(1 for l in lines if any(w in l.lower() for w in ["complete","present","yes","submitted","available","provided"]))
            missing    = sum(1 for l in lines if any(w in l.lower() for w in ["missing","absent","no","not submitted"]))
            incomplete = sum(1 for l in lines if any(w in l.lower() for w in ["incomplete","pending","partial"]))
            total = len(lines); score = round((complete/total)*100) if total else 0
            rec = "✅ Approve for Review" if score>=80 else "⚠️ Return for Completion" if score>=50 else "❌ Reject"
            c1,c2,c3,c4 = st.columns(4)
            c1.metric("Total", total); c2.metric("Complete", complete)
            c3.metric("Incomplete", incomplete); c4.metric("Missing", missing)
            st.progress(score/100, text=f"Completeness Score: {score}%")
            card_cls = "success" if score>=80 else "warning" if score>=50 else "danger"
            st.markdown(f'<div class="result-card {card_cls}"><b>Recommendation:</b> {rec}</div>', unsafe_allow_html=True)
            st.download_button("⬇ Download Summary", f"Score:{score}%\nRecommendation:{rec}", file_name="checklist_summary.txt")

        else:
            lines = sum_input.split('\n')
            decisions, actions, issues = [], [], []
            for line in lines:
                ll = line.lower()
                if any(w in ll for w in ["decided","approved","resolved","agreed","concluded"]):
                    decisions.append(line.strip())
                elif any(w in ll for w in ["action","will","shall","to be done","responsible","follow up"]):
                    actions.append(line.strip())
                elif any(w in ll for w in ["pending","unresolved","defer","tabled"]):
                    issues.append(line.strip())
            c1,c2,c3 = st.columns(3)
            c1.metric("Decisions", len(decisions)); c2.metric("Actions", len(actions)); c3.metric("Open Issues", len(issues))
            if decisions:
                st.markdown("**Key Decisions**")
                for i,d in enumerate(decisions[:5],1): st.markdown(f"{i}. {d}")
            if actions:
                st.markdown("**Action Items**")
                for i,a in enumerate(actions[:6],1): st.markdown(f"{i}. {a}")
            if issues:
                st.markdown("**Unresolved Issues**")
                for i,x in enumerate(issues[:4],1): st.markdown(f"{i}. {x}")
            st.download_button("⬇ Download Meeting Summary", "\n".join(decisions+actions), file_name="meeting_summary.txt")
    elif run_sum:
        st.markdown('<div class="result-card warning">Please paste document content first.</div>', unsafe_allow_html=True)


# ── TAB 3 — COMPLETENESS ─────────────────────────────────────────────────────
with tab3:
    st.markdown("""
    <div class="section-header">
      <div class="icon purple">✅</div>
      <div>
        <h2>Completeness Assessment — Schedule Y</h2>
        <p>Verifies 20 mandatory CDSCO Schedule Y fields · RAG status · Automated recommendation</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    SCHEDULE_Y = [
        ("Protocol Synopsis","protocol synopsis","Critical"),
        ("Investigator Brochure","investigator brochure","Critical"),
        ("Form CT-04","ct-04","Critical"),
        ("Form CT-05","ct-05","Critical"),
        ("Ethics Committee Approval","ethics committee","Critical"),
        ("Informed Consent Form (English)","informed consent","Critical"),
        ("Informed Consent Form (Local Language)","local language","Critical"),
        ("Investigator CV","investigator cv","Major"),
        ("Site Master File","site master","Major"),
        ("Insurance Certificate","insurance","Major"),
        ("Drug Import License","import license","Major"),
        ("GCP Compliance Certificate","gcp","Major"),
        ("Patient Information Sheet","patient information","Major"),
        ("Case Report Form Template","case report form","Minor"),
        ("Statistical Analysis Plan","statistical analysis","Minor"),
        ("DSMB Charter","dsmb","Minor"),
        ("Pharmacovigilance Plan","pharmacovigilance","Minor"),
        ("Risk Management Plan","risk management","Minor"),
        ("Regulatory Approval (Country of Origin)","regulatory approval","Major"),
        ("Sponsor Authorisation Letter","sponsor authorisation","Major"),
    ]

    col_a, col_b = st.columns([2,1])
    with col_a:
        comp_input = st.text_area("Paste application checklist or document index", height=220, key="comp_input")
    with col_b:
        app_id = st.text_input("Application ID", placeholder="e.g. SUGAM-CT-2024-0892")
        st.markdown("<br>", unsafe_allow_html=True)
        run_comp = st.button("✅ Run Completeness Check", type="primary", use_container_width=True)

    if run_comp and comp_input.strip():
        text_lower = comp_input.lower()
        results = []
        critical_missing, major_missing = [], []
        for field, keyword, severity in SCHEDULE_Y:
            if keyword in text_lower:
                if any(w in text_lower for w in ["pending","to be submitted","tbd","partial"]):
                    status="INCOMPLETE"; rag="🟡 Amber"
                else:
                    status="PRESENT"; rag="🟢 Green"
            else:
                status="MISSING"; rag="🔴 Red"
                if severity=="Critical": critical_missing.append(field)
                elif severity=="Major":  major_missing.append(field)
            results.append({"Field":field,"Severity":severity,"Status":status,"RAG":rag})

        df_comp = pd.DataFrame(results)
        present    = sum(1 for r in results if r["Status"]=="PRESENT")
        incomplete = sum(1 for r in results if r["Status"]=="INCOMPLETE")
        missing    = sum(1 for r in results if r["Status"]=="MISSING")
        score      = round((present/len(results))*100)
        rec = "✅ Approve for Technical Review" if score>=85 and not critical_missing else \
              "⚠️ Return for Completion" if score>=60 else "❌ Reject — Critical fields missing"
        card_cls = "success" if score>=85 and not critical_missing else "warning" if score>=60 else "danger"

        st.markdown(f"### {'Application ' + app_id if app_id else 'Completeness Report'}")
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Total Fields",20); c2.metric("Present",present)
        c3.metric("Incomplete",incomplete); c4.metric("Missing",missing)
        st.progress(score/100, text=f"Schedule Y Completeness: {score}%")
        st.markdown(f'<div class="result-card {card_cls}"><b>Recommendation:</b> {rec}</div>', unsafe_allow_html=True)

        if critical_missing:
            st.error(f"Critical missing: {', '.join(critical_missing)}")
        if major_missing:
            st.warning(f"Major missing: {', '.join(major_missing)}")

        def style_rag(val):
            if "Green" in str(val): return "background-color:#dcfce7;color:#15803d;font-weight:600"
            if "Amber" in str(val): return "background-color:#fef9c3;color:#a16207;font-weight:600"
            if "Red"   in str(val): return "background-color:#fee2e2;color:#b91c1c;font-weight:600"
            return ""
        st.markdown('<div class="table-wrapper">', unsafe_allow_html=True)
        st.dataframe(df_comp.style.applymap(style_rag, subset=["RAG"]), use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.download_button("⬇ Download Report", df_comp.to_csv(index=False), file_name="completeness_report.csv", mime="text/csv")
    elif run_comp:
        st.markdown('<div class="result-card warning">Please paste application content first.</div>', unsafe_allow_html=True)


# ── TAB 4 — CLASSIFICATION ───────────────────────────────────────────────────
with tab4:
    st.markdown("""
    <div class="section-header">
      <div class="icon amber">🏷️</div>
      <div>
        <h2>SAE Classification & Prioritisation</h2>
        <p>ICD-10 keyword mapping · Severity grading · Duplicate detection · Review queue ordering</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    class_input = st.text_area("Paste SAE report for classification", height=200, key="class_input")
    st.markdown("**Duplicate Detection** — paste additional reports to cross-check")
    c1c, c2c = st.columns(2)
    with c1c: dup2 = st.text_area("SAE Report 2 (optional)", height=90, key="dup2")
    with c2c: dup3 = st.text_area("SAE Report 3 (optional)", height=90, key="dup3")

    col1, col2, col3 = st.columns([1,1,3])
    with col1:
        run_class = st.button("🏷️ Classify Case", type="primary", use_container_width=True)

    if run_class and class_input.strip():
        text = class_input.lower()
        if any(w in text for w in ["died","fatal","death","mortality","deceased"]):
            severity="DEATH"; sev_cls="sev-death"; priority_score=1
            reason_keywords=[w for w in ["died","fatal","death","mortality","deceased"] if w in text]
        elif any(w in text for w in ["permanent disability","paralysis","blind","deaf","permanent impairment"]):
            severity="DISABILITY"; sev_cls="sev-disab"; priority_score=2
            reason_keywords=[w for w in ["permanent disability","paralysis","blind","deaf"] if w in text]
        elif any(w in text for w in ["hospitalised","admitted","icu","inpatient","emergency admission","hospital"]):
            severity="HOSPITALISATION"; sev_cls="sev-hosp"; priority_score=3
            reason_keywords=[w for w in ["hospitalised","admitted","icu","inpatient","hospital"] if w in text]
        else:
            severity="OTHERS"; sev_cls="sev-other"; priority_score=4
            reason_keywords=["no critical keywords matched — default classification"]

        confidence="HIGH" if len(reason_keywords)>=3 else "MEDIUM" if len(reason_keywords)>=1 else "LOW"
        icd_map={"DEATH":"R96.x / R98 / R99","DISABILITY":"S00-T98 (permanent)","HOSPITALISATION":"Z75.1","OTHERS":"MedDRA PT"}
        report_map={"DEATH":"Expedited — 7 days (fatal)","DISABILITY":"Expedited — 15 days","HOSPITALISATION":"Expedited — 15 days","OTHERS":"Periodic — 90 days"}

        st.markdown(f'<div class="{sev_cls}">⬤ {severity}</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        c1,c2,c3 = st.columns(3)
        c1.metric("Severity",severity); c2.metric("Confidence",confidence); c3.metric("Priority Score",f"{priority_score}/4")
        st.markdown(f'<div class="result-card info"><b>Classification Reason:</b> Classified as <b>{severity}</b> because the following keywords were found: <i>{", ".join(reason_keywords)}</i>.<br>ICD-10 Reference: {icd_map[severity]} · Reporting: {report_map[severity]}</div>', unsafe_allow_html=True)

        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown("**Duplicate Detection**")
        def extract_ids(t):
            return (set(re.findall(r'\b(?:PT|SUBJ)[-]\w+[-]\w+\b',t)),
                    set(re.findall(r'\b[A-Z]{4,}[-]?\d+\s*mg\b',t)))
        id1,d1 = extract_ids(class_input); dup_found=False
        for i,other in enumerate([dup2,dup3],2):
            if other.strip():
                id2,d2 = extract_ids(other)
                if id1&id2 or d1&d2:
                    st.markdown(f'<div class="result-card danger">⚠️ DUPLICATE DETECTED — Report {i} shares identifiers with Report 1.</div>', unsafe_allow_html=True)
                    dup_found=True
        if not dup_found:
            st.markdown('<div class="result-card success">✓ No duplicates detected across provided reports.</div>', unsafe_allow_html=True)

        result_text=f"Severity:{severity}\nConfidence:{confidence}\nReason:{', '.join(reason_keywords)}\nPriority:{priority_score}/4\nICD-10:{icd_map[severity]}\nTimeline:{report_map[severity]}"
        st.download_button("⬇ Download Classification Report", result_text, file_name="classification_report.txt")
    elif run_class:
        st.markdown('<div class="result-card warning">Please paste an SAE report first.</div>', unsafe_allow_html=True)


# ── TAB 5 — COMPARISON ───────────────────────────────────────────────────────
with tab5:
    st.markdown("""
    <div class="section-header">
      <div class="icon sky">🔍</div>
      <div>
        <h2>Document Comparison</h2>
        <p>Identifies substantive vs administrative changes · Version-to-version diff · Downloadable change report</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.markdown("**Version 1 — Original**")
        v1 = st.text_area("", height=220, key="v1", placeholder="Paste original document...")
    with col_v2:
        st.markdown("**Version 2 — Updated**")
        v2 = st.text_area("", height=220, key="v2", placeholder="Paste updated document...")

    col1, col2, col3 = st.columns([1,1,3])
    with col1:
        run_comp5 = st.button("🔍 Compare Documents", type="primary", use_container_width=True)

    if run_comp5 and v1.strip() and v2.strip():
        lines1=[l.strip() for l in v1.splitlines() if l.strip()]
        lines2=[l.strip() for l in v2.splitlines() if l.strip()]
        matcher=difflib.SequenceMatcher(None,lines1,lines2)
        SUBST_KW=["dose","dosage","mg","ml","death","disability","outcome","causality","adverse",
                  "event","date","patient","diagnosis","icd","treatment","safety","efficacy","result","risk"]
        changes=[]
        for tag,i1,i2,j1,j2 in matcher.get_opcodes():
            if tag=="replace":
                for old,new in zip(lines1[i1:i2],lines2[j1:j2]):
                    is_sub=any(k in old.lower() or k in new.lower() for k in SUBST_KW)
                    changes.append({"Change Type":"CHANGED","Original":old,"New":new,"Substantive":"Yes" if is_sub else "No","Category":"Substantive" if is_sub else "Administrative"})
            elif tag=="delete":
                for line in lines1[i1:i2]:
                    is_sub=any(k in line.lower() for k in SUBST_KW)
                    changes.append({"Change Type":"REMOVED","Original":line,"New":"—","Substantive":"Yes" if is_sub else "No","Category":"Substantive" if is_sub else "Administrative"})
            elif tag=="insert":
                for line in lines2[j1:j2]:
                    is_sub=any(k in line.lower() for k in SUBST_KW)
                    changes.append({"Change Type":"ADDED","Original":"—","New":line,"Substantive":"Yes" if is_sub else "No","Category":"Substantive" if is_sub else "Administrative"})

        sub_count=sum(1 for c in changes if c["Substantive"]=="Yes")
        c1,c2,c3,c4,c5=st.columns(5)
        c1.metric("Total Changes",len(changes)); c2.metric("Added",sum(1 for c in changes if c["Change Type"]=="ADDED"))
        c3.metric("Removed",sum(1 for c in changes if c["Change Type"]=="REMOVED"))
        c4.metric("Changed",sum(1 for c in changes if c["Change Type"]=="CHANGED"))
        c5.metric("Substantive",sub_count)

        if sub_count>0:
            st.markdown(f'<div class="result-card danger">⚠️ {sub_count} substantive change(s) detected — require regulatory review.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="result-card success">✓ No substantive changes detected.</div>', unsafe_allow_html=True)

        if changes:
            df_diff=pd.DataFrame(changes)
            def style_diff(row):
                if row["Change Type"]=="ADDED":    return ["background-color:#dcfce7"]*len(row)
                if row["Change Type"]=="REMOVED":  return ["background-color:#fee2e2"]*len(row)
                if row["Substantive"]=="Yes":      return ["background-color:#fef9c3"]*len(row)
                return [""]*len(row)
            st.markdown('<div class="table-wrapper">', unsafe_allow_html=True)
            st.dataframe(df_diff.style.apply(style_diff,axis=1), use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.caption("🟢 Added · 🔴 Removed · 🟡 Changed (Substantive)")
            st.download_button("⬇ Download Comparison Report", df_diff.to_csv(index=False), file_name="comparison_report.csv", mime="text/csv")
        else:
            st.markdown('<div class="result-card success">Documents are identical — no changes found.</div>', unsafe_allow_html=True)
    elif run_comp5:
        st.markdown('<div class="result-card warning">Please paste both document versions.</div>', unsafe_allow_html=True)


# ── TAB 6 — INSPECTION REPORT ────────────────────────────────────────────────
with tab6:
    st.markdown("""
    <div class="section-header">
      <div class="icon pink">📋</div>
      <div>
        <h2>Inspection Report Generation</h2>
        <p>Raw observations → Formal CDSCO GCP inspection report · Critical / Major / Minor classification</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    with col_f1: inspector_name = st.text_input("Inspector Name", placeholder="Dr. A.K. Sharma")
    with col_f2: site_name      = st.text_input("Site Name", placeholder="AIIMS Delhi — Cardiology")
    with col_f3: site_number    = st.text_input("Site Number", placeholder="SITE-DEL-001")
    with col_f4: inspection_date = st.date_input("Inspection Date")

    obs_input = st.text_area("Paste raw inspection observations (one per line)", height=200, key="obs_input",
        placeholder="No record of drug accountability for subjects 3 and 7\nInformed consent form missing local language version\nMinor labelling issue on sample storage boxes")

    col1, col2, col3 = st.columns([1,1,3])
    with col1:
        run_insp = st.button("📋 Generate Report", type="primary", use_container_width=True)

    if run_insp and obs_input.strip():
        observations=[o.strip() for o in obs_input.splitlines() if o.strip()]
        CRITICAL_KW=["no record","falsified","patient safety","data integrity","unaccounted","missing","fraud"]
        MAJOR_KW=["incomplete","not documented","protocol deviation","untrained","not signed","not dated","expired"]
        report_rows=[]
        for i,obs in enumerate(observations,1):
            ol=obs.lower()
            if any(k in ol for k in CRITICAL_KW):
                risk="Critical"; deadline="15 days"; corrective="Immediate CAPA required. Site operations may be suspended."
            elif any(k in ol for k in MAJOR_KW):
                risk="Major"; deadline="30 days"; corrective="CAPA plan required within 30 days."
            else:
                risk="Minor"; deadline="60 days"; corrective="Document corrective action in site log."
            formal=f"During the inspection on {inspection_date.strftime('%d %B %Y')}, it was observed that {obs.lower().rstrip('.')}. This constitutes a {risk.lower()} GCP deviation."
            report_rows.append({"Obs No.":f"OBS-{i:03d}","Raw Observation":obs,"Formal Finding":formal,"Risk Level":risk,"Corrective Action":corrective,"Deadline":deadline})

        critical_c=sum(1 for r in report_rows if r["Risk Level"]=="Critical")
        major_c   =sum(1 for r in report_rows if r["Risk Level"]=="Major")
        minor_c   =sum(1 for r in report_rows if r["Risk Level"]=="Minor")

        c1,c2,c3=st.columns(3)
        c1.metric("Critical",critical_c); c2.metric("Major",major_c); c3.metric("Minor",minor_c)

        if critical_c>0:
            st.markdown(f'<div class="result-card danger">⚠️ {critical_c} Critical finding(s) — Immediate CAPA required.</div>', unsafe_allow_html=True)
        elif major_c>0:
            st.markdown(f'<div class="result-card warning">⚠️ {major_c} Major finding(s) — CAPA plan due in 30 days.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="result-card success">✓ No Critical or Major findings.</div>', unsafe_allow_html=True)

        df_report=pd.DataFrame(report_rows)
        def style_risk(val):
            if val=="Critical": return "background-color:#fee2e2;color:#991b1b;font-weight:700"
            if val=="Major":    return "background-color:#fef9c3;color:#92400e;font-weight:700"
            if val=="Minor":    return "background-color:#dcfce7;color:#166534"
            return ""
        st.markdown('<div class="table-wrapper">', unsafe_allow_html=True)
        st.dataframe(df_report.style.applymap(style_risk,subset=["Risk Level"]), use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

        full_report=f"CDSCO GCP SITE INSPECTION REPORT\n{'='*50}\nSite: {site_name}\nSite No: {site_number}\nDate: {inspection_date.strftime('%d %B %Y')}\nInspector: {inspector_name}\nSummary: {critical_c} Critical | {major_c} Major | {minor_c} Minor\n{'='*50}\n\n"
        for r in report_rows:
            full_report+=f"{r['Obs No.']} | {r['Risk Level'].upper()}\nFinding: {r['Formal Finding']}\nCorrective Action: {r['Corrective Action']}\nDeadline: {r['Deadline']}\n{'-'*50}\n\n"
        full_report+=f"Inspector: {inspector_name}\nSignature: _______________\nDate: {datetime.date.today().strftime('%d %B %Y')}"
        st.download_button("⬇ Download Inspection Report", full_report, file_name="cdsco_inspection_report.txt", mime="text/plain")
    elif run_insp:
        st.markdown('<div class="result-card warning">Please enter at least one inspection observation.</div>', unsafe_allow_html=True)
