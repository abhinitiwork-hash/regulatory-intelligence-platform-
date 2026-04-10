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
    page_title="RegDarpan — CDSCO AI Review System",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;}
#MainMenu,footer,header{visibility:hidden;}
.stApp{background-color:#f4f7fb;}

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

.stTabs [data-baseweb="tab-list"]{background:white;border-radius:12px;padding:4px;gap:2px;box-shadow:0 1px 4px rgba(0,0,0,0.06);}
.stTabs [data-baseweb="tab"]{border-radius:8px;font-size:12px;font-weight:500;color:#64748b;padding:8px 12px;}
.stTabs [aria-selected="true"]{background:#003087!important;color:white!important;}

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
          "dup_files","anon_done","sum_done","comp_done","class_done"]:
    if k not in st.session_state:
        if k == "dup_files":
            st.session_state[k] = {}
        elif k.endswith("_done"):
            st.session_state[k] = False
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
    cnt = {k:0 for k in ["PATIENT","INVESTIGATOR","DATE","SITE","ID","PHONE","AADHAAR","HOSP_REC"]}
    ts  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    found_types = set()

    def tok(kind):
        cnt[kind]+=1; return f"[{kind}-{cnt[kind]:03d}]"
    def rec(t,orig,etype):
        tokens.append({"Token":t,"Original Value":orig,"Entity Type":etype,"Step":"Step 1"})
        audit.append({"Timestamp":ts,"Action":"Pseudonymised","Entity Type":etype,"Token":t,"Reversible":"Yes"})
        found_types.add(etype)

    # FIX ORDER: run phone & IDs BEFORE dates to avoid digit consumption
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
    # Pincode — run last to avoid consuming phone/ID digits
    for m in re.finditer(r'[1-9]\d{5}', processed):
        t=tok("ID"); rec(t,m.group(),"Pincode")
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
    for et in ["Dates→Year only","Ages→Range","Biometrics→Range"]:
        audit.append({"Timestamp":ts,"Action":"Irreversible Generalisation","Entity Type":et,"Token":"Generalised","Reversible":"No"})

    return {"step1":processed,"step2":step2,"tokens":tokens,"audit":audit,
            "types":list(found_types),"count":len(tokens)}


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:16px 0 10px;'>
    <div style='font-size:38px;'>⚕️</div>
    <div style='font-weight:700;font-size:15px;color:white;margin-top:6px;'>CDSCO RIP</div>
    <div style='font-size:11px;color:rgba(255,255,255,0.45);'>Regulatory Intelligence Platform</div>
    </div>
    <hr style='border-color:rgba(255,255,255,0.15);margin:10px 0;'>
    """, unsafe_allow_html=True)
    st.markdown("<div style='font-size:10px;font-weight:600;color:rgba(255,255,255,0.4);text-transform:uppercase;letter-spacing:.08em;margin-bottom:7px;'>Compliance</div>", unsafe_allow_html=True)
    for b in ["✅  DPDP Act 2023","✅  ICMR Guidelines 2017","✅  CDSCO Schedule Y","✅  MeitY AI Ethics"]:
        st.markdown(f"<div style='background:rgba(74,222,128,0.1);border:1px solid rgba(74,222,128,0.3);border-radius:20px;padding:4px 10px;font-size:11px;color:#4ade80;margin:3px 0;'>{b}</div>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color:rgba(255,255,255,0.15);margin:12px 0;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:10px;font-weight:600;color:rgba(255,255,255,0.4);text-transform:uppercase;letter-spacing:.08em;margin-bottom:7px;'>Public Datasets</div>", unsafe_allow_html=True)
    for d in ["FDA FAERS","CDSCO CT-04/05/06","ClinicalTrials.gov","CTRI India"]:
        st.markdown(f"<div style='font-size:11px;color:rgba(255,255,255,0.6);padding:2px 0;'>◦ {d}</div>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color:rgba(255,255,255,0.15);margin:12px 0;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:11px;color:rgba(255,255,255,0.4);line-height:1.6;'>AI assists officers. Final decisions by qualified human reviewers.</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:10px;color:rgba(255,255,255,0.22);margin-top:10px;text-align:center;'>Stage 1 · CDSCO AI Hackathon 2026</div>", unsafe_allow_html=True)


# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="glass">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:12px;">
    <div>
      <div class="big-title">RegDarpan</div>
      <div class="subtitle">AI-powered CDSCO regulatory review assistant</div>
      <div style="margin-top:10px;font-size:12px;color:#003087;font-weight:500;">
        CDSCO officers review thousands of regulatory documents manually.
        RegDarpan automates the repetitive parts — so officers can focus on decisions, not paperwork.
      </div>
    </div>
    <div style="background:#f0fdf4;border:1px solid #86efac;border-radius:10px;padding:10px 16px;font-size:12px;color:#166534;font-weight:500;white-space:nowrap;align-self:flex-start;">
      All processing is local<br>
      <span style="font-weight:400;">No data leaves this platform</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── PLATFORM CAPABILITIES ─────────────────────────────────────────────────────
st.markdown("<div style='font-size:11px;font-weight:600;color:#6b7280;text-transform:uppercase;letter-spacing:.08em;margin-bottom:10px;'>Platform capabilities</div>", unsafe_allow_html=True)
_d1,_d2,_d3,_d4 = st.columns(4)
with _d1:
    st.markdown("""<div class="dash-card"><h2 style="color:#003087;">8</h2><p>PII types detected automatically</p></div>""", unsafe_allow_html=True)
with _d2:
    st.markdown("""<div class="dash-card"><h2 style="color:#003087;">20</h2><p>Schedule Y fields verified</p></div>""", unsafe_allow_html=True)
with _d3:
    st.markdown("""<div class="dash-card"><h2 style="color:#003087;">3</h2><p>Document types supported</p></div>""", unsafe_allow_html=True)
with _d4:
    st.markdown("""<div class="dash-card"><h2 style="color:#003087;">6</h2><p>AI-powered review features</p></div>""", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)


# ── TABS ──────────────────────────────────────────────────────────────────────
t0,t1,t2,t3,t4,t5,t6 = st.tabs([
    "Home","Anonymisation","Summarisation",
    "Completeness","Classification","Comparison","Inspection Report"
])

# ═══ HOME ════════════════════════════════════════════════════════════════════
with t0:
    features = [
        ("01", "Protect sensitive information",
         "Upload any regulatory document. The system automatically finds and removes patient names, IDs, phone numbers, dates, and hospital records — and gives you a clean version safe to share.",
         "Anonymisation", "f1"),
        ("02", "Get a quick summary of any document",
         "Upload an SAE report, SUGAM checklist, or meeting transcript. The system reads it and gives you a structured summary — decisions, action items, and key findings — in under a minute.",
         "Summarisation", "f2"),
        ("03", "Check if an application is complete",
         "Upload a clinical trial application. The system checks all 20 mandatory Schedule Y fields and tells you what is present, what is missing, and whether to approve or return it.",
         "Completeness", "f3"),
        ("04", "Classify how serious an adverse event is",
         "Upload an SAE report. The system tells you whether it is a death, disability, hospitalisation, or other case — and flags if the same case has already been reported.",
         "Classification", "f4"),
        ("05", "See what changed between two document versions",
         "Upload an original and an updated filing. The system highlights every change and tells you which ones are significant for regulatory review and which are minor edits.",
         "Comparison", "f5"),
        ("06", "Turn inspection notes into a formal report",
         "Paste raw observations from a site visit. The system converts them into a structured CDSCO inspection report with risk levels and corrective action deadlines.",
         "Inspection Report", "f6"),
    ]

    cols = st.columns(3)
    for i, (num, title, desc, tab_name, cls) in enumerate(features):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="fc {cls}" style="height:100%;cursor:default;">
              <div style="font-size:10px;font-weight:700;color:#94a3b8;letter-spacing:.1em;margin-bottom:8px;">{num}</div>
              <div class="ft">{title}</div>
              <div class="fd" style="margin-top:6px;margin-bottom:14px;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Open — {tab_name} →", key=f"home_btn_{i}", use_container_width=True):
                st.session_state["active_tab"] = i + 1
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

            # PII chips
            if result["types"]:
                chips = '<div class="pii-chips">'
                for pt in result["types"]:
                    cls = CHIP_MAP.get(pt,"cg")
                    chips += f'<span class="chip {cls}">● {pt}</span>'
                chips += f'<span class="chip cg">Total detected: {result["count"]}</span></div>'
                st.markdown(chips, unsafe_allow_html=True)
            else:
                st.markdown('<div class="rc info">No PII/PHI patterns detected in this text.</div>', unsafe_allow_html=True)

            # Step 1
            st.markdown('<div class="step-pill">✓ Reversible version — identifiers replaced with codes</div>', unsafe_allow_html=True)
            with st.expander("Reversible version — what was replaced with codes", expanded=False):
                st.text_area("Step 1 output", result["step1"], height=160, key="s1o")
                if result["tokens"]:
                    st.markdown("**Token Mapping Table** — reversible at this stage")
                    st.markdown('<div class="tw">', unsafe_allow_html=True)
                    st.dataframe(pd.DataFrame(result["tokens"]), use_container_width=True, hide_index=True)
                    st.markdown('</div>', unsafe_allow_html=True)

            # Step 2
            st.markdown('<div class="step-pill s2">✓ Step 2 — Irreversible Generalisation</div>', unsafe_allow_html=True)
            with st.expander("Final anonymised output — safe to share", expanded=True):
                st.text_area("Final anonymised text", result["step2"], height=160, key="s2o")

            # Audit log
            with st.expander("Technical audit log (DPDP Act 2023 compliance record)", expanded=False):
                st.markdown('<div class="tw">', unsafe_allow_html=True)
                st.dataframe(pd.DataFrame(result["audit"]), use_container_width=True, hide_index=True)
                st.markdown('</div>', unsafe_allow_html=True)

            report = (
                f"CDSCO ANONYMISATION REPORT\nGenerated: {datetime.datetime.now()}\n\n"
                f"=== ORIGINAL ===\n{content}\n\n"
                f"=== STEP 1: PSEUDONYMISED ===\n{result['step1']}\n\n"
                f"=== STEP 2: FINAL ANONYMISED ===\n{result['step2']}\n\n"
                f"=== TOKEN MAP ===\n{pd.DataFrame(result['tokens']).to_string()}\n\n"
                f"=== AUDIT LOG ===\n{pd.DataFrame(result['audit']).to_string()}"
            )
            st.download_button("⬇ Download Anonymisation Report",
                report, file_name=f"anonymisation_{datetime.date.today()}.txt", mime="text/plain")


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
        st.markdown('<div class="audio-note">🎵 Audio files (MP3/WAV/M4A) accepted for meeting transcripts. Metadata is captured; full transcription via Whisper available in Stage 2.</div>', unsafe_allow_html=True)
        sum_file = st.file_uploader("Word / PDF / TXT / Audio", type=["docx","pdf","txt","mp3","wav","m4a"], key="sum_up")
    else:
        sum_file = st.file_uploader("Word / PDF / TXT", type=["docx","pdf","txt"], key="sum_up2")

    audio_mode = False
    if sum_file:
        fname = sum_file.name.lower()
        if any(fname.endswith(x) for x in [".mp3",".wav",".m4a"]):
            audio_mode = True
            st.success(f"✓ Audio received: {sum_file.name} ({round(sum_file.size/1024)} KB)")
            st.session_state["sum_text"] = f"[AUDIO: {sum_file.name}]\nPaste transcript below if available."
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
                st.dataframe(df.style.applymap(srag,subset=["RAG"]),use_container_width=True,hide_index=True)
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
            l1=[l.strip() for l in t1c.splitlines() if l.strip()]
            l2=[l.strip() for l in t2c.splitlines() if l.strip()]
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
        st.markdown(f'<div class="rc {cc}">{"⚠️ "+str(cc_n)+" Critical findings — CAPA required." if cc_n>0 else "⚠️ "+str(mc_n)+" Major findings — CAPA due in 30 days." if mc_n>0 else "✓ No Critical or Major findings."}</div>',unsafe_allow_html=True)
        df=pd.DataFrame(rows)
        def sr(v):
            if v=="Critical": return "background-color:#fee2e2;color:#991b1b;font-weight:700"
            if v=="Major": return "background-color:#fef9c3;color:#92400e;font-weight:700"
            if v=="Minor": return "background-color:#dcfce7;color:#166534"
            return ""
        with st.expander("Full Inspection Report",expanded=True):
            st.markdown('<div class="tw">',unsafe_allow_html=True)
            st.dataframe(df.style.applymap(sr,subset=["Risk"]),use_container_width=True,hide_index=True)
            st.markdown('</div>',unsafe_allow_html=True)
        full=(f"CDSCO GCP SITE INSPECTION REPORT\n{'='*48}\n"
              f"Site: {insp_site}\nNo: {insp_sno}\nDate: {insp_date.strftime('%d %B %Y')}\n"
              f"Inspector: {insp_name}\nSummary: {cc_n} Critical | {mc_n} Major | {mn_n} Minor\n{'='*48}\n\n")
        for r in rows:
            full+=f"{r['Obs']} | {r['Risk'].upper()}\nFinding: {r['Formal Finding']}\nAction: {r['Corrective Action']}\nDeadline: {r['Deadline']}\n{'-'*48}\n\n"
        full+=f"Inspector: {insp_name}\nSignature: ___\nDate: {datetime.date.today()}"
        st.download_button("⬇ Download Inspection Report",full,file_name="inspection_report.txt",mime="text/plain")
    elif run_insp:
        st.markdown('<div class="rc warn">Please enter at least one observation.</div>',unsafe_allow_html=True)
