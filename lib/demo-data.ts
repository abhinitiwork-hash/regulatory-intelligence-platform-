import {
  CompletenessIssue,
  DemoAuditEvent,
  DemoDocument,
  DemoMetric,
  DemoPriorityItem,
  IntakeSynopsis,
  InspectionFindingItem,
  JudgingFlowStep,
  ModuleShortcut,
  RedactionEntity,
  ReviewerUser,
  RiskControlTopic,
  TourStep,
  VersionChangeItem
} from "@/lib/demo-types";

export const REVIEWERS: ReviewerUser[] = [
  {
    id: "rev-01",
    name: "Dr. Kavita Menon",
    role: "Senior CDSCO Reviewer",
    focus: "Clinical safety and oversight"
  },
  {
    id: "rev-02",
    name: "Rohan Iyer",
    role: "Regulatory Data Analyst",
    focus: "Completeness and audit readiness"
  }
];

export const DASHBOARD_METRICS: DemoMetric[] = [
  {
    id: "metric-01",
    label: "Documents reviewed",
    value: 18,
    detail: "Across safety, protocol, and inspection queues"
  },
  {
    id: "metric-02",
    label: "PII risks resolved",
    value: 42,
    detail: "Masked before structured intelligence runs"
  },
  {
    id: "metric-03",
    label: "Critical gaps flagged",
    value: 6,
    detail: "Escalated for sponsor clarification"
  },
  {
    id: "metric-04",
    label: "SAE cases triaged",
    value: 9,
    detail: "Reviewer validation pending on 2 cases"
  },
  {
    id: "metric-05",
    label: "Reviewer actions pending",
    value: 4,
    detail: "Human review remains the final gate"
  },
  {
    id: "metric-06",
    label: "Audit readiness score",
    value: 98,
    suffix: "%",
    detail: "Source-linked outputs retained throughout"
  }
];

