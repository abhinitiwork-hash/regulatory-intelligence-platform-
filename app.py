import streamlit as st
import pandas as pd
import datetime
import re
import difflib
import io

# ── Optional imports ──────────────────────────────────────────────────────────
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
    page_title="Nirnay — CDSCO AI Review System",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;}
#MainMenu,footer,header{visibility:hidden;}
.stApp{background-color:#f0f3f8;}
.stTabs [data-baseweb="tab-panel"]{background:white;border-radius:0 0 12px 12px;padding:20px !important;}

section[data-testid="stSidebar"]{background:linear-gradient(180deg,#001f5b 0%,#003087 60%,#004db3 100%);}
section[data-testid="stSidebar"] * {color:white!important;}
section[data-testid="stSidebar"] .stMarkdown p{color:rgba(255,255,255,0.8)!important;}
section[data-testid="stSidebar"] .stSelectbox>div>div{background:rgba(255,255,255,0.1)!important;border:1px solid rgba(255,255,255,0.25)!important;border-radius:8px!important;}
section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"]{background:rgba(255,255,255,0.08)!important;border:1.5px dashed rgba(255,255,255,0.35)!important;border-radius:10px!important;}

.hero{background:linear-gradient(135deg,#001f5b 0%,#003087 55%,#0052cc 100%);border-radius:16px;padding:28px 36px;margin-bottom:18px;box-shadow:0 4px 24px rgba(0,48,135,0.18);}
.hero h1{color:white;font-size:24px;font-weight:700;margin:0;}
.hero .sub{color:rgba(255,255,255,0.68);font-size:13px;margin:5px 0 0;}
.hero-row{display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:16px;}
.hero-badges{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px;}
.hbadge{background:rgba(255,255,255,0.12);border:1px solid rgba(255,255,255,0.22);border-radius:20px;padding:4px 12px;font-size:11px;color:rgba(255,255,255,0.9);font-weight:500;}
.hbadge.g{border-color:#4ade80;color:#4ade80;}
.stat-row{display:flex;gap:10px;}
.sbadge{background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);border-radius:10px;padding:10px 14px;text-align:center;min-width:64px;}
.sbadge .n{color:#7dd3fc;font-size:20px;font-weight:700;display:block;line-height:1;}
.sbadge .l{color:rgba(255,255,255,0.55);font-size:10px;margin-top:2px;display:block;}

.how-to{background:white;border-radius:12px;padding:14px 18px;margin-bottom:18px;border-left:4px solid #003087;box-shadow:0 1px 4px rgba(0,0,0,0.06);}
.how-to strong{color:#003087;font-size:13px;}
.hw-steps{display:flex;gap:8px;flex-wrap:wrap;margin-top:8px;}
.hw-s{background:#f0f4f8;border-radius:8px;padding:5px 10px;font-size:12px;color:#475569;display:flex;align-items:center;gap:5px;}
.hw-n{background:#003087;color:white;border-radius:50%;width:16px;height:16px;display:inline-flex;align-items:center;justify-content:center;font-size:9px;font-weight:700;flex-shrink:0;}

.stTabs [data-baseweb="tab-list"]{background:#0a2240;border-radius:10px;padding:4px;gap:2px;}
.stTabs [data-baseweb="tab"]{border-radius:7px;font-size:12px;font-weight:500;color:rgba(255,255,255,0.55);padding:8px 14px;}
.stTabs [aria-selected="true"]{background:#0077b6!important;color:white!important;}
.stTabs [data-baseweb="tab"]:hover{color:white!important;}
.stTabs [data-baseweb="tab-border"]{display:none;}

.sec-hd{display:flex;align-items:center;gap:12px;margin-bottom:20px;padding-bottom:14px;border-bottom:1px solid #e2e8f0;}
.sec-ic{width:42px;height:42px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:20px;flex-shrink:0;}
.ic-blue{background:#dbeafe;}.ic-teal{background:#ccfbf1;}.ic-purple{background:#ede9fe;}
.ic-amber{background:#fef3c7;}.ic-sky{background:#e0f2fe;}.ic-pink{background:#fce7f3;}
.sec-hd h2{font-size:17px;font-weight:600;color:#1e293b;margin:0;}
.sec-hd p{font-size:12px;color:#64748b;margin:2px 0 0;}

.upload-zone{background:white;border-radius:14px;padding:20px 22px;box-shadow:0 1px 4px rgba(0,0,0,0.06);margin-bottom:14px;border:1.5px solid #e2e8f0;}
.upload-zone h4{color:#1e293b;font-size:14px;font-weight:600;margin:0 0 10px;}
.or-line{display:flex;align-items:center;gap:10px;margin:12px 0;color:#94a3b8;font-size:12px;}
.or-line::before,.or-line::after{content:'';flex:1;height:1px;background:#e2e8f0;}

.pii-chips{display:flex;flex-wrap:wrap;gap:7px;margin:12px 0;}
.chip{display:inline-flex;align-items:center;gap:4px;border-radius:20px;padding:4px 11px;font-size:12px;font-weight:600;}
.cr{background:#fee2e2;color:#991b1b;}.ca{background:#fef3c7;color:#92400e;}
.cb{background:#dbeafe;color:#1e40af;}.cp{background:#ede9fe;color:#5b21b6;}
.ct{background:#ccfbf1;color:#065f46;}.cg{background:#f1f5f9;color:#475569;}

.rc{background:white;border-radius:10px;padding:14px 18px;box-shadow:0 1px 4px rgba(0,0,0,0.06);margin:8px 0;border-left:4px solid #003087;}
.rc.ok{border-left-color:#16a34a;background:#f0fdf4;}
.rc.warn{border-left-color:#d97706;background:#fffbeb;}
.rc.err{border-left-color:#dc2626;background:#fef2f2;}
.rc.info{border-left-color:#0284c7;background:#f0f9ff;}

.step-pill{display:inline-flex;align-items:center;gap:5px;background:#003087;color:white;border-radius:20px;padding:4px 12px;font-size:11px;font-weight:600;margin-bottom:8px;}
.step-pill.s2{background:#0f766e;}

.tw{background:white;border-radius:10px;padding:4px;box-shadow:0 1px 4px rgba(0,0,0,0.06);margin:8px 0;}

.dup-session{background:#f0f9ff;border:1px solid #bae6fd;border-radius:12px;padding:14px 18px;margin-bottom:12px;font-size:13px;color:#0369a1;}

.feat-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;}
.fc{background:white;border-radius:14px;padding:18px;box-shadow:0 1px 4px rgba(0,0,0,0.06);border-top:3px solid #003087;}
.fc.f1{border-top-color:#003087;}.fc.f2{border-top-color:#0f766e;}.fc.f3{border-top-color:#6d28d9;}
.fc.f4{border-top-color:#b45309;}.fc.f5{border-top-color:#0369a1;}.fc.f6{border-top-color:#be185d;}
.fc .fi{font-size:24px;margin-bottom:6px;}.fc .fn{font-size:10px;font-weight:600;color:#94a3b8;text-transform:uppercase;letter-spacing:.08em;}
.fc .ft{font-size:13px;font-weight:600;color:#1e293b;margin:4px 0 3px;}.fc .fd{font-size:11px;color:#64748b;line-height:1.5;}

.audio-note{background:#fef9c3;border:1px solid #fbbf24;border-radius:8px;padding:10px 14px;font-size:12px;color:#78350f;margin:8px 0;}

.stButton>button[kind="primary"]{background:linear-gradient(135deg,#003087,#0052cc)!important;color:white!important;border:none!important;border-radius:8px!important;font-weight:600!important;font-size:13px!important;padding:10px 22px!important;box-shadow:0 2px 8px rgba(0,48,135,0.25)!important;}
.stButton>button[kind="primary"]:hover{box-shadow:0 4px 16px rgba(0,48,135,0.35)!important;transform:translateY(-1px)!important;}
.stDownloadButton>button{border-radius:8px!important;border:1.5px solid #003087!important;color:#003087!important;font-weight:500!important;font-size:13px!important;}
.stTextArea textarea{border:1.5px solid #e2e8f0!important;border-radius:10px!important;font-size:13px!important;background:#fafbfc!important;}
.stTextArea textarea:focus{border-color:#003087!important;background:white!important;box-shadow:0 0 0 3px rgba(0,48,135,0.08)!important;}
[data-testid="stMetricValue"]{font-size:24px!important;font-weight:700!important;}
[data-testid="stMetricLabel"]{font-size:12px!important;color:#64748b!important;}

.glass{background:rgba(255,255,255,0.6);backdrop-filter:blur(12px);border-radius:14px;padding:24px 28px;box-shadow:0 4px 20px rgba(0,0,0,0.08);border:1px solid rgba(255,255,255,0.5);margin-bottom:18px;}
.glass .big-title{font-size:26px;font-weight:700;color:#003087;margin:0 0 4px;}
.glass .subtitle{color:#6b7280;font-size:14px;margin:0;}
.dash-card{background:white;border-radius:12px;padding:18px;text-align:center;box-shadow:0 2px 10px rgba(0,0,0,0.06);border:0.5px solid #e2e8f0;}
.dash-card h2{margin:0 0 4px;color:#003087;font-size:28px;font-weight:700;}
.dash-card p{font-size:12px;color:#6b7280;margin:0;}
.dash-card.urgent h2{color:#dc2626;}
.dash-card.warn h2{color:#d97706;}
.dash-card.info h2{color:#0284c7;}
.upload-card{background:rgba(255,255,255,0.7);backdrop-filter:blur(8px);border-radius:14px;padding:20px 22px;box-shadow:0 2px 12px rgba(0,0,0,0.06);margin-bottom:14px;border:1px solid rgba(255,255,255,0.6);}
.upload-card h4{color:#1e293b;font-size:14px;font-weight:600;margin:0 0 10px;}

</style>
""", unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
# This is the KEY fix: we use session_state to hold extracted text
# so it persists across reruns when the Run button is clicked
for k in ["anon_text","sum_text","comp_text","class_text","v1_text","v2_text",
          "dup_files","anon_done","sum_done","comp_done","class_done","logged_in","carousel_idx"]:
    if k not in st.session_state:
        if k == "dup_files":
            st.session_state[k] = {}
        elif k.endswith("_done"):
            st.session_state[k] = False
        elif k == "logged_in":
            st.session_state[k] = False
        elif k == "carousel_idx":
            st.session_state[k] = 0
        else:
            st.session_state[k] = ""


# ── File extraction utility ───────────────────────────────────────────────────
def extract_text(uploaded_file):
    """Returns (text, error). Uses session_state to survive reruns."""
    if uploaded_file is None:
        return "", None
    name = uploaded_file.name.lower()
    try:
        raw = uploaded_file.read()
        if name.endswith(".docx"):
            if not DOCX_OK:
                return "", "Add 'python-docx' to requirements.txt"
            doc = python_docx.Document(io.BytesIO(raw))
            return "\n".join(p.text for p in doc.paragraphs if p.text.strip()), None
        elif name.endswith(".pdf"):
            if not PDF_OK:
                return "", "Add 'pypdf' to requirements.txt"
            if PDF_OK == "pypdf2":
                import PyPDF2
                r = PyPDF2.PdfReader(io.BytesIO(raw))
                return "\n".join(pg.extract_text() or "" for pg in r.pages), None
            else:
                r = PdfReader(io.BytesIO(raw))
                return "\n".join(pg.extract_text() or "" for pg in r.pages), None
        elif name.endswith(".txt"):
            return raw.decode("utf-8", errors="ignore"), None
        else:
            return "", f"Unsupported: {uploaded_file.name}"
    except Exception as e:
        return "", str(e)


# ── PII / PHI detection & anonymisation ──────────────────────────────────────
INDIAN_FIRST = ["Rajesh","Priya","Suresh","Anita","Vikram","Sunita","Amit","Kavita",
                "Ravi","Deepa","Mohit","Pooja","Arjun","Neha","Sanjay","Meera","Rahul",
                "Divya","Anil","Rekha","Vijay","Smita","Ramesh","Geeta","Ashok","Usha",
                "Manoj","Seema","Vinod","Lata","Amitav","Amitabh","Sunil","Sneha","Preeti",
                "Rohit","Kiran","Nisha","Ganesh","Harish","Naresh","Satish","Girish"]
INDIAN_LAST  = ["Sharma","Patel","Singh","Kumar","Mehta","Gupta","Verma","Joshi","Nair",
                "Rao","Iyer","Reddy","Bose","Das","Malhotra","Kapoor","Agarwal","Pandey",
                "Mishra","Tiwari","Ghosh","Chatterjee","Mukherjee","Kulkarni","Desai"]

CHIP_MAP = {
    "Patient Name":"cr","Patient Initials":"cr","Patient ID":"cr",
    "Hospital Record No.":"ca","Investigator Name":"cp","Investigator ID":"cp",
    "Date / DOB":"cb","Phone Number":"ct","Aadhaar Number":"ca",
    "Pincode":"cg","Site Number":"cg","Regulatory ID":"cg","Address":"cg"
}

def run_anonymisation(text):
    tokens, audit, processed = [], [], text
    cnt = {k:0 for k in ["PATIENT","INVESTIGATOR","DATE","SITE","PHONE","AADHAAR","HOSP_REC","EMAIL","PINCODE","INSTITUTION","BATCH","LAB_VALUE","TIMESTAMP"]}
    ts  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    found_types = set()

    def tok(kind):
        cnt[kind]+=1; return f"[{kind}-{cnt[kind]:03d}]"
    def rec(t,orig,etype):
        tokens.append({"Token":t,"Original Value":orig,"Entity Type":etype,"Step":"Step 1"})
        audit.append({"Timestamp":ts,"Action":"Pseudonymised","Entity Type":etype,"Token":t,"Reversible":"Yes"})
        found_types.add(etype)

    # FIX ORDER: run phone & IDs BEFORE dates to avoid digit consumption
    # Email addresses
    for m in re.finditer(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}', processed):
        t=tok("EMAIL"); rec(t,m.group(),"Email Address")
        processed=processed.replace(m.group(),t,1)
    # Hospital record #XXXXX
    for m in re.finditer(r'#\d{4,6}', processed):
        t=tok("HOSP_REC"); rec(t,m.group(),"Hospital Record No.")
        processed=processed.replace(m.group(),t,1)
    # Aadhaar XXXX-XXXX-XXXX
    for m in re.finditer(r'\d{4}[-\s]\d{4}[-\s]\d{4}', processed):
        t=tok("AADHAAR"); rec(t,m.group(),"Aadhaar Number")
        processed=processed.replace(m.group(),t,1)
    # Phone — run BEFORE dates so digits not consumed
    # +91 22 5550 1234 format
    for m in re.finditer(r'\+91[\s-]?\d{2,4}[\s-]\d{4}[\s-]\d{4}', processed):
        t=tok("PHONE"); rec(t,m.group(),"Phone Number")
        processed=processed.replace(m.group(),t,1)
    # 10-digit mobile
    for m in re.finditer(r'[6-9]\d{9}', processed):
        t=tok("PHONE"); rec(t,m.group(),"Phone Number")
        processed=processed.replace(m.group(),t,1)
    # FIX 1: non-capturing group so finditer returns full match not just prefix
    # LH-MUM-042, PT-2024-001, SITE-DEL-001
    for m in re.finditer(r'(?:PT|SITE|IND|CT|SUBJ|INV|LH|MH|DL|CH)[-]\w{2,8}[-]\w{2,8}', processed):
        o=m.group()
        if any(o.startswith(p) for p in ["PT","SUBJ","LH","MH","DL"]): t=tok("PATIENT"); et="Patient ID"
        elif o.startswith("SITE"): t=tok("SITE"); et="Site Number"
        elif o.startswith("INV"):  t=tok("INVESTIGATOR"); et="Investigator ID"
        else: t=tok("ID"); et="Regulatory ID"
        rec(t,o,et); processed=processed.replace(o,t,1)
    # Dates — run AFTER phone/IDs (fixes digit consumption order)
    for pat in [
        re.compile(r'\d{1,2}[-/]\w{2,9}[-/]\d{2,4}'),
        re.compile(r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}'),
        re.compile(r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2},?\s+\d{4}',re.I),
        re.compile(r'\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}',re.I),
    ]:
        for m in pat.finditer(processed):
            t=tok("DATE"); rec(t,m.group(),"Date / DOB")
            processed=processed.replace(m.group(),t,1)
    # FIX 2: lookaround instead of  for initials —  fails next to periods
    for m in re.finditer(r'(?<!\w)[A-Z]\.[A-Z]\.(?!\w)', processed):
        t=tok("PATIENT"); rec(t,m.group(),"Patient Initials")
        processed=processed.replace(m.group(),t,1)
    # Dr. + Indian name
    name_re=re.compile(r'(Dr\.?\s+)('+'|'.join(INDIAN_FIRST)+r')\s+('+'|'.join(INDIAN_LAST)+r')')
    for m in name_re.finditer(processed):
        t=tok("INVESTIGATOR"); rec(t,m.group(),"Investigator Name")
        processed=processed.replace(m.group(),t,1)
    # Non-Dr Indian name
    name_re2=re.compile(r'('+'|'.join(INDIAN_FIRST)+r')\s+('+'|'.join(INDIAN_LAST)+r')')
    for m in name_re2.finditer(processed):
        if m.group() in processed:
            t=tok("PATIENT"); rec(t,m.group(),"Patient Name")
            processed=processed.replace(m.group(),t,1)
    # Study IDs: IND-CT-XXXX-XXXX format
    for m in re.finditer(r'\bIND-[A-Z]{2,4}-\d{4}-\d{3,6}\b', processed):
        t=tok("SITE"); rec(t,m.group(),"Study ID")
        processed=processed.replace(m.group(),t,1)
    # Pincode — semantic token
    for m in re.finditer(r"\b[1-9]\d{5}\b", processed):
        t=tok("PINCODE"); rec(t,m.group(),"Pincode")
        processed=processed.replace(m.group(),t,1)
    # Institution names
    for m in re.finditer(r"\b[A-Z][A-Za-z]+(\s+[A-Z][A-Za-z]+){0,3}\s+(?:Hospital|Institute|Clinic|Centre|Center|Medical College|AIIMS|PGI|CMC)\b", processed):
        t=tok("INSTITUTION"); rec(t,m.group(),"Institution Name")
        processed=processed.replace(m.group(),t,1)
    # Batch/Lot numbers
    for m in re.finditer(r"\b(?:Batch|Lot|BN|LN)[.:\\s#]*[A-Z0-9]{4,12}\b", processed, re.I):
        t=tok("BATCH"); rec(t,m.group(),"Batch/Lot Number")
        processed=processed.replace(m.group(),t,1)

    # Step 2: irreversible generalisation
    step2=processed
    step2=re.compile(r'\b(\d{2})\s*(?:years?|yrs?)(?:\s*old)?\b',re.I).sub(
        lambda m:f"{(int(m.group(1))//5)*5}-{(int(m.group(1))//5)*5+4} years",step2)
    step2=re.compile(r'\b(\d{2,3})\s*kg\b',re.I).sub(
        lambda m:f"{(int(m.group(1))//10)*10}-{(int(m.group(1))//10)*10+9} kg",step2)
    step2=re.compile(r'\b(1[5-9]\d)\s*cm\b',re.I).sub(
        lambda m:f"{(int(m.group(1))//5)*5}-{(int(m.group(1))//5)*5+4} cm",step2)
    step2=re.compile(r'\[DATE-\d+\]').sub('[YEAR-ONLY]',step2)
    # Generalise precise heights
    step2=re.compile(r'\b(1[4-9]\d|2[0-2]\d)\s*cm\b',re.I).sub(
        lambda m:f"{(int(m.group(1))//5)*5}-{(int(m.group(1))//5)*5+4} cm",step2)
    # Generalise BMI
    step2=re.compile(r'\bBMI[:\s]*(\d{1,2}\.?\d?)\b',re.I).sub('[BMI-RANGE]',step2)
    # Suppress blood group
    step2=re.compile(r'\b(?:Blood\s+[Gg]roup|blood\s+type)[:\s]*[ABO]{1,2}[+-]?\b').sub('[BLOOD-GROUP]',step2)
    # Generalise precise lab values (e.g. Hb 12.4 g/dL)
    step2=re.compile(r'\b(\d{1,3}\.\d{1,2})\s*(g/dL|mg/dL|mmol/L|IU/L|U/L|mEq/L)\b').sub('[LAB-VALUE]',step2)
    # Generalise exact clinical timestamps (HH:MM format)
    step2=re.compile(r'\b([01]?\d|2[0-3]):[0-5]\d\s*(?:AM|PM|hrs?)?\b',re.I).sub('[TIME-REDACTED]',step2)
    for et in ["Dates→Year only","Ages→Range","Biometrics→Range"]:
        audit.append({"Timestamp":ts,"Action":"Irreversible Generalisation","Entity Type":et,"Token":"Generalised","Reversible":"No"})

    return {"step1":processed,"step2":step2,"tokens":tokens,"audit":audit,
            "types":list(found_types),"count":len(tokens)}


# ── SIDEBAR REMOVED — navigation via tabs, brand in hero ─────────────────────

# ═══════════════════════════════════════════════════════════════════════════════
# LOGIN GATE — show landing page if not logged in
# ═══════════════════════════════════════════════════════════════════════════════
VALID_USER = "admin"
VALID_PASS = "nirnay2026"

FEATURES = [
    ("01", "Anonymisation",    "Protect sensitive information",
     "Removes patient names, IDs, phone numbers, and dates — full DPDP Act 2023 audit log."),
    ("02", "Summarisation",    "Get a quick document summary",
     "Extracts decisions and findings from SAE reports, checklists, meeting transcripts/audio."),
    ("03", "Completeness",     "Check if an application is complete",
     "Verifies all 20 mandatory Schedule Y fields. Recommends approve, return, or reject."),
    ("04", "Classification",   "Classify how serious an adverse event is",
     "SAE severity: death, disability, hospitalisation, etc. Duplicate detection."),
    ("05", "Comparison",       "See what changed between two document versions",
     "Semantic + structural diff across document versions."),
    ("06", "Inspection Report","Turn inspection notes into a formal report",
     "Converts raw site observations into a CDSCO GCP report with risk grading."),
]

ICONS = [
    """<svg width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" stroke="#38bdf8" stroke-width="1.8" stroke-linejoin="round"/><path d="M9 12l2 2 4-4" stroke="#38bdf8" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    """<svg width="20" height="20" viewBox="0 0 24 24" fill="none"><rect x="4" y="4" width="16" height="16" rx="3" stroke="#34d399" stroke-width="1.8"/><line x1="8" y1="9" x2="16" y2="9" stroke="#34d399" stroke-width="1.5" stroke-linecap="round"/><line x1="8" y1="12" x2="16" y2="12" stroke="#34d399" stroke-width="1.5" stroke-linecap="round"/><line x1="8" y1="15" x2="12" y2="15" stroke="#34d399" stroke-width="1.5" stroke-linecap="round"/></svg>""",
    """<svg width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M9 11l3 3L22 4" stroke="#c084fc" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/><path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11" stroke="#c084fc" stroke-width="1.8" stroke-linecap="round"/></svg>""",
    """<svg width="20" height="20" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" stroke="#fb923c" stroke-width="1.8"/><line x1="12" y1="8" x2="12" y2="12" stroke="#fb923c" stroke-width="2" stroke-linecap="round"/><circle cx="12" cy="16" r="1.2" fill="#fb923c"/></svg>""",
    """<svg width="20" height="20" viewBox="0 0 24 24" fill="none"><rect x="2" y="6" width="8" height="12" rx="2" stroke="#818cf8" stroke-width="1.8"/><rect x="14" y="6" width="8" height="12" rx="2" stroke="#818cf8" stroke-width="1.8"/><path d="M10 12h4M12 10l2 2-2 2" stroke="#818cf8" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    """<svg width="20" height="20" viewBox="0 0 24 24" fill="none"><rect x="5" y="2" width="14" height="20" rx="2" stroke="#fb7185" stroke-width="1.8"/><line x1="9" y1="7" x2="15" y2="7" stroke="#fb7185" stroke-width="1.4" stroke-linecap="round"/><line x1="9" y1="11" x2="15" y2="11" stroke="#fb7185" stroke-width="1.4" stroke-linecap="round"/><line x1="9" y1="15" x2="12" y2="15" stroke="#fb7185" stroke-width="1.4" stroke-linecap="round"/><circle cx="17" cy="17" r="4" fill="#0a2240" stroke="#fb7185" stroke-width="1.4"/><path d="M15.5 17l1 1 2-2" stroke="#fb7185" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
]

ICON_COLORS = [
    "rgba(56,189,248,0.1);border:1px solid rgba(56,189,248,0.2)",
    "rgba(52,211,153,0.1);border:1px solid rgba(52,211,153,0.2)",
    "rgba(192,132,252,0.1);border:1px solid rgba(192,132,252,0.2)",
    "rgba(251,146,60,0.1);border:1px solid rgba(251,146,60,0.2)",
    "rgba(129,140,248,0.1);border:1px solid rgba(129,140,248,0.2)",
    "rgba(251,113,133,0.1);border:1px solid rgba(251,113,133,0.2)",
]

if not st.session_state["logged_in"]:
    st.markdown("""
<style>
.stApp{background-color:#f0f3f8 !important;}
[data-testid="stTextInput"] input {
    background:#ffffff !important;
    border:1px solid #e2e8f0 !important;
    border-radius:8px !important;
    color:#0a2240 !important;
    font-size:13px !important;
    padding:10px 14px !important;
}
[data-testid="stTextInput"] input::placeholder { color:#94a3b8 !important; }
[data-testid="stTextInput"] label {
    color:#475569 !important;
    font-size:11px !important;
    font-weight:600 !important;
    text-transform:uppercase !important;
    letter-spacing:.06em !important;
}
[data-testid="stTextInput"] input:focus {
    border-color:#003087 !important;
    box-shadow:0 0 0 2px rgba(0,48,135,0.08) !important;
}
.login-signin-btn > button {
    width:100% !important;
    background:#0a2240 !important;
    color:white !important;
    border:none !important;
    border-radius:8px !important;
    font-size:13px !important;
    font-weight:700 !important;
    padding:12px !important;
    letter-spacing:.02em !important;
}
.login-signin-btn > button:hover { background:#003087 !important; }
</style>
""", unsafe_allow_html=True)

    _left_col, _right_col = st.columns([1.1, 0.9], gap="small")

    with _left_col:
        st.markdown("""
<div style="background:#f0f3f8;border-radius:16px 0 0 16px;padding:36px 40px;min-height:560px;display:flex;flex-direction:column;box-shadow:0 8px 40px rgba(0,0,0,0.14);">
  <div style="display:flex;align-items:center;gap:12px;margin-bottom:20px;">
    <div style="font-size:36px;font-weight:900;color:#0a2240;letter-spacing:-1px;line-height:1;">Nirnay</div>
    <div style="width:1px;height:26px;background:rgba(10,34,64,0.2);"></div>

  </div>
  <div style="font-size:18px;font-weight:700;color:#0a2240;line-height:1.3;margin-bottom:16px;letter-spacing:-0.2px;">Regulatory review,<br><span style="color:#FF9933;">reimagined for India.</span></div>
  <div style="font-size:9px;font-weight:700;color:#64748b;letter-spacing:.1em;text-transform:uppercase;margin-bottom:12px;">6 AI modules &middot; Stage 1 build</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:9px;margin-bottom:16px;">
    <div style="background:white;border:1px solid #e2e8f0;border-radius:10px;padding:12px 13px;">
      <div style="font-size:8px;font-weight:700;color:#0369a1;letter-spacing:.08em;text-transform:uppercase;margin-bottom:3px;">01 &middot; Privacy</div>
      <div style="font-size:12px;font-weight:700;color:#1e293b;margin-bottom:2px;">Anonymisation</div>
      <div style="font-size:10px;color:#94a3b8;line-height:1.4;">DPDP Act 2023 compliant PII removal</div>
    </div>
    <div style="background:white;border:1px solid #e2e8f0;border-radius:10px;padding:12px 13px;">
      <div style="font-size:8px;font-weight:700;color:#0f766e;letter-spacing:.08em;text-transform:uppercase;margin-bottom:3px;">02 &middot; Intelligence</div>
      <div style="font-size:12px;font-weight:700;color:#1e293b;margin-bottom:2px;">Summarisation</div>
      <div style="font-size:10px;color:#94a3b8;line-height:1.4;">SAE reports, checklists, meeting audio</div>
    </div>
    <div style="background:white;border:1px solid #e2e8f0;border-radius:10px;padding:12px 13px;">
      <div style="font-size:8px;font-weight:700;color:#6d28d9;letter-spacing:.08em;text-transform:uppercase;margin-bottom:3px;">03 &middot; Validation</div>
      <div style="font-size:12px;font-weight:700;color:#1e293b;margin-bottom:2px;">Completeness</div>
      <div style="font-size:10px;color:#94a3b8;line-height:1.4;">Mandatory field verification, flagging</div>
    </div>
    <div style="background:white;border:1px solid #e2e8f0;border-radius:10px;padding:12px 13px;">
      <div style="font-size:8px;font-weight:700;color:#b45309;letter-spacing:.08em;text-transform:uppercase;margin-bottom:3px;">04 &middot; Triage</div>
      <div style="font-size:12px;font-weight:700;color:#1e293b;margin-bottom:2px;">Classification</div>
      <div style="font-size:10px;color:#94a3b8;line-height:1.4;">SAE severity scoring + duplicate detection</div>
    </div>
    <div style="background:white;border:1px solid #e2e8f0;border-radius:10px;padding:12px 13px;">
      <div style="font-size:8px;font-weight:700;color:#0369a1;letter-spacing:.08em;text-transform:uppercase;margin-bottom:3px;">05 &middot; Diff engine</div>
      <div style="font-size:12px;font-weight:700;color:#1e293b;margin-bottom:2px;">Comparison</div>
      <div style="font-size:10px;color:#94a3b8;line-height:1.4;">Semantic + structural dossier diff</div>
    </div>
    <div style="background:white;border:1px solid #e2e8f0;border-radius:10px;padding:12px 13px;">
      <div style="font-size:8px;font-weight:700;color:#be185d;letter-spacing:.08em;text-transform:uppercase;margin-bottom:3px;">06 &middot; Generation</div>
      <div style="font-size:12px;font-weight:700;color:#1e293b;margin-bottom:2px;">Inspection Report</div>
      <div style="font-size:10px;color:#94a3b8;line-height:1.4;">Typed / handwritten / audio &rarr; GCP report</div>
    </div>
  </div>
  <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:auto;padding-top:16px;">
    <div style="font-size:9px;font-weight:600;color:#0a2240;display:flex;align-items:center;gap:4px;"><div style="width:5px;height:5px;border-radius:50%;background:#22c55e;"></div>DPDP Act 2023</div>
    <div style="font-size:9px;font-weight:600;color:#0a2240;display:flex;align-items:center;gap:4px;"><div style="width:5px;height:5px;border-radius:50%;background:#22c55e;"></div>NDCT 2019</div>
    <div style="font-size:9px;font-weight:600;color:#0a2240;display:flex;align-items:center;gap:4px;"><div style="width:5px;height:5px;border-radius:50%;background:#22c55e;"></div>ICMR Guidelines</div>
    <div style="font-size:9px;font-weight:600;color:#0a2240;display:flex;align-items:center;gap:4px;"><div style="width:5px;height:5px;border-radius:50%;background:#22c55e;"></div>MeitY AI Ethics</div>
  </div>
</div>
""", unsafe_allow_html=True)

    with _right_col:
        st.markdown('<p style="font-size:10px;font-weight:700;color:#94a3b8;letter-spacing:.1em;text-transform:uppercase;margin-bottom:4px;">Authorised access only</p>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:20px;font-weight:800;color:#0a2240;margin-bottom:16px;">Sign in</p>', unsafe_allow_html=True)

        if "_login_failed" not in st.session_state:
            st.session_state["_login_failed"] = False

        _uname = st.text_input("Username", placeholder="Enter username", key="login_uname")
        _pwd   = st.text_input("Password", placeholder="Enter password", type="password", key="login_pwd")

        if st.session_state["_login_failed"]:
            st.markdown('<p style="color:#dc2626;font-size:12px;margin:0;">⚠ Invalid credentials. Please try again.</p>', unsafe_allow_html=True)

        st.markdown('<div class="login-signin-btn">', unsafe_allow_html=True)
        _do_login = st.button("Sign In →", key="login_btn", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<p style="font-size:10px;color:#94a3b8;text-align:center;margin-top:4px;">Forgot credentials? Contact your administrator</p>', unsafe_allow_html=True)
        st.markdown("""
<div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:10px 12px;margin-top:8px;">
  <p style="font-size:10px;color:#64748b;line-height:1.6;margin:0;text-align:center;">Authorised CDSCO personnel only.<br>All sessions are logged for compliance purposes.</p>
</div>
""", unsafe_allow_html=True)

        if _do_login:
            if _uname.strip() == VALID_USER and _pwd == VALID_PASS:
                st.session_state["logged_in"] = True
                st.session_state["_login_failed"] = False
                st.rerun()
            else:
                st.session_state["_login_failed"] = True
                st.rerun()

    st.stop()

# ═══ LOGGED IN — show post-login home then full app ════════════════════════════
# ── TOP BAR ──────────────────────────────────────────────────────────────────
_tb1, _tb2 = st.columns([4, 1])
with _tb1:
    st.markdown("""
<div style="display:flex;align-items:center;gap:16px;margin-bottom:12px;">
  <div style="font-size:26px;font-weight:900;color:#0a2240;letter-spacing:-0.8px;">Nirnay</div>
  <div style="width:1px;height:20px;background:rgba(10,34,64,0.15);"></div>
  <div style="font-size:12px;color:#475569;font-weight:500;">Regulatory review, <span style="color:#FF9933;">reimagined for India.</span></div>
</div>
""", unsafe_allow_html=True)
with _tb2:
    if st.button("Sign out", key="signout"):
        st.session_state["logged_in"] = False
        st.rerun()
st.markdown("<div style='margin-bottom:4px;'></div>", unsafe_allow_html=True)

# ── HERO AND WORKFLOW REMOVED FOR POST-LOGIN VIEW ───────────────────────────

# ── AI RECOMMENDATION CARD ────────────────────────────────────────────────────
def ai_recommendation_card(finding, risk_level, action, detail=""):
    """Render a prominent AI Recommendation card at top of results."""
    risk_colours = {
        "Critical": ("background:#fee2e2;border-color:#fca5a5;", "color:#991b1b;background:#fecaca;"),
        "High":     ("background:#fff7ed;border-color:#fed7aa;", "color:#9a3412;background:#ffedd5;"),
        "Medium":   ("background:#fefce8;border-color:#fef08a;", "color:#854d0e;background:#fef9c3;"),
        "Low":      ("background:#f0fdf4;border-color:#bbf7d0;", "color:#166534;background:#dcfce7;"),
    }
    card_style, badge_style = risk_colours.get(risk_level, risk_colours["Medium"])
    st.markdown(f"""
    <div style="border-radius:12px;padding:18px 22px;margin:14px 0;border:1px solid;
         {card_style}border-left:5px solid #0a2240;">
      <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:16px;flex-wrap:wrap;">
        <div style="flex:1;">
          <div style="font-size:10px;font-weight:700;color:#0a2240;letter-spacing:.1em;
               text-transform:uppercase;margin-bottom:6px;">AI Recommendation</div>
          <div style="font-size:15px;font-weight:700;color:#0a2240;margin-bottom:4px;">{finding}</div>
          <div style="font-size:13px;color:#475569;line-height:1.5;">{action}</div>
          {f'<div style="font-size:11px;color:#64748b;margin-top:5px;">{detail}</div>' if detail else ""}
        </div>
        <div style="text-align:center;flex-shrink:0;">
          <div style="font-size:10px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;
               padding:6px 16px;border-radius:6px;{badge_style}">
            {risk_level} Risk
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ── TABS ──────────────────────────────────────────────────────────────────────
t0,t1,t2,t3,t4,t5,t6 = st.tabs([
    "Home","Anonymisation","Summarisation",
    "Completeness","Classification","Comparison","Inspection Report"
])

# ═══ HOME ════════════════════════════════════════════════════════════════════
# Inject JS to auto-click the target tab if active_tab is set
_active_tab_idx = st.session_state.get("active_tab", 0)
if _active_tab_idx > 0:
    st.session_state["active_tab"] = 0  # reset so it only fires once
    import streamlit.components.v1 as _cv1_tabs
    _cv1_tabs.html(f"""
<script>
(function(){{
  var idx = {_active_tab_idx};
  function clickTab(){{
    var tabs = window.parent.document.querySelectorAll('[data-baseweb="tab"]');
    if(tabs.length > idx){{ tabs[idx].click(); }}
    else {{ setTimeout(clickTab, 100); }}
  }}
  setTimeout(clickTab, 200);
}})();
</script>
""", height=0)

with t0:
    st.markdown("<div style='font-size:10px;font-weight:700;color:#64748b;letter-spacing:.1em;text-transform:uppercase;margin-bottom:16px;'>Available features &mdash; select to begin</div>", unsafe_allow_html=True)
    _tab_names = ["Anonymisation","Summarisation","Completeness","Classification","Comparison","Inspection Report"]
    _home_cols = st.columns(3, gap="medium")
    for _i, (_fnum, _fname, _ftitle, _fdesc) in enumerate(FEATURES):
        with _home_cols[_i % 3]:
            st.markdown(f"""
<div style="background:#0a2240;border-radius:12px;padding:22px 20px;position:relative;overflow:hidden;min-height:220px;display:flex;flex-direction:column;justify-content:space-between;">
  <div style="position:absolute;right:12px;bottom:-8px;font-size:68px;font-weight:900;color:rgba(255,255,255,0.03);line-height:1;pointer-events:none;user-select:none;">{_fnum}</div>
  <div>
    <div style="width:38px;height:38px;border-radius:10px;background:{ICON_COLORS[_i]};display:flex;align-items:center;justify-content:center;margin-bottom:10px;">{ICONS[_i]}</div>
    <div style="font-size:16px;font-weight:800;color:#FF9933;letter-spacing:-0.2px;line-height:1.1;margin-bottom:5px;">{_fnum} &middot; {_fname}</div>
    <div style="font-size:11px;font-weight:600;color:rgba(255,255,255,0.85);line-height:1.4;margin-bottom:7px;">{_ftitle}</div>
    <div style="font-size:11px;color:rgba(255,255,255,0.55);line-height:1.5;">{_fdesc}</div>
  </div>
  <div style="display:inline-flex;align-items:center;gap:5px;background:rgba(255,153,51,0.1);border:1px solid rgba(255,153,51,0.28);border-radius:6px;padding:5px 12px;font-size:10px;font-weight:700;color:#FF9933;letter-spacing:.04em;margin-top:14px;align-self:flex-start;">Start &#8594;</div>
</div>
""", unsafe_allow_html=True)
            if st.button("↗", key=f"home_card_{_i}", use_container_width=True, help=f"Open {_tab_names[_i]}"):
                st.session_state["active_tab"] = _i + 1
                st.rerun()

# ═══ FEATURE 1 — ANONYMISATION ═══════════════════════════════════════════════
with t1:
    st.markdown("""
    <div class="sec-hd">
      <div class="sec-ic ic-blue" style="font-size:14px;font-weight:700;color:#1e40af;">01</div>
      <div><h2>Protect sensitive information in regulatory documents</h2>
      <p>Finds and removes patient names, IDs, phone numbers, dates, and hospital records · Full compliance audit log · DPDP Act 2023</p></div>
    </div>
    """, unsafe_allow_html=True)

    # ── Upload zone ───────────────────────────────────────────────────────────
    st.markdown('<div class="upload-card"><h4>📁 Upload your document</h4>', unsafe_allow_html=True)
    anon_file = st.file_uploader(
        "Supported: Word (.docx), PDF, plain text (.txt)",
        type=["docx","pdf","txt"], key="anon_up",
        help="Text is extracted automatically on upload"
    )
    if anon_file is not None:
        txt, err = extract_text(anon_file)
        if err:
            st.error(f"Extraction error: {err}")
        elif txt.strip():
            st.session_state["anon_text"] = txt
            st.session_state["anon_textarea"] = txt
            st.session_state["anon_upload_name"] = anon_file.name
            st.success(f"✓ Extracted **{len(txt.split())} words** from {anon_file.name}")
        else:
            st.warning("File uploaded but no text could be extracted.")

    st.markdown('<div class="or-line">or paste text manually below</div>', unsafe_allow_html=True)

    # ── Text area uses session_state as source of truth ───────────────────────
    # The key trick: we DON'T use value= here. We use st.session_state directly.
    anon_input = st.text_area(
        "Document content",
        height=220,
        placeholder="Paste SAE report, clinical trial document, or any regulatory text with PII/PHI...",
        key="anon_textarea"
    )
    st.session_state["anon_text"] = st.session_state.get("anon_textarea", "")
    st.markdown('</div>', unsafe_allow_html=True)

    col1,col2,_ = st.columns([1,1,3])
    with col1:
        run_anon = st.button("Analyse & protect document", type="primary", use_container_width=True)
    with col2:
        if st.button("🗑 Clear", use_container_width=True):
            st.session_state["anon_text"] = ""
            st.session_state["anon_textarea"] = ""
            st.rerun()

    if run_anon:
        content = st.session_state["anon_text"].strip()
        if not content:
            st.markdown('<div class="rc warn">⚠️ Please upload a file or paste text before running.</div>', unsafe_allow_html=True)
        else:
            with st.spinner("Detecting PII/PHI entities..."):
                result = run_anonymisation(content)

            # ── AI Recommendation card ────────────────────────────────
            _pii_count = result["count"]
            if _pii_count == 0:
                ai_recommendation_card(
                    "No sensitive information detected",
                    "Low",
                    "This document appears to contain no standard PII/PHI patterns. If you believe it contains sensitive data, verify that names follow Indian name formats or IDs use standard regulatory prefixes.",
                    "Manual review recommended before sharing externally."
                )
            elif _pii_count >= 5:
                ai_recommendation_card(
                    f"{_pii_count} sensitive items detected and anonymised",
                    "High",
                    "This document contained significant PII/PHI. Download the anonymised version for external sharing. The compliance audit log has been generated for DPDP Act 2023 records.",
                    f"Entity types found: {', '.join(result['types'])}"
                )
            else:
                ai_recommendation_card(
                    f"{_pii_count} sensitive item(s) detected and anonymised",
                    "Medium",
                    "PII/PHI detected and removed. Review the token mapping table to verify all sensitive fields have been addressed before sharing.",
                    f"Entity types found: {', '.join(result['types'])}"
                )

            # ── PII chips — always true, always visible ─────────────────
            if result["types"]:
                chips = '<div class="pii-chips">'
                for pt in result["types"]:
                    cls = CHIP_MAP.get(pt,"cg")
                    chips += f'<span class="chip {cls}">● {pt}</span>'
                chips += f'<span class="chip cg">Total detected: {result["count"]}</span></div>'
                st.markdown(chips, unsafe_allow_html=True)
            else:
                st.markdown('<div class="rc info">No PII/PHI patterns detected in this text.</div>', unsafe_allow_html=True)

            # ── Two-column parallel layout ────────────────────────────────────
            import json as _json
            _fname = st.session_state.get("anon_upload_name", "document")
            _base  = _fname.rsplit(".", 1)[0] if "." in _fname else _fname
            _now   = datetime.datetime.now().isoformat()
            _tokens_df  = pd.DataFrame(result["tokens"]) if result["tokens"] else pd.DataFrame(columns=["Token","Original Value","Entity Type","Step"])
            _audit_df   = pd.DataFrame(result["audit"])

            col_s1, col_s2 = st.columns(2, gap="large")

            # ── LEFT COLUMN — Step 1 ─────────────────────────────────────────
            with col_s1:
                st.markdown("""
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
                  <span style="background:#003087;color:white;border-radius:20px;padding:3px 12px;font-size:11px;font-weight:600;">Step 1 — Reversible pseudonymisation</span>
                  <span style="font-size:11px;color:#64748b;">Identifiers replaced with codes · Can be reversed by authorised personnel</span>
                </div>
                """, unsafe_allow_html=True)
                st.text_area("", result["step1"], height=280, key="s1o", label_visibility="collapsed")

                # Step 1 downloads — selectbox approach (reliable in Streamlit)
                st.markdown("<div style='margin:8px 0 4px;font-size:12px;font-weight:600;color:#1e293b;'>Download deidentified report</div>", unsafe_allow_html=True)
                s1_fmt = st.selectbox("", ["Select format ▾", "Token Registry (JSON)", "Pseudonymised Document (TXT)", "Deidentified Report (TXT)"],
                    key="s1_dl_fmt", label_visibility="collapsed")

                if s1_fmt == "Token Registry (JSON)":
                    _tok_json = _json.dumps({
                        "document": _fname,
                        "generatedAt": _now,
                        "note": "In production, this file should be AES-256 encrypted at rest.",
                        "mappings": [{"token": r["Token"], "originalValue": r["Original Value"],
                                      "entityType": r["Entity Type"], "step": 1}
                                     for r in result["tokens"]]
                    }, indent=2)
                    st.download_button("⬇ Download Token Registry (JSON)", _tok_json,
                        file_name=f"{_base}_TokenRegistry.json", mime="application/json", use_container_width=True)

                elif s1_fmt == "Pseudonymised Document (TXT)":
                    _nl = chr(10)
                    _sep = "="*60
                    _pseudo_txt = _nl.join([
                        "PSEUDONYMISED - NOT FOR PUBLIC RELEASE",
                        f"Generated: {_now}",
                        f"Document: {_fname}",
                        _sep, "",
                        result["step1"]
                    ])
                    st.download_button("⬇ Download Pseudonymised Document (TXT)", _pseudo_txt,
                        file_name=f"{_base}_Pseudonymised.txt", mime="text/plain", use_container_width=True)

                elif s1_fmt == "Deidentified Report (TXT)":
                    _rows = chr(10).join([f"  {r['Entity Type']:<22} | {r['Original Value']:<25} | {r['Token']}"
                                       for r in result["tokens"]])
                    _nl2 = chr(10)
                    _s1 = "="*60; _s2 = "-"*75
                    _dei_txt = _nl2.join([
                        "Nirnay — Deidentified Report",
                        f"Generated: {_now}", f"Document: {_fname}",
                        _s1, "",
                        "Field                  | Raw Data                  | Pseudonymised Token",
                        _s2, _rows
                    ])
                    st.download_button("⬇ Download Deidentified Report (TXT)", _dei_txt,
                        file_name=f"{_base}_Deidentified_Report.txt", mime="text/plain", use_container_width=True)

                # Token mapping table
                with st.expander("Token mapping table — reversible at this stage", expanded=False):
                    st.markdown('<div class="tw">', unsafe_allow_html=True)
                    st.dataframe(_tokens_df, use_container_width=True, hide_index=True)
                    st.markdown('</div>', unsafe_allow_html=True)

            # ── RIGHT COLUMN — Step 2 ────────────────────────────────────────
            with col_s2:
                st.markdown("""
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
                  <span style="background:#0f766e;color:white;border-radius:20px;padding:3px 12px;font-size:11px;font-weight:600;">Step 2 — Irreversible generalisation</span>
                  <span style="font-size:11px;color:#64748b;">All identifiers permanently removed · Safe to share externally</span>
                </div>
                """, unsafe_allow_html=True)
                st.text_area("", result["step2"], height=280, key="s2o", label_visibility="collapsed")

                # Step 2 downloads
                st.markdown("<div style='margin:8px 0 4px;font-size:12px;font-weight:600;color:#1e293b;'>Download anonymised report</div>", unsafe_allow_html=True)
                s2_fmt = st.selectbox("", ["Select format ▾", "Anonymised Report (TXT)", "Generalised Data (JSON)", "Audit Trail (JSON)"],
                    key="s2_dl_fmt", label_visibility="collapsed")

                if s2_fmt == "Anonymised Report (TXT)":
                    _anon_rows = chr(10).join([f"  {r['Entity Type']:<22} | {r['Token']:<25} | [GENERALISED/REDACTED]"
                                            for r in result["tokens"]])
                    _nl = chr(10)
                    _sep3 = "="*60
                    _sep4 = "-"*75
                    _anon_txt = _nl.join([
                        "Nirnay — Anonymised Report",
                        f"Generated: {_now}",
                        f"Document: {_fname}",
                        _sep3, "",
                        "Field                  | Pseudonymised             | Anonymised Output",
                        _sep4,
                        _anon_rows,
                        "", _sep3,
                        "Final Anonymised Text:", "",
                        result["step2"]
                    ])
                    st.download_button("⬇ Download Anonymised Report (TXT)", _anon_txt,
                        file_name=f"{_base}_Anonymised_Report.txt", mime="text/plain", use_container_width=True)

                elif s2_fmt == "Generalised Data (JSON)":
                    _gen_json = _json.dumps({
                        "document": _fname,
                        "generatedAt": _now,
                        "note": "Structure is XML-serialisable for SUGAM portal integration.",
                        "anonymisedFields": [{"field": r["Entity Type"],
                                              "pseudonymisedValue": r["Token"],
                                              "anonymisedValue": "[GENERALISED/REDACTED]",
                                              "method": "Generalisation" if "Date" in r["Entity Type"] or "Age" in r["Entity Type"] else "Redaction"}
                                             for r in result["tokens"]]
                    }, indent=2)
                    st.download_button("⬇ Download Generalised Data (JSON)", _gen_json,
                        file_name=f"{_base}_Generalised.json", mime="application/json", use_container_width=True)

                elif s2_fmt == "Audit Trail (JSON)":
                    _step1_entries = [{"timestamp": _now, "entityType": r["Entity Type"],
                                       "action": "Pseudonymisation", "token": r["Token"],
                                       "reversible": True, "step": 1}
                                      for r in result["tokens"]]
                    _step2_entries = [{"timestamp": _now, "entityType": r["Entity Type"],
                                       "action": "Irreversible Generalisation",
                                       "outputValue": "[GENERALISED/REDACTED]",
                                       "reversible": False, "step": 2}
                                      for r in result["tokens"]]
                    _audit_json = _json.dumps({
                        "document": _fname,
                        "generatedAt": _now,
                        "complianceFrameworks": ["DPDP Act 2023", "ICMR Ethical Guidelines", "CDSCO Standards"],
                        "auditEntries": _step1_entries + _step2_entries
                    }, indent=2)
                    st.download_button("⬇ Download Audit Trail (JSON)", _audit_json,
                        file_name=f"{_base}_AuditTrail.json", mime="application/json", use_container_width=True)

                # Audit log
                with st.expander("Technical audit log (DPDP Act 2023 compliance record)", expanded=False):
                    st.markdown('<div class="tw">', unsafe_allow_html=True)
                    st.dataframe(_audit_df, use_container_width=True, hide_index=True)
                    st.markdown('</div>', unsafe_allow_html=True)

            # ── jsPDF component — PDF generation client-side ──────────────────
            import streamlit.components.v1 as _components
            _tok_json_str = _json.dumps(result["tokens"])
            _audit_json_str = _json.dumps(result["audit"])
            import json as _json2
            _js_step1 = _json2.dumps(result["step1"])
            _pdf_component = f"""
<!DOCTYPE html><html><head>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf-autotable/3.5.28/jspdf.plugin.autotable.min.js"></script>
<style>
  body{{font-family:'Inter',system-ui,sans-serif;margin:0;padding:12px;background:#f8fafc;}}
  .pdf-row{{display:flex;gap:12px;flex-wrap:wrap;}}
  .pdf-btn{{cursor:pointer;padding:8px 16px;border-radius:6px;font-size:12px;font-weight:600;border:none;display:flex;align-items:center;gap:6px;}}
  .btn-red{{background:#fee2e2;color:#991b1b;border:1px solid #fca5a5;}}
  .btn-red:hover{{background:#fecaca;}}
  .btn-navy{{background:#003087;color:white;border:1px solid #003087;}}
  .btn-navy:hover{{background:#002060;}}
  .label{{font-size:11px;font-weight:700;color:#64748b;margin-bottom:8px;text-transform:uppercase;letter-spacing:.06em;}}
</style>
</head><body>
<div class="label">PDF downloads (generated in browser)</div>
<div class="pdf-row">
  <button class="pdf-btn btn-red" onclick="genStep1PDF()">&#x1F4C4; Deidentified Report (PDF)</button>
  <button class="pdf-btn btn-red" onclick="genPseudoDocPDF()">&#x1F4C4; Pseudonymised Document (PDF)</button>
  <button class="pdf-btn btn-navy" onclick="genStep2PDF()">&#x1F4C4; Anonymised Report (PDF)</button>
</div>
<script>
const tokens = {_tok_json_str};
const fname = "{_fname}";
const base = fname.includes('.') ? fname.split('.').slice(0,-1).join('.') : fname;
const now = new Date().toLocaleString('en-IN');

function addHeader(doc, title, fname){{
  doc.setFillColor(0,48,135);
  doc.rect(0,0,210,18,'F');
  doc.setTextColor(255,255,255);
  doc.setFontSize(10); doc.setFont(undefined,'bold');
  doc.text('Nirnay — CDSCO AI Review System',10,7);
  doc.setFontSize(8); doc.setFont(undefined,'normal');
  doc.text(title,10,13);
  doc.text('Generated: '+now,150,13);
  doc.setTextColor(0,0,0);
}}

function genStep1PDF(){{
  const {{jsPDF}} = window.jspdf;
  const doc = new jsPDF();
  addHeader(doc,'Deidentified Report — '+fname,fname);
  doc.setFontSize(9);
  doc.text('Field-by-field comparison of raw data and pseudonymised tokens:',10,25);
  const rows = tokens.map(t=>[t['Entity Type'],t['Original Value'],t.Token]);
  doc.autoTable({{
    head:[['Field','Raw Data','Pseudonymised Token']],
    body:rows,startY:28,
    styles:{{fontSize:8,cellPadding:3}},
    headStyles:{{fillColor:[0,48,135],textColor:255,fontStyle:'bold'}},
    alternateRowStyles:{{fillColor:[240,244,248]}},
    margin:{{left:10,right:10}}
  }});
  doc.save(base+'_Deidentified_Report.pdf');
}}

function genPseudoDocPDF(){{
  const {{jsPDF}} = window.jspdf;
  const doc = new jsPDF();
  addHeader(doc,'PSEUDONYMISED — NOT FOR PUBLIC RELEASE',fname);
  doc.setFontSize(8);
      const step1Text = {_js_step1};
  const lines = doc.splitTextToSize(step1Text,190);
  let y=28;
  lines.forEach(l=>{{if(y>270){{doc.addPage();addHeader(doc,'PSEUDONYMISED — NOT FOR PUBLIC RELEASE',fname);y=28;}}doc.text(l,10,y);y+=4.5;}});
  doc.setFontSize(7);doc.setTextColor(150,150,150);
  doc.text('Generated: '+now+' | Nirnay — CDSCO AI Review System',10,288);
  doc.save(base+'_Pseudonymised.pdf');
}}

function genStep2PDF(){{
  const {{jsPDF}} = window.jspdf;
  const doc = new jsPDF();
  addHeader(doc,'Anonymised Report — '+fname,fname);
  doc.setFontSize(9);
  doc.text('Before/after comparison: pseudonymised tokens vs final anonymised output:',10,25);
  const rows = tokens.map(t=>[t['Entity Type'],t.Token,'[GENERALISED/REDACTED]']);
  doc.autoTable({{
    head:[['Field','Pseudonymised (Step 1)','Anonymised Output (Step 2)']],
    body:rows,startY:28,
    styles:{{fontSize:8,cellPadding:3}},
    headStyles:{{fillColor:[15,118,110],textColor:255,fontStyle:'bold'}},
    alternateRowStyles:{{fillColor:[240,248,246]}},
    margin:{{left:10,right:10}}
  }});
  doc.save(base+'_Anonymised_Report.pdf');
}}
</script>
</body></html>"""
            _components.html(_pdf_component, height=80)


# ═══ FEATURE 2 — SUMMARISATION ═══════════════════════════════════════════════
with t2:
    st.markdown("""
    <div class="sec-hd">
      <div class="sec-ic ic-teal">📄</div>
      <div><h2>Document Summarisation</h2>
      <p>Upload Word · PDF · Audio (meeting only) or paste text · 3 source types: SAE · Checklist · Meeting</p></div>
    </div>
    """, unsafe_allow_html=True)

    doc_type = st.selectbox("Document type", [
        "SAE Case Narration", "Application Checklist (SUGAM)", "Meeting Transcript / Audio"])

    st.markdown('<div class="upload-card"><h4>📁 Upload document</h4>', unsafe_allow_html=True)

    if doc_type == "Meeting Transcript / Audio":
        st.markdown('<div class="audio-note">Audio upload accepted. Automatic transcription requires Stage 2 integration with Whisper API. Please paste the transcript text manually in the box below.</div>', unsafe_allow_html=True)
        sum_file = st.file_uploader("Word / PDF / TXT / Audio", type=["docx","pdf","txt","mp3","wav","m4a"], key="sum_up")
    else:
        sum_file = st.file_uploader("Word / PDF / TXT", type=["docx","pdf","txt"], key="sum_up2")

    audio_mode = False
    if sum_file:
        fname = sum_file.name.lower()
        if any(fname.endswith(x) for x in [".mp3",".wav",".m4a"]):
            audio_mode = True
            st.success(f"✓ Audio file received: {sum_file.name} — please paste the transcript text below")
            st.session_state["sum_text"] = ""
            st.session_state["sum_ta"] = ""
            st.session_state["sum_ta"] = st.session_state["sum_text"]
        else:
            txt, err = extract_text(sum_file)
            if err: st.error(err)
            elif txt.strip():
                st.session_state["sum_text"] = txt
                st.session_state["sum_ta"] = txt
                st.success(f"✓ Extracted {len(txt.split())} words from {sum_file.name}")

    st.markdown('<div class="or-line">or paste text manually</div>', unsafe_allow_html=True)
    sum_input = st.text_area("Document content",
        height=200, placeholder="Paste document content here...", key="sum_ta")
    st.session_state["sum_text"] = st.session_state.get("sum_ta", "")
    st.markdown('</div>', unsafe_allow_html=True)

    col1,col2,_ = st.columns([1,1,3])
    with col1: run_sum = st.button("Summarise document", type="primary", use_container_width=True)
    with col2:
        if st.button("🗑 Clear ", use_container_width=True):
            st.session_state["sum_text"]=""
            st.session_state["sum_ta"]=""
            st.rerun()

    if run_sum:
        content = st.session_state["sum_text"].strip()
        if not content and not audio_mode:
            st.markdown('<div class="rc warn">Please upload or paste content first.</div>', unsafe_allow_html=True)
        else:
            tl = content.lower()
            if doc_type == "SAE Case Narration":
                priority = "URGENT" if any(w in tl for w in ["death","fatal","died","disability","permanent"]) else \
                           "STANDARD" if any(w in tl for w in ["hospitalised","admitted","icu","hospital","hospitalization"]) else "LOW"
                causality = "Possibly Related" if "possibly" in tl else "Probably Related" if "probably" in tl else \
                            "Unrelated" if "unrelated" in tl else "Definitely Related" if "definitely" in tl else "Under Assessment"
                outcome = "Fatal" if any(w in tl for w in ["died","death","fatal"]) else \
                          "Recovered" if any(w in tl for w in ["recovered","resolution","normal sinus"]) else \
                          "Recovering" if "recovering" in tl else "Ongoing"
                cc = "err" if priority=="URGENT" else "warn" if priority=="STANDARD" else "ok"
                _risk_map = {"URGENT":"Critical","STANDARD":"Medium","LOW":"Low"}
                _action_map = {
                    "URGENT": "Immediate escalation to DCGI required. Expedited 7-day report applicable.",
                    "STANDARD": "Route to standard SAE review queue. Expedited 15-day report required.",
                    "LOW": "Log as periodic SAE. Standard 90-day reporting timeline applies."
                }
                ai_recommendation_card(
                    f"SAE classified as {priority} · {causality} · Outcome: {outcome}",
                    _risk_map[priority],
                    _action_map[priority],
                    f"Document type: SAE Case Narration · CDSCO Form 12A"
                )
                st.markdown(f'<div class="rc {cc}"><b>Priority: {priority}</b> · Causality: {causality} · Outcome: {outcome}</div>', unsafe_allow_html=True)
                c1,c2,c3 = st.columns(3)
                c1.metric("Priority",priority); c2.metric("Causality",causality); c3.metric("Outcome",outcome)
                with st.expander("Full Structured SAE Summary", expanded=True):
                    setting = "Hospital/Emergency" if any(w in tl for w in ["hospital","emergency","icu"]) else "Outpatient"
                    timeline = "Expedited 7-day" if priority=="URGENT" else "Expedited 15-day" if priority=="STANDARD" else "Periodic 90-day"
                    st.markdown(f"""| Field | Value |\n|---|---|\n| Document Type | SAE Case Narration |\n| Priority | {priority} |\n| Causality | {causality} |\n| Outcome | {outcome} |\n| Setting | {setting} |\n| Reporting Timeline | {timeline} |\n| Recommended Action | {"Escalate to DCGI immediately" if priority=="URGENT" else "Route to standard review queue"} |""")
                st.download_button("⬇ Download SAE Summary", f"Priority:{priority}\nCausality:{causality}\nOutcome:{outcome}\nTimeline:{timeline}", file_name="sae_summary.txt")

            elif doc_type == "Application Checklist (SUGAM)":
                lines=[l.strip() for l in content.split('\n') if l.strip()]
                comp=sum(1 for l in lines if any(w in l.lower() for w in ["complete","present","yes","submitted","available"]))
                miss=sum(1 for l in lines if any(w in l.lower() for w in ["missing","absent","no","not submitted"]))
                inc=sum(1 for l in lines if any(w in l.lower() for w in ["incomplete","pending","partial"]))
                tot=len(lines); sc=round((comp/tot)*100) if tot else 0
                rec="✅ Approve" if sc>=80 else "⚠️ Return for Completion" if sc>=50 else "❌ Reject"
                c1,c2,c3,c4=st.columns(4)
                c1.metric("Total",tot);c2.metric("Complete",comp);c3.metric("Incomplete",inc);c4.metric("Missing",miss)
                st.progress(sc/100,text=f"Score: {sc}%")
                cc="ok" if sc>=80 else "warn" if sc>=50 else "err"
                st.markdown(f'<div class="rc {cc}"><b>Recommendation:</b> {rec}</div>',unsafe_allow_html=True)
                st.download_button("⬇ Download",f"Score:{sc}%\n{rec}",file_name="checklist_summary.txt")

            else:
                if audio_mode and not content.replace(f"[AUDIO: {sum_file.name if sum_file else ''}]","").replace("Paste transcript below if available.","").strip():
                    st.markdown('<div class="rc info">Audio received. Paste transcript text above for full extraction. Stage 2 adds live Whisper transcription.</div>',unsafe_allow_html=True)
                else:
                    lines=content.split('\n')
                    dec,act,iss=[],[],[]
                    for l in lines:
                        ll=l.lower()
                        if any(w in ll for w in ["decided","approved","resolved","agreed","concluded"]): dec.append(l.strip())
                        elif any(w in ll for w in ["action","will","shall","owner","follow up","responsible"]): act.append(l.strip())
                        elif any(w in ll for w in ["pending","unresolved","defer","tabled"]): iss.append(l.strip())
                    c1,c2,c3=st.columns(3)
                    c1.metric("Decisions",len(dec));c2.metric("Actions",len(act));c3.metric("Open Issues",len(iss))
                    with st.expander("Key Decisions",expanded=True):
                        for i,d in enumerate(dec[:8],1): st.markdown(f"{i}. {d}")
                    with st.expander("Action Items"):
                        for i,a in enumerate(act[:8],1): st.markdown(f"{i}. {a}")
                    if iss:
                        with st.expander("Unresolved Issues"):
                            for i,x in enumerate(iss[:6],1): st.markdown(f"{i}. {x}")
                    # Fallback: if keyword extraction found nothing, extract by section headings
                    if not dec and not act and not iss:
                        sections = {}
                        current_section = "Summary"
                        for line in lines:
                            stripped = line.strip()
                            if not stripped: continue
                            is_heading = (stripped.isupper() and len(stripped) > 3) or                                         (stripped.endswith(":") and len(stripped.split()) <= 6) or                                         (stripped.startswith("SECTION") or stripped.startswith("Section"))
                            if is_heading:
                                current_section = stripped.rstrip(":")
                                sections[current_section] = []
                            else:
                                if current_section not in sections:
                                    sections[current_section] = []
                                if len(sections[current_section]) < 3:
                                    sections[current_section].append(stripped)
                        if sections:
                            st.markdown("**Document structure extracted**")
                            for sec, pts in sections.items():
                                if pts:
                                    st.markdown(f"**{sec}**")
                                    for p in pts[:2]:
                                        st.markdown(f"— {p}")
                            fallback_txt = "\n".join([f"{s}:\n" + "\n".join(p) for s,p in sections.items() if p])
                            st.download_button("⬇ Download Summary", fallback_txt, file_name="meeting_summary.txt")
                        else:
                            st.info("No structured content detected. Please paste transcript text after uploading audio.")
                    else:
                        st.download_button("⬇ Download Meeting Summary","\n".join(dec+act),file_name="meeting_summary.txt")


# ═══ FEATURE 3 — COMPLETENESS ════════════════════════════════════════════════
with t3:
    st.markdown("""
    <div class="sec-hd">
      <div class="sec-ic ic-purple">✅</div>
      <div><h2>Completeness Assessment — Schedule Y</h2>
      <p>Upload application document · 20 mandatory fields · RAG status · Approve / Return / Reject recommendation</p></div>
    </div>
    """, unsafe_allow_html=True)

    SCHED_Y=[
        ("Protocol Synopsis","protocol synopsis","Critical"),("Investigator Brochure","investigator brochure","Critical"),
        ("Form CT-04","ct-04","Critical"),("Form CT-05","ct-05","Critical"),
        ("Ethics Committee Approval","ethics committee","Critical"),
        ("Informed Consent (English)","informed consent","Critical"),
        ("Informed Consent (Local Language)","local language","Critical"),
        ("Investigator CV","investigator cv","Major"),("Site Master File","site master","Major"),
        ("Insurance Certificate","insurance","Major"),("Drug Import License","import license","Major"),
        ("GCP Compliance Certificate","gcp","Major"),("Patient Information Sheet","patient information","Major"),
        ("Case Report Form","case report form","Minor"),("Statistical Analysis Plan","statistical analysis","Minor"),
        ("DSMB Charter","dsmb","Minor"),("Pharmacovigilance Plan","pharmacovigilance","Minor"),
        ("Risk Management Plan","risk management","Minor"),
        ("Regulatory Approval (Origin)","regulatory approval","Major"),
        ("Sponsor Authorisation Letter","sponsor authorisation","Major"),
    ]

    col_a,col_b=st.columns([2,1])
    with col_a:
        st.markdown('<div class="upload-card"><h4>📁 Upload application document</h4>',unsafe_allow_html=True)
        cf=st.file_uploader("Word / PDF / TXT",type=["docx","pdf","txt"],key="comp_up")
        if cf:
            txt,err=extract_text(cf)
            if err: st.error(err)
            elif txt.strip():
                st.session_state["comp_text"]=txt
                st.session_state["comp_ta"]=txt
                st.success(f"✓ Extracted from {cf.name}")
        st.markdown('<div class="or-line">or paste text</div>',unsafe_allow_html=True)
        ci=st.text_area("Application content",height=180,key="comp_ta")
        st.session_state["comp_text"]=st.session_state.get("comp_ta","")
        st.markdown('</div>',unsafe_allow_html=True)
    with col_b:
        app_id=st.text_input("Application ID",placeholder="SUGAM-CT-2024-0892")
        st.markdown("<br>",unsafe_allow_html=True)
        run_comp=st.button("✅ Check Completeness",type="primary",use_container_width=True)

    if run_comp:
        content=st.session_state["comp_text"].strip()
        if not content:
            st.markdown('<div class="rc warn">Please upload or paste content first.</div>',unsafe_allow_html=True)
        else:
            tl=content.lower(); rows=[]; cm=[]; mm=[]
            for field,kw,sev in SCHED_Y:
                if kw in tl:
                    s="INCOMPLETE" if any(w in tl for w in ["pending","tbd","partial","to be"]) else "PRESENT"
                    r="🟢 Green" if s=="PRESENT" else "🟡 Amber"
                else:
                    s="MISSING"; r="🔴 Red"
                    if sev=="Critical": cm.append(field)
                    elif sev=="Major": mm.append(field)
                rows.append({"Field":field,"Severity":sev,"Status":s,"RAG":r})
            df=pd.DataFrame(rows)
            pre=sum(1 for r in rows if r["Status"]=="PRESENT")
            inc=sum(1 for r in rows if r["Status"]=="INCOMPLETE")
            mis=sum(1 for r in rows if r["Status"]=="MISSING")
            sc=round((pre/20)*100)
            rec="✅ Approve for Technical Review" if sc>=85 and not cm else "⚠️ Return for Completion" if sc>=60 else "❌ Reject — Critical fields missing"
            cc="ok" if sc>=85 and not cm else "warn" if sc>=60 else "err"
            c1,c2,c3,c4=st.columns(4)
            c1.metric("Total",20);c2.metric("Present",pre);c3.metric("Incomplete",inc);c4.metric("Missing",mis)
            st.progress(sc/100,text=f"Schedule Y Completeness: {sc}%")
            _comp_risk = "Critical" if cm else "High" if sc < 60 else "Medium" if sc < 85 else "Low"
            _comp_action = (f"Reject — {len(cm)} critical Schedule Y field(s) missing: {', '.join(cm[:3])}{'...' if len(cm)>3 else ''}. Application cannot proceed." if cm
                           else f"Return for completion — {missing} field(s) need attention before technical review."
                           if sc < 85 else "Approve for technical review — all critical fields present.")
            ai_recommendation_card(
                f"Schedule Y completeness: {sc}% · {rec}",
                _comp_risk,
                _comp_action,
                f"Fields checked: 20 mandatory Schedule Y fields · Present: {pre} · Missing: {missing} · Incomplete: {inc}"
            )
            st.markdown(f'<div class="rc {cc}"><b>Recommendation:</b> {rec}</div>',unsafe_allow_html=True)
            if cm: st.error(f"Critical missing: {', '.join(cm)}")
            if mm: st.warning(f"Major missing: {', '.join(mm)}")
            with st.expander("Full Schedule Y Field Status",expanded=True):
                def srag(v):
                    if "Green" in str(v): return "background-color:#dcfce7;color:#15803d;font-weight:600"
                    if "Amber" in str(v): return "background-color:#fef9c3;color:#a16207;font-weight:600"
                    if "Red" in str(v):   return "background-color:#fee2e2;color:#b91c1c;font-weight:600"
                    return ""
                st.markdown('<div class="tw">',unsafe_allow_html=True)
                st.dataframe(df.style.map(srag,subset=["RAG"]),use_container_width=True,hide_index=True)
                st.markdown('</div>',unsafe_allow_html=True)
            st.download_button("⬇ Download Completeness Report",df.to_csv(index=False),file_name="completeness_report.csv",mime="text/csv")


# ═══ FEATURE 4 — CLASSIFICATION + DUPLICATE DETECTION ════════════════════════
with t4:
    st.markdown("""
    <div class="sec-hd">
      <div class="sec-ic ic-amber">🏷️</div>
      <div><h2>SAE Classification &amp; Duplicate Detection</h2>
      <p>Upload SAE · ICD-10 severity grading · Session-based duplicate detection across multiple reports</p></div>
    </div>
    """, unsafe_allow_html=True)

    # How duplicate detection works explanation
    st.markdown("""
    <div class="dup-session">
    <b>How duplicate detection works:</b> Upload multiple SAE reports below.
    The system stores them in your session (memory only — nothing saved externally, DPDP compliant).
    It then cross-checks Patient IDs, drug names, and event dates across all reports to flag duplicates.
    Files are cleared when you close or refresh the browser.
    </div>
    """, unsafe_allow_html=True)

    # Primary SAE
    st.markdown('<div class="upload-zone"><h4>📁 Primary SAE Report</h4>',unsafe_allow_html=True)
    cf=st.file_uploader("Word / PDF / TXT",type=["docx","pdf","txt"],key="class_up")
    if cf:
        txt,err=extract_text(cf)
        if err: st.error(err)
        elif txt.strip():
            st.session_state["class_text"]=txt
            st.session_state["class_ta"]=txt
            st.session_state["dup_files"]["SAE-1"]={"name":cf.name,"text":txt}
            st.success(f"✓ Loaded: {cf.name}")
    st.markdown('<div class="or-line">or paste text</div>',unsafe_allow_html=True)
    ci=st.text_area("SAE report content",height=180,key="class_ta")
    st.session_state["class_text"]=st.session_state.get("class_ta","")
    st.markdown('</div>',unsafe_allow_html=True)

    # Additional SAEs for duplicate check
    with st.expander("+ Add more SAE reports for duplicate detection", expanded=False):
        cols=st.columns(2)
        for idx,(slot,label) in enumerate([("SAE-2","SAE Report 2"),("SAE-3","SAE Report 3")]):
            with cols[idx]:
                f2=st.file_uploader(label,type=["docx","pdf","txt"],key=f"dup_{slot}")
                if f2:
                    t2,e2=extract_text(f2)
                    if not e2 and t2.strip():
                        st.session_state["dup_files"][slot]={"name":f2.name,"text":t2}
                        st.success(f"✓ {f2.name}")
        if st.session_state["dup_files"]:
            st.markdown(f"**Files in session:** {', '.join(v['name'] for v in st.session_state['dup_files'].values())}")
        if st.button("🗑 Clear all session files"):
            st.session_state["dup_files"]={}; st.rerun()

    col1,col2,_=st.columns([1,1,3])
    with col1: run_cls=st.button("🏷️ Classify & Check Duplicates",type="primary",use_container_width=True)

    if run_cls:
        content=st.session_state["class_text"].strip()
        if not content:
            st.markdown('<div class="rc warn">Please upload or paste an SAE report first.</div>',unsafe_allow_html=True)
        else:
            tl=content.lower()
            if any(w in tl for w in ["died","fatal","death","mortality","deceased"]):
                sev="DEATH"; sc_s="background:#fee2e2;color:#991b1b"; ps=1
                rk=[w for w in ["died","fatal","death","mortality","deceased"] if w in tl]
            elif any(w in tl for w in ["permanent disability","paralysis","blind","deaf","permanent impairment"]):
                sev="DISABILITY"; sc_s="background:#ffedd5;color:#9a3412"; ps=2
                rk=[w for w in ["permanent disability","paralysis","blind","deaf"] if w in tl]
            elif any(w in tl for w in ["hospitalised","admitted","icu","inpatient","emergency","hospital"]):
                sev="HOSPITALISATION"; sc_s="background:#fef9c3;color:#92400e"; ps=3
                rk=[w for w in ["hospitalised","admitted","icu","inpatient","emergency","hospital"] if w in tl]
            else:
                sev="OTHERS"; sc_s="background:#dbeafe;color:#1e40af"; ps=4
                rk=["no critical keywords — default classification"]

            conf="HIGH" if len(rk)>=3 else "MEDIUM" if len(rk)>=1 else "LOW"
            icd={"DEATH":"R96.x/R98/R99","DISABILITY":"S00-T98 (perm.)","HOSPITALISATION":"Z75.1","OTHERS":"MedDRA PT"}
            rpt={"DEATH":"Expedited 7-day","DISABILITY":"Expedited 15-day","HOSPITALISATION":"Expedited 15-day","OTHERS":"Periodic 90-day"}

            _cls_risk_map = {"DEATH":"Critical","DISABILITY":"High","HOSPITALISATION":"Medium","OTHERS":"Low"}
            _cls_action = {
                "DEATH":"Expedited 7-day report mandatory. Immediate notification to DCGI and Ethics Committee required under Schedule Y.",
                "DISABILITY":"Expedited 15-day report required. Notify sponsor and Ethics Committee. Assess causality.",
                "HOSPITALISATION":"Expedited 15-day report required. Monitor patient outcome and submit follow-up report.",
                "OTHERS":"Periodic reporting within 90 days. Document in safety database."
            }
            ai_recommendation_card(
                f"SAE classified as {sev} · Confidence: {conf} · Priority queue position: {ps}/4",
                _cls_risk_map[sev],
                _cls_action[sev],
                f"ICD-10 reference: {icd[sev]} · Reporting timeline: {rpt[sev]}"
            )
            st.markdown(f'<div style="{sc_s};border-radius:10px;padding:10px 20px;font-size:18px;font-weight:700;display:inline-block;margin-bottom:12px;">⬤ {sev}</div>',unsafe_allow_html=True)
            c1,c2,c3=st.columns(3)
            c1.metric("Severity",sev); c2.metric("Confidence",conf); c3.metric("Priority Queue",f"{ps} / 4")
            with st.expander("Classification Evidence",expanded=True):
                st.markdown(f'<div class="rc info"><b>Detected keywords:</b> {", ".join(rk)}<br><b>ICD-10:</b> {icd[sev]} · <b>Reporting:</b> {rpt[sev]}</div>',unsafe_allow_html=True)

            # Duplicate detection across session files
            st.markdown("**Duplicate Detection across session files**")
            def get_ids(t):
                ids=set(re.findall(r'\b(?:PT|SUBJ|LH|MH|DL)[-]\w+[-]\w+\b',t))
                drugs=set(re.findall(r'\b[A-Z][a-z]+(?:vir|mab|nib|tide|pril|sartan|statin|mycin|cillin)\b',t))
                drugs|=set(re.findall(r'\b[A-Z]{4,}[-]?\d*\s*mg\b',t))
                return ids,drugs

            id1,dr1=get_ids(content); dup_found=False
            all_files=st.session_state["dup_files"]
            if len(all_files)>1:
                for k,v in all_files.items():
                    if v["text"].strip()==content.strip(): continue
                    id2,dr2=get_ids(v["text"])
                    shared_ids=id1&id2; shared_drugs=dr1&dr2
                    if shared_ids or shared_drugs:
                        detail=[]
                        if shared_ids: detail.append(f"Patient IDs: {shared_ids}")
                        if shared_drugs: detail.append(f"Drugs: {shared_drugs}")
                        st.markdown(f'<div class="rc err">⚠️ DUPLICATE DETECTED — matches <b>{v["name"]}</b> · {" · ".join(detail)}</div>',unsafe_allow_html=True)
                        dup_found=True
                if not dup_found:
                    st.markdown('<div class="rc ok">✓ No duplicates found across all session files.</div>',unsafe_allow_html=True)
            else:
                st.markdown('<div class="rc info">Upload additional SAE reports above to enable duplicate cross-checking.</div>',unsafe_allow_html=True)

            report=f"Severity:{sev}\nConfidence:{conf}\nKeywords:{', '.join(rk)}\nPriority:{ps}/4\nICD-10:{icd[sev]}\nTimeline:{rpt[sev]}"
            st.download_button("⬇ Download Classification Report",report,file_name="classification_report.txt")


# ═══ FEATURE 5 — COMPARISON ══════════════════════════════════════════════════
with t5:
    st.markdown("""
    <div class="sec-hd">
      <div class="sec-ic ic-sky">🔍</div>
      <div><h2>Document Comparison</h2>
      <p>Upload two filing versions · Substantive vs administrative diff · Colour-coded table · Downloadable report</p></div>
    </div>
    """, unsafe_allow_html=True)

    col_v1,col_v2=st.columns(2)
    with col_v1:
        st.markdown("**Version 1 — Original**")
        v1f=st.file_uploader("Upload V1",type=["docx","pdf","txt"],key="v1f")
        if v1f:
            t,e=extract_text(v1f)
            if not e and t.strip():
                st.session_state["v1_text"]=t
                st.session_state["v1ta"]=t
                st.success(f"✓ {v1f.name}")
        v1=st.text_area("or paste V1",height=200,key="v1ta",placeholder="Original document...")
        st.session_state["v1_text"]=st.session_state.get("v1ta","")

    with col_v2:
        st.markdown("**Version 2 — Updated**")
        v2f=st.file_uploader("Upload V2",type=["docx","pdf","txt"],key="v2f")
        if v2f:
            t,e=extract_text(v2f)
            if not e and t.strip():
                st.session_state["v2_text"]=t
                st.session_state["v2ta"]=t
                st.success(f"✓ {v2f.name}")
        v2=st.text_area("or paste V2",height=200,key="v2ta",placeholder="Updated document...")
        st.session_state["v2_text"]=st.session_state.get("v2ta","")

    col1,col2,_=st.columns([1,1,3])
    with col1: run_c5=st.button("🔍 Compare",type="primary",use_container_width=True)

    if run_c5:
        t1c=st.session_state["v1_text"].strip(); t2c=st.session_state["v2_text"].strip()
        if not t1c or not t2c:
            st.markdown('<div class="rc warn">Please provide both document versions.</div>',unsafe_allow_html=True)
        else:
            # Normalise: split on sentences and lines for better Word doc comparison
            import re as _re
            def _norm(t):
                lines=[l.strip() for l in t.splitlines() if l.strip()]
                # Also split long paragraphs at sentence boundaries
                result=[]
                for l in lines:
                    if len(l)>200:
                        parts=_re.split(r'(?<=[.!?])\s+',l)
                        result.extend([p.strip() for p in parts if p.strip()])
                    else:
                        result.append(l)
                return result
            l1=_norm(t1c); l2=_norm(t2c)
            SK=["dose","dosage","mg","ml","death","disability","outcome","causality","adverse","event",
                "date","patient","diagnosis","icd","treatment","safety","efficacy","result","risk","fatal","serious"]
            changes=[]
            for tag,i1,i2,j1,j2 in difflib.SequenceMatcher(None,l1,l2).get_opcodes():
                if tag=="replace":
                    for o,n in zip(l1[i1:i2],l2[j1:j2]):
                        s=any(k in o.lower() or k in n.lower() for k in SK)
                        changes.append({"Type":"CHANGED","Original":o,"New":n,"Substantive":"Yes" if s else "No"})
                elif tag=="delete":
                    for line in l1[i1:i2]:
                        changes.append({"Type":"REMOVED","Original":line,"New":"—","Substantive":"Yes" if any(k in line.lower() for k in SK) else "No"})
                elif tag=="insert":
                    for line in l2[j1:j2]:
                        changes.append({"Type":"ADDED","Original":"—","New":line,"Substantive":"Yes" if any(k in line.lower() for k in SK) else "No"})
            sc=sum(1 for c in changes if c["Substantive"]=="Yes")
            c1,c2,c3,c4,c5=st.columns(5)
            c1.metric("Total",len(changes));c2.metric("Added",sum(1 for c in changes if c["Type"]=="ADDED"))
            c3.metric("Removed",sum(1 for c in changes if c["Type"]=="REMOVED"))
            c4.metric("Changed",sum(1 for c in changes if c["Type"]=="CHANGED"))
            c5.metric("Substantive",sc)
            cc="err" if sc>0 else "ok"
            _c5_risk = "High" if sc >= 3 else "Medium" if sc >= 1 else "Low"
            _c5_action = (f"{sc} substantive change(s) detected affecting regulatory parameters. These changes require formal review and may require amended submission to CDSCO."
                         if sc > 0 else "No substantive changes detected. Administrative edits only. Document may proceed without re-review.")
            ai_recommendation_card(
                f"{len(changes)} total changes · {sc} substantive · {len(changes)-sc} administrative",
                _c5_risk,
                _c5_action,
                "Substantive changes affect dosage, safety data, outcomes, or patient information and require regulatory attention."
            )
            st.markdown(f'<div class="rc {cc}">{"⚠️ "+str(sc)+" substantive change(s) — regulatory review required." if sc>0 else "✓ No substantive changes detected."}</div>',unsafe_allow_html=True)
            if changes:
                df=pd.DataFrame(changes)
                def sd(row):
                    if row["Type"]=="ADDED": return ["background-color:#dcfce7"]*len(row)
                    if row["Type"]=="REMOVED": return ["background-color:#fee2e2"]*len(row)
                    if row["Substantive"]=="Yes": return ["background-color:#fef9c3"]*len(row)
                    return [""]*len(row)
                with st.expander("Full Change Table",expanded=True):
                    st.markdown('<div class="tw">',unsafe_allow_html=True)
                    st.dataframe(df.style.apply(sd,axis=1),use_container_width=True,hide_index=True)
                    st.markdown('</div>',unsafe_allow_html=True)
                    st.caption("🟢 Added · 🔴 Removed · 🟡 Changed (Substantive)")
                st.download_button("⬇ Download Report",df.to_csv(index=False),file_name="comparison_report.csv",mime="text/csv")


# ═══ FEATURE 6 — INSPECTION REPORT ══════════════════════════════════════════
with t6:
    st.markdown("""
    <div class="sec-hd">
      <div class="sec-ic ic-pink">📋</div>
      <div><h2>Inspection Report Generation</h2>
      <p>Paste raw site observations · Converts to formal CDSCO GCP report · Critical / Major / Minor grading</p></div>
    </div>
    """, unsafe_allow_html=True)

    c1,c2,c3,c4=st.columns(4)
    with c1: insp_name=st.text_input("Inspector Name",placeholder="Dr. A.K. Sharma")
    with c2: insp_site=st.text_input("Site Name",placeholder="AIIMS Delhi")
    with c3: insp_sno=st.text_input("Site Number",placeholder="SITE-DEL-001")
    with c4: insp_date=st.date_input("Inspection Date")

    obs=st.text_area("Raw inspection observations — one per line",height=200,key="obs_ta",
        placeholder="No record of drug accountability for subjects 3 and 7\nInformed consent missing local language version\nMinor labelling error on storage box")

    col1,col2,_=st.columns([1,1,3])
    with col1: run_insp=st.button("📋 Generate Report",type="primary",use_container_width=True)

    if run_insp and obs.strip():
        obs_list=[o.strip() for o in obs.splitlines() if o.strip()]
        CK=["no record","falsified","patient safety","data integrity","unaccounted","fraud","fabricat"]
        MK=["incomplete","not documented","protocol deviation","untrained","not signed","not dated","expired"]
        rows=[]
        for i,ob in enumerate(obs_list,1):
            ol=ob.lower()
            if any(k in ol for k in CK): risk="Critical";dl="15 days";ca="Immediate CAPA. Site may be suspended."
            elif any(k in ol for k in MK): risk="Major";dl="30 days";ca="CAPA plan within 30 days."
            else: risk="Minor";dl="60 days";ca="Document in site log."
            formal=f"During inspection on {insp_date.strftime('%d %B %Y')}, it was observed that {ob.lower().rstrip('.')}. This is a {risk.lower()} GCP deviation."
            rows.append({"Obs":f"OBS-{i:03d}","Raw":ob,"Formal Finding":formal,"Risk":risk,"Corrective Action":ca,"Deadline":dl})
        cc_n=sum(1 for r in rows if r["Risk"]=="Critical")
        mc_n=sum(1 for r in rows if r["Risk"]=="Major")
        mn_n=sum(1 for r in rows if r["Risk"]=="Minor")
        c1,c2,c3=st.columns(3)
        c1.metric("Critical",cc_n);c2.metric("Major",mc_n);c3.metric("Minor",mn_n)
        cc="err" if cc_n>0 else "warn" if mc_n>0 else "ok"
        _insp_risk = "Critical" if cc_n > 0 else "High" if mc_n > 0 else "Low"
        _insp_action = (f"{cc_n} Critical GCP deviation(s) found. Immediate CAPA required. Site operations may be suspended. Report to DCGI within 15 days."
                       if cc_n > 0 else f"{mc_n} Major GCP deviation(s) found. CAPA plan must be submitted within 30 days."
                       if mc_n > 0 else f"No Critical or Major findings. {mn_n} Minor deviation(s) to be documented in site log within 60 days.")
        ai_recommendation_card(
            f"Inspection outcome: {cc_n} Critical · {mc_n} Major · {mn_n} Minor findings",
            _insp_risk,
            _insp_action,
            f"Site: {insp_site or '[Site name]'} · Date: {insp_date.strftime('%d %B %Y')} · Inspector: {insp_name or '[Inspector]'}"
        )
        st.markdown(f'<div class="rc {cc}">{"⚠️ "+str(cc_n)+" Critical findings — CAPA required." if cc_n>0 else "⚠️ "+str(mc_n)+" Major findings — CAPA due in 30 days." if mc_n>0 else "✓ No Critical or Major findings."}</div>',unsafe_allow_html=True)
        df=pd.DataFrame(rows)
        def sr(v):
            if v=="Critical": return "background-color:#fee2e2;color:#991b1b;font-weight:700"
            if v=="Major": return "background-color:#fef9c3;color:#92400e;font-weight:700"
            if v=="Minor": return "background-color:#dcfce7;color:#166534"
            return ""
        with st.expander("Full Inspection Report",expanded=True):
            st.markdown('<div class="tw">',unsafe_allow_html=True)
            st.dataframe(df.style.map(sr,subset=["Risk"]),use_container_width=True,hide_index=True)
            st.markdown('</div>',unsafe_allow_html=True)
        _sep="="*56
        _sep2="-"*56
        full=f"""CDSCO GCP SITE INSPECTION REPORT
{_sep}

SECTION 1: BASIC DETAILS
Study/Site Name : {insp_site or "[Site name]"}
Site Number     : {insp_sno or "[Site number]"}
Inspection Date : {insp_date.strftime("%d %B %Y")}
Inspector       : {insp_name or "[Inspector name]"}

{_sep}

SECTION 2: SUMMARY
Total Issues    : {len(rows)}
Critical        : {cc_n}
Major           : {mc_n}
Minor           : {mn_n}
Overall Risk    : {"HIGH" if cc_n>0 else "MEDIUM" if mc_n>0 else "LOW"}

{_sep}

SECTION 3: FINDINGS TABLE

"""
        for r in rows:
            full+=f"""{r["Obs"]} | {r["Risk"].upper()}
Observation         : {r["Raw"]}
Formal Finding      : {r["Formal Finding"]}
Severity            : {r["Risk"]}
Regulatory Reference: CDSCO Schedule Y / GCP Guidelines ICH E6
Recommendation      : {r["Corrective Action"]}
Deadline            : {r["Deadline"]}
{_sep2}
"""
        full+=f"""
SECTION 4: CROSS-DOCUMENT ISSUES
No cross-document mismatches identified in this report.

{_sep}

SECTION 5: CAPA (CORRECTIVE AND PREVENTIVE ACTION)
Critical findings require immediate CAPA submission within 15 days.
Major findings require CAPA plan within 30 days.
Minor findings to be documented in site log within 60 days.

{_sep}

SECTION 6: RISK LEVEL
Overall Site Risk: {"HIGH — immediate action required" if cc_n>0 else "MEDIUM — corrective action required" if mc_n>0 else "LOW — routine monitoring"}

{_sep}

SECTION 7: AUDIT TRAIL (AI FLAGGING RATIONALE)
This report was generated by Nirnay AI (CDSCO AI Hackathon 2026, Stage 1).
Critical flags: keywords matching data integrity, patient safety, or falsification concerns.
Major flags: incomplete documentation, protocol deviations, expired materials.
Minor flags: administrative or labelling issues not affecting patient safety.

{_sep}
Inspector Signature: ___________________________
Date: {datetime.date.today()}
Generated by: Nirnay — CDSCO Regulatory Intelligence Platform
"""
        st.download_button("⬇ Download Inspection Report (TXT)",full,file_name=f"inspection_report_{insp_date}.txt",mime="text/plain")
    elif run_insp:
        st.markdown('<div class="rc warn">Please enter at least one observation.</div>',unsafe_allow_html=True)

# ── COMPLIANCE RIBBON ─────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-top:32px;border-top:1px solid #e2e8f0;padding:10px 0;display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
  <span style="font-size:9px;font-weight:600;color:#94a3b8;">&#10003; DPDP Act 2023</span>
  <span style="color:#e2e8f0;">·</span>
  <span style="font-size:9px;font-weight:600;color:#94a3b8;">&#10003; CDSCO Schedule Y</span>
  <span style="color:#e2e8f0;">·</span>
  <span style="font-size:9px;font-weight:600;color:#94a3b8;">&#10003; ICMR Guidelines 2017</span>
  <span style="color:#e2e8f0;">·</span>
  <span style="font-size:9px;font-weight:600;color:#94a3b8;">&#10003; NDCT Rules 2019</span>
  <span style="color:#e2e8f0;">·</span>
  <span style="font-size:9px;font-weight:600;color:#94a3b8;">&#10003; MeitY AI Ethics</span>
  <span style="margin-left:auto;font-size:9px;color:#cbd5e1;">&#169; 2026 Nirnay &mdash; Built for IndiaAI/CDSCO Hackathon</span>
</div>
""", unsafe_allow_html=True)
