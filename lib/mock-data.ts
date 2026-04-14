import {
  AuditEntry,
  DashboardMetric,
  IntelligenceModulePreview,
  NavItem,
  ProductTourStep,
  ReviewBoardSignal,
  RiskControlItem,
  SeverityClassification,
  SourceDocument
} from "@/lib/types";

export const MOCK_GENERATED_AT = "2026-04-14T09:30:00Z";

export const NAV_ITEMS: NavItem[] = [
  {
    id: "dashboard",
    label: "Dashboard",
    shortLabel: "01",
    description: "Operational view"
  },
  {
    id: "document-intake",
    label: "Document Intake",
    shortLabel: "02",
    description: "Upload and classify"
  },
  {
    id: "anonymisation",
    label: "Anonymisation",
    shortLabel: "03",
    description: "Redaction workflow"
  },
  {
    id: "sae-review",
    label: "SAE Review",
    shortLabel: "04",
    description: "Serious adverse event review"
  },
  {
    id: "completeness-check",
    label: "Completeness Check",
    shortLabel: "05",
    description: "Mandatory field assurance"
  },
  {
    id: "version-compare",
    label: "Version Compare",
    shortLabel: "06",
    description: "Protocol deltas and impact"
  },
  {
    id: "inspection-report",
    label: "Inspection Report",
    shortLabel: "07",
    description: "From notes to formal report"
  },
  {
    id: "audit-trail",
    label: "Audit Trail",
    shortLabel: "08",
    description: "Traceability ledger"
  }
];

export const DASHBOARD_METRICS: DashboardMetric[] = [
  {
    label: "Documents reviewed",
    value: "18",
    delta: "Today across safety, protocol, and inspection queues",
    tone: "blue"
  },
  {
    label: "PII risks resolved",
    value: "42",
    delta: "Masked before downstream intelligence runs",
    tone: "cyan"
  },
  {
    label: "Critical gaps flagged",
    value: "06",
    delta: "Escalated for sponsor clarification",
    tone: "amber"
  },
  {
    label: "SAE cases triaged",
    value: "09",
    delta: "Seriousness extraction and reviewer review staged",
    tone: "blue"
  },
  {
    label: "Reviewer actions pending",
    value: "04",
    delta: "Human review remains the decision gate",
    tone: "slate"
  },
  {
    label: "Audit readiness score",
    value: "98%",
    delta: "Source-linked outputs and confidence preserved",
    tone: "green"
  }
];

export const LIVE_REVIEW_SIGNALS: ReviewBoardSignal[] = [
  {
    id: "signal-01",
    title: "Protocol endpoint shift detected",
    status: "Substantive amendment",
    metric: "v2.1 → v3.0",
    summary: "Primary endpoint window increased from 12 to 16 weeks and needs amendment review.",
    tone: "amber",
    navTarget: "version-compare"
  },
  {
    id: "signal-02",
    title: "SAE subject AC-204 awaiting reviewer sign-off",
    status: "High-priority safety case",
    metric: "2 missing disclosures",
    summary: "Hospitalisation and medically significant intervention were extracted with pending concomitant medication details.",
    tone: "red",
    navTarget: "sae-review"
  },
  {
    id: "signal-03",
    title: "PII shield completed on narrative batch",
    status: "Protected data ready",
    metric: "9 entities redacted",
    summary: "Patient, investigator, site, and sponsor identifiers were masked before export.",
    tone: "cyan",
    navTarget: "anonymisation"
  },
  {
    id: "signal-04",
    title: "Inspection note formalisation queued",
    status: "Evidence synthesis in progress",
    metric: "1 critical finding candidate",
    summary: "Superseded consent usage and delayed SAE documentation require formal report generation.",
    tone: "blue",
    navTarget: "inspection-report"
  }
];