export const SAMPLE_DOCUMENTS: DemoDocument[] = [
  {
    id: "doc-001",
    name: "CT-23_SUGAM_submission_v1.pdf",
    format: "PDF",
    documentType: "SUGAM Application",
    source: "SUGAM intake mirror",
    stage: "Document Intake",
    status: "Ready for Review",
    riskLevel: "High",
    confidence: 0.96,
    updatedAt: "14 Apr 2026, 2:02 pm",
    assignedModule: "Completeness Check",
    reviewer: "Rohan Iyer",
    summary: "Synthetic application packet with missing EC approval reference and indemnity document.",
    preview:
      "Application CT-23-2026-1148 submitted by Helix Biotech Pvt Ltd for Phase II randomized trial of HBT-17.",
    metadata: {
      sponsor: "Helix Biotech Pvt Ltd",
      study: "HBT-17 Autoimmune Dermatitis",
      site: "Apex Care Hospital, Bengaluru",
      protocolVersion: "Amendment 03"
    },
    tags: ["SUGAM", "Missing fields", "High priority"]
  },
  {
    id: "doc-002",
    name: "SAE_narrative_subject_204.txt",
    format: "TXT",
    documentType: "SAE Narrative",
    source: "Safety intake batch",
    stage: "Human Review",
    status: "In Review",
    riskLevel: "Critical",
    confidence: 0.98,
    updatedAt: "14 Apr 2026, 2:06 pm",
    assignedModule: "SAE Review",
    reviewer: "Dr. Kavita Menon",
    summary: "Serious adverse event with hospitalisation and missing concomitant medication history.",
    preview:
      "Subject AC-204 developed diffuse rash, hypotension, and breathing difficulty 30 minutes after dosing and was admitted for monitoring.",
    metadata: {
      subject: "AC-204",
      seriousness: "Hospitalisation",
      site: "Apex Care Hospital, Bengaluru",
      sponsor: "Helix Biotech Pvt Ltd"
    },
    tags: ["SAE", "Hospitalisation", "Reviewer override enabled"]
  },
  {
    id: "doc-003",
    name: "ethics_committee_minutes.docx",
    format: "DOCX",
    documentType: "Meeting Transcript",
    source: "Ethics committee archive",
    stage: "Intelligence",
    status: "Queued",
    riskLevel: "Medium",
    confidence: 0.94,
    updatedAt: "14 Apr 2026, 1:58 pm",
    assignedModule: "Summarisation",
    reviewer: "Rohan Iyer",
    summary: "Transcript contains deferred questions on subject compensation and retention wording.",
    preview:
      "Committee requested clarity on optional biomarker storage language and participant compensation annexure alignment.",
    metadata: {
      committee: "Apex EC",
      date: "09 Apr 2026",
      attendees: "7"
    },
    tags: ["Transcript", "Summarisation", "Follow-up questions"]
  },
  {
    id: "doc-004",
    name: "site_visit_notes_photo.jpg",
    format: "IMG",
    documentType: "Inspection Notes",
    source: "Field inspection upload",
    stage: "Intelligence",
    status: "Escalated",
    riskLevel: "High",
    confidence: 0.92,
    updatedAt: "14 Apr 2026, 2:10 pm",
    assignedModule: "Inspection Report",
    reviewer: "Dr. Kavita Menon",
    summary: "Handwritten inspection notes suggest superseded consent use and delayed SAE evidence filing.",
    preview:
      "Consent forms for AC-110, AC-112, and AC-119 used version 2.1 instead of the approved 2.3 template.",
    metadata: {
      inspector: "North Zone GCP Team",
      site: "Apex Care Hospital, Bengaluru",
      inspectionDate: "12 Apr 2026"
    },
    tags: ["Inspection", "Consent deviation", "Escalated"]
  },
  {
    id: "doc-005",
    name: "protocol_amendment_3_redline.pdf",
    format: "PDF",
    documentType: "Protocol Amendment",
    source: "Protocol amendment intake",
    stage: "Intelligence",
    status: "Ready for Review",
    riskLevel: "High",
    confidence: 0.95,
    updatedAt: "14 Apr 2026, 2:12 pm",
    assignedModule: "Version Compare",
    reviewer: "Rohan Iyer",
    summary: "Substantive changes detected in eligibility, endpoint duration, and consent language.",
    preview:
      "Adults aged 18-70 years with HbA1c 6.5% to 10.5% proposed for inclusion with a revised 16-week primary endpoint window.",
    metadata: {
      baseline: "Protocol v2.1",
      amended: "Protocol v3.0",
      sponsor: "Helix Biotech Pvt Ltd"
    },
    tags: ["Protocol", "Substantive change", "Consent impact"]
  },
  {
    id: "doc-006",
    name: "MDO_form12_submission_packet.docx",
    format: "DOCX",
    documentType: "SUGAM Application",
    source: "MD Online staging mirror",
    stage: "Document Intake",
    status: "Queued",
    riskLevel: "Medium",
    confidence: 0.93,
    updatedAt: "14 Apr 2026, 1:54 pm",
    assignedModule: "Completeness Check",
    reviewer: "Rohan Iyer",
    summary: "Device application packet requires insurance attachment reference and authorised signatory date.",
    preview:
      "Application MDO-14-2026-332 requests import and clinical performance evaluation for implantable glucose sensor HBT-MD7.",
    metadata: {
      sponsor: "Helix Medsystems Pvt Ltd",
      product: "HBT-MD7",
      site: "Crescent Institute of Medical Sciences, Chennai",
      dossierVersion: "Submission 01"
    },
    tags: ["MD Online", "Device", "Completeness"]
  },
  {
    id: "doc-007",
    name: "sae_follow_up_subject_117.pdf",
    format: "PDF",
    documentType: "SAE Narrative",
    source: "Safety follow-up intake",
    stage: "Human Review",
    status: "Ready for Review",
    riskLevel: "Critical",
    confidence: 0.96,
    updatedAt: "14 Apr 2026, 1:52 pm",
    assignedModule: "SAE Review",
    reviewer: "Dr. Kavita Menon",
    summary: "Follow-up SAE packet records prolonged hospital stay and revised investigator causality note.",
    preview:
      "Subject HBT-117 remained admitted for 48 hours following infusion reaction; follow-up note adds steroid administration and sponsor notification evidence.",
    metadata: {
      subject: "HBT-117",
      seriousness: "Hospitalisation",
      site: "MetroCare Research Unit, Mumbai",
      sponsor: "Helix Biotech Pvt Ltd"
    },
    tags: ["SAE follow-up", "Hospitalisation", "Safety review"]
  },
  {
    id: "doc-008",
    name: "ec_transcript_09apr_subject_rights.txt",
    format: "TXT",
    documentType: "Meeting Transcript",
    source: "Ethics committee recorder upload",
    stage: "Intelligence",
    status: "Ready for Review",
    riskLevel: "Medium",
    confidence: 0.95,
    updatedAt: "14 Apr 2026, 1:49 pm",
    assignedModule: "Summarisation",
    reviewer: "Rohan Iyer",
    summary: "Transcript flags compensation matrix ambiguity and optional biomarker language requiring sponsor response.",
    preview:
      "Committee chair requested a simpler explanation of future biomarker retention and a clarified compensation escalation table before approval.",
    metadata: {
      committee: "MetroCare EC",
      date: "09 Apr 2026",
      agenda: "Subject rights and compensation"
    },
    tags: ["Transcript", "Synopsis", "EC follow-up"]
  },
  {
    id: "doc-009",
    name: "protocol_amendment_4_consent_redline.docx",
    format: "DOCX",
    documentType: "Protocol Amendment",
    source: "Sponsor amendment upload",
    stage: "Intelligence",
    status: "Queued",
    riskLevel: "High",
    confidence: 0.94,
    updatedAt: "14 Apr 2026, 1:47 pm",
    assignedModule: "Version Compare",
    reviewer: "Rohan Iyer",
    summary: "Consent annexure expands sample retention language and updates withdrawal wording.",
    preview:
      "Amendment 04 introduces future-use specimen language and clarifies pregnancy follow-up obligations after study withdrawal.",
    metadata: {
      baseline: "Consent Annexure v2.3",
      amended: "Consent Annexure v2.4",
      sponsor: "Helix Biotech Pvt Ltd"
    },
    tags: ["Consent", "Privacy", "Amendment"]
  },
  {
    id: "doc-010",
    name: "north_zone_reinspection_notes.png",
    format: "IMG",
    documentType: "Inspection Notes",
    source: "North Zone reinspection upload",
    stage: "Intelligence",
    status: "Ready for Review",
    riskLevel: "High",
    confidence: 0.9,
    updatedAt: "14 Apr 2026, 1:43 pm",
    assignedModule: "Inspection Report",
    reviewer: "Dr. Kavita Menon",
    summary: "Reinspection notes capture CAPA closure evidence and one remaining pharmacy log discrepancy.",
    preview:
      "CAPA training records were available; one investigational product reconciliation entry remained unsigned on 10 Apr 2026.",
    metadata: {
      inspector: "North Zone GCP Team",
      site: "MetroCare Research Unit, Mumbai",
      inspectionDate: "13 Apr 2026"
    },
    tags: ["Inspection", "CAPA", "Reinspection"]
  }
];

