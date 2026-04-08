import streamlit as st
import re
import datetime
import difflib
import pandas as pd

st.set_page_config(
    page_title="CDSCO Regulatory Intelligence Platform",
    page_icon="🏥",
    layout="wide"
)

st.markdown("""
<style>
    .main-header {
        background-color: #003087;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    .main-header h1 {
        color: white;
        font-size: 24px;
        margin: 0;
        font-family: Arial, sans-serif;
    }
    .main-header p {
        color: #9FE1CB;
        margin: 4px 0 0 0;
        font-size: 14px;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 13px;
        font-weight: 500;
    }
    .audit-box {
        background: #f0f4fa;
        border-left: 4px solid #003087;
        padding: 10px 14px;
        border-radius: 4px;
        font-size: 13px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
<h1>CDSCO Regulatory Intelligence Platform</h1>
<p>AI-powered regulatory workflow automation | Stage 1 Demo</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### Compliance")
    st.success("DPDP Act 2023")
    st.success("ICMR Guidelines 2017")
    st.success("CDSCO Schedule Y")
    st.success("MeitY AI Ethics")
    st.markdown("---")
    st.caption("This tool assists regulatory officers. All final decisions must be made by qualified human reviewers.")
    st.markdown("---")
    st.caption("Public datasets: FDA FAERS · CDSCO Forms · ClinicalTrials.gov · CTRI")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "1. Anonymisation",
    "2. Summarisation",
    "3. Completeness Check",
    "4. Classification",
    "5. Document Comparison",
    "6. Inspection Report"
])

# ─────────────────────────────────────────────
# FEATURE 1 — ANONYMISATION
# ─────────────────────────────────────────────
with tab1:
    st.subheader("AI-Powered Data Anonymisation")
    st.caption("Two-step process: Pseudonymisation → Irreversible Anonymisation | Compliant with DPDP Act 2023")

    input_text = st.text_area("Paste regulatory document content here", height=280,
        placeholder="Paste SAE report, clinical trial document, or any regulatory text...")

    col1, col2 = st.columns([1, 3])
    with col1:
        run_anon = st.button("Run Anonymisation", type="primary", use_container_width=True)

    if run_anon and input_text.strip():
        st.markdown("---")

        INDIAN_FIRST = ["Rajesh","Priya","Suresh","Anita","Vikram","Sunita","Amit","Kavita",
                        "Ravi","Deepa","Mohit","Pooja","Arjun","Neha","Sanjay","Meera",
                        "Rahul","Divya","Anil","Rekha","Vijay","Smita","Ramesh","Geeta",
                        "Ashok","Usha","Manoj","Seema","Vinod","Lata"]
        INDIAN_LAST  = ["Sharma","Patel","Singh","Kumar","Mehta","Gupta","Verma","Joshi",
                        "Nair","Rao","Iyer","Reddy","Bose","Das","Malhotra","Kapoor",
                        "Agarwal","Pandey","Mishra","Tiwari"]

        token_map   = []
        audit_log   = []
        processed   = input_text
        counters    = {"PATIENT":0,"INVESTIGATOR":0,"DATE":0,"SITE":0,"ID":0,
                       "PHONE":0,"AADHAAR":0,"ADDRESS":0}
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        def next_token(kind):
            counters[kind] += 1
            return f"[{kind}-{counters[kind]:03d}]"

        # Aadhaar
        aadhaar_re = re.compile(r'\b\d{4}[-\s]\d{4}[-\s]\d{4}\b')
        for m in aadhaar_re.finditer(processed):
            tok = next_token("AADHAAR")
            token_map.append({"Token":tok,"Original Value":m.group(),"Entity Type":"Aadhaar Number","Step":"Step 1"})
            audit_log.append({"Timestamp":ts,"Action":"Pseudonymised","Entity Type":"Aadhaar","Token":tok,"Reversible":"Yes"})
            processed = processed.replace(m.group(), tok, 1)

        # Phone
        phone_re = re.compile(r'\b[6-9]\d{9}\b')
        for m in phone_re.finditer(processed):
            tok = next_token("PHONE")
            token_map.append({"Token":tok,"Original Value":m.group(),"Entity Type":"Phone Number","Step":"Step 1"})
            audit_log.append({"Timestamp":ts,"Action":"Pseudonymised","Entity Type":"Phone","Token":tok,"Reversible":"Yes"})
            processed = processed.replace(m.group(), tok, 1)

        # Structured IDs
        id_re = re.compile(r'\b(PT|SITE|IND|CT|SUBJ|INV)[-]\w+[-]\w+\b')
        for m in id_re.finditer(processed):
            original = m.group()
            if original.startswith("PT") or original.startswith("SUBJ"):
                tok = next_token("PATIENT")
                etype = "Patient ID"
            elif original.startswith("SITE"):
                tok = next_token("SITE")
                etype = "Site Number"
            elif original.startswith("INV"):
                tok = next_token("INVESTIGATOR")
                etype = "Investigator ID"
            else:
                tok = next_token("ID")
                etype = "Regulatory ID"
            token_map.append({"Token":tok,"Original Value":original,"Entity Type":etype,"Step":"Step 1"})
            audit_log.append({"Timestamp":ts,"Action":"Pseudonymised","Entity Type":etype,"Token":tok,"Reversible":"Yes"})
            processed = processed.replace(original, tok, 1)

        # Dates
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

        # Indian names
        name_re = re.compile(r'\b(?:Dr\.?\s+)?(' + '|'.join(INDIAN_FIRST) + r')\s+(?:\w+\s+)?(' + '|'.join(INDIAN_LAST) + r')\b')
        for m in name_re.finditer(processed):
            full_name = m.group()
            if "Dr" in full_name or "Dr." in full_name:
                tok = next_token("INVESTIGATOR")
                etype = "Investigator Name"
            else:
                tok = next_token("PATIENT")
                etype = "Patient Name"
            token_map.append({"Token":tok,"Original Value":full_name,"Entity Type":etype,"Step":"Step 1"})
            audit_log.append({"Timestamp":ts,"Action":"Pseudonymised","Entity Type":etype,"Token":tok,"Reversible":"Yes"})
            processed = processed.replace(full_name, tok, 1)

        st.success("Step 1 Complete — Pseudonymisation")
        st.text_area("Step 1 Output (Pseudonymised)", processed, height=180)

        if token_map:
            st.markdown("**Token Mapping Table**")
            df_tokens = pd.DataFrame(token_map)
            st.dataframe(df_tokens, use_container_width=True, hide_index=True)
        else:
            st.info("No PII/PHI patterns detected in this text.")

        # STEP 2 — Irreversible Anonymisation
        step2 = processed
        age_re = re.compile(r'\b(\d{2})\s*(?:years?|yrs?)\s*(?:old)?\b', re.IGNORECASE)
        def age_range(m):
            age = int(m.group(1))
            low = (age // 5) * 5
            return f"{low}-{low+4} years"
        step2 = age_re.sub(age_range, step2)

        date_tok_re = re.compile(r'\[DATE-\d+\]')
        step2 = date_tok_re.sub('[YEAR-GENERALISED]', step2)

        weight_re = re.compile(r'\b(\d{2,3})\s*kg\b', re.IGNORECASE)
        def weight_range(m):
            w = int(m.group(1))
            low = (w // 10) * 10
            return f"{low}-{low+9} kg"
        step2 = weight_re.sub(weight_range, step2)

        audit_log.append({"Timestamp":ts,"Action":"Irreversible Generalisation","Entity Type":"All Dates","Token":"[YEAR-GENERALISED]","Reversible":"No"})
        audit_log.append({"Timestamp":ts,"Action":"Irreversible Generalisation","Entity Type":"Ages","Token":"Age Range","Reversible":"No"})
        audit_log.append({"Timestamp":ts,"Action":"Irreversible Generalisation","Entity Type":"Weight","Token":"Weight Range","Reversible":"No"})

        st.success("Step 2 Complete — Irreversible Anonymisation")
        st.text_area("Step 2 Output (Final Anonymised)", step2, height=180)

        st.markdown("**Audit Log**")
        df_audit = pd.DataFrame(audit_log)
        st.dataframe(df_audit, use_container_width=True, hide_index=True)

        download_text = f"=== STEP 1: PSEUDONYMISED ===\n{processed}\n\n=== STEP 2: FINAL ANONYMISED ===\n{step2}\n\n=== TOKEN MAP ===\n{pd.DataFrame(token_map).to_string()}\n\n=== AUDIT LOG ===\n{df_audit.to_string()}"
        st.download_button("Download Anonymisation Report", download_text, file_name="anonymisation_report.txt", mime="text/plain")

    elif run_anon:
        st.warning("Please paste some document content first.")


# ─────────────────────────────────────────────
# FEATURE 2 — SUMMARISATION
# ─────────────────────────────────────────────
with tab2:
    st.subheader("Document Summarisation")
    st.caption("Handles three source types: SAE Case Narration | Application Checklist | Meeting Transcript")

    doc_type = st.selectbox("Select document type", ["SAE Case Narration","Application Checklist (SUGAM)","Meeting Transcript / Audio Transcript"])
    sum_input = st.text_area("Paste document content", height=280)
    run_sum = st.button("Summarise Document", type="primary")

    if run_sum and sum_input.strip():
        text = sum_input.lower()
        st.markdown("---")

        if doc_type == "SAE Case Narration":
            priority = "URGENT" if any(w in text for w in ["death","fatal","died","disability","permanent"]) else \
                       "STANDARD" if any(w in text for w in ["hospitalised","admitted","icu","inpatient"]) else "LOW"
            priority_color = "🔴" if priority=="URGENT" else "🟡" if priority=="STANDARD" else "🟢"

            causality = "Possibly Related" if "possibly" in text else \
                        "Probably Related" if "probably" in text else \
                        "Unrelated" if "unrelated" in text else \
                        "Definitely Related" if "definitely" in text else "Under Assessment"

            outcome = "Fatal" if any(w in text for w in ["died","death","fatal"]) else \
                      "Recovering" if any(w in text for w in ["recovering","improving"]) else \
                      "Recovered" if "recovered" in text else \
                      "Ongoing" if "ongoing" in text else "Unknown"

            st.markdown(f"### {priority_color} SAE Summary — Priority: {priority}")

            c1, c2, c3 = st.columns(3)
            c1.metric("Causality", causality)
            c2.metric("Outcome", outcome)
            c3.metric("Priority", priority)

            st.markdown("**Structured Summary**")
            st.markdown(f"""
| Field | Extracted Value |
|---|---|
| Document Type | SAE Case Narration |
| Causality Assessment | {causality} |
| Patient Outcome | {outcome} |
| Review Priority | {priority} |
| Reportability | Expedited (15-day) if serious |
| Recommended Action | {'Immediate escalation to DCGI' if priority=='URGENT' else 'Standard review queue'} |
            """)
            st.download_button("Download SAE Summary", f"SAE Summary\nCausality: {causality}\nOutcome: {outcome}\nPriority: {priority}", file_name="sae_summary.txt")

        elif doc_type == "Application Checklist (SUGAM)":
            lines = [l.strip() for l in sum_input.split('\n') if l.strip()]
            complete = sum(1 for l in lines if any(w in l.lower() for w in ["complete","present","yes","submitted","available","provided"]))
            missing  = sum(1 for l in lines if any(w in l.lower() for w in ["missing","absent","no","not submitted","not provided"]))
            incomplete = sum(1 for l in lines if any(w in l.lower() for w in ["incomplete","pending","partial","to be"]))
            total = len(lines)
            score = round((complete/total)*100) if total else 0

            rec = "Approve for Review" if score>=80 else "Return for Completion" if score>=50 else "Reject — Critical gaps"

            st.markdown("### Completeness Summary")
            c1,c2,c3,c4 = st.columns(4)
            c1.metric("Total Items", total)
            c2.metric("Complete", complete, delta=None)
            c3.metric("Incomplete", incomplete)
            c4.metric("Missing", missing)
            st.progress(score/100, text=f"Completeness Score: {score}%")
            st.info(f"**Recommendation:** {rec}")
            st.download_button("Download Checklist Summary", f"Total:{total}\nComplete:{complete}\nMissing:{missing}\nScore:{score}%\nRecommendation:{rec}", file_name="checklist_summary.txt")

        else:  # Meeting transcript
            lines = sum_input.split('\n')
            decisions, actions, issues = [], [], []
            for line in lines:
                ll = line.lower()
                if any(w in ll for w in ["decided","approved","resolved","agreed","concluded"]):
                    decisions.append(line.strip())
                elif any(w in ll for w in ["action","will","shall","to be done","responsible","owner","follow up"]):
                    actions.append(line.strip())
                elif any(w in ll for w in ["pending","unresolved","defer","tabled","next meeting"]):
                    issues.append(line.strip())

            st.markdown("### Meeting Summary")
            st.markdown(f"**Key Decisions ({len(decisions)} found)**")
            for i,d in enumerate(decisions[:5],1):
                st.markdown(f"{i}. {d}")
            st.markdown(f"**Action Items ({len(actions)} found)**")
            for i,a in enumerate(actions[:6],1):
                st.markdown(f"{i}. {a}")
            if issues:
                st.markdown(f"**Unresolved Issues ({len(issues)} found)**")
                for i,x in enumerate(issues[:4],1):
                    st.markdown(f"{i}. {x}")
            st.download_button("Download Meeting Summary", f"Decisions:\n"+"\n".join(decisions)+"\n\nActions:\n"+"\n".join(actions), file_name="meeting_summary.txt")
    elif run_sum:
        st.warning("Please paste document content first.")


# ─────────────────────────────────────────────
# FEATURE 3 — COMPLETENESS ASSESSMENT
# ─────────────────────────────────────────────
with tab3:
    st.subheader("Completeness Assessment — Schedule Y Verification")
    st.caption("Checks against mandatory CDSCO Schedule Y fields for clinical trial applications")

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

    comp_input = st.text_area("Paste application checklist or document index", height=250)

    col_a, col_b = st.columns(2)
    with col_a:
        app_id = st.text_input("Application ID (optional)", placeholder="e.g. SUGAM-CT-2024-0892")
    run_comp = st.button("Run Completeness Check", type="primary")

    if run_comp and comp_input.strip():
        text_lower = comp_input.lower()
        results = []
        critical_missing, major_missing = [], []

        for field, keyword, severity in SCHEDULE_Y:
            if keyword in text_lower:
                if any(w in text_lower for w in ["pending","to be submitted","not applicable","tbd","partial"]):
                    status = "INCOMPLETE"; rag = "🟡 Amber"
                else:
                    status = "PRESENT"; rag = "🟢 Green"
            else:
                status = "MISSING"; rag = "🔴 Red"
                if severity == "Critical": critical_missing.append(field)
                elif severity == "Major":  major_missing.append(field)
            results.append({"Field": field, "Severity": severity, "Status": status, "RAG": rag})

        df_comp = pd.DataFrame(results)
        total    = len(results)
        present  = sum(1 for r in results if r["Status"]=="PRESENT")
        incomplete = sum(1 for r in results if r["Status"]=="INCOMPLETE")
        missing  = sum(1 for r in results if r["Status"]=="MISSING")
        score    = round((present/total)*100)

        st.markdown(f"### Completeness Report{' — ' + app_id if app_id else ''}")
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Total Fields", total)
        c2.metric("Present", present)
        c3.metric("Incomplete", incomplete)
        c4.metric("Missing", missing)
        st.progress(score/100, text=f"Schedule Y Completeness: {score}%")

        rec = "✅ Approve for Technical Review" if score>=85 and not critical_missing else \
              "⚠️ Return for Completion" if score>=60 else "❌ Reject — Critical fields missing"
        st.markdown(f"**Recommendation:** {rec}")

        if critical_missing:
            st.error(f"Critical missing fields: {', '.join(critical_missing)}")
        if major_missing:
            st.warning(f"Major missing fields: {', '.join(major_missing)}")

        st.markdown("**Full Field Status**")

        def style_rag(val):
            if "Green" in str(val): return "background-color: #d4edda; color: #155724"
            if "Amber" in str(val): return "background-color: #fff3cd; color: #856404"
            if "Red"   in str(val): return "background-color: #f8d7da; color: #721c24"
            return ""

        styled = df_comp.style.applymap(style_rag, subset=["RAG"])
        st.dataframe(styled, use_container_width=True, hide_index=True)
        st.download_button("Download Completeness Report", df_comp.to_csv(index=False), file_name="completeness_report.csv", mime="text/csv")
    elif run_comp:
        st.warning("Please paste application content first.")


# ─────────────────────────────────────────────
# FEATURE 4 — CLASSIFICATION
# ─────────────────────────────────────────────
with tab4:
    st.subheader("SAE Classification & Prioritisation")
    st.caption("Severity classification | Duplicate detection | Officer review queue")

    class_input = st.text_area("Paste SAE report for classification", height=220)

    st.markdown("**Duplicate Detection** — paste additional SAE reports (optional)")
    dup2 = st.text_area("SAE Report 2 (optional)", height=100)
    dup3 = st.text_area("SAE Report 3 (optional)", height=100)

    run_class = st.button("Classify Case", type="primary")

    if run_class and class_input.strip():
        text = class_input.lower()

        # Severity classification
        if any(w in text for w in ["died","fatal","death","mortality","deceased"]):
            severity = "DEATH"; sev_color = "🔴"; priority_score = 1
            reason_keywords = [w for w in ["died","fatal","death","mortality","deceased"] if w in text]
        elif any(w in text for w in ["permanent disability","paralysis","blind","deaf","unable to work permanently","permanent impairment"]):
            severity = "DISABILITY"; sev_color = "🟠"; priority_score = 2
            reason_keywords = [w for w in ["permanent disability","paralysis","blind","deaf"] if w in text]
        elif any(w in text for w in ["hospitalised","admitted","icu","inpatient","emergency admission","hospital"]):
            severity = "HOSPITALISATION"; sev_color = "🟡"; priority_score = 3
            reason_keywords = [w for w in ["hospitalised","admitted","icu","inpatient","hospital"] if w in text]
        else:
            severity = "OTHERS"; sev_color = "🔵"; priority_score = 4
            reason_keywords = ["no critical keywords matched"]

        keyword_count = len(reason_keywords)
        confidence = "HIGH" if keyword_count >= 3 else "MEDIUM" if keyword_count >= 1 else "LOW"

        st.markdown(f"### {sev_color} Classification: {severity}")
        c1,c2,c3 = st.columns(3)
        c1.metric("Severity", severity)
        c2.metric("Confidence", confidence)
        c3.metric("Priority Score", f"{priority_score} / 4")

        st.info(f"**Reason:** Classified as {severity} because the following keywords were found in the event description: {', '.join(reason_keywords)}.")

        icd_map = {"DEATH":"R96.x / R98 / R99","DISABILITY":"S00-T98 (permanent)","HOSPITALISATION":"Z75.1 / Hospital admission codes","OTHERS":"Refer to MedDRA PT"}
        report_map = {"DEATH":"Expedited — 7 days (fatal)","DISABILITY":"Expedited — 15 days","HOSPITALISATION":"Expedited — 15 days","OTHERS":"Periodic — 90 days"}

        st.markdown(f"""
| Classification Detail | Value |
|---|---|
| Severity Category | {severity} |
| Applicable ICD-10 | {icd_map[severity]} |
| CDSCO Reporting Timeline | {report_map[severity]} |
| Confidence Level | {confidence} ({keyword_count} keywords matched) |
| Officer Priority Queue | Position {priority_score} (1=highest) |
        """)

        # Duplicate detection
        st.markdown("---")
        st.markdown("**Duplicate Detection Result**")

        def extract_ids(text):
            ids = re.findall(r'\b(?:PT|SUBJ)[-]\w+[-]\w+\b', text)
            drugs = re.findall(r'\b[A-Z]{4,}[-]?\d+\s*mg\b', text)
            dates = re.findall(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', text)
            return set(ids), set(drugs), set(dates)

        id1,d1,dt1 = extract_ids(class_input)
        duplicates_found = False

        for i, other in enumerate([dup2, dup3], 2):
            if other.strip():
                id2,d2,dt2 = extract_ids(other)
                id_match   = bool(id1 & id2)
                drug_match = bool(d1 & d2)
                if id_match or drug_match:
                    st.error(f"DUPLICATE DETECTED — Report {i} shares {'Patient ID: '+str(id1&id2) if id_match else ''} {'Drug: '+str(d1&d2) if drug_match else ''} with Report 1.")
                    duplicates_found = True

        if not duplicates_found:
            st.success("NO DUPLICATE DETECTED across provided reports.")

        result_text = f"Severity: {severity}\nConfidence: {confidence}\nReason: {', '.join(reason_keywords)}\nPriority Score: {priority_score}/4\nICD-10: {icd_map[severity]}\nReporting Timeline: {report_map[severity]}"
        st.download_button("Download Classification Report", result_text, file_name="classification_report.txt")
    elif run_class:
        st.warning("Please paste an SAE report first.")


# ─────────────────────────────────────────────
# FEATURE 5 — DOCUMENT COMPARISON
# ─────────────────────────────────────────────
with tab5:
    st.subheader("Document Comparison")
    st.caption("Identifies substantive and administrative changes between document versions")

    col_v1, col_v2 = st.columns(2)
    with col_v1:
        v1 = st.text_area("Version 1 — Original Document", height=250)
    with col_v2:
        v2 = st.text_area("Version 2 — Updated Document", height=250)

    run_comp5 = st.button("Compare Documents", type="primary")

    if run_comp5 and v1.strip() and v2.strip():
        lines1 = [l.strip() for l in v1.splitlines() if l.strip()]
        lines2 = [l.strip() for l in v2.splitlines() if l.strip()]

        matcher = difflib.SequenceMatcher(None, lines1, lines2)
        changes = []

        SUBSTANTIVE_KEYWORDS = ["dose","dosage","mg","ml","death","disability","outcome","causality",
                                 "adverse","event","date","patient","diagnosis","icd","treatment",
                                 "safety","efficacy","result","conclusion","risk","benefit"]

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == "replace":
                for old, new in zip(lines1[i1:i2], lines2[j1:j2]):
                    is_sub = any(k in old.lower() or k in new.lower() for k in SUBSTANTIVE_KEYWORDS)
                    changes.append({"Change Type":"CHANGED","Original Text":old,"New Text":new,
                                    "Substantive":("Yes" if is_sub else "No"),
                                    "Category":("Substantive" if is_sub else "Administrative")})
            elif tag == "delete":
                for line in lines1[i1:i2]:
                    is_sub = any(k in line.lower() for k in SUBSTANTIVE_KEYWORDS)
                    changes.append({"Change Type":"REMOVED","Original Text":line,"New Text":"—",
                                    "Substantive":("Yes" if is_sub else "No"),
                                    "Category":("Substantive" if is_sub else "Administrative")})
            elif tag == "insert":
                for line in lines2[j1:j2]:
                    is_sub = any(k in line.lower() for k in SUBSTANTIVE_KEYWORDS)
                    changes.append({"Change Type":"ADDED","Original Text":"—","New Text":line,
                                    "Substantive":("Yes" if is_sub else "No"),
                                    "Category":("Substantive" if is_sub else "Administrative")})

        st.markdown("### Comparison Report")
        sub_count   = sum(1 for c in changes if c["Substantive"]=="Yes")
        admin_count = sum(1 for c in changes if c["Substantive"]=="No")
        added   = sum(1 for c in changes if c["Change Type"]=="ADDED")
        removed = sum(1 for c in changes if c["Change Type"]=="REMOVED")
        changed = sum(1 for c in changes if c["Change Type"]=="CHANGED")

        c1,c2,c3,c4,c5 = st.columns(5)
        c1.metric("Total Changes", len(changes))
        c2.metric("Added", added)
        c3.metric("Removed", removed)
        c4.metric("Changed", changed)
        c5.metric("Substantive", sub_count)

        if sub_count > 0:
            st.error(f"{sub_count} substantive change(s) detected — require regulatory review.")
        else:
            st.success("No substantive changes detected.")

        if changes:
            df_diff = pd.DataFrame(changes)

            def style_diff(row):
                if row["Change Type"] == "ADDED":   return ["background-color:#d4edda"]*len(row)
                if row["Change Type"] == "REMOVED": return ["background-color:#f8d7da"]*len(row)
                if row["Substantive"] == "Yes":     return ["background-color:#fff3cd"]*len(row)
                return [""]*len(row)

            styled_diff = df_diff.style.apply(style_diff, axis=1)
            st.dataframe(styled_diff, use_container_width=True, hide_index=True)
            st.caption("🟢 Added | 🔴 Removed | 🟡 Changed (Substantive)")
            st.download_button("Download Comparison Report", df_diff.to_csv(index=False), file_name="comparison_report.csv", mime="text/csv")
        else:
            st.success("Documents are identical — no changes found.")
    elif run_comp5:
        st.warning("Please paste both document versions.")


# ─────────────────────────────────────────────
# FEATURE 6 — INSPECTION REPORT GENERATION
# ─────────────────────────────────────────────
with tab6:
    st.subheader("Inspection Report Generation")
    st.caption("Converts raw site inspection observations into formal CDSCO-compliant inspection reports")

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        inspector_name = st.text_input("Inspector Name", placeholder="e.g. Dr. A.K. Sharma")
        site_name      = st.text_input("Site Name", placeholder="e.g. AIIMS Delhi — Cardiology Dept")
    with col_f2:
        inspection_date = st.date_input("Inspection Date")
        site_number     = st.text_input("Site Number", placeholder="e.g. SITE-DEL-001")

    obs_input = st.text_area("Paste raw inspection observations (one per line)", height=220,
        placeholder="e.g.\nNo record of drug accountability for subjects 3 and 7\nInformed consent form missing local language version\nMinor labelling issue on sample storage boxes")

    run_insp = st.button("Generate Formal Inspection Report", type="primary")

    if run_insp and obs_input.strip():
        observations = [o.strip() for o in obs_input.splitlines() if o.strip()]

        CRITICAL_KW = ["no record","falsified","patient safety","data integrity","unaccounted","missing","fraud","fabricat"]
        MAJOR_KW    = ["incomplete","not documented","protocol deviation","untrained","not signed","not dated","expired"]
        MINOR_KW    = ["labelling","filing","administrative","minor","formatting","typo"]

        report_rows = []
        for i, obs in enumerate(observations, 1):
            obs_lower = obs.lower()
            if any(k in obs_lower for k in CRITICAL_KW):
                risk = "Critical"; deadline = "15 days"
                corrective = "Immediate CAPA required. Site operations may be suspended pending resolution."
            elif any(k in obs_lower for k in MAJOR_KW):
                risk = "Major"; deadline = "30 days"
                corrective = "Corrective and Preventive Action (CAPA) plan to be submitted within 30 days."
            else:
                risk = "Minor"; deadline = "60 days"
                corrective = "Document corrective action in site log. Report at next scheduled inspection."

            formal = f"During the inspection conducted on {inspection_date.strftime('%d %B %Y')}, it was observed that {obs.lower().rstrip('.')}. This constitutes a {risk.lower()} GCP deviation requiring corrective action."

            report_rows.append({
                "Obs No.": f"OBS-{i:03d}",
                "Raw Observation": obs,
                "Formal Finding": formal,
                "Risk Level": risk,
                "Corrective Action": corrective,
                "Deadline": deadline
            })

        critical_count = sum(1 for r in report_rows if r["Risk Level"]=="Critical")
        major_count    = sum(1 for r in report_rows if r["Risk Level"]=="Major")
        minor_count    = sum(1 for r in report_rows if r["Risk Level"]=="Minor")

        st.markdown("---")
        report_header = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CDSCO GCP SITE INSPECTION REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Site Name     : {site_name or '[SITE NAME]'}
Site Number   : {site_number or '[SITE NUMBER]'}
Inspection Date: {inspection_date.strftime('%d %B %Y')}
Inspector     : {inspector_name or '[INSPECTOR NAME]'}
Report Date   : {datetime.date.today().strftime('%d %B %Y')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SUMMARY: {critical_count} Critical | {major_count} Major | {minor_count} Minor
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        st.code(report_header)

        c1,c2,c3 = st.columns(3)
        c1.metric("Critical Findings", critical_count)
        c2.metric("Major Findings", major_count)
        c3.metric("Minor Findings", minor_count)

        if critical_count > 0:
            st.error(f"{critical_count} Critical finding(s) — immediate CAPA required.")
        elif major_count > 0:
            st.warning(f"{major_count} Major finding(s) — CAPA plan required within 30 days.")
        else:
            st.success("No Critical or Major findings.")

        df_report = pd.DataFrame(report_rows)

        def style_risk(val):
            if val == "Critical": return "background-color:#f8d7da;color:#721c24;font-weight:bold"
            if val == "Major":    return "background-color:#fff3cd;color:#856404;font-weight:bold"
            if val == "Minor":    return "background-color:#d4edda;color:#155724"
            return ""

        styled_rep = df_report.style.applymap(style_risk, subset=["Risk Level"])
        st.dataframe(styled_rep, use_container_width=True, hide_index=True)

        full_report = report_header + "\n"
        for r in report_rows:
            full_report += f"\n{r['Obs No.']} | {r['Risk Level'].upper()}\n"
            full_report += f"Finding: {r['Formal Finding']}\n"
            full_report += f"Corrective Action: {r['Corrective Action']}\n"
            full_report += f"Deadline: {r['Deadline']}\n"
            full_report += "─" * 60 + "\n"
        full_report += f"\nInspector: {inspector_name or '[INSPECTOR NAME]'}\nSignature: _______________\nDate: {datetime.date.today().strftime('%d %B %Y')}"

        st.download_button("Download Formal Inspection Report", full_report, file_name="cdsco_inspection_report.txt", mime="text/plain")
    elif run_insp:
        st.warning("Please enter at least one inspection observation.")