export const INTELLIGENCE_MODULES: IntelligenceModulePreview[] = [
  {
    id: "module-anonymisation",
    code: "PRV-01",
    title: "Anonymisation",
    summary: "Mask PII and PHI before intelligence workflows.",
    detail: "Entity detection, confidence scoring, side-by-side redaction, and JSON export.",
    status: "Operational",
    tone: "cyan",
    navTarget: "anonymisation"
  },
  {
    id: "module-summarisation",
    code: "INT-02",
    title: "Summarisation",
    summary: "Condense long packets into structured reviewer briefs.",
    detail: "Meeting transcripts, narratives, and inspection notes are reduced into auditable summaries.",
    status: "Embedded in intake pipeline",
    tone: "blue",
    navTarget: "document-intake"
  },
  {
    id: "module-completeness",
    code: "CHK-03",
    title: "Completeness Check",
    summary: "Flag mandatory gaps before submission progression.",
    detail: "Critical, major, and minor field assurance with reviewer action prompts.",
    status: "Operational",
    tone: "amber",
    navTarget: "completeness-check"
  },
  {
    id: "module-sae",
    code: "SAFE-04",
    title: "SAE Triage",
    summary: "Extract seriousness, severity, causality, and missing disclosures.",
    detail: "Reviewer can accept, edit, or override without losing traceability.",
    status: "Operational",
    tone: "blue",
    navTarget: "sae-review"
  },
  {
    id: "module-version",
    code: "CMP-05",
    title: "Version Compare",
    summary: "Surface substantive changes between protocol versions.",
    detail: "Eligibility, endpoint, and consent wording changes are tied to regulatory impact.",
    status: "Operational",
    tone: "amber",
    navTarget: "version-compare"
  },
  {
    id: "module-inspection",
    code: "FIELD-06",
    title: "Inspection Report",
    summary: "Turn rough notes into formal inspection findings.",
    detail: "Site details, evidence summary, severity grouping, and CAPA-ready actions.",
    status: "Operational",
    tone: "blue",
    navTarget: "inspection-report"
  },
  {
    id: "module-audit",
    code: "TRACE-07",
    title: "Audit Trail",
    summary: "Persist source-linked outputs, reviewer actions, and timestamps.",
    detail: "Every AI suggestion remains attributable, reviewable, and exportable.",
    status: "Operational",
    tone: "green",
    navTarget: "audit-trail"
  }
];

export const RISK_CONTROL_ITEMS: RiskControlItem[] = [
  {
    id: "risk-01",
    title: "Source-linked outputs",
    metric: "100%",
    detail: "Every structured output retains a direct source reference for audit packet assembly.",
    tone: "blue"
  },
  {
    id: "risk-02",
    title: "Confidence scores exposed",
    metric: "92-98%",
    detail: "Reviewers can see model certainty before acting on a recommendation.",
    tone: "cyan"
  },
  {
    id: "risk-03",
    title: "Reviewer override",
    metric: "Always on",
    detail: "Nirnay never auto-disposes a case and preserves manual override as the authority path.",
    tone: "green"
  },
  {
    id: "risk-04",
    title: "Low-confidence escalation",
    metric: "<85%",
    detail: "When certainty drops, cases are escalated instead of guessed through.",
    tone: "amber"
  },
  {
    id: "risk-05",
    title: "Full audit log",
    metric: "Immutable trail",
    detail: "AI outputs, reviewer actions, timestamps, and references are captured together.",
    tone: "slate"
  }
];