export const PRIORITY_ITEMS: DemoPriorityItem[] = [
  {
    id: "priority-01",
    title: "SAE subject AC-204 requires final seriousness sign-off",
    riskLevel: "Critical",
    owner: "Dr. Kavita Menon",
    summary: "Hospitalisation confirmed; concomitant medication history remains absent.",
    nextStep: "Complete reviewer note and generate review packet.",
    route: "/sae-review"
  },
  {
    id: "priority-02",
    title: "Protocol endpoint amendment needs substantive review note",
    riskLevel: "High",
    owner: "Rohan Iyer",
    summary: "Primary endpoint window extended from 12 to 16 weeks.",
    nextStep: "Create reviewer summary and attach impact rationale.",
    route: "/version-compare"
  },
  {
    id: "priority-03",
    title: "Inspection notes need formal report export",
    riskLevel: "High",
    owner: "Dr. Kavita Menon",
    summary: "Superseded consent version used across 3 subject files.",
    nextStep: "Generate report and escalate CAPA recommendation.",
    route: "/inspection-report"
  },
  {
    id: "priority-04",
    title: "Application CT-23 still lacks EC approval reference",
    riskLevel: "High",
    owner: "Rohan Iyer",
    summary: "Critical completeness item remains unresolved in the application packet.",
    nextStep: "Confirm reviewer disposition and issue deficiency memo.",
    route: "/completeness-check"
  }
];

export const MODULE_SHORTCUTS: ModuleShortcut[] = [
  {
    id: "shortcut-01",
    title: "Document Intake",
    description: "Route new packets into the correct review lane.",
    route: "/document-intake",
    badge: "Queue control"
  },
  {
    id: "shortcut-02",
    title: "Anonymisation",
    description: "Mask PII and PHI before downstream analysis.",
    route: "/anonymisation",
    badge: "Entity ledger"
  },
  {
    id: "shortcut-03",
    title: "SAE Review",
    description: "Triage safety narratives with reviewer-controlled overrides.",
    route: "/sae-review",
    badge: "Safety triage"
  },
  {
    id: "shortcut-04",
    title: "Completeness Check",
    description: "Surface mandatory omissions and deficiency actions.",
    route: "/completeness-check",
    badge: "Deficiency register"
  },
  {
    id: "shortcut-05",
    title: "Version Compare",
    description: "Explain substantive vs administrative changes.",
    route: "/version-compare",
    badge: "Protocol delta"
  },
  {
    id: "shortcut-06",
    title: "Inspection Report",
    description: "Draft formal findings from field notes.",
    route: "/inspection-report",
    badge: "Drafting engine"
  },
  {
    id: "shortcut-07",
    title: "Audit Trail",
    description: "Review source-linked outputs and final actions.",
    route: "/audit-trail",
    badge: "Traceability"
  },
  {
    id: "shortcut-08",
    title: "Risk Controls",
    description: "Show governance posture for official review.",
    route: "/risk-controls",
    badge: "Oversight"
  }
];

export const WHAT_NIRNAY_DOES = [
  {
    id: "cap-01",
    title: "Protect regulated data",
    summary: "Anonymisation identifies PII/PHI before evidence extraction begins.",
    details:
      "Nirnay highlights sensitive entities, supports reviewer validation, and exports structured anonymisation payloads ready for downstream services."
  },
  {
    id: "cap-02",
    title: "Structure evidence",
    summary: "Long narratives and meeting notes turn into structured reviewer artifacts.",
    details:
      "The workbench converts transcripts, narratives, and field notes into consistent summaries, findings, and action panels without hiding source references."
  },
  {
    id: "cap-03",
    title: "Keep reviewers in control",
    summary: "Every AI output is editable, overrideable, and logged.",
    details:
      "Safety classifications, completeness findings, and protocol impacts stay assistive only. Human reviewers remain the final authority."
  }
];

export const TRUST_CONTROLS = [
  {
    id: "trust-01",
    title: "Source-linked outputs",
    detail: "Each recommendation retains a source reference so the reviewer can verify the evidence trail."
  },
  {
    id: "trust-02",
    title: "Confidence disclosure",
    detail: "Confidence is visible at field level and at workflow level, enabling escalation instead of hidden uncertainty."
  },
  {
    id: "trust-03",
    title: "Human override",
    detail: "Nirnay never auto-disposes a case and records reviewer intervention as the authoritative action."
  },
  {
    id: "trust-04",
    title: "Audit readiness",
    detail: "AI outputs, reviewer actions, timestamps, and source references are exportable as a coherent audit packet."
  }
];

