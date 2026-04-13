import streamlit as st
import pandas as pd
import datetime
import re
import difflib
import io
import json

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
    page_title="Nirnay — CDSCO AI Review",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=Playfair+Display:wght@600;700&display=swap');

html,body,[class*="css"]{font-family:'DM Sans',sans-serif !important;}
#MainMenu,footer,header{visibility:hidden;}
[data-testid="stToolbar"]{display:none;}
.stDeployButton{display:none;}
.stApp{background:#F2F0ED !important;}
.main .block-container{padding:0 !important; max-width:100% !important;}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"]{background:#0D1B2A;border-radius:10px;padding:4px;gap:2px;}
.stTabs [data-baseweb="tab"]{border-radius:7px;font-size:12px;font-weight:500;color:rgba(255,255,255,0.5);padding:8px 16px;font-family:'DM Sans',sans-serif !important;}
.stTabs [aria-selected="true"]{background:#1A6B52 !important;color:#fff !important;}
.stTabs [data-baseweb="tab"]:hover{color:#fff !important;}
.stTabs [data-baseweb="tab-border"]{display:none;}
.stTabs [data-baseweb="tab-panel"]{background:#F2F0ED;border-radius:0 0 12px 12px;padding:20px !important;}

/* ── Buttons ── */
.stButton>button{background:#0D1B2A !important;color:#5EC4A8 !important;border:none !important;border-radius:8px !important;
  font-family:'DM Sans',sans-serif !important;font-size:13px !important;font-weight:500 !important;
  padding:10px 22px !important;transition:background 0.15s !important;}
.stButton>button:hover{background:#1a2e42 !important;}
.stButton>button[kind="primary"]{background:#0D1B2A !important;color:#5EC4A8 !important;}
.stDownloadButton>button{background:#1A6B52 !important;color:#fff !important;border:none !important;
  border-radius:8px !important;font-family:'DM Sans',sans-serif !important;font-size:13px !important;font-weight:500 !important;}
.stDownloadButton>button:hover{background:#1D8060 !important;}

/* ── Inputs ── */
.stTextArea textarea,.stTextInput input{background:#fff !important;border:1px solid #E2DED8 !important;
  border-radius:8px !important;font-size:13px !important;font-family:'DM Sans',sans-serif !important;color:#0D1B2A !important;}
.stTextArea textarea:focus,.stTextInput input:focus{border-color:#1A6B52 !important;box-shadow:0 0 0 2px rgba(26,107,82,0.12) !important;}
.stSelectbox>div>div{background:#fff !important;border:1px solid #E2DED8 !important;border-radius:8px !important;font-size:13px !important;}
[data-testid="stFileUploader"]{background:#fff;border:1.5px dashed #C8C4BE;border-radius:10px;padding:6px;}
[data-testid="stFileUploader"]:hover{border-color:#1A6B52;}

/* ── Metrics ── */
[data-testid="stMetricValue"]{font-size:22px !important;font-weight:700 !important;color:#0D1B2A !important;}
[data-testid="stMetricLabel"]{font-size:12px !important;color:#667788 !important;}

/* ── Expander ── */
.streamlit-expanderHeader{font-family:'DM Sans',sans-serif !important;font-size:13px !important;
  font-weight:500 !important;background:#fff !important;border:1px solid #E2DED8 !important;border-radius:8px !important;}

/* ── Dataframe ── */
.stDataFrame{border:1px solid #E2DED8 !important;border-radius:10px !important;overflow:hidden !important;}

/* ── Custom components ── */
.nrn-topbar{background:#0D1B2A;padding:0 32px;display:flex;align-items:center;height:56px;gap:0;margin-bottom:0;}
.nrn-logo{font-family:'Playfair Display',serif;font-size:20px;color:#fff;letter-spacing:-0.3px;margin-right:10px;}
.nrn-badge{font-size:9px;font-weight:600;color:#5EC4A8;border:1px solid #5EC4A840;padding:2px 8px;
  border-radius:4px;letter-spacing:1px;text-transform:uppercase;margin-right:20px;}
.nrn-tagline{font-size:12px;color:#556677;border-left:1px solid #ffffff18;padding-left:16px;flex:1;}
.nrn-tagline em{color:#8AAABB;font-style:normal;}

.ncard{background:#fff;border:1px solid #E2DED8;border-radius:12px;padding:20px 22px;margin-bottom:14px;}
.ncard-title{font-size:11px;font-weight:600;color:#0D1B2A;margin-bottom:4px;text-transform:uppercase;letter-spacing:0.5px;}
.ncard-sub{font-size:12px;color:#99AABB;margin-bottom:12px;}

.sec-hd{display:flex;align-items:flex-start;gap:14px;margin-bottom:20px;padding-bottom:16px;border-bottom:1px solid #E2DED8;}
.sec-num{font-family:'Playfair Display',serif;font-size:32px;font-weight:700;line-height:1;flex-shrink:0;}
.sec-hd h2{font-size:17px;font-weight:600;color:#0D1B2A;margin:0 0 3px;}
.sec-hd p{font-size:12px;color:#667788;margin:0;line-height:1.6;}

.rc{background:#fff;border-radius:8px;padding:12px 16px;margin:8px 0;border-left:4px solid #0D1B2A;font-size:13px;}
.rc.ok{border-left-color:#1A6B52;background:#EBF6F2;color:#1A6B52;}
.rc.warn{border-left-color:#854F0B;background:#FDF3EC;color:#854F0B;}
.rc.err{border-left-color:#8B2020;background:#FCEAEA;color:#8B2020;}
.rc.info{border-left-color:#185FA5;background:#EAF3FB;color:#185FA5;}

.metric-card{background:#fff;border:1px solid #E2DED8;border-radius:10px;padding:16px 18px;text-align:left;}
.metric-card .mv{font-size:22px;font-weight:700;color:#0D1B2A;line-height:1;margin-bottom:4px;}
.metric-card .ml{font-size:11px;color:#99AABB;text-transform:uppercase;letter-spacing:0.6px;}

.ai-card{border-radius:10px;padding:16px 20px;margin:12px 0;border:1px solid;border-left:4px solid #0D1B2A;}
.ai-card.c-low{background:#EBF6F2;border-color:#B8E8DA;}
.ai-card.c-med{background:#FDF3EC;border-color:#F5C4A0;}
.ai-card.c-high{background:#FFF3E0;border-color:#FFC880;}
.ai-card.c-crit{background:#FCEAEA;border-color:#F5B0B0;}
.ai-eyebrow{font-size:10px;font-weight:700;color:#0D1B2A;letter-spacing:.1em;text-transform:uppercase;margin-bottom:5px;}
.ai-finding{font-size:15px;font-weight:700;color:#0D1B2A;margin-bottom:4px;}
.ai-action{font-size:13px;color:#445566;line-height:1.5;}
.ai-detail{font-size:11px;color:#778899;margin-top:4px;}
.ai-badge{font-size:10px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;padding:5px 14px;border-radius:6px;}

.diff-critical{background:#FCEAEA;border-left:3px solid #E24B4A;padding:8px 12px;border-radius:0 6px 6px 0;margin-bottom:6px;font-size:13px;}
.diff-moderate{background:#FDF3EC;border-left:3px solid #EF9F27;padding:8px 12px;border-radius:0 6px 6px 0;margin-bottom:6px;font-size:13px;}
.diff-cosmetic{background:#F2F0ED;border-left:3px solid #C8C4BE;padding:8px 12px;border-radius:0 6px 6px 0;margin-bottom:6px;font-size:13px;}

.step-pill{display:inline-flex;align-items:center;gap:5px;background:#0D1B2A;color:#5EC4A8;border-radius:20px;
  padding:4px 12px;font-size:11px;font-weight:600;margin-bottom:8px;}
.step-pill.s2{background:#1A6B52;color:#fff;}

.compliance-strip{display:flex;gap:20px;flex-wrap:wrap;padding:16px 32px;border-top:1px solid #E2DED8;margin-top:28px;background:#F2F0ED;}
.comp-tag{display:flex;align-items:center;gap:6px;font-size:11px;color:#99AABB;}
.comp-dot{width:5px;height:5px;border-radius:50%;display:inline-block;}
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
_defaults = {
    "logged_in": False,
    "anon_text": "", "anon_textarea": "",
    "sum_text": "", "sum_ta": "",
    "comp_text": "", "comp_ta": "",
    "class_text": "", "class_ta": "",
    "v1_text": "", "v1ta": "",
    "v2_text": "", "v2ta": "",
    "dup_files": {},
    "_login_failed": False,
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ── File extraction ───────────────────────────────────────────────────────────
def extract_text(uploaded_file):
    if uploaded_file is None:
        return "", None
    name = uploaded_file.name.lower()
    try:
        raw = uploaded_file.read()
        if name.endswith(".docx"):
            if not DOCX_OK:
                return "", "python-docx not installed"
            doc = python_docx.Document(io.BytesIO(raw))
            return "\n".join(p.text for p in doc.paragraphs if p.text.strip()), None
        elif name.endswith(".pdf"):
            if not PDF_OK:
                return "", "pypdf not installed"
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
            return "", f"Unsupported format: {uploaded_file.name}"
    except Exception as e:
        return "", str(e)


# ── Anonymisation engine ──────────────────────────────────────────────────────
INDIAN_FIRST = ["Rajesh","Priya","Suresh","Anita","Vikram","Sunita","Amit","Kavita",
                "Ravi","Deepa","Mohit","Pooja","Arjun","Neha","Sanjay","Meera","Rahul",
                "Divya","Anil","Rekha","Vijay","Smita","Ramesh","Geeta","Ashok","Usha",
                "Manoj","Seema","Vinod","Lata","Rohit","Kiran","Nisha","Ganesh","Harish"]
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
    """
    Two-step pipeline. Returns dict with step1/step2 outputs, entity counts, audit.
    Raw values in token_map are ONLY used internally — never rendered to UI.
    """
    token_map = {}   # internal only — never passed to UI
    audit = []
    entity_counts = {}
    cnt = {k: 0 for k in ["PATIENT","INVESTIGATOR","DATE","SITE","ID","PHONE","AADHAAR","HOSP_REC"]}
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    found_types = set()
    processed = text

    def tok(kind):
        cnt[kind] += 1
        return f"[{kind}-{cnt[kind]:03d}]"

    def rec(t, orig, etype):
        token_map[t] = orig   # raw value stored internally only
        audit.append({"Timestamp": ts, "Action": "Pseudonymised", "Entity Type": etype,
                      "Token": t, "Reversible": "Yes"})
        found_types.add(etype)
        entity_counts[etype] = entity_counts.get(etype, 0) + 1

    # Email
    for m in re.finditer(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}', processed):
        t = tok("ID"); rec(t, m.group(), "Email Address")
        processed = processed.replace(m.group(), t, 1)
    # Hospital record
    for m in re.finditer(r'#\d{4,6}', processed):
        t = tok("HOSP_REC"); rec(t, m.group(), "Hospital Record No.")
        processed = processed.replace(m.group(), t, 1)
    # Aadhaar
    for m in re.finditer(r'\d{4}[-\s]\d{4}[-\s]\d{4}', processed):
        t = tok("AADHAAR"); rec(t, m.group(), "Aadhaar Number")
        processed = processed.replace(m.group(), t, 1)
    # Phone +91
    for m in re.finditer(r'\+91[\s-]?\d{2,4}[\s-]\d{4}[\s-]\d{4}', processed):
        t = tok("PHONE"); rec(t, m.group(), "Phone Number")
        processed = processed.replace(m.group(), t, 1)
    # 10-digit mobile
    for m in re.finditer(r'[6-9]\d{9}', processed):
        t = tok("PHONE"); rec(t, m.group(), "Phone Number")
        processed = processed.replace(m.group(), t, 1)
    # Coded IDs
    for m in re.finditer(r'(?:PT|SITE|IND|CT|SUBJ|INV|LH|MH|DL|CH)[-]\w{2,8}[-]\w{2,8}', processed):
        o = m.group()
        if any(o.startswith(p) for p in ["PT","SUBJ","LH","MH","DL"]):
            t = tok("PATIENT"); et = "Patient ID"
        elif o.startswith("SITE"):
            t = tok("SITE"); et = "Site Number"
        elif o.startswith("INV"):
            t = tok("INVESTIGATOR"); et = "Investigator ID"
        else:
            t = tok("ID"); et = "Regulatory ID"
        rec(t, o, et); processed = processed.replace(o, t, 1)
    # Dates
    for pat in [
        re.compile(r'\d{1,2}[-/]\w{2,9}[-/]\d{2,4}'),
        re.compile(r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}'),
        re.compile(r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2},?\s+\d{4}', re.I),
        re.compile(r'\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}', re.I),
    ]:
        for m in pat.finditer(processed):
            t = tok("DATE"); rec(t, m.group(), "Date / DOB")
            processed = processed.replace(m.group(), t, 1)
    # Initials
    for m in re.finditer(r'(?<!\w)[A-Z]\.[A-Z]\.(?!\w)', processed):
        t = tok("PATIENT"); rec(t, m.group(), "Patient Initials")
        processed = processed.replace(m.group(), t, 1)
    # Dr. + Indian name
    name_re = re.compile(r'(Dr\.?\s+)(' + '|'.join(INDIAN_FIRST) + r')\s+(' + '|'.join(INDIAN_LAST) + r')')
    for m in name_re.finditer(processed):
        t = tok("INVESTIGATOR"); rec(t, m.group(), "Investigator Name")
        processed = processed.replace(m.group(), t, 1)
    # Non-Dr Indian name
    name_re2 = re.compile(r'(' + '|'.join(INDIAN_FIRST) + r')\s+(' + '|'.join(INDIAN_LAST) + r')')
    for m in name_re2.finditer(processed):
        if m.group() in processed:
            t = tok("PATIENT"); rec(t, m.group(), "Patient Name")
            processed = processed.replace(m.group(), t, 1)
    # Pincode (last)
    for m in re.finditer(r'[1-9]\d{5}', processed):
        t = tok("ID"); rec(t, m.group(), "Pincode")
        processed = processed.replace(m.group(), t, 1)

    step1 = processed

    # Step 2: irreversible generalisation
    step2 = step1
    step2 = re.compile(r'\b(\d{2})\s*(?:years?|yrs?)(?:\s*old)?\b', re.I).sub(
        lambda m: f"{(int(m.group(1))//5)*5}-{(int(m.group(1))//5)*5+4} years", step2)
    step2 = re.compile(r'\b(\d{2,3})\s*kg\b', re.I).sub(
        lambda m: f"{(int(m.group(1))//10)*10}-{(int(m.group(1))//10)*10+9} kg", step2)
    step2 = re.compile(r'\[DATE-\d+\]').sub('[YEAR-ONLY]', step2)

    for et in ["Dates→Year only", "Ages→Range", "Biometrics→Range"]:
        audit.append({"Timestamp": ts, "Action": "Irreversible Generalisation",
                      "Entity Type": et, "Token": "Generalised", "Reversible": "No"})

    total = sum(entity_counts.values())

    # Delete internal token_map — never returned
    del token_map

    return {
        "step1": step1,
        "step2": step2,
        "audit": audit,
        "entity_counts": entity_counts,
        "found_types": list(found_types),
        "total": total,
    }


# ── AI recommendation card ────────────────────────────────────────────────────
def ai_card(finding, risk, action, detail=""):
    cls_map = {"Low": "c-low", "Medium": "c-med", "High": "c-high", "Critical": "c-crit"}
    badge_map = {
        "Low":      "background:#EBF6F2;color:#1A6B52;",
        "Medium":   "background:#FDF3EC;color:#854F0B;",
        "High":     "background:#FFF3E0;color:#974A00;",
        "Critical": "background:#FCEAEA;color:#8B2020;",
    }
    cls = cls_map.get(risk, "c-med")
    badge_style = badge_map.get(risk, badge_map["Medium"])
    st.markdown(f"""
    <div class="ai-card {cls}">
      <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:16px;flex-wrap:wrap;">
        <div style="flex:1;">
          <div class="ai-eyebrow">AI Recommendation</div>
          <div class="ai-finding">{finding}</div>
          <div class="ai-action">{action}</div>
          {f'<div class="ai-detail">{detail}</div>' if detail else ""}
        </div>
        <div style="text-align:center;flex-shrink:0;">
          <div class="ai-badge" style="{badge_style}">{risk} Risk</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ── Compliance footer ─────────────────────────────────────────────────────────
def compliance_footer():
    st.markdown("""
    <div class="compliance-strip">
      <span class="comp-tag"><span class="comp-dot" style="background:#5EC4A8;"></span>DPDP Act 2023</span>
      <span class="comp-tag"><span class="comp-dot" style="background:#7AB8D8;"></span>ICMR Guidelines</span>
      <span class="comp-tag"><span class="comp-dot" style="background:#A88FD0;"></span>NDHM Policy</span>
      <span class="comp-tag"><span class="comp-dot" style="background:#E09A60;"></span>MeitY AI Ethics</span>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# LOGIN PAGE
# ══════════════════════════════════════════════════════════════════════════════
VALID_USER = "admin"
VALID_PASS = "nirnay2026"

if not st.session_state["logged_in"]:
    st.markdown("""
    <style>
    .stApp{background:#EAEAE6 !important;}
    [data-testid="stTextInput"] input{
        background:rgba(255,255,255,0.14) !important;border:1px solid rgba(255,255,255,0.3) !important;
        border-radius:8px !important;color:#fff !important;font-size:13px !important;padding:10px 14px !important;}
    [data-testid="stTextInput"] input::placeholder{color:rgba(255,255,255,0.4) !important;}
    [data-testid="stTextInput"] label{color:rgba(255,255,255,0.6) !important;font-size:10px !important;
        font-weight:600 !important;letter-spacing:.08em !important;text-transform:uppercase !important;}
    [data-testid="stTextInput"] input:focus{border-color:#5EC4A8 !important;}
    div[data-testid="column"]:last-child{background:#0D1B2A;padding:40px 36px !important;min-height:580px;}
    .login-btn>button{background:#1A6B52 !important;color:#fff !important;border:none !important;
        border-radius:8px !important;font-size:13px !important;font-weight:600 !important;
        padding:12px !important;width:100% !important;}
    .login-btn>button:hover{background:#1D8060 !important;}
    </style>
    """, unsafe_allow_html=True)

    lcol, rcol = st.columns([1.15, 0.85], gap="small")

    # ── LEFT: Brand + module grid ──
    with lcol:
        st.markdown("""
<div style="background:#F2F0ED;padding:44px 44px 36px;min-height:580px;display:flex;flex-direction:column;gap:0;box-shadow:0 8px 40px rgba(0,0,0,0.1);">

  <div style="display:flex;align-items:center;gap:14px;margin-bottom:20px;">
    <div style="font-family:'Playfair Display',serif;font-size:28px;font-weight:700;color:#0D1B2A;letter-spacing:-0.5px;">Nirnay</div>
    <div style="width:1px;height:28px;background:#C8C4BE;"></div>
    <div>
      <div style="font-size:9px;font-weight:600;color:#8899AA;letter-spacing:1.2px;text-transform:uppercase;">CDSCO</div>
      <div style="font-size:9px;font-weight:600;color:#8899AA;letter-spacing:1.2px;text-transform:uppercase;">AI REVIEW SYSTEM</div>
    </div>
  </div>

  <div style="margin-bottom:28px;">
    <div style="font-size:21px;font-weight:400;color:#0D1B2A;line-height:1.35;">Regulatory review,</div>
    <div style="font-size:21px;font-weight:600;color:#1A6B52;line-height:1.35;">reimagined for India.</div>
  </div>

  <div style="font-size:10px;font-weight:600;color:#AAAAAA;letter-spacing:1px;text-transform:uppercase;margin-bottom:14px;">6 AI modules · Stage 1 build</div>

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:28px;">
    <div style="background:#fff;border:1px solid #E2DED8;border-radius:10px;padding:13px;">
      <div style="font-size:9px;font-weight:600;color:#1A6B52;letter-spacing:0.5px;margin-bottom:3px;">01 · PRIVACY</div>
      <div style="font-size:13px;font-weight:600;color:#0D1B2A;margin-bottom:2px;">Anonymisation</div>
      <div style="font-size:11px;color:#99AABB;line-height:1.4;">DPDP Act 2023 compliant PII removal</div>
    </div>
    <div style="background:#fff;border:1px solid #E2DED8;border-radius:10px;padding:13px;">
      <div style="font-size:9px;font-weight:600;color:#185FA5;letter-spacing:0.5px;margin-bottom:3px;">02 · INTELLIGENCE</div>
      <div style="font-size:13px;font-weight:600;color:#0D1B2A;margin-bottom:2px;">Summarisation</div>
      <div style="font-size:11px;color:#99AABB;line-height:1.4;">SAE reports, checklists, meeting audio</div>
    </div>
    <div style="background:#fff;border:1px solid #E2DED8;border-radius:10px;padding:13px;">
      <div style="font-size:9px;font-weight:600;color:#534AB7;letter-spacing:0.5px;margin-bottom:3px;">03 · VALIDATION</div>
      <div style="font-size:13px;font-weight:600;color:#0D1B2A;margin-bottom:2px;">Completeness</div>
      <div style="font-size:11px;color:#99AABB;line-height:1.4;">Mandatory field verification, flagging</div>
    </div>
    <div style="background:#fff;border:1px solid #E2DED8;border-radius:10px;padding:13px;">
      <div style="font-size:9px;font-weight:600;color:#854F0B;letter-spacing:0.5px;margin-bottom:3px;">04 · TRIAGE</div>
      <div style="font-size:13px;font-weight:600;color:#0D1B2A;margin-bottom:2px;">Classification</div>
      <div style="font-size:11px;color:#99AABB;line-height:1.4;">SAE severity scoring + duplicate detection</div>
    </div>
    <div style="background:#fff;border:1px solid #E2DED8;border-radius:10px;padding:13px;">
      <div style="font-size:9px;font-weight:600;color:#3B6D11;letter-spacing:0.5px;margin-bottom:3px;">05 · DIFF ENGINE</div>
      <div style="font-size:13px;font-weight:600;color:#0D1B2A;margin-bottom:2px;">Comparison</div>
      <div style="font-size:11px;color:#99AABB;line-height:1.4;">Semantic + structural dossier version diff</div>
    </div>
    <div style="background:#fff;border:1px solid #E2DED8;border-radius:10px;padding:13px;">
      <div style="font-size:9px;font-weight:600;color:#993556;letter-spacing:0.5px;margin-bottom:3px;">06 · GENERATION</div>
      <div style="font-size:13px;font-weight:600;color:#0D1B2A;margin-bottom:2px;">Inspection Report</div>
      <div style="font-size:11px;color:#99AABB;line-height:1.4;">Typed / handwritten / audio → GCP report</div>
    </div>
  </div>

  <div style="display:flex;gap:14px;flex-wrap:wrap;margin-top:auto;">
    <span style="display:flex;align-items:center;gap:5px;font-size:11px;color:#99AABB;"><span style="width:5px;height:5px;border-radius:50%;background:#5EC4A8;display:inline-block;"></span>DPDP Act 2023</span>
    <span style="display:flex;align-items:center;gap:5px;font-size:11px;color:#99AABB;"><span style="width:5px;height:5px;border-radius:50%;background:#7AB8D8;display:inline-block;"></span>ICMR Guidelines</span>
    <span style="display:flex;align-items:center;gap:5px;font-size:11px;color:#99AABB;"><span style="width:5px;height:5px;border-radius:50%;background:#A88FD0;display:inline-block;"></span>NDHM Policy</span>
    <span style="display:flex;align-items:center;gap:5px;font-size:11px;color:#99AABB;"><span style="width:5px;height:5px;border-radius:50%;background:#E09A60;display:inline-block;"></span>MeitY AI Ethics</span>
  </div>

</div>
        """, unsafe_allow_html=True)

    # ── RIGHT: Login form ──
    with rcol:
        st.markdown("""
<div style="padding-top:44px;">
  <div style="font-size:10px;font-weight:600;color:#445566;letter-spacing:1.2px;text-transform:uppercase;margin-bottom:16px;">Authorised access only</div>
  <div style="font-family:'Playfair Display',serif;font-size:22px;color:#fff;margin-bottom:4px;font-weight:600;">Sign in to Nirnay</div>
  <div style="font-size:12px;color:#445566;margin-bottom:28px;line-height:1.6;">CDSCO regulatory review platform.<br>Use credentials provided by your team lead.</div>
</div>
        """, unsafe_allow_html=True)

        _uname = st.text_input("Username", placeholder="Enter username", key="login_uname")
        _pwd   = st.text_input("Password", placeholder="••••••••••", type="password", key="login_pwd")

        if st.session_state["_login_failed"]:
            st.markdown('<div style="color:#fca5a5;font-size:12px;margin:-6px 0 8px;">⚠ Invalid credentials.</div>', unsafe_allow_html=True)

        st.markdown('<div class="login-btn">', unsafe_allow_html=True)
        _do_login = st.button("Sign In →", key="login_btn", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("""
<div style="margin-top:20px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.12);border-radius:8px;padding:12px 14px;">
  <p style="font-size:11px;color:#445566;line-height:1.7;text-align:center;margin:0;">
    Authorised CDSCO personnel only.<br>All sessions are logged for compliance.
  </p>
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


# ══════════════════════════════════════════════════════════════════════════════
# POST-LOGIN APP
# ══════════════════════════════════════════════════════════════════════════════

# ── Top bar ───────────────────────────────────────────────────────────────────
tb1, tb2 = st.columns([4, 1])
with tb1:
    st.markdown("""
<div class="nrn-topbar">
  <span class="nrn-logo">Nirnay</span>
  <span class="nrn-badge">CDSCO · AI Review</span>
  <span class="nrn-tagline">Regulatory review, <em>reimagined for India.</em></span>
</div>
    """, unsafe_allow_html=True)
with tb2:
    if st.button("Sign out", key="signout"):
        st.session_state["logged_in"] = False
        st.rerun()

# ── Tabs ──────────────────────────────────────────────────────────────────────
t0,t1,t2,t3,t4,t5,t6 = st.tabs([
    "Home", "Anonymisation", "Summarisation",
    "Completeness", "Classification", "Comparison", "Inspection Report"
])

FEATURES = [
    ("01","#1A6B52","Anonymisation","Privacy","DPDP Act 2023 compliant PII removal. In-memory — raw data never stored."),
    ("02","#185FA5","Summarisation","Intelligence","Extracts decisions and findings from SAE reports, checklists, meeting audio."),
    ("03","#534AB7","Completeness","Validation","Mandatory field verification against clinical application checklists."),
    ("04","#854F0B","Classification","Triage","SAE severity scoring: death, disability, hospitalisation. Duplicate detection."),
    ("05","#3B6D11","Comparison","Diff Engine","Semantic + structural diff across dossier versions. Critical/moderate/cosmetic triage."),
    ("06","#993556","Inspection Report","Generation","Typed notes / handwritten scans / audio → formal CDSCO GCP report."),
]

# ══════════════════════════════════════════════════════════════════════════════
# HOME
# ══════════════════════════════════════════════════════════════════════════════
with t0:
    st.markdown("<div style='padding:24px 8px 8px;font-size:10px;font-weight:600;color:#99AABB;letter-spacing:1px;text-transform:uppercase;'>Available features — select to begin</div>", unsafe_allow_html=True)

    cols = st.columns(3, gap="medium")
    tab_names = ["Anonymisation","Summarisation","Completeness","Classification","Comparison","Inspection Report"]

    for i,(num,color,name,label,desc) in enumerate(FEATURES):
        with cols[i % 3]:
            st.markdown(f"""
<div style="background:#0D1B2A;border-radius:12px;padding:22px 20px;position:relative;overflow:hidden;min-height:200px;display:flex;flex-direction:column;justify-content:space-between;margin-bottom:8px;">
  <div style="position:absolute;right:12px;bottom:-10px;font-size:72px;font-weight:700;color:rgba(255,255,255,0.04);line-height:1;pointer-events:none;font-family:'Playfair Display',serif;">{num}</div>
  <div>
    <div style="font-size:9px;font-weight:600;color:{color};letter-spacing:0.8px;text-transform:uppercase;margin-bottom:4px;">{num} · {label.upper()}</div>
    <div style="font-size:16px;font-weight:700;color:#fff;margin-bottom:6px;">{name}</div>
    <div style="font-size:11px;color:rgba(255,255,255,0.45);line-height:1.6;">{desc}</div>
  </div>
  <div style="display:inline-flex;align-items:center;gap:5px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.15);border-radius:6px;padding:5px 12px;font-size:10px;font-weight:600;color:rgba(255,255,255,0.7);margin-top:14px;align-self:flex-start;">Start →</div>
</div>
            """, unsafe_allow_html=True)
            if st.button(f"Open {tab_names[i]}", key=f"home_{i}", use_container_width=True):
                st.session_state["active_tab"] = i + 1
                st.rerun()

    # Tab-switching via JS
    _idx = st.session_state.get("active_tab", 0)
    if _idx > 0:
        st.session_state["active_tab"] = 0
        import streamlit.components.v1 as _cv1
        _cv1.html(f"""<script>(function(){{var idx={_idx};function c(){{var t=window.parent.document.querySelectorAll('[data-baseweb="tab"]');if(t.length>idx)t[idx].click();else setTimeout(c,100);}}setTimeout(c,200);}})();</script>""", height=0)

    compliance_footer()


# ══════════════════════════════════════════════════════════════════════════════
# FEATURE 1 — ANONYMISATION
# ══════════════════════════════════════════════════════════════════════════════
with t1:
    st.markdown("""
    <div class="sec-hd">
      <div class="sec-num" style="color:#1A6B52;">01</div>
      <div><h2>Anonymisation</h2>
      <p>Detects and removes PII/PHI from regulatory documents · Two-step DPDP Act 2023 pipeline · In-memory only — original file discarded immediately after processing</p></div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("How the two-step pipeline works", expanded=False):
        c1e, c2e = st.columns(2)
        with c1e:
            st.markdown("""**Step 1 — Pseudonymisation**
            
Every PII entity is replaced with a token: `[PATIENT-001]`, `[DATE-002]`.
Token mapping is used only internally — never shown in the UI.""")
        with c2e:
            st.markdown("""**Step 2 — Irreversible Anonymisation**
            
Tokens are generalised: dates become `[YEAR-ONLY]`, ages become ranges.
Output has zero recovery path. Safe to share externally.""")

    st.markdown("---")

    anon_file = st.file_uploader(
        "Upload document (PDF, DOCX, TXT) — processed in-memory only",
        type=["docx","pdf","txt"], key="anon_up"
    )

    if anon_file is not None:
        raw_bytes = anon_file.read()
        _name = anon_file.name.lower()
        try:
            if _name.endswith(".docx") and DOCX_OK:
                _doc = python_docx.Document(io.BytesIO(raw_bytes))
                _extracted = "\n".join(p.text for p in _doc.paragraphs if p.text.strip())
            elif _name.endswith(".pdf") and PDF_OK:
                _r = PdfReader(io.BytesIO(raw_bytes))
                _extracted = "\n".join(pg.extract_text() or "" for pg in _r.pages)
            elif _name.endswith(".txt"):
                _extracted = raw_bytes.decode("utf-8", errors="ignore")
            else:
                _extracted = ""
        except Exception as e:
            _extracted = ""
            st.error(f"Extraction error: {e}")

        # Discard raw bytes immediately
        del raw_bytes

        if _extracted.strip():
            st.session_state["anon_upload_name"] = anon_file.name
            st.success(f"✓ File loaded · {len(_extracted.split())} words extracted · Original discarded from memory")
            # Immediately run anonymisation — do NOT store raw text in session_state
            with st.spinner("Running anonymisation pipeline..."):
                _result = run_anonymisation(_extracted)
            del _extracted  # discard raw extracted text

            # ── Show summary — entity counts only, never values ──
            st.markdown("---")
            _total = _result["total"]
            _counts = _result["entity_counts"]

            # Metrics
            mcols = st.columns(min(len(_counts) + 1, 5))
            with mcols[0]:
                st.metric("Total Entities", _total)
            for _i, (_etype, _cnt) in enumerate(list(_counts.items())[:4]):
                with mcols[_i + 1]:
                    st.metric(_etype.replace("_"," ").title(), _cnt)

            # AI recommendation
            if _total == 0:
                ai_card("No PII/PHI patterns detected", "Low",
                    "No standard identifiers found. Verify manually if document contains non-standard PII.",
                    "Manual review recommended before external sharing.")
            elif _total >= 5:
                ai_card(f"{_total} entities detected and anonymised", "High",
                    "Document contained significant PII. Download the anonymised version for sharing. Audit log generated.",
                    f"Types found: {', '.join(_result['found_types'])}")
            else:
                ai_card(f"{_total} entity/entities detected and anonymised", "Medium",
                    "PII detected and removed. Download anonymised output below.",
                    f"Types found: {', '.join(_result['found_types'])}")

            # Status
            st.markdown("""
            <div class="ncard">
              <div class="ncard-title">Process Status</div>
              <div style="font-size:13px;color:#0D1B2A;line-height:2;">
                ✓ PII detection complete<br>
                ✓ Step 1 — Pseudonymisation complete<br>
                ✓ Step 2 — Irreversible anonymisation complete<br>
                ✓ Original file discarded from memory<br>
                ✓ DPDP Act 2023 audit log generated
              </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("#### Downloads")
            st.caption("Two outputs as per CDSCO two-step anonymisation guidelines. No raw PII values in any output.")

            dl1, dl2 = st.columns(2)
            _fname = st.session_state.get("anon_upload_name", "document")
            _base = _fname.rsplit(".", 1)[0] if "." in _fname else _fname
            _now = datetime.datetime.now().isoformat()

            with dl1:
                st.markdown("""<div class="ncard"><div class="ncard-title">Anonymised Document</div>
                <div class="ncard-sub">Irreversibly anonymised — safe to share</div></div>""", unsafe_allow_html=True)
                _anon_txt = "\n".join([
                    "Nirnay — Anonymised Document",
                    f"Generated: {_now}", f"Source: {_fname}",
                    "="*60, "",
                    _result["step2"]
                ])
                st.download_button("⬇ Download Anonymised Document (TXT)",
                    _anon_txt, file_name=f"{_base}_anonymised.txt", mime="text/plain",
                    use_container_width=True)

            with dl2:
                st.markdown("""<div class="ncard"><div class="ncard-title">DPDP Audit Log</div>
                <div class="ncard-sub">Entity types and counts only — compliance artifact</div></div>""", unsafe_allow_html=True)
                _audit_payload = {
                    "system": "Nirnay — CDSCO AI Review Platform",
                    "timestamp": _now,
                    "source_file": _fname,
                    "compliance": ["DPDP Act 2023", "ICMR Ethical Guidelines", "NDHM Policy"],
                    "note": "This log contains entity types and counts only. No raw PII values are recorded.",
                    "step_1": "Pseudonymisation complete",
                    "step_2": "Irreversible anonymisation complete",
                    "entity_breakdown": _counts,
                    "total_entities": _total,
                    "audit_entries": _result["audit"]
                }
                st.download_button("⬇ Download Audit Log (JSON)",
                    json.dumps(_audit_payload, indent=2),
                    file_name=f"{_base}_audit_log.json", mime="application/json",
                    use_container_width=True)

            st.info("ℹ️ The audit log contains entity types and counts only. No raw PII values are recorded anywhere in this system.")

    else:
        # Text paste mode
        st.markdown('<div style="font-size:12px;color:#99AABB;margin:8px 0 4px;">Or paste document text directly</div>', unsafe_allow_html=True)
        anon_ta = st.text_area("Document text",
            height=200, placeholder="Paste SAE report, clinical trial document, or any regulatory text with PII/PHI...",
            key="anon_textarea", label_visibility="collapsed")

        if st.button("Analyse & anonymise text", key="run_anon_paste", type="primary"):
            content = st.session_state.get("anon_textarea", "").strip()
            if not content:
                st.markdown('<div class="rc warn">Please paste text or upload a file first.</div>', unsafe_allow_html=True)
            else:
                with st.spinner("Running anonymisation..."):
                    _result = run_anonymisation(content)
                _total = _result["total"]
                _counts = _result["entity_counts"]
                _fname = "pasted_document"
                _base = "pasted_document"
                _now = datetime.datetime.now().isoformat()

                if _total == 0:
                    ai_card("No PII/PHI patterns detected", "Low",
                        "No standard identifiers found.", "Manual review recommended.")
                else:
                    ai_card(f"{_total} entities detected and anonymised", "High" if _total >= 5 else "Medium",
                        f"Types found: {', '.join(_result['found_types'])}")

                mcols2 = st.columns(min(len(_counts)+1, 5))
                with mcols2[0]:
                    st.metric("Total Entities", _total)
                for _j, (_et, _c) in enumerate(list(_counts.items())[:4]):
                    with mcols2[_j+1]:
                        st.metric(_et.replace("_"," ").title(), _c)

                c_left, c_right = st.columns(2)
                with c_left:
                    st.markdown('<div class="step-pill">Step 1 — Pseudonymised</div>', unsafe_allow_html=True)
                    st.text_area("", _result["step1"], height=220, key="s1_out", label_visibility="collapsed")
                with c_right:
                    st.markdown('<div class="step-pill s2">Step 2 — Irreversibly anonymised</div>', unsafe_allow_html=True)
                    st.text_area("", _result["step2"], height=220, key="s2_out", label_visibility="collapsed")

                dl1b, dl2b = st.columns(2)
                with dl1b:
                    st.download_button("⬇ Download Anonymised Text",
                        _result["step2"], file_name="anonymised.txt", mime="text/plain",
                        use_container_width=True)
                with dl2b:
                    _audit_p = {"timestamp": _now, "entity_counts": _counts,
                                "total": _total, "note": "Entity types and counts only — no raw values."}
                    st.download_button("⬇ Download Audit Log (JSON)",
                        json.dumps(_audit_p, indent=2),
                        file_name="audit_log.json", mime="application/json",
                        use_container_width=True)

    compliance_footer()


# ══════════════════════════════════════════════════════════════════════════════
# FEATURE 2 — SUMMARISATION
# ══════════════════════════════════════════════════════════════════════════════
with t2:
    st.markdown("""
    <div class="sec-hd">
      <div class="sec-num" style="color:#185FA5;">02</div>
      <div><h2>Document Summarisation</h2>
      <p>Three source types: SAE Case Narration · Application Checklist · Meeting Transcript / Audio</p></div>
    </div>
    """, unsafe_allow_html=True)

    doc_type = st.selectbox("Document type", [
        "SAE Case Narration", "Application Checklist (SUGAM)", "Meeting Transcript / Audio"])

    if doc_type == "Meeting Transcript / Audio":
        st.markdown('<div class="rc info">Audio files accepted. Paste the transcript text in the box below for processing. Whisper-based live transcription is available in Stage 2.</div>', unsafe_allow_html=True)
        sum_file = st.file_uploader("Upload (DOCX/PDF/TXT/Audio)", type=["docx","pdf","txt","mp3","wav","m4a"], key="sum_up")
    else:
        sum_file = st.file_uploader("Upload document (DOCX/PDF/TXT)", type=["docx","pdf","txt"], key="sum_up2")

    audio_mode = False
    if sum_file:
        fname = sum_file.name.lower()
        if any(fname.endswith(x) for x in [".mp3",".wav",".m4a"]):
            audio_mode = True
            st.success(f"✓ Audio received: {sum_file.name} — paste transcript below")
        else:
            txt, err = extract_text(sum_file)
            if err:
                st.error(err)
            elif txt.strip():
                st.session_state["sum_text"] = txt
                st.session_state["sum_ta"] = txt
                st.success(f"✓ {len(txt.split())} words extracted")

    sum_input = st.text_area("Document content",
        height=180, placeholder="Paste document content here...", key="sum_ta",
        label_visibility="collapsed")
    st.session_state["sum_text"] = st.session_state.get("sum_ta", "")

    col1s, col2s, _ = st.columns([1,1,3])
    with col1s:
        run_sum = st.button("Summarise", type="primary", use_container_width=True)
    with col2s:
        if st.button("Clear", key="clear_sum", use_container_width=True):
            st.session_state["sum_text"] = ""; st.session_state["sum_ta"] = ""; st.rerun()

    if run_sum:
        content = st.session_state["sum_text"].strip()
        if not content and not audio_mode:
            st.markdown('<div class="rc warn">Please upload or paste content first.</div>', unsafe_allow_html=True)
        else:
            tl = content.lower()
            if doc_type == "SAE Case Narration":
                priority = ("URGENT" if any(w in tl for w in ["death","fatal","died","disability","permanent"])
                            else "STANDARD" if any(w in tl for w in ["hospitalised","admitted","icu","hospital"])
                            else "LOW")
                causality = ("Definitely Related" if "definitely" in tl
                             else "Probably Related" if "probably" in tl
                             else "Possibly Related" if "possibly" in tl
                             else "Unrelated" if "unrelated" in tl
                             else "Under Assessment")
                outcome = ("Fatal" if any(w in tl for w in ["died","death","fatal"])
                           else "Recovered" if any(w in tl for w in ["recovered","resolution"])
                           else "Recovering" if "recovering" in tl
                           else "Ongoing")
                cc = "err" if priority=="URGENT" else "warn" if priority=="STANDARD" else "ok"
                timeline = ("Expedited 7-day" if priority=="URGENT"
                            else "Expedited 15-day" if priority=="STANDARD"
                            else "Periodic 90-day")
                _r_map = {"URGENT":"Critical","STANDARD":"Medium","LOW":"Low"}
                _a_map = {
                    "URGENT": "Immediate escalation to DCGI. Expedited 7-day report applicable.",
                    "STANDARD": "Route to standard SAE queue. Expedited 15-day report required.",
                    "LOW": "Log as periodic SAE. Standard 90-day timeline applies."
                }
                ai_card(f"SAE classified as {priority} · {causality} · {outcome}",
                    _r_map[priority], _a_map[priority],
                    f"Reporting timeline: {timeline} · Form 12A")
                c1s, c2s, c3s = st.columns(3)
                c1s.metric("Priority", priority); c2s.metric("Causality", causality); c3s.metric("Outcome", outcome)
                with st.expander("Full SAE Summary", expanded=True):
                    setting = "Hospital/Emergency" if any(w in tl for w in ["hospital","emergency","icu"]) else "Outpatient"
                    st.markdown(f"""| Field | Value |
|---|---|
| Document Type | SAE Case Narration |
| Priority | {priority} |
| Causality | {causality} |
| Outcome | {outcome} |
| Setting | {setting} |
| Reporting Timeline | {timeline} |""")
                st.download_button("⬇ Download Summary",
                    f"Priority:{priority}\nCausality:{causality}\nOutcome:{outcome}\nTimeline:{timeline}",
                    file_name="sae_summary.txt")

            elif doc_type == "Application Checklist (SUGAM)":
                lines = [l.strip() for l in content.split('\n') if l.strip()]
                comp = sum(1 for l in lines if any(w in l.lower() for w in ["complete","present","yes","submitted","available"]))
                miss = sum(1 for l in lines if any(w in l.lower() for w in ["missing","absent","no","not submitted"]))
                inc  = sum(1 for l in lines if any(w in l.lower() for w in ["incomplete","pending","partial"]))
                tot = len(lines); sc = round((comp/tot)*100) if tot else 0
                rec = "Approve" if sc>=80 else "Return for Completion" if sc>=50 else "Reject"
                cc = "ok" if sc>=80 else "warn" if sc>=50 else "err"
                c1s,c2s,c3s,c4s = st.columns(4)
                c1s.metric("Total",tot); c2s.metric("Complete",comp); c3s.metric("Incomplete",inc); c4s.metric("Missing",miss)
                st.progress(sc/100, text=f"Completeness: {sc}%")
                st.markdown(f'<div class="rc {cc}"><b>Recommendation:</b> {rec}</div>', unsafe_allow_html=True)
                st.download_button("⬇ Download", f"Score:{sc}%\n{rec}", file_name="checklist_summary.txt")

            else:  # Meeting
                if audio_mode and not content.strip():
                    st.markdown('<div class="rc info">Audio received. Paste transcript text above for full extraction.</div>', unsafe_allow_html=True)
                else:
                    lines = content.split('\n')
                    dec, act, iss = [], [], []
                    for l in lines:
                        ll = l.lower()
                        if any(w in ll for w in ["decided","approved","resolved","agreed","concluded"]): dec.append(l.strip())
                        elif any(w in ll for w in ["action","will","shall","owner","follow up"]): act.append(l.strip())
                        elif any(w in ll for w in ["pending","unresolved","defer","tabled"]): iss.append(l.strip())
                    c1s,c2s,c3s = st.columns(3)
                    c1s.metric("Decisions",len(dec)); c2s.metric("Actions",len(act)); c3s.metric("Open Issues",len(iss))
                    if dec:
                        with st.expander("Key Decisions", expanded=True):
                            for i,d in enumerate(dec[:8],1): st.markdown(f"{i}. {d}")
                    if act:
                        with st.expander("Action Items"):
                            for i,a in enumerate(act[:8],1): st.markdown(f"{i}. {a}")
                    if iss:
                        with st.expander("Open Issues"):
                            for i,x in enumerate(iss[:6],1): st.markdown(f"{i}. {x}")
                    if dec or act:
                        st.download_button("⬇ Download Summary",
                            "\n".join(dec+act), file_name="meeting_summary.txt")
                    elif not dec and not act and not iss and content.strip():
                        st.info("No structured keywords detected. Review pasted content.")

    compliance_footer()


# ══════════════════════════════════════════════════════════════════════════════
# FEATURE 3 — COMPLETENESS
# ══════════════════════════════════════════════════════════════════════════════
with t3:
    st.markdown("""
    <div class="sec-hd">
      <div class="sec-num" style="color:#534AB7;">03</div>
      <div><h2>Completeness Assessment</h2>
      <p>Upload application document · 20 mandatory clinical trial fields · RAG status · Approve / Return / Reject recommendation</p></div>
    </div>
    """, unsafe_allow_html=True)

    SCHED_Y = [
        ("Protocol Synopsis","protocol synopsis","Critical"),
        ("Investigator Brochure","investigator brochure","Critical"),
        ("Form CT-04","ct-04","Critical"),
        ("Form CT-05","ct-05","Critical"),
        ("Ethics Committee Approval","ethics committee","Critical"),
        ("Informed Consent (English)","informed consent","Critical"),
        ("Informed Consent (Local Language)","local language","Critical"),
        ("Investigator CV","investigator cv","Major"),
        ("Site Master File","site master","Major"),
        ("Insurance Certificate","insurance","Major"),
        ("Drug Import License","import license","Major"),
        ("GCP Compliance Certificate","gcp","Major"),
        ("Patient Information Sheet","patient information","Major"),
        ("Case Report Form","case report form","Minor"),
        ("Statistical Analysis Plan","statistical analysis","Minor"),
        ("DSMB Charter","dsmb","Minor"),
        ("Pharmacovigilance Plan","pharmacovigilance","Minor"),
        ("Risk Management Plan","risk management","Minor"),
        ("Regulatory Approval (Origin)","regulatory approval","Major"),
        ("Sponsor Authorisation Letter","sponsor authorisation","Major"),
    ]

    col_a, col_b = st.columns([2,1])
    with col_a:
        cf = st.file_uploader("Upload application document (DOCX/PDF/TXT)", type=["docx","pdf","txt"], key="comp_up")
        if cf:
            txt, err = extract_text(cf)
            if err: st.error(err)
            elif txt.strip():
                st.session_state["comp_text"] = txt
                st.session_state["comp_ta"] = txt
                st.success(f"✓ Extracted from {cf.name}")
        ci = st.text_area("Or paste application content", height=180, key="comp_ta",
            label_visibility="collapsed", placeholder="Paste application text here...")
        st.session_state["comp_text"] = st.session_state.get("comp_ta","")
    with col_b:
        app_id = st.text_input("Application ID", placeholder="SUGAM-CT-2024-0892")
        st.markdown("<br>", unsafe_allow_html=True)
        run_comp = st.button("Check Completeness", type="primary", use_container_width=True)

    if run_comp:
        content = st.session_state["comp_text"].strip()
        if not content:
            st.markdown('<div class="rc warn">Please upload or paste content first.</div>', unsafe_allow_html=True)
        else:
            tl = content.lower(); rows = []; cm = []; mm = []
            for field, kw, sev in SCHED_Y:
                if kw in tl:
                    s = "INCOMPLETE" if any(w in tl for w in ["pending","tbd","partial","to be"]) else "PRESENT"
                    r = "🟢 Green" if s=="PRESENT" else "🟡 Amber"
                else:
                    s = "MISSING"; r = "🔴 Red"
                    if sev == "Critical": cm.append(field)
                    elif sev == "Major":  mm.append(field)
                rows.append({"Field":field,"Severity":sev,"Status":s,"RAG":r})
            df = pd.DataFrame(rows)
            pre = sum(1 for r in rows if r["Status"]=="PRESENT")
            inc = sum(1 for r in rows if r["Status"]=="INCOMPLETE")
            mis = sum(1 for r in rows if r["Status"]=="MISSING")
            sc = round((pre/20)*100)
            rec = ("✅ Approve for Technical Review" if sc>=85 and not cm
                   else "⚠️ Return for Completion" if sc>=60
                   else "❌ Reject — Critical fields missing")
            cc = "ok" if sc>=85 and not cm else "warn" if sc>=60 else "err"

            c1c,c2c,c3c,c4c = st.columns(4)
            c1c.metric("Total", 20); c2c.metric("Present", pre); c3c.metric("Incomplete", inc); c4c.metric("Missing", mis)
            st.progress(sc/100, text=f"Completeness: {sc}%")

            _cr = "Critical" if cm else "High" if sc<60 else "Medium" if sc<85 else "Low"
            _ca = (f"Reject — {len(cm)} critical field(s) missing: {', '.join(cm[:3])}." if cm
                   else f"Return for completion — {mis} field(s) need attention." if sc<85
                   else "Approve for technical review — all critical fields present.")
            ai_card(f"Completeness: {sc}% · {rec}", _cr, _ca,
                f"Fields checked: 20 · Present: {pre} · Missing: {mis} · Incomplete: {inc}")

            st.markdown(f'<div class="rc {cc}"><b>Recommendation:</b> {rec}</div>', unsafe_allow_html=True)
            if cm: st.error(f"Critical missing: {', '.join(cm)}")
            if mm: st.warning(f"Major missing: {', '.join(mm)}")

            with st.expander("Full Field Status", expanded=True):
                def srag(v):
                    if "Green" in str(v): return "background-color:#EBF6F2;color:#1A6B52;font-weight:600"
                    if "Amber" in str(v): return "background-color:#FDF3EC;color:#854F0B;font-weight:600"
                    if "Red" in str(v):   return "background-color:#FCEAEA;color:#8B2020;font-weight:600"
                    return ""
                st.dataframe(df.style.map(srag, subset=["RAG"]), use_container_width=True, hide_index=True)
            st.download_button("⬇ Download Completeness Report",
                df.to_csv(index=False), file_name="completeness_report.csv", mime="text/csv")

    compliance_footer()


# ══════════════════════════════════════════════════════════════════════════════
# FEATURE 4 — CLASSIFICATION
# ══════════════════════════════════════════════════════════════════════════════
with t4:
    st.markdown("""
    <div class="sec-hd">
      <div class="sec-num" style="color:#854F0B;">04</div>
      <div><h2>SAE Classification &amp; Duplicate Detection</h2>
      <p>ICD-10 severity grading · Priority queue · Session-based duplicate detection across multiple reports</p></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="rc info">
    <b>Duplicate detection:</b> Upload multiple SAE reports — the system cross-checks patient IDs,
    drug names, and event signatures across all session files. Files exist in memory only and are
    cleared on browser close (DPDP compliant).
    </div>
    """, unsafe_allow_html=True)

    cf4 = st.file_uploader("Upload primary SAE report (DOCX/PDF/TXT)", type=["docx","pdf","txt"], key="class_up")
    if cf4:
        txt, err = extract_text(cf4)
        if err: st.error(err)
        elif txt.strip():
            st.session_state["class_text"] = txt; st.session_state["class_ta"] = txt
            st.session_state["dup_files"]["SAE-1"] = {"name":cf4.name,"text":txt}
            st.success(f"✓ Loaded: {cf4.name}")

    ci4 = st.text_area("Or paste SAE report text", height=180, key="class_ta",
        label_visibility="collapsed", placeholder="Paste SAE case narration here...")
    st.session_state["class_text"] = st.session_state.get("class_ta","")

    with st.expander("+ Add more SAE reports for duplicate detection", expanded=False):
        dc1, dc2 = st.columns(2)
        for idx, (slot, label) in enumerate([("SAE-2","SAE Report 2"),("SAE-3","SAE Report 3")]):
            with [dc1, dc2][idx]:
                f2 = st.file_uploader(label, type=["docx","pdf","txt"], key=f"dup_{slot}")
                if f2:
                    t2, e2 = extract_text(f2)
                    if not e2 and t2.strip():
                        st.session_state["dup_files"][slot] = {"name":f2.name,"text":t2}
                        st.success(f"✓ {f2.name}")
        if st.session_state["dup_files"]:
            st.info(f"Session files: {', '.join(v['name'] for v in st.session_state['dup_files'].values())}")
        if st.button("Clear all session files", key="clear_dup"):
            st.session_state["dup_files"] = {}; st.rerun()

    if st.button("Classify & Check Duplicates", type="primary", key="run_cls"):
        content = st.session_state["class_text"].strip()
        if not content:
            st.markdown('<div class="rc warn">Please upload or paste an SAE report first.</div>', unsafe_allow_html=True)
        else:
            tl = content.lower()
            if any(w in tl for w in ["died","fatal","death","mortality","deceased"]):
                sev="DEATH"; ps=1; rk=[w for w in ["died","fatal","death","mortality","deceased"] if w in tl]
            elif any(w in tl for w in ["permanent disability","paralysis","blind","deaf","permanent impairment"]):
                sev="DISABILITY"; ps=2; rk=[w for w in ["permanent disability","paralysis","blind","deaf"] if w in tl]
            elif any(w in tl for w in ["hospitalised","admitted","icu","inpatient","emergency","hospital"]):
                sev="HOSPITALISATION"; ps=3; rk=[w for w in ["hospitalised","admitted","icu","inpatient","emergency"] if w in tl]
            else:
                sev="OTHERS"; ps=4; rk=["no critical keywords — default classification"]

            SEV_COLORS = {
                "DEATH":"background:#FCEAEA;color:#8B2020;",
                "DISABILITY":"background:#FFF3E0;color:#974A00;",
                "HOSPITALISATION":"background:#FDF3EC;color:#854F0B;",
                "OTHERS":"background:#EAF3FB;color:#185FA5;",
            }
            conf = "HIGH" if len(rk)>=3 else "MEDIUM" if len(rk)>=1 else "LOW"
            icd = {"DEATH":"R96.x/R98/R99","DISABILITY":"S00-T98 (perm.)","HOSPITALISATION":"Z75.1","OTHERS":"MedDRA PT"}
            rpt = {"DEATH":"Expedited 7-day","DISABILITY":"Expedited 15-day","HOSPITALISATION":"Expedited 15-day","OTHERS":"Periodic 90-day"}
            _rm = {"DEATH":"Critical","DISABILITY":"High","HOSPITALISATION":"Medium","OTHERS":"Low"}
            _am = {
                "DEATH": "Expedited 7-day report mandatory. Immediate notification to DCGI and Ethics Committee.",
                "DISABILITY": "Expedited 15-day report required. Notify sponsor and Ethics Committee.",
                "HOSPITALISATION": "Expedited 15-day report required. Monitor outcome, submit follow-up.",
                "OTHERS": "Periodic reporting within 90 days. Document in safety database."
            }
            ai_card(f"SAE classified as {sev} · Confidence: {conf} · Priority: {ps}/4",
                _rm[sev], _am[sev], f"ICD-10: {icd[sev]} · Timeline: {rpt[sev]}")

            st.markdown(f'<div style="{SEV_COLORS[sev]}border-radius:8px;padding:10px 20px;font-size:18px;font-weight:700;display:inline-block;margin-bottom:12px;">⬤ {sev}</div>', unsafe_allow_html=True)
            c1cl,c2cl,c3cl = st.columns(3)
            c1cl.metric("Severity", sev); c2cl.metric("Confidence", conf); c3cl.metric("Priority Queue", f"{ps}/4")

            with st.expander("Classification Evidence", expanded=True):
                st.markdown(f'<div class="rc info"><b>Detected keywords:</b> {", ".join(rk)}<br><b>ICD-10:</b> {icd[sev]} · <b>Reporting:</b> {rpt[sev]}</div>', unsafe_allow_html=True)

            # Duplicate detection
            st.markdown("**Duplicate detection across session files**")
            def get_ids(t):
                ids = set(re.findall(r'\b(?:PT|SUBJ|LH|MH|DL)[-]\w+[-]\w+\b', t))
                drugs = set(re.findall(r'\b[A-Z][a-z]+(?:vir|mab|nib|tide|pril|sartan|statin|mycin|cillin)\b', t))
                drugs |= set(re.findall(r'\b[A-Z]{4,}[-]?\d*\s*mg\b', t))
                return ids, drugs

            id1, dr1 = get_ids(content); dup_found = False
            all_files = st.session_state["dup_files"]
            if len(all_files) > 1:
                for k, v in all_files.items():
                    if v["text"].strip() == content.strip(): continue
                    id2, dr2 = get_ids(v["text"])
                    shared_ids = id1 & id2; shared_drugs = dr1 & dr2
                    if shared_ids or shared_drugs:
                        detail = []
                        if shared_ids: detail.append(f"Patient IDs: {shared_ids}")
                        if shared_drugs: detail.append(f"Drugs: {shared_drugs}")
                        st.markdown(f'<div class="rc err">⚠️ DUPLICATE DETECTED — matches <b>{v["name"]}</b> · {" · ".join(detail)}</div>', unsafe_allow_html=True)
                        dup_found = True
                if not dup_found:
                    st.markdown('<div class="rc ok">✓ No duplicates found across session files.</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="rc info">Add more SAE reports above to enable cross-session duplicate checking.</div>', unsafe_allow_html=True)

            st.download_button("⬇ Download Classification Report",
                f"Severity:{sev}\nConfidence:{conf}\nKeywords:{', '.join(rk)}\nPriority:{ps}/4\nICD-10:{icd[sev]}\nTimeline:{rpt[sev]}",
                file_name="classification_report.txt")

    compliance_footer()


# ══════════════════════════════════════════════════════════════════════════════
# FEATURE 5 — COMPARISON
# ══════════════════════════════════════════════════════════════════════════════
with t5:
    st.markdown("""
    <div class="sec-hd">
      <div class="sec-num" style="color:#3B6D11;">05</div>
      <div><h2>Document Comparison</h2>
      <p>Upload two dossier versions · Substantive vs administrative diff · Critical / Moderate / Cosmetic triage · Downloadable report</p></div>
    </div>
    """, unsafe_allow_html=True)

    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.markdown("**Version 1 — Original**")
        v1f = st.file_uploader("Upload V1", type=["docx","pdf","txt"], key="v1f")
        if v1f:
            t, e = extract_text(v1f)
            if not e and t.strip():
                st.session_state["v1_text"] = t; st.session_state["v1ta"] = t
                st.success(f"✓ {v1f.name}")
        v1 = st.text_area("Or paste V1", height=180, key="v1ta",
            label_visibility="collapsed", placeholder="Paste original document text...")
        st.session_state["v1_text"] = st.session_state.get("v1ta","")

    with col_v2:
        st.markdown("**Version 2 — Revised**")
        v2f = st.file_uploader("Upload V2", type=["docx","pdf","txt"], key="v2f")
        if v2f:
            t, e = extract_text(v2f)
            if not e and t.strip():
                st.session_state["v2_text"] = t; st.session_state["v2ta"] = t
                st.success(f"✓ {v2f.name}")
        v2 = st.text_area("Or paste V2", height=180, key="v2ta",
            label_visibility="collapsed", placeholder="Paste revised document text...")
        st.session_state["v2_text"] = st.session_state.get("v2ta","")

    if st.button("Compare Documents", type="primary", key="run_c5"):
        t1c = st.session_state["v1_text"].strip()
        t2c = st.session_state["v2_text"].strip()
        if not t1c or not t2c:
            st.markdown('<div class="rc warn">Please provide both document versions.</div>', unsafe_allow_html=True)
        else:
            l1 = [l.strip() for l in t1c.splitlines() if l.strip()]
            l2 = [l.strip() for l in t2c.splitlines() if l.strip()]
            SK = ["dose","dosage","mg","ml","death","disability","outcome","causality","adverse","event",
                  "date","patient","diagnosis","icd","treatment","safety","efficacy","result","risk","fatal","serious"]

            changes = []
            for tag,i1,i2,j1,j2 in difflib.SequenceMatcher(None,l1,l2).get_opcodes():
                if tag == "replace":
                    for o,n in zip(l1[i1:i2],l2[j1:j2]):
                        s = any(k in o.lower() or k in n.lower() for k in SK)
                        changes.append({"Type":"CHANGED","Original":o,"New":n,"Substantive":"Yes" if s else "No"})
                elif tag == "delete":
                    for line in l1[i1:i2]:
                        changes.append({"Type":"REMOVED","Original":line,"New":"—","Substantive":"Yes" if any(k in line.lower() for k in SK) else "No"})
                elif tag == "insert":
                    for line in l2[j1:j2]:
                        changes.append({"Type":"ADDED","Original":"—","New":line,"Substantive":"Yes" if any(k in line.lower() for k in SK) else "No"})

            sc = sum(1 for c in changes if c["Substantive"]=="Yes")
            similarity = round(difflib.SequenceMatcher(None,t1c,t2c).ratio()*100, 1)

            c1cp,c2cp,c3cp,c4cp,c5cp = st.columns(5)
            c1cp.metric("Similarity",f"{similarity}%"); c2cp.metric("Total Changes",len(changes))
            c3cp.metric("Added",sum(1 for c in changes if c["Type"]=="ADDED"))
            c4cp.metric("Removed",sum(1 for c in changes if c["Type"]=="REMOVED"))
            c5cp.metric("Substantive",sc)

            _cr5 = "High" if sc>=3 else "Medium" if sc>=1 else "Low"
            _ca5 = (f"{sc} substantive change(s) affect regulatory parameters. Formal review and possible amended submission required."
                    if sc > 0 else "No substantive changes. Administrative edits only. Document may proceed.")
            ai_card(f"{len(changes)} total · {sc} substantive · {len(changes)-sc} administrative",
                _cr5, _ca5,
                "Substantive changes affect dosage, safety, outcomes, or patient information.")

            cc5 = "err" if sc>0 else "ok"
            st.markdown(f'<div class="rc {cc5}">{"⚠️ "+str(sc)+" substantive change(s) — regulatory review required." if sc>0 else "✓ No substantive changes detected."}</div>', unsafe_allow_html=True)

            # Categorised view
            if changes:
                tab_crit5, tab_all5 = st.tabs([f"Substantive changes ({sc})", "All changes"])
                with tab_crit5:
                    subst = [c for c in changes if c["Substantive"]=="Yes"]
                    if subst:
                        for c in subst:
                            st.markdown(f"""
                            <div class="diff-critical">
                              <div style="font-weight:600;margin-bottom:3px;">{c['Type']}</div>
                              {"<div style='color:#8B2020;font-size:12px;'>Removed: "+c['Original']+"</div>" if c['Original'] != '—' else ""}
                              {"<div style='color:#1A6B52;font-size:12px;'>Added: "+c['New']+"</div>" if c['New'] != '—' else ""}
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.success("✓ No substantive changes")

                with tab_all5:
                    df5 = pd.DataFrame(changes)
                    def sd5(row):
                        if row["Type"]=="ADDED": return ["background-color:#EBF6F2"]*len(row)
                        if row["Type"]=="REMOVED": return ["background-color:#FCEAEA"]*len(row)
                        if row["Substantive"]=="Yes": return ["background-color:#FDF3EC"]*len(row)
                        return [""]*len(row)
                    st.dataframe(df5.style.apply(sd5,axis=1), use_container_width=True, hide_index=True)
                    st.caption("🟢 Added · 🔴 Removed · 🟡 Changed (Substantive)")

                st.download_button("⬇ Download Comparison Report",
                    df5.to_csv(index=False), file_name="comparison_report.csv", mime="text/csv")

    compliance_footer()


# ══════════════════════════════════════════════════════════════════════════════
# FEATURE 6 — INSPECTION REPORT
# ══════════════════════════════════════════════════════════════════════════════
with t6:
    st.markdown("""
    <div class="sec-hd">
      <div class="sec-num" style="color:#993556;">06</div>
      <div><h2>Inspection Report Generation</h2>
      <p>Raw observations → formal CDSCO GCP report · Critical / Major / Minor risk grading · CAPA timelines</p></div>
    </div>
    """, unsafe_allow_html=True)

    c1i,c2i,c3i,c4i = st.columns(4)
    with c1i: insp_name = st.text_input("Inspector Name", placeholder="Dr. A.K. Sharma")
    with c2i: insp_site = st.text_input("Site Name", placeholder="AIIMS Delhi")
    with c3i: insp_sno  = st.text_input("Site Number", placeholder="SITE-DEL-001")
    with c4i: insp_date = st.date_input("Inspection Date")

    insp_type = st.selectbox("Inspection type", ["GCP","GMP","GDP","GLP"])

    obs = st.text_area("Raw observations — one per line", height=200, key="obs_ta",
        placeholder="No record of drug accountability for subjects 3 and 7\nInformed consent missing local language version\nMinor labelling error on storage box")

    if st.button("Generate Inspection Report", type="primary", key="run_insp"):
        if not obs.strip():
            st.markdown('<div class="rc warn">Please enter at least one observation.</div>', unsafe_allow_html=True)
        else:
            obs_list = [o.strip() for o in obs.splitlines() if o.strip()]
            CK = ["no record","falsified","patient safety","data integrity","unaccounted","fraud","fabricat","unreported"]
            MK = ["incomplete","not documented","protocol deviation","untrained","not signed","not dated","expired","missing"]
            rows6 = []
            for i, ob in enumerate(obs_list, 1):
                ol = ob.lower()
                if any(k in ol for k in CK):
                    risk="Critical"; dl="15 days"; ca="Immediate CAPA. Site may be suspended. Report to DCGI within 15 days."
                elif any(k in ol for k in MK):
                    risk="Major"; dl="30 days"; ca="Submit CAPA plan within 30 days."
                else:
                    risk="Minor"; dl="60 days"; ca="Document in site log within 60 days."
                formal = (f"During inspection on {insp_date.strftime('%d %B %Y')}, it was observed that "
                          f"{ob.lower().rstrip('.')}. This constitutes a {risk.lower()} {insp_type} deviation.")
                rows6.append({
                    "Obs": f"OBS-{i:03d}","Raw Observation":ob,
                    "Formal Finding":formal,"Risk Level":risk,
                    "Corrective Action":ca,"CAPA Deadline":dl
                })

            cc_n = sum(1 for r in rows6 if r["Risk Level"]=="Critical")
            mc_n = sum(1 for r in rows6 if r["Risk Level"]=="Major")
            mn_n = sum(1 for r in rows6 if r["Risk Level"]=="Minor")

            c1r,c2r,c3r = st.columns(3)
            c1r.metric("Critical",cc_n); c2r.metric("Major",mc_n); c3r.metric("Minor",mn_n)

            overall = ("Unsatisfactory" if cc_n>0 else "Acceptable with conditions" if mc_n>0 else "Satisfactory")
            overall_css = "err" if cc_n>0 else "warn" if mc_n>0 else "ok"
            _ri = "Critical" if cc_n>0 else "High" if mc_n>0 else "Low"
            _ai = (f"{cc_n} Critical {insp_type} deviation(s). Immediate CAPA. Site may be suspended. Report to DCGI within 15 days."
                   if cc_n>0 else f"{mc_n} Major deviation(s). CAPA within 30 days."
                   if mc_n>0 else f"No Critical/Major findings. {mn_n} Minor deviation(s) to document within 60 days.")

            ai_card(f"Inspection outcome: {cc_n} Critical · {mc_n} Major · {mn_n} Minor",
                _ri, _ai, f"Site: {insp_site or '[Site]'} · {insp_date.strftime('%d %B %Y')} · Inspector: {insp_name or '[Inspector]'}")

            st.markdown(f'<div class="rc {overall_css}"><b>Overall classification:</b> {overall}</div>', unsafe_allow_html=True)

            df6 = pd.DataFrame(rows6)
            def sr6(v):
                if v=="Critical": return "background-color:#FCEAEA;color:#8B2020;font-weight:700"
                if v=="Major":    return "background-color:#FDF3EC;color:#854F0B;font-weight:700"
                if v=="Minor":    return "background-color:#EBF6F2;color:#1A6B52"
                return ""
            with st.expander("Full Inspection Report", expanded=True):
                st.dataframe(df6.style.map(sr6, subset=["Risk Level"]),
                    use_container_width=True, hide_index=True)

            full = (
                f"CENTRAL DRUGS STANDARD CONTROL ORGANISATION\n"
                f"{'='*60}\n"
                f"SITE INSPECTION REPORT — {insp_type}\n"
                f"{'='*60}\n"
                f"Site Name   : {insp_site}\n"
                f"Site Number : {insp_sno}\n"
                f"Date        : {insp_date.strftime('%d %B %Y')}\n"
                f"Inspector   : {insp_name}\n"
                f"Summary     : {cc_n} Critical | {mc_n} Major | {mn_n} Minor\n"
                f"Classification: {overall}\n"
                f"{'='*60}\n\n"
            )
            for r in rows6:
                full += (f"{r['Obs']} | {r['Risk Level'].upper()}\n"
                         f"Finding  : {r['Formal Finding']}\n"
                         f"Action   : {r['Corrective Action']}\n"
                         f"Deadline : {r['CAPA Deadline']}\n"
                         f"{'-'*60}\n\n")
            full += (f"Inspector Signature: ___________________\n"
                     f"Date: {datetime.date.today()}\n"
                     f"{'='*60}\n"
                     f"Generated by Nirnay v1.0 — CDSCO AI Review System")

            dl6a, dl6b = st.columns(2)
            with dl6a:
                st.download_button("⬇ Download Inspection Report (TXT)", full,
                    file_name=f"CDSCO_{insp_type}_Inspection_Report.txt", mime="text/plain",
                    use_container_width=True)
            with dl6b:
                st.download_button("⬇ Download Report Data (CSV)",
                    df6.to_csv(index=False),
                    file_name=f"CDSCO_{insp_type}_Inspection_Data.csv", mime="text/csv",
                    use_container_width=True)

    compliance_footer()