export const PRODUCT_TOUR_STEPS: ProductTourStep[] = [
  {
    id: "tour-01",
    phase: "Step 01",
    title: "Document Intake",
    summary: "Packets are classified and routed the moment they enter the workbench.",
    detail:
      "Nirnay accepts PDF, DOCX, TXT, and image placeholders, classifies the submission type, and stages it for the correct regulatory workflow.",
    signal: "Routing confidence preserved before deeper analysis",
    route: "document-intake",
    safeguards: [
      "Source file retained with classification rationale",
      "OCR/parser integration boundary kept explicit"
    ],
    outputs: [
      "Document class",
      "Routing rationale",
      "Intake metadata"
    ]
  },
  {
    id: "tour-02",
    phase: "Step 02",
    title: "Anonymisation",
    summary: "Protected data is masked before downstream intelligence is trusted.",
    detail:
      "PII and PHI entities are detected with confidence scores, shown side by side, and exported as structured redaction payloads.",
    signal: "Protected-data controls execute before analysis",
    route: "anonymisation",
    safeguards: [
      "Entity-level confidence display",
      "Reviewer validation before release"
    ],
    outputs: [
      "Redacted narrative",
      "Entity ledger",
      "Anonymised JSON"
    ]
  },
  {
    id: "tour-03",
    phase: "Step 03",
    title: "Intelligence",
    summary: "Structured evidence is extracted without hiding the reasoning surface.",
    detail:
      "Completeness checks, protocol deltas, and summarised evidence are assembled into reviewer-ready outputs instead of opaque AI prose.",
    signal: "When confidence is low, Nirnay does not guess. It escalates.",
    route: "completeness-check",
    safeguards: [
      "Gap severity labels",
      "Source-backed evidence summaries"
    ],
    outputs: [
      "Missing field list",
      "Substantive change notices",
      "Structured reviewer brief"
    ]
  },
  {
    id: "tour-04",
    phase: "Step 04",
    title: "Human Review",
    summary: "The reviewer remains the decision-maker for safety and compliance determinations.",
    detail:
      "SAE extraction can be accepted, edited, or overridden, and the reviewer action is logged as the authoritative disposition.",
    signal: "Human judgement remains the final gate",
    route: "sae-review",
    safeguards: [
      "Explicit accept/edit/override actions",
      "No auto-submission or silent changes"
    ],
    outputs: [
      "Final severity determination",
      "Reviewer notes",
      "Escalation action"
    ]
  },
  {
    id: "tour-05",
    phase: "Step 05",
    title: "Audit Packet",
    summary: "Every module rolls into a traceable, audit-ready record.",
    detail:
      "Nirnay assembles AI outputs, confidence, reviewer actions, timestamps, and source references into an audit-friendly decision trail.",
    signal: "Audit readiness is a first-class output, not an afterthought",
    route: "audit-trail",
    safeguards: [
      "Full activity logging",
      "Reviewer accountability preserved"
    ],
    outputs: [
      "Audit ledger",
      "Decision trace",
      "Source-linked packet"
    ]
  }
];

export const SAMPLE_DOCUMENTS: SourceDocument[] = [
  {
    id: "doc-sugam-01",
    name: "CT-23_SUGAM_submission_v1.pdf",
    format: "PDF",
    source: "Hackathon demo set",
    description: "Synthetic application packet mirrored on a SUGAM intake scenario.",
    documentType: "SUGAM Application",
    confidence: 0.96,
    ingestionNote: "OCR and metadata extraction would attach here in production."
  },
  {
    id: "doc-sae-01",
    name: "SAE_narrative_subject_204.txt",
    format: "TXT",
    source: "Hackathon demo set",
    description: "SAE narrative with structured extraction-ready content.",
    documentType: "SAE Narrative",
    confidence: 0.98
  },
  {
    id: "doc-meeting-01",
    name: "ethics_committee_minutes.docx",
    format: "DOCX",
    source: "Hackathon demo set",
    description: "Transcript-style note set for summarisation and version traceability.",
    documentType: "Meeting Transcript",
    confidence: 0.94
  },
  {
    id: "doc-inspection-01",
    name: "site_visit_notes_photo.jpg",
    format: "Image",
    source: "Hackathon demo set",
    description: "Image placeholder for handwritten inspection notes.",
    documentType: "Inspection Notes",
    confidence: 0.92,
    ingestionNote: "Handwriting OCR service would convert image notes to text here."
  },
  {
    id: "doc-protocol-01",
    name: "protocol_amendment_3_redline.pdf",
    format: "PDF",
    source: "Hackathon demo set",
    description: "Protocol amendment package for substantive change review.",
    documentType: "Protocol Amendment",
    confidence: 0.95
  }
];

export const SAMPLE_ANONYMISATION_TEXT = `Patient Name: Meera Sharma, Age: 47, Initials: MS, Phone: 9812345678.
Address: 14 Lake View Road, New Delhi 110021.
Hospital ID: HN-44721. Investigator: Dr. Arvind Rao.
Site Name: Apex Care Hospital, Bengaluru.
Sponsor Name: Helix Biotech Pvt Ltd.
Clinical note: Patient reported dizziness and rash two hours after IMP administration and was shifted for overnight observation.`;

export const SAMPLE_SAE_NARRATIVE = `Subject AC-204 is a 47-year-old female with controlled type 2 diabetes enrolled in Protocol HBT-17.
On 11 April 2026, approximately 30 minutes after investigational product administration, the subject developed diffuse rash, hypotension, and breathing difficulty.
The subject was admitted to Apex Care Hospital for monitoring and intravenous antihistamines. The investigator assessed the event as serious due to hospitalisation and medically significant intervention.
Investigational product dosing was stopped. The subject improved within 24 hours and was discharged stable.
Concomitant medication history is not available in the initial report. Reporter signature page was not attached.`;