export const TOUR_STEPS: TourStep[] = [
  {
    id: "tour-01",
    title: "Document Intake",
    route: "/document-intake",
    signal: "Packets are classified and routed as soon as they enter the system.",
    detail:
      "Upload or select seeded packets, inspect metadata, and send cases into the next workflow stage with full traceability.",
    outputs: ["Detected type", "Metadata panel", "Routing confidence"]
  },
  {
    id: "tour-02",
    title: "Anonymisation",
    route: "/anonymisation",
    signal: "Protected data is masked before any downstream intelligence is trusted.",
    detail:
      "Reviewer sees the original narrative beside the redacted output, with entity-level controls and escalation for lower-confidence detections.",
    outputs: ["Entity ledger", "Validation summary", "Downloadable JSON"]
  },
  {
    id: "tour-03",
    title: "Intelligence",
    route: "/completeness-check",
    signal: "Nirnay structures evidence rather than producing opaque AI prose.",
    detail:
      "Completeness checks, summaries, and version impacts are shown as reviewable, source-linked findings rather than black-box recommendations.",
    outputs: ["Gap list", "Impact summaries", "Reviewer prompts"]
  },
  {
    id: "tour-04",
    title: "Human Review",
    route: "/sae-review",
    signal: "The reviewer remains the decision-maker for safety and compliance outcomes.",
    detail:
      "Structured SAE extraction can be accepted, edited, or overridden, and those interventions become part of the audit trail.",
    outputs: ["Review packet", "Override log", "Reviewer notes"]
  },
  {
    id: "tour-05",
    title: "Audit Output",
    route: "/audit-trail",
    signal: "Every action becomes a source-linked audit artifact.",
    detail:
      "Final logs can be searched, filtered, inspected, and exported so the product stands up in formal review or inspection settings.",
    outputs: ["Audit ledger", "Searchable entries", "CSV / JSON exports"]
  }
];

export const JUDGING_FLOW_STEPS: JudgingFlowStep[] = [
  {
    id: "judge-01",
    route: "/dashboard",
    label: "Dashboard",
    purpose: "Open with the operating picture, priority queue, and audit posture.",
    requirement: "Review cockpit and reviewer workload",
    strongMoment: "The operating picture makes it immediately clear that Nirnay is a reviewer workbench, not a chatbot."
  },
  {
    id: "judge-02",
    route: "/document-intake",
    label: "Document Intake",
    purpose: "Show document classification, metadata extraction, and structured synopsis.",
    requirement: "Document intake, routing, and summarisation",
    strongMoment: "Run classification, then show the structured synopsis panel for the meeting transcript or application packet."
  },
  {
    id: "judge-03",
    route: "/anonymisation",
    label: "Anonymisation",
    purpose: "Demonstrate visible PII/PHI redaction with reviewer approval.",
    requirement: "Sensitive data anonymisation",
    strongMoment: "Side-by-side original vs redacted text with low-confidence escalation and downloadable JSON."
  },
  {
    id: "judge-04",
    route: "/sae-review",
    label: "SAE Review",
    purpose: "Show structured extraction, seriousness classification, evidence, and override.",
    requirement: "SAE triage and severity classification",
    strongMoment: "Change severity, resolve a missing item, and generate the review packet."
  },
  {
    id: "judge-05",
    route: "/completeness-check",
    label: "Completeness Check",
    purpose: "Flag missing mandatory fields and create a reviewer action memo.",
    requirement: "Missing mandatory field detection",
    strongMoment: "Update an issue disposition, watch completion change, then generate the deficiency memo."
  },
  {
    id: "judge-06",
    route: "/version-compare",
    label: "Version Compare",
    purpose: "Show substantive protocol changes and likely regulatory impact.",
    requirement: "Version comparison and impact explanation",
    strongMoment: "Open the endpoint or consent change and create the reviewer summary."
  },
  {
    id: "judge-07",
    route: "/inspection-report",
    label: "Inspection Report",
    purpose: "Turn rough notes into a formal inspection report draft.",
    requirement: "Inspection report generation from unstructured notes",
    strongMoment: "Run the staged generation flow and show editable findings with severity tags."
  },
  {
    id: "judge-08",
    route: "/audit-trail",
    label: "Audit Trail",
    purpose: "Close with traceability, confidence visibility, and reviewer action history.",
    requirement: "Auditability, reviewer control, and exportability",
    strongMoment: "Search or filter the ledger, open a record, and export the log."
  }
];

