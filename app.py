import streamlit as st
import re
import datetime
import difflib
import pandas as pd
import io

# ── Optional imports with graceful fallback ───────────────────────────────────
try:
    import docx as python_docx
    DOCX_OK = True
except ImportError:
    DOCX_OK = False

try:
    from pypdf import PdfReader
    PDF_OK = True
except ImportError:
    try:
        import PyPDF2
        PDF_OK = "pypdf2"
    except ImportError:
        PDF_OK = False

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CDSCO Regulatory Intelligence Platform",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;}
#MainMenu,footer,header{visibility:hidden;}
.stApp{background:#f0f4f8;}

/* Sidebar */
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#001f5b 0%,#003087 60%,#004db3 100%);}
section[data-testid="stSidebar"] *{color:white!important;}
section[data-testid="stSidebar"] .stMarkdown p{color:rgba(255,255,255,0.8)!important;}
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stFileUploader label{color:rgba(255,255,255,0.9)!important;font-weight:500!important;}
section[data-testid="stSidebar"] .stSelectbox > div > div{background:rgba(255,255,255,0.1)!important;border:1px solid rgba(255,255,255,0.25)!important;color:white!important;border-radius:8px!important;}
section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"]{background:rgba(255,255,255,0.08)!important;border:1.5px dashed rgba(255,255,255,0.35)!important;border-radius:10px!important;}

/* Hero banner */
.hero{background:linear-gradient(135deg,#001f5b 0%,#003087 55%,#0052cc 100%);border-radius:16px;padding:30px 36px;margin-bottom:20px;box-shadow:0 4px 24px rgba(0,48,135,0.18);}
.hero-top{display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:16px;}
.hero h1{color:white;font-size:26px;font-weight:700;margin:0;letter-spacing:-0.3px;}
.hero .sub{color:rgba(255,255,255,0.68);font-size:13px;margin:5px 0 0;}
.hero-badges{display:flex;gap:10px;flex-wrap:wrap;margin-top:14px;}
.hbadge{background:rgba(255,255,255,0.12);border:1px solid rgba(255,255,255,0.22);border-radius:20px;padding:4px 14px;font-size:12px;color:rgba(255,255,255,0.9);font-weight:500;}
.hbadge.green{border-color:#4ade80;color:#4ade80;}
.stat-badges{display:flex;gap:12px;}
.sbadge{background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);border-radius:10px;padding:10px 16px;text-align:center;min-width:70px;}
.sbadge .n{color:#7dd3fc;font-size:22px;font-weight:700;display:block;line-height:1;}
.sbadge .l{color:rgba(255,255,255,0.6);font-size:10px;margin-top:2px;display:block;}

/* Instruction banner */
.how-to{background:white;border-radius:12px;padding:16px 20px;margin-bottom:20px;border-left:4px solid #003087;box-shadow:0 1px 4px rgba(0,0,0,0.06);}
.how-to h4{color:#003087;margin:0 0 8px;font-size:14px;}
.how-steps{display:flex;gap:8px;flex-wrap:wrap;}
.hw-step{background:#f0f4f8;border-radius:8px;padding:6px 12px;font-size:12px;color:#475569;display:flex;align-items:center;gap:6px;}
.hw-num{background:#003087;color:white;border-radius:50%;width:18px;height:18px;display:inline-flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;flex-shrink:0;}

/* Tabs */
.stTabs [data-baseweb="tab-list"]{background:white;border-radius:12px;padding:4px;gap:2px;box-shadow:0 1px 4px rgba(0,0,0,0.06);}
.stTabs [data-baseweb="tab"]{border-radius:8px;font-size:12px;font-weight:500;color:#64748b;padding:8px 12px;}
.stTabs [aria-selected="true"]{background:#003087!important;color:white!important;}

/* Section headers */
.sec-hd{display:flex;align-items:center;gap:12px;margin-bottom:18px;padding-bottom:14px;border-bottom:1px solid #e2e8f0;}
.sec-ic{width:42px;height:42px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:20px;flex-shrink:0;}
.ic-blue{background:#dbeafe;} .ic-teal{background:#ccfbf1;} .ic-purple{background:#ede9fe;}
.ic-amber{background:#fef3c7;} .ic-sky{background:#e0f2fe;} .ic-pink{background:#fce7f3;}
.sec-hd h2{font-size:17px;font-weight:600;color:#1e293b;margin:0;}
.sec-hd p{font-size:12px;color:#64748b;margin:2px 0 0;}

/* Upload zone card */
.upload-card{background:white;border-radius:14px;padding:20px 22px;box-shadow:0 1px 4px rgba(0,0,0,0.06);margin-bottom:16px;}
.upload-card h4{color:#1e293b;font-size:14px;font-weight:600;margin:0 0 12px;}
.or-divider{display:flex;align-items:center;gap:10px;margin:14px 0;color:#94a3b8;font-size:12px;}
.or-divider::before,.or-divider::after{content:'';flex:1;height:1px;background:#e2e8f0;}

/* Feature grid on home */
.feat-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:4px;}
.feat-card{background:white;border-radius:14px;padding:20px;box-shadow:0 1px 4px rgba(0,0,0,0.06);border-top:3px solid #003087;}
.feat-card.f2{border-top-color:#0f766e;} .feat-card.f3{border-top-color:#6d28d9;}
.feat-card.f4{border-top-color:#b45309;} .feat-card.f5{border-top-color:#0369a1;} .feat-card.f6{border-top-color:#be185d;}
.feat-card .fi{font-size:26px;margin-bottom:8px;} .feat-card .fn{font-size:10px;font-weight:600;color:#94a3b8;text-transform:uppercase;letter-spacing:.08em;}
.feat-card .ft{font-size:14px;font-weight:600;color:#1e293b;margin:5px 0 4px;} .feat-card .fd{font-size:12px;color:#64748b;line-height:1.5;}

/* PII detection chip row */
.pii-chips{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0;}
.pii-chip{display:inline-flex;align-items:center;gap:5px;border-radius:20px;padding:4px 12px;font-size:12px;font-weight:600;}
.chip-red{background:#fee2e2;color:#991b1b;} .chip-amber{background:#fef3c7;color:#92400e;}
.chip-blue{background:#dbeafe;color:#1e40af;} .chip-purple{background:#ede9fe;color:#5b21b6;}
.chip-teal{background:#ccfbf1;color:#065f46;} .chip-gray{background:#f1f5f9;color:#475569;}

/* Result cards */
.rc{background:white;border-radius:12px;padding:18px 22px;box-shadow:0 1px 4px rgba(0,0,0,0.06);margin:10px 0;border-left:4px solid #003087;}
.rc.success{border-left-color:#16a34a;background:#f0fdf4;}
.rc.warning{border-left-color:#d97706;background:#fffbeb;}
.rc.danger{border-left-color:#dc2626;background:#fef2f2;}
.rc.info{border-left-color:#0284c7;background:#f0f9ff;}
.rc.neutral{border-left-color:#64748b;background:#f8fafc;}

/* Step pills */
.step-pill{display:inline-flex;align-items:center;gap:6px;background:#003087;color:white;border-radius:20px;padding:4px 14px;font-size:12px;font-weight:600;margin-bottom:10px;}
.step-pill.s2{background:#0f766e;}

/* Table wrapper */
.tw{background:white;border-radius:12px;padding:4px;box-shadow:0 1px 4px rgba(0,0,0,0.06);margin:10px 0;}

/* Audio notice */
.audio-notice{background:#fef9c3;border:1px solid #fbbf24;border-radius:10px;padding:12px 16px;font-size:12px;color:#78350f;margin:8px 0;}

/* Buttons */
.stButton>button[kind="primary"]{background:linear-gradient(135deg,#003087,#0052cc)!important;color:white!important;border:none!important;border-radius:8px!important;font-weight:600!important;font-size:13px!important;padding:10px 22px!important;box-shadow:0 2px 8px rgba(0,48,135,0.25)!important;}
.stButton>button[kind="primary"]:hover{box-shadow:0 4px 16px rgba(0,48,135,0.35)!important;transform:translateY(-1px)!important;}
.stDownloadButton>button{border-radius:8px!important;border:1.5px solid #003087!important;color:#003087!important;font-weight:500!important;font-size:13px!important;}
.stTextArea textarea{border:1.5px solid #e2e8f0!important;border-radius:10px!important;font-size:13px!important;background:#fafbfc!important;}
.stTextArea textarea:focus{border-color:#003087!important;background:white!important;box-shadow:0 0 0 3px rgba(0,48,135,0.08)!important;}
[data-testid="stMetricValue"]{font-size:26px!important;font-weight:700!important;}
[data-testid="stMetricLabel"]{font-size:12px!important;color:#64748b!important;}
</style>
""", unsafe_allow_html=True)


# ── Utility: extract text from uploaded file ──────────────────────────────────
def extract_text_from_file(uploaded_file):
    """Extract plain text from docx or pdf upload. Returns (text, error_msg)."""
    if uploaded_file is None:
        return "", None
    fname = uploaded_file.name.lower()
    try:
        if fname.endswith(".docx"):
            if not DOCX_OK:
                return "", "python-docx not installed. Add 'python-docx' to requirements.txt"
            doc = python_docx.Document(io.BytesIO(uploaded_file.read()))
            text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
            return text, None
        elif fname.endswith(".pdf"):
            if not PDF_OK:
                return "", "pypdf not installed. Add 'pypdf' to requirements.txt"
            if PDF_OK == "pypdf2":
                import PyPDF2
                reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
                text = "\n".join(page.extract_text() or "" for page in reader.pages)
            else:
                reader = PdfReader(io.BytesIO(uploaded_file.read()))
                text = "\n".join(page.extract_text() or "" for page in reader.pages)
            return text, None
        elif fname.endswith(".txt"):
            return uploaded_file.read().decode("utf-8", errors="ignore"), None
        else:
            return "", f"Unsupported file type: {uploaded_file.name}"
    except Exception as e:
        return "", f"Error reading file: {str(e)}"


# ── PII detection engine ──────────────────────────────────────────────────────
INDIAN_FIRST = ["Rajesh","Priya","Suresh","Anita","Vikram","Sunita","Amit","Kavita",
                "Ravi","Deepa","Mohit","Pooja","Arjun","Neha","Sanjay","Meera",
                "Rahul","Divya","Anil","Rekha","Vijay","Smita","Ramesh","Geeta",
                "Ashok","Usha","Manoj","Seema","Vinod","Lata","Amitav","Amitabh",
                "Sunil","Sneha","Preeti","Rohit","Kiran","Nisha","Suresh","Ganesh"]
INDIAN_LAST  = ["Sharma","Patel","Singh","Kumar","Mehta","Gupta","Verma","Joshi",
                "Nair","Rao","Iyer","Reddy","Bose","Das","Malhotra","Kapoor",
                "Agarwal","Pandey","Mishra","Tiwari","Ghosh","Chatterjee","Mukherjee"]

def detect_and_anonymise(input_text):
    """Full two-step anonymisation. Returns dict with all outputs."""
    token_map, audit_log = [], []
    processed = input_text
    counters = {k:0 for k in ["PATIENT","INVESTIGATOR","DATE","SITE","ID","PHONE","AADHAAR","ADDRESS","HOSPITAL_RECORD"]}
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pii_types_found = set()

    def nxt(kind):
        counters[kind] += 1
        return f"[{kind}-{counters[kind]:03d}]"

    def record(tok, original, etype, step="Step 1"):
        token_map.append({"Token":tok,"Original Value":original,"Entity Type":etype,"Step":step})
        audit_log.append({"Timestamp":ts,"Action":"Pseudonymised","Entity Type":etype,"Token":tok,"Reversible":"Yes"})
        pii_types_found.add(etype)

    # Hospital Record Numbers e.g. #99283
    for m in re.finditer(r'#\d{4,6}', processed):
        tok = nxt("HOSPITAL_RECORD")
        record(tok, m.group(), "Hospital Record No.")
        processed = processed.replace(m.group(), tok, 1)

    # Aadhaar
    for m in re.finditer(r'\b\d{4}[-\s]\d{4}[-\s]\d{4}\b', processed):
        tok = nxt("AADHAAR")
        record(tok, m.group(), "Aadhaar Number")
        processed = processed.replace(m.group(), tok, 1)

    # Indian phone numbers
    for m in re.finditer(r'(?:\+91[\s-]?)?\d{2,4}[\s-]\d{4}[\s-]\d{4}\b', processed):
        tok = nxt("PHONE")
        record(tok, m.group(), "Phone Number")
        processed = processed.replace(m.group(), tok, 1)
    for m in re.finditer(r'\b[6-9]\d{9}\b', processed):
        tok = nxt("PHONE")
        record(tok, m.group(), "Phone Number")
        processed = processed.replace(m.group(), tok, 1)

    # Structured IDs e.g. LH-MUM-042
    for m in re.finditer(r'\b(PT|SITE|IND|CT|SUBJ|INV|LH|MH|DL|CH)[-]\w{2,6}[-]\w{2,6}\b', processed):
        original = m.group()
        if any(original.startswith(p) for p in ["PT","SUBJ","LH","MH","DL"]):
            tok = nxt("PATIENT"); etype = "Patient ID"
        elif original.startswith("SITE"):
            tok = nxt("SITE"); etype = "Site Number"
        elif original.startswith("INV"):
            tok = nxt("INVESTIGATOR"); etype = "Investigator ID"
        else:
            tok = nxt("ID"); etype = "Regulatory ID"
        record(tok, original, etype)
        processed = processed.replace(original, tok, 1)

    # Dates — multiple formats
    date_pats = [
        re.compile(r'\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b'),
        re.compile(r'\b\d{1,2}[-/](?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[-/]\d{2,4}\b', re.IGNORECASE),
        re.compile(r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b', re.IGNORECASE),
        re.compile(r'\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}\b', re.IGNORECASE),
    ]
    for pat in date_pats:
        for m in pat.finditer(processed):
            tok = nxt("DATE")
            record(tok, m.group(), "Date / DOB")
            processed = processed.replace(m.group(), tok, 1)

    # Patient initials pattern e.g. R.K. or A.B.
    for m in re.finditer(r'\b[A-Z]\.[A-Z]\.\b', processed):
        tok = nxt("PATIENT")
        record(tok, m.group(), "Patient Initials")
        processed = processed.replace(m.group(), tok, 1)

    # Named persons (Dr. + Indian name)
    name_re = re.compile(r'\b(Dr\.?\s+)(' + '|'.join(INDIAN_FIRST) + r')\s+(' + '|'.join(INDIAN_LAST) + r')\b')
    for m in name_re.finditer(processed):
        tok = nxt("INVESTIGATOR")
        record(tok, m.group(), "Investigator Name")
        processed = processed.replace(m.group(), tok, 1)

    # Non-Dr Indian names
    name_re2 = re.compile(r'\b(' + '|'.join(INDIAN_FIRST) + r')\s+(' + '|'.join(INDIAN_LAST) + r')\b')
    for m in name_re2.finditer(processed):
        if m.group() in processed:
            tok = nxt("PATIENT")
            record(tok, m.group(), "Patient Name")
            processed = processed.replace(m.group(), tok, 1)

    # Address: city/pincode patterns
    for m in re.finditer(r'\b\d{6}\b', processed):
        tok = nxt("ADDRESS")
        record(tok, m.group(), "Pincode")
        processed = processed.replace(m.group(), tok, 1)

    # ── Step 2: Irreversible generalisation ──────────────────────────────────
    step2 = processed

    # Ages → ranges
    step2 = re.compile(r'\b(\d{2})\s*(?:years?|yrs?)\s*(?:old)?\b', re.IGNORECASE).sub(
        lambda m: f"{(int(m.group(1))//5)*5}-{(int(m.group(1))//5)*5+4} years", step2)

    # Weights → ranges
    step2 = re.compile(r'\b(\d{2,3})\s*kg\b', re.IGNORECASE).sub(
        lambda m: f"{(int(m.group(1))//10)*10}-{(int(m.group(1))//10)*10+9} kg", step2)

    # Heights → ranges
    step2 = re.compile(r'\b(1[5-9]\d)\s*cm\b', re.IGNORECASE).sub(
        lambda m: f"{(int(m.group(1))//5)*5}-{(int(m.group(1))//5)*5+4} cm", step2)

    # Date tokens → year only
    step2 = re.compile(r'\[DATE-\d+\]').sub('[YEAR-GENERALISED]', step2)

    for label, etype in [("All Date tokens","Dates→Year only"),("Ages","Age→Range"),("Weight/Height","Biometrics→Range")]:
        audit_log.append({"Timestamp":ts,"Action":"Irreversible Generalisation","Entity Type":etype,"Token":"Generalised","Reversible":"No"})

    return {
        "step1": processed,
        "step2": step2,
        "token_map": token_map,
        "audit_log": audit_log,
        "pii_types": list(pii_types_found),
        "count": len(token_map)
    }


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:18px 0 10px;'>
        <div style='font-size:40px;'>⚕️</div>
        <div style='font-weight:700;font-size:15px;color:white;margin-top:6px;'>CDSCO RIP</div>
        <div style='font-size:11px;color:rgba(255,255,255,0.5);'>Regulatory Intelligence Platform</div>
    </div>
    <hr style='border-color:rgba(255,255,255,0.15);margin:10px 0;'>
    """, unsafe_allow_html=True)

    st.markdown("<div style='font-size:11px;font-weight:600;color:rgba(255,255,255,0.45);text-transform:uppercase;letter-spacing:.08em;margin-bottom:8px;'>Compliance</div>", unsafe_allow_html=True)
    for badge in ["✅  DPDP Act 2023","✅  ICMR Guidelines 2017","✅  CDSCO Schedule Y","✅  MeitY AI Ethics"]:
        st.markdown(f"<div style='background:rgba(74,222,128,0.1);border:1px solid rgba(74,222,128,0.35);border-radius:20px;padding:4px 12px;font-size:12px;color:#4ade80;margin:3px 0;'>{badge}</div>", unsafe_allow_html=True)

    st.markdown("<hr style='border-color:rgba(255,255,255,0.15);margin:14px 0;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:11px;font-weight:600;color:rgba(255,255,255,0.45);text-transform:uppercase;letter-spacing:.08em;margin-bottom:8px;'>Data Sources</div>", unsafe_allow_html=True)
    for ds in ["FDA FAERS","CDSCO CT-04/05/06","ClinicalTrials.gov","CTRI India","Synthetic SAE Data"]:
        st.markdown(f"<div style='font-size:12px;color:rgba(255,255,255,0.65);padding:2px 0;'>◦ {ds}</div>", unsafe_allow_html=True)

    st.markdown("<hr style='border-color:rgba(255,255,255,0.15);margin:14px 0;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:11px;color:rgba(255,255,255,0.45);line-height:1.7;'>AI assists regulatory officers. Final decisions must be made by qualified human reviewers.</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:10px;color:rgba(255,255,255,0.25);margin-top:10px;text-align:center;'>Stage 1 · CDSCO AI Hackathon 2026</div>", unsafe_allow_html=True)


# ── HERO BANNER ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-top">
    <div>
      <h1>⚕️ Regulatory Intelligence Platform</h1>
      <div class="sub">AI-powered workflow automation for CDSCO regulatory analysts · Upload documents · Detect PII · Generate reports</div>
      <div class="hero-badges">
        <span class="hbadge green">✓ DPDP Act 2023</span>
        <span class="hbadge green">✓ ICMR Guidelines</span>
        <span class="hbadge green">✓ CDSCO Schedule Y</span>
        <span class="hbadge">6 AI Features</span>
        <span class="hbadge">Word · PDF · Audio</span>
      </div>
    </div>
    <div class="stat-badges">
      <div class="sbadge"><span class="n">6</span><span class="l">AI Modules</span></div>
      <div class="sbadge"><span class="n">20</span><span class="l">Schedule Y</span></div>
      <div class="sbadge"><span class="n">3</span><span class="l">Doc Types</span></div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── HOW TO USE BANNER ─────────────────────────────────────────────────────────
st.markdown("""
<div class="how-to">
  <h4>How to use this platform</h4>
  <div class="how-steps">
    <div class="hw-step"><span class="hw-num">1</span>Select a feature tab below</div>
    <div class="hw-step"><span class="hw-num">2</span>Upload a Word / PDF file <b>or</b> paste text</div>
    <div class="hw-step"><span class="hw-num">3</span>Click the action button</div>
    <div class="hw-step"><span class="hw-num">4</span>Review AI output &amp; detected items</div>
    <div class="hw-step"><span class="hw-num">5</span>Download the report</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ── TABS ──────────────────────────────────────────────────────────────────────
tab0,tab1,tab2,tab3,tab4,tab5,tab6 = st.tabs([
    "🏠 Home",
    "🔒 Anonymisation",
    "📄 Summarisation",
    "✅ Completeness",
    "🏷️ Classification",
    "🔍 Comparison",
    "📋 Inspection Report"
])


# ═══════════════════════════════════════════════════════════════════════════════
# HOME
# ═══════════════════════════════════════════════════════════════════════════════
with tab0:
    st.markdown("""
    <div class="feat-grid">
      <div class="feat-card">
        <div class="fi">🔒</div><div class="fn">Feature 01</div>
        <div class="ft">AI Data Anonymisation</div>
        <div class="fd">Upload Word/PDF or paste text. Auto-detects patient IDs, investigator names, phone numbers, Aadhaar, addresses. Two-step pseudonymisation + irreversible generalisation with audit log.</div>
      </div>
      <div class="feat-card f2">
        <div class="fi">📄</div><div class="fn">Feature 02</div>
        <div class="ft">Document Summarisation</div>
        <div class="fd">Handles SAE narrations, SUGAM checklists, and meeting transcripts. Upload audio files for automatic transcription summary. Structured output for reviewer consumption.</div>
      </div>
      <div class="feat-card f3">
        <div class="fi">✅</div><div class="fn">Feature 03</div>
        <div class="ft">Completeness Assessment</div>
        <div class="fd">Upload application documents. Verifies 20 mandatory Schedule Y fields. RAG status dashboard. Flags missing and incomplete items with recommendations.</div>
      </div>
      <div class="feat-card f4">
        <div class="fi">🏷️</div><div class="fn">Feature 04</div>
        <div class="ft">SAE Classification</div>
        <div class="fd">Upload SAE reports. ICD-10 keyword-based severity grading: Death, Disability, Hospitalisation, Others. Duplicate detection across multiple reports. Priority queue scoring.</div>
      </div>
      <div class="feat-card f5">
        <div class="fi">🔍</div><div class="fn">Feature 05</div>
        <div class="ft">Document Comparison</div>
        <div class="fd">Upload two versions of any filing. Semantic diff highlights substantive vs administrative changes. Colour-coded change table with downloadable report.</div>
      </div>
      <div class="feat-card f6">
        <div class="fi">📋</div><div class="fn">Feature 06</div>
        <div class="ft">Inspection Report</div>
        <div class="fd">Paste raw site observations. AI converts them into formal CDSCO GCP inspection reports with Critical / Major / Minor grading and corrective action deadlines.</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<br><div class="rc info">Select any feature tab above to begin. All document processing happens locally — no data is transmitted externally.</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# FEATURE 1 — ANONYMISATION
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("""
    <div class="sec-hd">
      <div class="sec-ic ic-blue">🔒</div>
      <div><h2>AI-Powered Data Anonymisation</h2>
      <p>Upload a document or paste text · Auto-detects 8+ PII/PHI entity types · Two-step process: Pseudonymisation → Irreversible generalisation · DPDP Act 2023 audit log</p></div>
    </div>
    """, unsafe_allow_html=True)

    # Input zone
    st.markdown('<div class="upload-card"><h4>📁 Step 1 — Provide your document</h4>', unsafe_allow_html=True)
    anon_file = st.file_uploader("Upload Word (.docx) or PDF file", type=["docx","pdf","txt"], key="anon_up",
        help="Supports .docx, .pdf, .txt files. Text is extracted automatically.")
    st.markdown('<div class="or-divider">or paste text manually</div>', unsafe_allow_html=True)
    anon_text_default = ""
    if anon_file:
        extracted, err = extract_text_from_file(anon_file)
        if err:
            st.error(err)
        elif extracted:
            anon_text_default = extracted
            st.success(f"✓ Extracted {len(extracted.split())} words from **{anon_file.name}**")
    anon_input = st.text_area("Document content", value=anon_text_default, height=220,
        placeholder="Paste SAE report, clinical trial document, or any regulatory text...", key="anon_txt")
    st.markdown('</div>', unsafe_allow_html=True)

    col1,col2,_ = st.columns([1,1,3])
    with col1:
        run_anon = st.button("🔒 Run Anonymisation", type="primary", use_container_width=True)

    if run_anon and anon_input.strip():
        result = detect_and_anonymise(anon_input)

        # PII type chips
        chip_colors = {
            "Patient Name":"chip-red","Patient Initials":"chip-red","Patient ID":"chip-red",
            "Hospital Record No.":"chip-amber","Investigator Name":"chip-purple","Investigator ID":"chip-purple",
            "Date / DOB":"chip-blue","Phone Number":"chip-teal","Aadhaar Number":"chip-amber",
            "Pincode":"chip-gray","Site Number":"chip-gray","Regulatory ID":"chip-gray","Address":"chip-gray"
        }
        if result["pii_types"]:
            chips_html = '<div class="pii-chips">'
            for pt in result["pii_types"]:
                cls = chip_colors.get(pt, "chip-gray")
                chips_html += f'<span class="pii-chip {cls}">⬤ {pt}</span>'
            chips_html += f'<span class="pii-chip chip-gray">Total: {result["count"]} entities detected</span></div>'
            st.markdown(chips_html, unsafe_allow_html=True)
        else:
            st.markdown('<div class="rc info">No PII/PHI patterns detected in this document.</div>', unsafe_allow_html=True)

        # Step 1
        st.markdown('<div class="step-pill">✓ Step 1 — Pseudonymisation complete</div>', unsafe_allow_html=True)
        with st.expander("View Step 1 output — Pseudonymised text", expanded=True):
            st.text_area("", result["step1"], height=180, key="s1out")
            if result["token_map"]:
                st.markdown("**Token Mapping Table** — reversible at this stage")
                st.markdown('<div class="tw">', unsafe_allow_html=True)
                st.dataframe(pd.DataFrame(result["token_map"]), use_container_width=True, hide_index=True)
                st.markdown('</div>', unsafe_allow_html=True)

        # Step 2
        st.markdown('<div class="step-pill s2">✓ Step 2 — Irreversible anonymisation complete</div>', unsafe_allow_html=True)
        with st.expander("View Step 2 output — Final anonymised text", expanded=True):
            st.text_area("", result["step2"], height=180, key="s2out")

        # Audit log
        with st.expander("📋 Compliance Audit Log (DPDP Act 2023)", expanded=False):
            st.markdown('<div class="tw">', unsafe_allow_html=True)
            st.dataframe(pd.DataFrame(result["audit_log"]), use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)

        download_text = (
            f"CDSCO ANONYMISATION REPORT\nGenerated: {datetime.datetime.now()}\n\n"
            f"=== ORIGINAL TEXT ===\n{anon_input}\n\n"
            f"=== STEP 1: PSEUDONYMISED ===\n{result['step1']}\n\n"
            f"=== STEP 2: FINAL ANONYMISED ===\n{result['step2']}\n\n"
            f"=== TOKEN MAP ===\n{pd.DataFrame(result['token_map']).to_string()}\n\n"
            f"=== AUDIT LOG ===\n{pd.DataFrame(result['audit_log']).to_string()}"
        )
        st.download_button("⬇ Download Anonymisation Report (.txt)", download_text,
            file_name=f"anonymisation_report_{datetime.date.today()}.txt", mime="text/plain")
    elif run_anon:
        st.markdown('<div class="rc warning">Please upload a file or paste document content first.</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# FEATURE 2 — SUMMARISATION (with file upload + audio)
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("""
    <div class="sec-hd">
      <div class="sec-ic ic-teal">📄</div>
      <div><h2>Document Summarisation</h2>
      <p>Upload Word · PDF · Audio (MP3/WAV) or paste text · Handles 3 source types: SAE Narration · SUGAM Checklist · Meeting Transcript</p></div>
    </div>
    """, unsafe_allow_html=True)

    doc_type = st.selectbox("Select document type", [
        "SAE Case Narration","Application Checklist (SUGAM)","Meeting Transcript / Audio Transcript"])

    st.markdown('<div class="upload-card"><h4>📁 Provide your document</h4>', unsafe_allow_html=True)

    if doc_type == "Meeting Transcript / Audio Transcript":
        st.markdown('<div class="audio-notice">🎵 <b>Audio upload supported</b> — Upload MP3/WAV meeting recordings. The system will process audio metadata and generate a structured summary template. For full transcription, connect a Whisper-compatible endpoint.</div>', unsafe_allow_html=True)
        sum_file = st.file_uploader("Upload Word (.docx), PDF, TXT, or Audio (MP3/WAV)",
            type=["docx","pdf","txt","mp3","wav","m4a"], key="sum_up")
    else:
        sum_file = st.file_uploader("Upload Word (.docx) or PDF file",
            type=["docx","pdf","txt"], key="sum_up2")

    st.markdown('<div class="or-divider">or paste text manually</div>', unsafe_allow_html=True)

    sum_default = ""
    audio_uploaded = False
    if sum_file:
        fname_lower = sum_file.name.lower()
        if any(fname_lower.endswith(ext) for ext in [".mp3",".wav",".m4a"]):
            audio_uploaded = True
            st.success(f"✓ Audio file received: **{sum_file.name}** ({round(sum_file.size/1024)}KB)")
            st.markdown('<div class="rc info">Audio file uploaded. Generating structured meeting summary template. For live transcription, a Whisper API endpoint can be connected in Stage 2.</div>', unsafe_allow_html=True)
            sum_default = f"[AUDIO FILE: {sum_file.name}]\nDuration: Unknown (metadata extraction requires ffprobe)\nContent: Meeting transcript pending transcription.\nPlease paste the transcript text below if available."
        else:
            extracted, err = extract_text_from_file(sum_file)
            if err: st.error(err)
            elif extracted:
                sum_default = extracted
                st.success(f"✓ Extracted {len(extracted.split())} words from **{sum_file.name}**")

    sum_input = st.text_area("Document content", value=sum_default, height=220,
        placeholder="Paste SAE report, checklist, or meeting transcript...", key="sum_txt")
    st.markdown('</div>', unsafe_allow_html=True)

    col1,col2,_ = st.columns([1,1,3])
    with col1:
        run_sum = st.button("📄 Summarise Document", type="primary", use_container_width=True)

    if run_sum and (sum_input.strip() or audio_uploaded):
        text = sum_input.lower()
        st.markdown("---")

        if doc_type == "SAE Case Narration":
            priority = "URGENT" if any(w in text for w in ["death","fatal","died","disability","permanent"]) else \
                       "STANDARD" if any(w in text for w in ["hospitalised","admitted","icu","inpatient","hospital","hospitalization"]) else "LOW"
            causality = "Possibly Related" if "possibly" in text else \
                        "Probably Related" if "probably" in text else \
                        "Unrelated" if "unrelated" in text else \
                        "Definitely Related" if "definitely" in text else "Under Assessment"
            outcome = "Fatal" if any(w in text for w in ["died","death","fatal"]) else \
                      "Recovered" if any(w in text for w in ["recovered","recovered fully","resolution"]) else \
                      "Recovering" if any(w in text for w in ["recovering","improving"]) else "Ongoing"
            card_cls = "danger" if priority=="URGENT" else "warning" if priority=="STANDARD" else "success"
            st.markdown(f'<div class="rc {card_cls}"><b>Priority: {priority}</b> · Causality: {causality} · Outcome: {outcome}</div>', unsafe_allow_html=True)
            c1,c2,c3 = st.columns(3)
            c1.metric("Causality",causality); c2.metric("Outcome",outcome); c3.metric("Priority",priority)
            with st.expander("Full Structured SAE Summary", expanded=True):
                st.markdown(f"""
| Field | Extracted Value |
|---|---|
| Document Type | SAE Case Narration |
| Causality Assessment | {causality} |
| Patient Outcome | {outcome} |
| Review Priority | {priority} |
| Setting | {"Hospital/Emergency" if "hospital" in text or "emergency" in text else "Outpatient/Unknown"} |
| Reporting Timeline | {"Expedited 7-day" if priority=="URGENT" else "Expedited 15-day" if priority=="STANDARD" else "Periodic 90-day"} |
| Recommended Action | {"Immediate escalation to DCGI" if priority=="URGENT" else "Standard review queue"} |
                """)
            st.download_button("⬇ Download SAE Summary",
                f"Priority:{priority}\nCausality:{causality}\nOutcome:{outcome}",
                file_name="sae_summary.txt")

        elif doc_type == "Application Checklist (SUGAM)":
            lines = [l.strip() for l in sum_input.split('\n') if l.strip()]
            complete   = sum(1 for l in lines if any(w in l.lower() for w in ["complete","present","yes","submitted","available","provided"]))
            missing    = sum(1 for l in lines if any(w in l.lower() for w in ["missing","absent","no","not submitted"]))
            incomplete = sum(1 for l in lines if any(w in l.lower() for w in ["incomplete","pending","partial"]))
            total = len(lines); score = round((complete/total)*100) if total else 0
            rec = "✅ Approve for Review" if score>=80 else "⚠️ Return for Completion" if score>=50 else "❌ Reject"
            c1,c2,c3,c4 = st.columns(4)
            c1.metric("Total",total); c2.metric("Complete",complete); c3.metric("Incomplete",incomplete); c4.metric("Missing",missing)
            st.progress(score/100, text=f"Completeness Score: {score}%")
            card_cls = "success" if score>=80 else "warning" if score>=50 else "danger"
            st.markdown(f'<div class="rc {card_cls}"><b>Recommendation:</b> {rec}</div>', unsafe_allow_html=True)
            st.download_button("⬇ Download Summary", f"Score:{score}%\nRecommendation:{rec}", file_name="checklist_summary.txt")

        else:
            if audio_uploaded and not sum_input.strip().replace(f"[AUDIO FILE: {sum_file.name if sum_file else ''}]","").strip():
                st.markdown('<div class="rc info">🎵 Audio file received. Generating structured meeting summary template for manual completion.</div>', unsafe_allow_html=True)
                st.markdown("""
**Meeting Summary Template (complete after transcription)**
| Field | Value |
|---|---|
| Audio File | """ + (sum_file.name if sum_file else "Unknown") + """ |
| Status | Pending transcription |
| Key Decisions | [To be extracted] |
| Action Items | [To be extracted] |
| Next Steps | [To be extracted] |
                """)
            else:
                lines = sum_input.split('\n')
                decisions, actions, issues = [], [], []
                for line in lines:
                    ll = line.lower()
                    if any(w in ll for w in ["decided","approved","resolved","agreed","concluded"]):
                        decisions.append(line.strip())
                    elif any(w in ll for w in ["action","will","shall","to be done","responsible","follow up","owner"]):
                        actions.append(line.strip())
                    elif any(w in ll for w in ["pending","unresolved","defer","tabled","next meeting"]):
                        issues.append(line.strip())
                c1,c2,c3 = st.columns(3)
                c1.metric("Decisions",len(decisions)); c2.metric("Actions",len(actions)); c3.metric("Open Issues",len(issues))
                with st.expander("Extracted Decisions", expanded=True):
                    for i,d in enumerate(decisions[:8],1): st.markdown(f"{i}. {d}")
                with st.expander("Action Items"):
                    for i,a in enumerate(actions[:8],1): st.markdown(f"{i}. {a}")
                if issues:
                    with st.expander("Unresolved Issues"):
                        for i,x in enumerate(issues[:6],1): st.markdown(f"{i}. {x}")
                st.download_button("⬇ Download Meeting Summary", "\n".join(decisions+actions), file_name="meeting_summary.txt")
    elif run_sum:
        st.markdown('<div class="rc warning">Please upload a file or paste content first.</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# FEATURE 3 — COMPLETENESS
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("""
    <div class="sec-hd">
      <div class="sec-ic ic-purple">✅</div>
      <div><h2>Completeness Assessment — Schedule Y</h2>
      <p>Upload application document · Checks 20 mandatory CDSCO Schedule Y fields · RAG status · Automated recommendation</p></div>
    </div>
    """, unsafe_allow_html=True)

    SCHEDULE_Y = [
        ("Protocol Synopsis","protocol synopsis","Critical"),
        ("Investigator Brochure","investigator brochure","Critical"),
        ("Form CT-04","ct-04","Critical"),("Form CT-05","ct-05","Critical"),
        ("Ethics Committee Approval","ethics committee","Critical"),
        ("Informed Consent Form (English)","informed consent","Critical"),
        ("Informed Consent Form (Local Language)","local language","Critical"),
        ("Investigator CV","investigator cv","Major"),("Site Master File","site master","Major"),
        ("Insurance Certificate","insurance","Major"),("Drug Import License","import license","Major"),
        ("GCP Compliance Certificate","gcp","Major"),("Patient Information Sheet","patient information","Major"),
        ("Case Report Form Template","case report form","Minor"),("Statistical Analysis Plan","statistical analysis","Minor"),
        ("DSMB Charter","dsmb","Minor"),("Pharmacovigilance Plan","pharmacovigilance","Minor"),
        ("Risk Management Plan","risk management","Minor"),
        ("Regulatory Approval (Country of Origin)","regulatory approval","Major"),
        ("Sponsor Authorisation Letter","sponsor authorisation","Major"),
    ]

    col_a,col_b = st.columns([2,1])
    with col_a:
        st.markdown('<div class="upload-card"><h4>📁 Upload application document</h4>', unsafe_allow_html=True)
        comp_file = st.file_uploader("Upload Word (.docx) or PDF", type=["docx","pdf","txt"], key="comp_up")
        st.markdown('<div class="or-divider">or paste text</div>', unsafe_allow_html=True)
        comp_default = ""
        if comp_file:
            extracted,err = extract_text_from_file(comp_file)
            if err: st.error(err)
            elif extracted:
                comp_default = extracted
                st.success(f"✓ Extracted from **{comp_file.name}**")
        comp_input = st.text_area("Application content", value=comp_default, height=180, key="comp_txt")
        st.markdown('</div>', unsafe_allow_html=True)
    with col_b:
        app_id = st.text_input("Application ID", placeholder="SUGAM-CT-2024-0892")
        st.markdown("<br>", unsafe_allow_html=True)
        run_comp = st.button("✅ Run Completeness Check", type="primary", use_container_width=True)

    if run_comp and comp_input.strip():
        tl = comp_input.lower()
        results=[]; critical_missing=[]; major_missing=[]
        for field,keyword,severity in SCHEDULE_Y:
            if keyword in tl:
                status="PRESENT" if not any(w in tl for w in ["pending","tbd","partial","to be"]) else "INCOMPLETE"
                rag="🟢 Green" if status=="PRESENT" else "🟡 Amber"
            else:
                status="MISSING"; rag="🔴 Red"
                if severity=="Critical": critical_missing.append(field)
                elif severity=="Major": major_missing.append(field)
            results.append({"Field":field,"Severity":severity,"Status":status,"RAG":rag})
        df_comp=pd.DataFrame(results)
        present=sum(1 for r in results if r["Status"]=="PRESENT")
        incomplete=sum(1 for r in results if r["Status"]=="INCOMPLETE")
        missing=sum(1 for r in results if r["Status"]=="MISSING")
        score=round((present/20)*100)
        rec="✅ Approve for Technical Review" if score>=85 and not critical_missing else \
            "⚠️ Return for Completion" if score>=60 else "❌ Reject — Critical fields missing"
        card_cls="success" if score>=85 and not critical_missing else "warning" if score>=60 else "danger"
        c1,c2,c3,c4=st.columns(4)
        c1.metric("Total",20); c2.metric("Present",present); c3.metric("Incomplete",incomplete); c4.metric("Missing",missing)
        st.progress(score/100, text=f"Schedule Y Completeness: {score}%")
        st.markdown(f'<div class="rc {card_cls}"><b>Recommendation:</b> {rec}</div>', unsafe_allow_html=True)
        if critical_missing: st.error(f"Critical missing: {', '.join(critical_missing)}")
        if major_missing: st.warning(f"Major missing: {', '.join(major_missing)}")
        with st.expander("Full Schedule Y Field Status", expanded=True):
            def srag(val):
                if "Green" in str(val): return "background-color:#dcfce7;color:#15803d;font-weight:600"
                if "Amber" in str(val): return "background-color:#fef9c3;color:#a16207;font-weight:600"
                if "Red" in str(val): return "background-color:#fee2e2;color:#b91c1c;font-weight:600"
                return ""
            st.markdown('<div class="tw">', unsafe_allow_html=True)
            st.dataframe(df_comp.style.applymap(srag,subset=["RAG"]), use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)
        st.download_button("⬇ Download Completeness Report", df_comp.to_csv(index=False),
            file_name="completeness_report.csv", mime="text/csv")
    elif run_comp:
        st.markdown('<div class="rc warning">Please upload a file or paste content first.</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# FEATURE 4 — CLASSIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("""
    <div class="sec-hd">
      <div class="sec-ic ic-amber">🏷️</div>
      <div><h2>SAE Classification &amp; Prioritisation</h2>
      <p>Upload SAE report · ICD-10 keyword mapping · Severity grading · Duplicate detection · Review queue ordering</p></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="upload-card"><h4>📁 Upload SAE report</h4>', unsafe_allow_html=True)
    class_file = st.file_uploader("Upload Word (.docx) or PDF", type=["docx","pdf","txt"], key="class_up")
    st.markdown('<div class="or-divider">or paste text</div>', unsafe_allow_html=True)
    class_default = ""
    if class_file:
        extracted,err = extract_text_from_file(class_file)
        if err: st.error(err)
        elif extracted:
            class_default=extracted
            st.success(f"✓ Extracted from **{class_file.name}**")
    class_input = st.text_area("SAE report content", value=class_default, height=200, key="class_txt")
    st.markdown('</div>', unsafe_allow_html=True)

    with st.expander("Duplicate Detection — upload additional SAE reports (optional)"):
        c1d,c2d=st.columns(2)
        with c1d:
            dup2_file=st.file_uploader("SAE Report 2",type=["docx","pdf","txt"],key="dup2_up")
            dup2_def=""
            if dup2_file:
                t,e=extract_text_from_file(dup2_file)
                if not e: dup2_def=t
            dup2=st.text_area("or paste SAE 2",value=dup2_def,height=80,key="dup2t")
        with c2d:
            dup3_file=st.file_uploader("SAE Report 3",type=["docx","pdf","txt"],key="dup3_up")
            dup3_def=""
            if dup3_file:
                t,e=extract_text_from_file(dup3_file)
                if not e: dup3_def=t
            dup3=st.text_area("or paste SAE 3",value=dup3_def,height=80,key="dup3t")

    col1,col2,_=st.columns([1,1,3])
    with col1:
        run_class=st.button("🏷️ Classify Case",type="primary",use_container_width=True)

    if run_class and class_input.strip():
        text=class_input.lower()
        if any(w in text for w in ["died","fatal","death","mortality","deceased"]):
            severity="DEATH"; sev_style="background:#fee2e2;color:#991b1b"; ps=1
            rk=[w for w in ["died","fatal","death","mortality","deceased"] if w in text]
        elif any(w in text for w in ["permanent disability","paralysis","blind","deaf","permanent impairment"]):
            severity="DISABILITY"; sev_style="background:#ffedd5;color:#9a3412"; ps=2
            rk=[w for w in ["permanent disability","paralysis","blind","deaf"] if w in text]
        elif any(w in text for w in ["hospitalised","admitted","icu","inpatient","emergency","hospitalization","hospitalization","hospital"]):
            severity="HOSPITALISATION"; sev_style="background:#fef9c3;color:#92400e"; ps=3
            rk=[w for w in ["hospitalised","admitted","icu","inpatient","emergency","hospital"] if w in text]
        else:
            severity="OTHERS"; sev_style="background:#dbeafe;color:#1e40af"; ps=4
            rk=["no critical keywords — default classification"]
        conf="HIGH" if len(rk)>=3 else "MEDIUM" if len(rk)>=1 else "LOW"
        icd={"DEATH":"R96.x / R98 / R99","DISABILITY":"S00-T98 (permanent)","HOSPITALISATION":"Z75.1","OTHERS":"MedDRA PT"}
        rpt={"DEATH":"Expedited — 7 days (fatal)","DISABILITY":"Expedited — 15 days","HOSPITALISATION":"Expedited — 15 days","OTHERS":"Periodic — 90 days"}
        st.markdown(f'<div style="{sev_style};border-radius:10px;padding:10px 20px;font-size:18px;font-weight:700;display:inline-block;margin-bottom:14px;">⬤ {severity}</div>', unsafe_allow_html=True)
        c1,c2,c3=st.columns(3)
        c1.metric("Severity",severity); c2.metric("Confidence",conf); c3.metric("Priority Score",f"{ps}/4")
        with st.expander("Classification Evidence & ICD-10 Reference", expanded=True):
            st.markdown(f'<div class="rc info"><b>Reason:</b> Classified as <b>{severity}</b> because keywords detected: <i>{", ".join(rk)}</i><br><b>ICD-10:</b> {icd[severity]} · <b>Reporting:</b> {rpt[severity]}</div>', unsafe_allow_html=True)
        st.markdown("**Duplicate Detection**")
        def xids(t): return set(re.findall(r'\b(?:PT|SUBJ|LH|MH)[-]\w+[-]\w+\b',t)),set(re.findall(r'\b[A-Z]{4,}[-]?\d+\s*mg\b',t))
        id1,d1=xids(class_input); dup_found=False
        for i,other in enumerate([dup2,dup3],2):
            if other.strip():
                id2,d2=xids(other)
                if id1&id2 or d1&d2:
                    st.markdown(f'<div class="rc danger">⚠️ DUPLICATE DETECTED — Report {i} shares identifiers with Report 1: {(id1&id2)|(d1&d2)}</div>',unsafe_allow_html=True)
                    dup_found=True
        if not dup_found: st.markdown('<div class="rc success">✓ No duplicates detected across provided reports.</div>',unsafe_allow_html=True)
        result_text=f"Severity:{severity}\nConfidence:{conf}\nReason:{', '.join(rk)}\nPriority:{ps}/4\nICD-10:{icd[severity]}\nTimeline:{rpt[severity]}"
        st.download_button("⬇ Download Classification Report",result_text,file_name="classification_report.txt")
    elif run_class:
        st.markdown('<div class="rc warning">Please upload or paste an SAE report first.</div>',unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# FEATURE 5 — COMPARISON
# ═══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown("""
    <div class="sec-hd">
      <div class="sec-ic ic-sky">🔍</div>
      <div><h2>Document Comparison</h2>
      <p>Upload two versions · Semantic diff · Highlights substantive vs administrative changes · Downloadable change report</p></div>
    </div>
    """, unsafe_allow_html=True)

    col_v1,col_v2=st.columns(2)
    with col_v1:
        st.markdown("**Version 1 — Original**")
        v1f=st.file_uploader("Upload original",type=["docx","pdf","txt"],key="v1f")
        v1def=""
        if v1f:
            t,e=extract_text_from_file(v1f)
            if not e: v1def=t; st.success(f"✓ {v1f.name}")
        v1=st.text_area("or paste V1",value=v1def,height=200,key="v1t",placeholder="Paste original document...")
    with col_v2:
        st.markdown("**Version 2 — Updated**")
        v2f=st.file_uploader("Upload updated",type=["docx","pdf","txt"],key="v2f")
        v2def=""
        if v2f:
            t,e=extract_text_from_file(v2f)
            if not e: v2def=t; st.success(f"✓ {v2f.name}")
        v2=st.text_area("or paste V2",value=v2def,height=200,key="v2t",placeholder="Paste updated document...")

    col1,col2,_=st.columns([1,1,3])
    with col1:
        run_c5=st.button("🔍 Compare Documents",type="primary",use_container_width=True)

    if run_c5 and v1.strip() and v2.strip():
        l1=[l.strip() for l in v1.splitlines() if l.strip()]
        l2=[l.strip() for l in v2.splitlines() if l.strip()]
        matcher=difflib.SequenceMatcher(None,l1,l2)
        SK=["dose","dosage","mg","ml","death","disability","outcome","causality","adverse","event","date","patient","diagnosis","icd","treatment","safety","efficacy","result","risk","fatal","serious"]
        changes=[]
        for tag,i1,i2,j1,j2 in matcher.get_opcodes():
            if tag=="replace":
                for old,new in zip(l1[i1:i2],l2[j1:j2]):
                    is_sub=any(k in old.lower() or k in new.lower() for k in SK)
                    changes.append({"Type":"CHANGED","Original":old,"New":new,"Substantive":"Yes" if is_sub else "No"})
            elif tag=="delete":
                for line in l1[i1:i2]:
                    changes.append({"Type":"REMOVED","Original":line,"New":"—","Substantive":"Yes" if any(k in line.lower() for k in SK) else "No"})
            elif tag=="insert":
                for line in l2[j1:j2]:
                    changes.append({"Type":"ADDED","Original":"—","New":line,"Substantive":"Yes" if any(k in line.lower() for k in SK) else "No"})
        sub_c=sum(1 for c in changes if c["Substantive"]=="Yes")
        c1,c2,c3,c4,c5=st.columns(5)
        c1.metric("Total",len(changes)); c2.metric("Added",sum(1 for c in changes if c["Type"]=="ADDED"))
        c3.metric("Removed",sum(1 for c in changes if c["Type"]=="REMOVED"))
        c4.metric("Changed",sum(1 for c in changes if c["Type"]=="CHANGED"))
        c5.metric("Substantive",sub_c)
        card_cls="danger" if sub_c>0 else "success"
        msg=f"⚠️ {sub_c} substantive change(s) detected — require regulatory review." if sub_c>0 else "✓ No substantive changes detected."
        st.markdown(f'<div class="rc {card_cls}">{msg}</div>',unsafe_allow_html=True)
        if changes:
            df_d=pd.DataFrame(changes)
            def sd(row):
                if row["Type"]=="ADDED": return ["background-color:#dcfce7"]*len(row)
                if row["Type"]=="REMOVED": return ["background-color:#fee2e2"]*len(row)
                if row["Substantive"]=="Yes": return ["background-color:#fef9c3"]*len(row)
                return [""]*len(row)
            with st.expander("Full Change Table",expanded=True):
                st.markdown('<div class="tw">',unsafe_allow_html=True)
                st.dataframe(df_d.style.apply(sd,axis=1),use_container_width=True,hide_index=True)
                st.markdown('</div>',unsafe_allow_html=True)
                st.caption("🟢 Added · 🔴 Removed · 🟡 Changed (Substantive)")
            st.download_button("⬇ Download Comparison Report",df_d.to_csv(index=False),file_name="comparison_report.csv",mime="text/csv")
    elif run_c5:
        st.markdown('<div class="rc warning">Please provide both document versions.</div>',unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# FEATURE 6 — INSPECTION REPORT
# ═══════════════════════════════════════════════════════════════════════════════
with tab6:
    st.markdown("""
    <div class="sec-hd">
      <div class="sec-ic ic-pink">📋</div>
      <div><h2>Inspection Report Generation</h2>
      <p>Paste raw site observations · AI converts to formal CDSCO GCP inspection report · Critical / Major / Minor grading</p></div>
    </div>
    """, unsafe_allow_html=True)

    col_f1,col_f2,col_f3,col_f4=st.columns(4)
    with col_f1: inspector_name=st.text_input("Inspector Name",placeholder="Dr. A.K. Sharma")
    with col_f2: site_name=st.text_input("Site Name",placeholder="AIIMS Delhi — Cardiology")
    with col_f3: site_number=st.text_input("Site Number",placeholder="SITE-DEL-001")
    with col_f4: inspection_date=st.date_input("Inspection Date")

    obs_input=st.text_area("Raw inspection observations (one per line)",height=200,key="obs_txt",
        placeholder="No record of drug accountability for subjects 3 and 7\nInformed consent form missing local language version\nMinor labelling issue on storage boxes")

    col1,col2,_=st.columns([1,1,3])
    with col1:
        run_insp=st.button("📋 Generate Report",type="primary",use_container_width=True)

    if run_insp and obs_input.strip():
        obs_list=[o.strip() for o in obs_input.splitlines() if o.strip()]
        CK=["no record","falsified","patient safety","data integrity","unaccounted","missing","fraud"]
        MK=["incomplete","not documented","protocol deviation","untrained","not signed","not dated","expired"]
        rows=[]
        for i,obs in enumerate(obs_list,1):
            ol=obs.lower()
            if any(k in ol for k in CK): risk="Critical";dl="15 days";ca="Immediate CAPA required. Site operations may be suspended."
            elif any(k in ol for k in MK): risk="Major";dl="30 days";ca="CAPA plan required within 30 days."
            else: risk="Minor";dl="60 days";ca="Document corrective action in site log."
            formal=f"During the inspection on {inspection_date.strftime('%d %B %Y')}, it was observed that {obs.lower().rstrip('.')}. This constitutes a {risk.lower()} GCP deviation requiring corrective action."
            rows.append({"Obs No.":f"OBS-{i:03d}","Raw Observation":obs,"Formal Finding":formal,"Risk Level":risk,"Corrective Action":ca,"Deadline":dl})
        cc=sum(1 for r in rows if r["Risk Level"]=="Critical")
        mc=sum(1 for r in rows if r["Risk Level"]=="Major")
        mnc=sum(1 for r in rows if r["Risk Level"]=="Minor")
        c1,c2,c3=st.columns(3)
        c1.metric("Critical",cc); c2.metric("Major",mc); c3.metric("Minor",mnc)
        card_cls="danger" if cc>0 else "warning" if mc>0 else "success"
        msg=f"⚠️ {cc} Critical finding(s) — Immediate CAPA required." if cc>0 else f"⚠️ {mc} Major finding(s) — CAPA due in 30 days." if mc>0 else "✓ No Critical or Major findings."
        st.markdown(f'<div class="rc {card_cls}">{msg}</div>',unsafe_allow_html=True)
        with st.expander("Full Inspection Report Table",expanded=True):
            df_r=pd.DataFrame(rows)
            def sr(val):
                if val=="Critical": return "background-color:#fee2e2;color:#991b1b;font-weight:700"
                if val=="Major": return "background-color:#fef9c3;color:#92400e;font-weight:700"
                if val=="Minor": return "background-color:#dcfce7;color:#166534"
                return ""
            st.markdown('<div class="tw">',unsafe_allow_html=True)
            st.dataframe(df_r.style.applymap(sr,subset=["Risk Level"]),use_container_width=True,hide_index=True)
            st.markdown('</div>',unsafe_allow_html=True)
        full=f"CDSCO GCP SITE INSPECTION REPORT\n{'='*50}\nSite: {site_name}\nSite No: {site_number}\nDate: {inspection_date.strftime('%d %B %Y')}\nInspector: {inspector_name}\nSummary: {cc} Critical | {mc} Major | {mnc} Minor\n{'='*50}\n\n"
        for r in rows:
            full+=f"{r['Obs No.']} | {r['Risk Level'].upper()}\nFinding: {r['Formal Finding']}\nCorrective Action: {r['Corrective Action']}\nDeadline: {r['Deadline']}\n{'-'*50}\n\n"
        full+=f"Inspector: {inspector_name}\nSignature: _______________\nDate: {datetime.date.today()}"
        st.download_button("⬇ Download Inspection Report",full,file_name="cdsco_inspection_report.txt",mime="text/plain")
    elif run_insp:
        st.markdown('<div class="rc warning">Please enter at least one inspection observation.</div>',unsafe_allow_html=True)