export const SAMPLE_FORM_OBJECT = {
  applicationId: "CT-23-2026-1148",
  sponsorName: "Helix Biotech Pvt Ltd",
  studyTitle: "Phase II Randomized Trial of HBT-17 in Autoimmune Dermatitis",
  principalInvestigator: "Dr. Arvind Rao",
  ethicsCommitteeApprovalNumber: "",
  siteAddress: "Apex Care Hospital, Bengaluru",
  indemnityDocumentReference: "",
  subjectCompensationPlan: "Included in annexure 8",
  protocolVersion: "Amendment 03 / 07 Apr 2026",
  informedConsentVersion: "",
  manufacturingLicenceReference: "Form-28D-445",
  saeReportingContact: "",
  investigationalProductStoragePlan: "Cold chain range 2C-8C",
  medicalMonitorName: "Dr. Sonia Kapoor"
};

export const SAMPLE_PROTOCOL_BASELINE = `Eligibility Criteria:
- Adults aged 18-65 years with HbA1c between 7.0% and 10.0%.
Primary Endpoint:
- Reduction in severe flare count over 12 weeks.
Consent Wording:
- Samples may be retained for protocol-specified safety analysis only.`;

export const SAMPLE_PROTOCOL_AMENDED = `Eligibility Criteria:
- Adults aged 18-70 years with HbA1c between 6.5% and 10.5%.
Primary Endpoint:
- Reduction in moderate-to-severe flare count over 16 weeks.
Consent Wording:
- Samples may be retained for protocol-specified safety analysis and future biomarker research with subject authorization.`;

export const SAMPLE_INSPECTION_NOTES = `Site: Apex Care Hospital, Bengaluru
PI: Dr. Kavita Menon
Date: 12 Apr 2026
- Consent forms for subjects AC-110, AC-112, and AC-119 used superseded version 2.1 instead of approved version 2.3.
- SAE log for subject AC-204 updated late; evidence of 24-hour notification to sponsor not filed.
- IMP temperature log has missing entries on 08 Apr and 09 Apr.
- Delegation log and pharmacy binder were otherwise complete.`;

export const SAE_SEVERITY_OPTIONS: SeverityClassification[] = [
  "Death",
  "Life-threatening",
  "Hospitalisation",
  "Disability",
  "Medically significant",
  "Non-serious"
];

export const INITIAL_AUDIT_TRAIL: AuditEntry[] = [
  {
    id: "audit-01",
    module: "Document Intake",
    action: "Classified incoming packet",
    actor: "AI",
    confidence: 0.96,
    timestamp: "2026-04-14 14:02 IST",
    sourceReference: "CT-23_SUGAM_submission_v1.pdf",
    status: "Generated",
    note: "Detected SUGAM Application from filename, form markers, and annexure structure."
  },
  {
    id: "audit-02",
    module: "Anonymisation",
    action: "Redaction draft produced",
    actor: "AI",
    confidence: 0.95,
    timestamp: "2026-04-14 14:04 IST",
    sourceReference: "SAE_narrative_subject_204.txt",
    status: "Generated",
    note: "PHI and sponsor-linked identifiers masked for reviewer validation."
  },
  {
    id: "audit-03",
    module: "SAE Review",
    action: "Severity classification generated",
    actor: "AI",
    confidence: 0.92,
    timestamp: "2026-04-14 14:06 IST",
    sourceReference: "SAE_narrative_subject_204.txt",
    status: "Generated",
    note: "Hospitalisation and medically significant intervention identified."
  },
  {
    id: "audit-04",
    module: "Completeness Check",
    action: "Missing fields flagged",
    actor: "AI",
    confidence: 0.97,
    timestamp: "2026-04-14 14:08 IST",
    sourceReference: "CT-23-2026-1148",
    status: "Generated",
    note: "Mandatory fields triaged into critical, major, and minor reviewer actions."
  },
  {
    id: "audit-05",
    module: "Inspection Report",
    action: "Formal report draft assembled",
    actor: "AI",
    confidence: 0.9,
    timestamp: "2026-04-14 14:10 IST",
    sourceReference: "site_visit_notes_photo.jpg",
    status: "Generated",
    note: "Findings grouped by severity and tied to source observation lines."
  }
];