export const INTAKE_SYNOPSES: Record<string, IntakeSynopsis> = {
  "doc-001": {
    headline: "Application synopsis prepared for completeness review",
    confidence: 0.96,
    summary:
      "Application CT-23-2026-1148 is a Phase II submission for HBT-17. Core sponsor and site metadata are present, but ethics and indemnity references remain incomplete.",
    keySignals: [
      "EC approval number absent from the form body.",
      "Indemnity reference is not linked to the packet.",
      "Protocol amendment 03 is cited consistently across annexures."
    ],
    reviewerPrompts: [
      "Confirm whether the ethics approval reference appears in an annexure outside the intake extract.",
      "Decide if sponsor clarification is required before technical review."
    ],
    nextAction: "Route to Completeness Check and issue deficiency action if EC reference remains absent."
  },
  "doc-002": {
    headline: "Safety narrative synopsis prepared for human review",
    confidence: 0.98,
    summary:
      "Narrative indicates an infusion-related reaction with hospital admission, medically significant intervention, and incomplete concomitant medication history.",
    keySignals: [
      "Hospitalisation is explicitly documented.",
      "Dosing interruption is recorded.",
      "Concomitant medication history is missing."
    ],
    reviewerPrompts: [
      "Validate seriousness and final severity classification.",
      "Determine whether follow-up from the site is required before case closure."
    ],
    nextAction: "Open SAE Review for structured triage and reviewer sign-off."
  },
  "doc-003": {
    headline: "Meeting synopsis identifies unresolved ethics questions",
    confidence: 0.94,
    summary:
      "Committee discussion centers on optional biomarker storage, subject compensation language, and annexure alignment before approval.",
    keySignals: [
      "Retention wording for optional samples remains under discussion.",
      "Compensation annexure needs alignment with the protocol narrative.",
      "No decision was recorded on the revised retention clause."
    ],
    reviewerPrompts: [
      "Confirm whether a sponsor response is already on file.",
      "Capture unresolved items for the next EC communication."
    ],
    nextAction: "Attach synopsis to the review packet and route open questions to the sponsor."
  },
  "doc-004": {
    headline: "Inspection note synopsis highlights consent and safety filing deviations",
    confidence: 0.92,
    summary:
      "Handwritten inspection notes indicate superseded consent use and delayed SAE evidence filing at the site.",
    keySignals: [
      "Three subject files cite consent version 2.1 instead of 2.3.",
      "SAE notification evidence is not filed for AC-204.",
      "Other binders appear complete."
    ],
    reviewerPrompts: [
      "Confirm whether re-consent is required.",
      "Assess whether CAPA timeline should be escalated."
    ],
    nextAction: "Generate formal inspection findings and recommended actions."
  },
  "doc-005": {
    headline: "Protocol delta synopsis marks substantive amendments",
    confidence: 0.95,
    summary:
      "Eligibility range, endpoint window, and consent wording all changed in a way that can affect safety oversight and ethics review.",
    keySignals: [
      "Eligibility age ceiling increased to 70 years.",
      "Primary endpoint window extended from 12 to 16 weeks.",
      "Future biomarker use added to consent language."
    ],
    reviewerPrompts: [
      "Check whether statistical justification is attached.",
      "Verify EC review for broader specimen retention language."
    ],
    nextAction: "Open Version Compare and record regulatory impact."
  },
  "doc-006": {
    headline: "Device submission synopsis highlights administrative gaps",
    confidence: 0.93,
    summary:
      "MD Online mirrored packet contains the core device dossier but does not clearly attach insurance reference and authorised signatory date.",
    keySignals: [
      "Product metadata is present.",
      "Insurance reference is missing from intake fields.",
      "Authorised signatory block needs verification."
    ],
    reviewerPrompts: [
      "Determine whether missing references are critical for acceptance.",
      "Confirm if device dossier version matches sponsor cover letter."
    ],
    nextAction: "Route to Completeness Check for deficiency handling."
  },
  "doc-007": {
    headline: "Follow-up SAE synopsis updates the safety timeline",
    confidence: 0.96,
    summary:
      "Follow-up packet confirms extended hospital stay, adds steroid administration, and improves sponsor notification evidence.",
    keySignals: [
      "Hospital stay extended to 48 hours.",
      "Intervention now includes steroid treatment.",
      "Sponsor notification evidence appears in the follow-up attachment."
    ],
    reviewerPrompts: [
      "Check whether severity classification should remain unchanged.",
      "Verify whether previous missing information is now resolved."
    ],
    nextAction: "Review as an SAE follow-up and update the packet status."
  },
  "doc-008": {
    headline: "Ethics transcript synopsis prepares sponsor follow-up questions",
    confidence: 0.95,
    summary:
      "Committee discussion asks for clearer biomarker retention wording and a revised compensation matrix before approval can proceed.",
    keySignals: [
      "Future-use specimen language is not yet acceptable to the committee.",
      "Compensation matrix needs simplification for subjects.",
      "Approval appears deferred pending sponsor clarification."
    ],
    reviewerPrompts: [
      "Capture the two unresolved questions in the next sponsor response request.",
      "Confirm whether compensation wording aligns with the consent annexure."
    ],
    nextAction: "Attach the synopsis to the review packet and route to sponsor clarification."
  },
  "doc-009": {
    headline: "Consent annexure synopsis indicates privacy-impacting changes",
    confidence: 0.94,
    summary:
      "Amendment 04 broadens future-use sample language and modifies withdrawal obligations, creating a privacy and ethics review burden.",
    keySignals: [
      "Future-use biomarker language is expanded.",
      "Withdrawal obligations change after discontinuation.",
      "Consent wording is more permissive than the prior annexure."
    ],
    reviewerPrompts: [
      "Check whether the revised consent was approved by the EC.",
      "Assess whether the broader retention scope needs sponsor justification."
    ],
    nextAction: "Open Version Compare and document privacy impact."
  },
  "doc-010": {
    headline: "Reinspection synopsis narrows remaining CAPA risk",
    confidence: 0.9,
    summary:
      "Reinspection notes show most CAPA items closed, with one remaining unsigned investigational product reconciliation entry.",
    keySignals: [
      "Training CAPA evidence is available.",
      "One pharmacy reconciliation entry remains unsigned.",
      "No fresh consent deviations were observed."
    ],
    reviewerPrompts: [
      "Determine whether the remaining pharmacy log issue is major or minor.",
      "Confirm whether CAPA closure evidence is sufficient for closure note."
    ],
    nextAction: "Use the inspection report generator to draft the closure-oriented site note."
  }
};

export const REDACTION_SAMPLE = {
  documentId: "doc-002",
  originalText: `Patient Name: Meera Sharma, Age: 47, Initials: MS, Phone: 9812345678.
Address: 14 Lake View Road, New Delhi 110021.
Hospital ID: HN-44721. Investigator: Dr. Arvind Rao.
Site Name: Apex Care Hospital, Bengaluru.
Sponsor Name: Helix Biotech Pvt Ltd.
Clinical note: Patient reported dizziness and rash two hours after IMP administration and was shifted for overnight observation.`,
  entities: [
    {
      id: "entity-01",
      label: "Patient Name",
      category: "PHI",
      value: "Meera Sharma",
      replacement: "[PATIENT_NAME_01]",
      confidence: 0.99,
      approved: true
    },
    {
      id: "entity-02",
      label: "Age",
      category: "PHI",
      value: "47",
      replacement: "[AGE_01]",
      confidence: 0.92,
      approved: true
    },
    {
      id: "entity-03",
      label: "Initials",
      category: "PHI",
      value: "MS",
      replacement: "[INITIALS_01]",
      confidence: 0.88,
      approved: true
    },
    {
      id: "entity-04",
      label: "Phone",
      category: "PII",
      value: "9812345678",
      replacement: "[PHONE_01]",
      confidence: 0.99,
      approved: true
    },
    {
      id: "entity-05",
      label: "Address",
      category: "PII",
      value: "14 Lake View Road, New Delhi 110021",
      replacement: "[ADDRESS_01]",
      confidence: 0.97,
      approved: true
    },
    {
      id: "entity-06",
      label: "Hospital ID",
      category: "PHI",
      value: "HN-44721",
      replacement: "[HOSPITAL_ID_01]",
      confidence: 0.98,
      approved: true
    },
    {
      id: "entity-07",
      label: "Investigator Name",
      category: "PII",
      value: "Dr. Arvind Rao",
      replacement: "[INVESTIGATOR_01]",
      confidence: 0.94,
      approved: true
    },
    {
      id: "entity-08",
      label: "Site Name",
      category: "PII",
      value: "Apex Care Hospital, Bengaluru",
      replacement: "[SITE_01]",
      confidence: 0.91,
      approved: true
    },
    {
      id: "entity-09",
      label: "Sponsor Name",
      category: "PII",
      value: "Helix Biotech Pvt Ltd",
      replacement: "[SPONSOR_01]",
      confidence: 0.89,
      approved: true
    }
  ] satisfies RedactionEntity[]
};

export const SAE_REVIEW_SEED = {
  narrative: `Subject AC-204 is a 47-year-old female with controlled type 2 diabetes enrolled in Protocol HBT-17.
On 11 April 2026, approximately 30 minutes after investigational product administration, the subject developed diffuse rash, hypotension, and breathing difficulty.
The subject was admitted to Apex Care Hospital for monitoring and intravenous antihistamines. The investigator assessed the event as serious due to hospitalisation and medically significant intervention.
Investigational product dosing was stopped. The subject improved within 24 hours and was discharged stable.
Concomitant medication history is not available in the initial report. Reporter signature page was not attached.`,
  fields: [
    {
      key: "patientProfile",
      label: "Patient profile",
      value: "47-year-old female subject with controlled type 2 diabetes enrolled in Protocol HBT-17.",
      evidence: [
        {
          id: "e1",
          label: "Demographic evidence",
          snippet: "Subject AC-204 is a 47-year-old female with controlled type 2 diabetes enrolled in Protocol HBT-17.",
          confidence: 0.97
        }
      ]
    },
    {
      key: "event",
      label: "Event",
      value: "Diffuse rash, hypotension, and breathing difficulty within 30 minutes of investigational product administration.",
      evidence: [
        {
          id: "e2",
          label: "Event timing",
          snippet: "Approximately 30 minutes after investigational product administration, the subject developed diffuse rash, hypotension, and breathing difficulty.",
          confidence: 0.95
        }
      ]
    },
    {
      key: "seriousnessCriteria",
      label: "Seriousness criteria",
      value: "Hospitalisation; Medically significant intervention",
      evidence: [
        {
          id: "e3",
          label: "Seriousness basis",
          snippet: "The investigator assessed the event as serious due to hospitalisation and medically significant intervention.",
          confidence: 0.93
        }
      ]
    },
    {
      key: "severity",
      label: "Severity",
      value: "Hospitalisation",
      evidence: [
        {
          id: "e4",
          label: "Disposition",
          snippet: "The subject was admitted to Apex Care Hospital for monitoring and intravenous antihistamines.",
          confidence: 0.94
        }
      ]
    },
    {
      key: "causality",
      label: "Causality",
      value: "Possibly related to investigational product pending concomitant medication review.",
      evidence: [
        {
          id: "e5",
          label: "Causality rationale",
          snippet: "Investigational product dosing was stopped and the subject improved within 24 hours.",
          confidence: 0.88
        }
      ]
    },
    {
      key: "actionTaken",
      label: "Action taken",
      value: "Dosing interrupted, subject monitored in hospital, IV antihistamines administered.",
      evidence: [
        {
          id: "e6",
          label: "Intervention",
          snippet: "Investigational product dosing was stopped. The subject improved within 24 hours and was discharged stable.",
          confidence: 0.9
        }
      ]
    },
    {
      key: "outcome",
      label: "Outcome",
      value: "Recovered and discharged stable within 24 hours.",
      evidence: [
        {
          id: "e7",
          label: "Outcome evidence",
          snippet: "The subject improved within 24 hours and was discharged stable.",
          confidence: 0.95
        }
      ]
    }
  ],
  missingInfo: ["Concomitant medication history", "Reporter signature page", "IMP lot number"]
};

export const COMPLETENESS_ISSUES: CompletenessIssue[] = [
  {
    id: "cmp-01",
    section: "Ethics",
    field: "Ethics Committee Approval Number",
    gapLevel: "Critical",
    status: "Open",
    comment: "",
    value: "Not provided",
    action: "Attach current EC approval reference before progression."
  },
  {
    id: "cmp-02",
    section: "Insurance",
    field: "Indemnity Document Reference",
    gapLevel: "High",
    status: "Open",
    comment: "",
    value: "Not provided",
    action: "Provide insurance or indemnity evidence."
  },
  {
    id: "cmp-03",
    section: "Ethics",
    field: "Informed Consent Version",
    gapLevel: "High",
    status: "Open",
    comment: "",
    value: "Not provided",
    action: "Reference the current approved consent version."
  },
  {
    id: "cmp-04",
    section: "Safety",
    field: "SAE Reporting Contact",
    gapLevel: "Medium",
    status: "Open",
    comment: "",
    value: "Not provided",
    action: "Provide designated safety escalation contact."
  }
];

export const VERSION_CHANGES: VersionChangeItem[] = [
  {
    id: "chg-01",
    area: "Eligibility",
    classification: "Substantive",
    impactLevel: "High",
    before: "Adults aged 18-65 years with HbA1c between 7.0% and 10.0%.",
    after: "Adults aged 18-70 years with HbA1c between 6.5% and 10.5%.",
    impact: "Expands recruitment pool and changes baseline risk assumptions. Reviewer should check justification and EC alignment."
  },
  {
    id: "chg-02",
    area: "Endpoint",
    classification: "Substantive",
    impactLevel: "High",
    before: "Reduction in severe flare count over 12 weeks.",
    after: "Reduction in moderate-to-severe flare count over 16 weeks.",
    impact: "Alters efficacy endpoint definition and observation window. Statistical and regulatory review required."
  },
  {
    id: "chg-03",
    area: "Consent Language",
    classification: "Substantive",
    impactLevel: "High",
    before: "Samples may be retained for protocol-specified safety analysis only.",
    after: "Samples may be retained for protocol-specified safety analysis and future biomarker research with subject authorization.",
    impact: "Introduces broader secondary use language that requires EC and privacy review."
  },
  {
    id: "chg-04",
    area: "Administrative",
    classification: "Administrative",
    impactLevel: "Low",
    before: "Medical monitor office address version 2.1",
    after: "Medical monitor office address version 3.0",
    impact: "Administrative contact update only; no direct participant safety impact."
  }
];

export const INSPECTION_SEED = {
  notes: `Site: Apex Care Hospital, Bengaluru
PI: Dr. Kavita Menon
Date: 12 Apr 2026
- Consent forms for subjects AC-110, AC-112, and AC-119 used superseded version 2.1 instead of approved version 2.3.
- SAE log for subject AC-204 updated late; evidence of 24-hour notification to sponsor not filed.
- IMP temperature log has missing entries on 08 Apr and 09 Apr.
- Delegation log and pharmacy binder were otherwise complete.`,
  findings: [
    {
      id: "finding-01",
      level: "Critical",
      title: "Superseded informed consent version used at site",
      evidence: "Subjects AC-110, AC-112, and AC-119 signed version 2.1 instead of approved version 2.3.",
      action: "Assess re-consent requirement and document CAPA within 48 hours."
    },
    {
      id: "finding-02",
      level: "Major",
      title: "Delayed SAE notification evidence",
      evidence: "SAE log for AC-204 updated late and sponsor notification evidence not filed.",
      action: "Reconstruct notification timeline and retrain site safety staff."
    },
    {
      id: "finding-03",
      level: "Minor",
      title: "Incomplete temperature log",
      evidence: "Missing IMP storage entries on 08 Apr and 09 Apr.",
      action: "Close the log gap and verify storage excursions."
    }
  ] satisfies InspectionFindingItem[]
};

export const AUDIT_EVENTS: DemoAuditEvent[] = [
  {
    id: "audit-01",
    timestamp: "14 Apr 2026, 2:02 pm",
    module: "Document Intake",
    action: "Classified incoming packet",
    confidence: 0.96,
    reviewerAction: "Queued for completeness",
    finalStatus: "Generated",
    sourceReference: "CT-23_SUGAM_submission_v1.pdf",
    note: "Detected SUGAM Application from form markers and annexure structure."
  },
  {
    id: "audit-02",
    timestamp: "14 Apr 2026, 2:04 pm",
    module: "Anonymisation",
    action: "Redaction draft produced",
    confidence: 0.95,
    reviewerAction: "Validation pending",
    finalStatus: "Generated",
    sourceReference: "SAE_narrative_subject_204.txt",
    note: "PII and PHI masked with entity-level confidence scoring."
  },
  {
    id: "audit-03",
    timestamp: "14 Apr 2026, 2:06 pm",
    module: "SAE Review",
    action: "Severity classification generated",
    confidence: 0.92,
    reviewerAction: "Override available",
    finalStatus: "Generated",
    sourceReference: "SAE_narrative_subject_204.txt",
    note: "Hospitalisation and medically significant intervention detected."
  },
  {
    id: "audit-04",
    timestamp: "14 Apr 2026, 2:08 pm",
    module: "Completeness Check",
    action: "Missing fields flagged",
    confidence: 0.97,
    reviewerAction: "Sponsor clarification required",
    finalStatus: "Generated",
    sourceReference: "CT-23-2026-1148",
    note: "Mandatory fields triaged into critical, high, and medium issues."
  },
  {
    id: "audit-05",
    timestamp: "14 Apr 2026, 2:10 pm",
    module: "Inspection Report",
    action: "Draft report assembled",
    confidence: 0.9,
    reviewerAction: "Review findings",
    finalStatus: "Generated",
    sourceReference: "site_visit_notes_photo.jpg",
    note: "Findings grouped by severity and linked to source note evidence."
  },
  {
    id: "audit-06",
    timestamp: "14 Apr 2026, 2:12 pm",
    module: "Version Compare",
    action: "Substantive changes summarised",
    confidence: 0.95,
    reviewerAction: "Impact note reviewed",
    finalStatus: "Generated",
    sourceReference: "protocol_amendment_3_redline.pdf",
    note: "Eligibility, endpoint, and consent wording changes were classified as substantive."
  },
  {
    id: "audit-07",
    timestamp: "14 Apr 2026, 1:59 pm",
    module: "Document Intake",
    action: "Structured synopsis created",
    confidence: 0.94,
    reviewerAction: "Reviewer prompts recorded",
    finalStatus: "Generated",
    sourceReference: "ec_transcript_09apr_subject_rights.txt",
    note: "Synopsis captured unresolved ethics questions and recommended sponsor follow-up."
  },
  {
    id: "audit-08",
    timestamp: "14 Apr 2026, 2:05 pm",
    module: "Anonymisation",
    action: "Low-confidence entity escalated",
    confidence: 0.89,
    reviewerAction: "Manual review required",
    finalStatus: "Escalated",
    sourceReference: "SAE_narrative_subject_204.txt",
    note: "Sponsor name and initials remained below the escalation threshold."
  },
  {
    id: "audit-09",
    timestamp: "14 Apr 2026, 2:14 pm",
    module: "Completeness Check",
    action: "Issue disposition updated",
    confidence: 1,
    reviewerAction: "Deficiency retained",
    finalStatus: "Completed",
    sourceReference: "CT-23-2026-1148",
    note: "Reviewer kept EC approval number as unresolved pending sponsor clarification."
  },
  {
    id: "audit-10",
    timestamp: "14 Apr 2026, 2:16 pm",
    module: "Audit Trail",
    action: "Audit export package prepared",
    confidence: 1,
    reviewerAction: "Traceability evidence retained",
    finalStatus: "Completed",
    sourceReference: "NIRNAY_AUDIT_PACKET_2026-04-14",
    note: "Search-filtered audit ledger compiled for supervisory review."
  }
];

export const RISK_CONTROL_TOPICS: RiskControlTopic[] = [
  {
    id: "risk-01",
    title: "Hallucination risk",
    concern: "Could the system invent a finding or missing field that is not supported by the source?",
    mitigation: [
      "Outputs are source-linked and evidence-backed.",
      "Confidence is shown to the reviewer instead of hidden.",
      "Low-confidence results are escalated, not silently accepted."
    ]
  },
  {
    id: "risk-02",
    title: "Missed PII",
    concern: "Could Nirnay fail to mask an identifier in a sensitive narrative?",
    mitigation: [
      "PII and PHI are surfaced as explicit entities before export.",
      "Reviewer approval can be captured at entity level.",
      "Low-confidence detections can be escalated into a separate queue."
    ]
  },
  {
    id: "risk-03",
    title: "Low-quality scans",
    concern: "How does the system behave when handwriting or OCR quality is poor?",
    mitigation: [
      "Intake marks binary documents as OCR-dependent and preserves that state.",
      "Inspection report generation stages progress so parsing quality is visible.",
      "Reviewers can edit the generated report inline before export."
    ]
  },
  {
    id: "risk-04",
    title: "Legal accountability",
    concern: "Who is accountable for the final regulatory decision?",
    mitigation: [
      "Nirnay is assistive only and never auto-disposes a case.",
      "Reviewer actions are the final logged disposition.",
      "Audit logs preserve timestamp, reviewer action, and source evidence."
    ]
  },
  {
    id: "risk-05",
    title: "Integration readiness",
    concern: "Can this be attached later to SUGAM and MD Online without rework?",
    mitigation: [
      "Outputs are structured as review artifacts, not chat transcripts.",
      "Document metadata, review packets, and audit logs are export-ready.",
      "Each workflow uses local mock services that can be swapped for APIs later."
    ]
  },
  {
    id: "risk-06",
    title: "Bias and model drift",
    concern: "How do reviewers detect drift or inconsistent AI recommendations over time?",
    mitigation: [
      "Confidence disclosure remains visible on every AI output.",
      "Audit trail enables longitudinal review of overrides and escalations.",
      "Human review remains mandatory for consequential determinations."
    ]
  },
  {
    id: "risk-07",
    title: "Human oversight",
    concern: "How is human oversight implemented in day-to-day operations?",
    mitigation: [
      "Accept, edit, override, resolve, and escalation actions are explicit.",
      "Pending reviewer actions are surfaced in the dashboard.",
      "No workflow reaches a final regulatory decision without reviewer intervention."
    ]
  }
];
