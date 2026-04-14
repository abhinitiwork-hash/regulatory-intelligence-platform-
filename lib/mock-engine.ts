import {
  AnonymisationResult,
  AuditEntry,
  CompletenessResult,
  DocumentType,
  InspectionFinding,
  InspectionReport,
  IntakeClassification,
  RegulatoryFieldCheck,
  SaeReviewResult,
  SeverityClassification,
  VersionCompareResult
} from "@/lib/types";
import {
  MOCK_GENERATED_AT,
  SAMPLE_FORM_OBJECT,
  SAMPLE_PROTOCOL_AMENDED,
  SAMPLE_PROTOCOL_BASELINE
} from "@/lib/mock-data";

const classificationOrder: Array<{
  type: DocumentType;
  keywords: RegExp;
  rationale: string[];
  confidence: number;
}> = [
  {
    type: "SAE Narrative",
    keywords: /(sae|serious adverse|narrative|subject)/i,
    rationale: [
      "Detected SAE and subject-level safety terminology.",
      "Narrative-style chronology suggests adverse event reporting."
    ],
    confidence: 0.98
  },
  {
    type: "Protocol Amendment",
    keywords: /(protocol|amendment|redline|endpoint|consent)/i,
    rationale: [
      "Matched protocol amendment markers in filename or text.",
      "Content typically routed for substantive change review."
    ],
    confidence: 0.95
  },
  {
    type: "Inspection Notes",
    keywords: /(inspection|site visit|finding|handwritten|note)/i,
    rationale: [
      "Inspection lexicon detected from source reference.",
      "Workflow routes to inspection report drafting."
    ],
    confidence: 0.93
  },
  {
    type: "Meeting Transcript",
    keywords: /(meeting|minutes|transcript|committee)/i,
    rationale: [
      "Meeting and committee signals suggest transcript summarisation.",
      "Sequential note structure matches review meeting material."
    ],
    confidence: 0.94
  }
];

const completenessRules: Array<{
  field: keyof typeof SAMPLE_FORM_OBJECT;
  section: string;
  label: string;
  missingLevel: "Critical" | "Major" | "Minor";
  actionNeeded: string;
}> = [
  {
    field: "applicationId",
    section: "Administrative",
    label: "Application ID",
    missingLevel: "Critical",
    actionNeeded: "Attach the registered CDSCO application identifier."
  },
  {
    field: "sponsorName",
    section: "Administrative",
    label: "Sponsor Name",
    missingLevel: "Critical",
    actionNeeded: "Provide the legal sponsor entity name."
  },
  {
    field: "studyTitle",
    section: "Study Metadata",
    label: "Study Title",
    missingLevel: "Major",
    actionNeeded: "Insert the approved protocol title."
  },
  {
    field: "principalInvestigator",
    section: "Site Information",
    label: "Principal Investigator",
    missingLevel: "Critical",
    actionNeeded: "Add the PI responsible for the submission."
  },
  {
    field: "ethicsCommitteeApprovalNumber",
    section: "Ethics",
    label: "Ethics Committee Approval Number",
    missingLevel: "Critical",
    actionNeeded: "Attach the current ethics committee approval reference."
  },
  {
    field: "siteAddress",
    section: "Site Information",
    label: "Site Address",
    missingLevel: "Major",
    actionNeeded: "Enter the primary study site address."
  },
  {
    field: "indemnityDocumentReference",
    section: "Insurance",
    label: "Indemnity Document Reference",
    missingLevel: "Major",
    actionNeeded: "Provide indemnity or insurance coverage evidence."
  },
  {
    field: "subjectCompensationPlan",
    section: "Participant Safety",
    label: "Subject Compensation Plan",
    missingLevel: "Major",
    actionNeeded: "Describe compensation approach for trial-related injury."
  },
  {
    field: "protocolVersion",
    section: "Study Metadata",
    label: "Protocol Version",
    missingLevel: "Critical",
    actionNeeded: "Attach the reviewed protocol version identifier."
  },
  {
    field: "informedConsentVersion",
    section: "Ethics",
    label: "Informed Consent Version",
    missingLevel: "Major",
    actionNeeded: "Reference the current approved consent form version."
  },
  {
    field: "manufacturingLicenceReference",
    section: "Product",
    label: "Manufacturing Licence Reference",
    missingLevel: "Major",
    actionNeeded: "Link the manufacturing or import licence reference."
  },
  {
    field: "saeReportingContact",
    section: "Safety",
    label: "SAE Reporting Contact",
    missingLevel: "Minor",
    actionNeeded: "Provide the designated SAE contact for escalation."
  },
  {
    field: "investigationalProductStoragePlan",
    section: "Product",
    label: "Investigational Product Storage Plan",
    missingLevel: "Major",
    actionNeeded: "Document storage conditions and monitoring plan."
  },
  {
    field: "medicalMonitorName",
    section: "Safety",
    label: "Medical Monitor Name",
    missingLevel: "Minor",
    actionNeeded: "Name the medical monitor or safety physician."
  }
];

export function classifyDocument(reference: string): IntakeClassification {
  const lower = reference.toLowerCase();

  for (const option of classificationOrder) {
    if (option.keywords.test(lower)) {
      return {
        documentType: option.type,
        confidence: option.confidence,
        rationale: option.rationale
      };
    }
  }

  return {
    documentType: "SUGAM Application",
    confidence: 0.91,
    rationale: [
      "Defaulted to submission intake based on regulated document naming pattern.",
      "Production classifier would call OCR and a document-routing model here."
    ]
  };
}

export function generateAnonymisationResult(
  text: string,
  sourceReference: string
): AnonymisationResult {
  const rules = [
    {
      label: "Patient Name",
      category: "PHI" as const,
      pattern: /Meera Sharma/gi,
      replacement: "[PATIENT_NAME_01]",
      confidence: 0.99
    },
    {
      label: "Age",
      category: "PHI" as const,
      pattern: /\b47\b/g,
      replacement: "[AGE_01]",
      confidence: 0.93
    },
    {
      label: "Initials",
      category: "PHI" as const,
      pattern: /\bMS\b/g,
      replacement: "[INITIALS_01]",
      confidence: 0.9
    },
    {
      label: "Phone",
      category: "PII" as const,
      pattern: /\b9812345678\b/g,
      replacement: "[PHONE_01]",
      confidence: 0.99
    },
    {
      label: "Address",
      category: "PII" as const,
      pattern: /14 Lake View Road, New Delhi 110021/gi,
      replacement: "[ADDRESS_01]",
      confidence: 0.97
    },
    {
      label: "Hospital ID",
      category: "PHI" as const,
      pattern: /\bHN-44721\b/g,
      replacement: "[HOSPITAL_ID_01]",
      confidence: 0.98
    },
    {
      label: "Investigator Name",
      category: "PII" as const,
      pattern: /Dr\. Arvind Rao/gi,
      replacement: "[INVESTIGATOR_01]",
      confidence: 0.95
    },
    {
      label: "Site Name",
      category: "PII" as const,
      pattern: /Apex Care Hospital, Bengaluru/gi,
      replacement: "[SITE_01]",
      confidence: 0.94
    },
    {
      label: "Sponsor Name",
      category: "PII" as const,
      pattern: /Helix Biotech Pvt Ltd/gi,
      replacement: "[SPONSOR_01]",
      confidence: 0.94
    }
  ];

  let redactedText = text;
  const entities = rules.flatMap((rule) => {
    const matches = Array.from(text.matchAll(rule.pattern));

    if (matches.length === 0) {
      return [];
    }

    redactedText = redactedText.replace(rule.pattern, rule.replacement);

    return matches.map((match, index) => ({
      label: rule.label,
      category: rule.category,
      value: match[0],
      redactedValue:
        matches.length > 1 ? `${rule.replacement}_${index + 1}` : rule.replacement,
      confidence: rule.confidence
    }));
  });

  const confidence =
    entities.reduce((sum, item) => sum + item.confidence, 0) / (entities.length || 1);

  return {
    sourceReference,
    originalText: text,
    redactedText,
    entities,
    confidence,
    exportPayload: {
      sourceReference,
      generatedAt: MOCK_GENERATED_AT,
      schemaVersion: "nirnay/anonymisation/v1",
      redactedText,
      entities
    }
  };
}

function classifySeverity(narrative: string): SeverityClassification {
  const lower = narrative.toLowerCase();

  if (lower.includes("death") || lower.includes("expired")) {
    return "Death";
  }

  if (lower.includes("life-threatening") || lower.includes("icu")) {
    return "Life-threatening";
  }

  if (lower.includes("admitted") || lower.includes("hospital")) {
    return "Hospitalisation";
  }

  if (lower.includes("disability")) {
    return "Disability";
  }

  if (lower.includes("medically significant") || lower.includes("intervention")) {
    return "Medically significant";
  }

  return "Non-serious";
}

export function parseSaeNarrative(narrative: string): SaeReviewResult {
  const severity = classifySeverity(narrative);

  const result: SaeReviewResult = {
    patientProfile: "47-year-old female subject with controlled type 2 diabetes; Protocol HBT-17",
    event:
      "Diffuse rash, hypotension, and breathing difficulty within 30 minutes of investigational product administration.",
    seriousnessCriteria: ["Hospitalisation", "Medically significant intervention"],
    severity,
    causality: "Possibly related to investigational product pending full concomitant medication review.",
    actionTaken:
      "Dosing interrupted, subject admitted for monitoring, IV antihistamines administered, sponsor notification initiated.",
    outcome: "Recovered and discharged stable within 24 hours.",
    missingInfo: [
      "Concomitant medication history",
      "Reporter signature page",
      "Lot number of administered investigational product"
    ],
    confidence: 0.92,
    sourceNarrative: narrative,
    exportPayload: {
      generatedAt: MOCK_GENERATED_AT,
      schemaVersion: "nirnay/sae-review/v1",
      severity,
      seriousnessCriteria: ["Hospitalisation", "Medically significant intervention"],
      narrative
    }
  };

  return result;
}

export function runCompletenessCheck(form = SAMPLE_FORM_OBJECT): CompletenessResult {
  const fields: RegulatoryFieldCheck[] = completenessRules.map((rule) => {
    const rawValue = form[rule.field];
    const value = typeof rawValue === "string" ? rawValue : "";
    const missing = value.trim().length === 0;

    return {
      section: rule.section,
      field: rule.label,
      value: missing ? "Not provided" : value,
      mandatory: true,
      gapLevel: missing ? rule.missingLevel : "Complete",
      status: missing ? "Missing" : "Present",
      actionNeeded: missing ? rule.actionNeeded : "No reviewer action required."
    };
  });

  const missingFields = fields.filter((field) => field.status === "Missing");
  const completenessScore = Math.round(
    ((fields.length - missingFields.length) / fields.length) * 100
  );

  return {
    formName: "Stage 1 CDSCO Submission Packet",
    completenessScore,
    fields,
    summary: {
      critical: missingFields.filter((field) => field.gapLevel === "Critical").length,
      major: missingFields.filter((field) => field.gapLevel === "Major").length,
      minor: missingFields.filter((field) => field.gapLevel === "Minor").length
    },
    exportPayload: {
      generatedAt: MOCK_GENERATED_AT,
      schemaVersion: "nirnay/completeness/v1",
      completenessScore,
      missingFields: missingFields.map((field) => ({
        field: field.field,
        gapLevel: field.gapLevel,
        actionNeeded: field.actionNeeded
      }))
    }
  };
}

export function compareProtocolVersions(
  baseline = SAMPLE_PROTOCOL_BASELINE,
  amended = SAMPLE_PROTOCOL_AMENDED
): VersionCompareResult {
  const changes = [
    {
      id: "change-eligibility",
      area: "Eligibility criteria",
      before: "Adults aged 18-65 years with HbA1c between 7.0% and 10.0%.",
      after: "Adults aged 18-70 years with HbA1c between 6.5% and 10.5%.",
      impact:
        "Expands the recruitment pool and shifts baseline risk assumptions. Reviewer should confirm updated justification and ethics approval alignment.",
      significance: "Substantive" as const,
      confidence: 0.94
    },
    {
      id: "change-endpoint",
      area: "Primary endpoint",
      before: "Reduction in severe flare count over 12 weeks.",
      after: "Reduction in moderate-to-severe flare count over 16 weeks.",
      impact:
        "Alters efficacy endpoint definition and observation window. Requires revalidation of statistical analysis and amendment tracking.",
      significance: "Substantive" as const,
      confidence: 0.97
    },
    {
      id: "change-consent",
      area: "Consent wording",
      before: "Samples may be retained for protocol-specified safety analysis only.",
      after:
        "Samples may be retained for protocol-specified safety analysis and future biomarker research with subject authorization.",
      impact:
        "Introduces broader secondary use language. Reviewer should verify subject consent language, EC approval, and data protection controls.",
      significance: "Substantive" as const,
      confidence: 0.95
    }
  ];

  return {
    baselineLabel: "Protocol v2.1",
    amendedLabel: "Protocol v3.0",
    summary: "Three substantive amendments detected across eligibility, endpoint, and consent language.",
    changes,
    exportPayload: {
      generatedAt: MOCK_GENERATED_AT,
      schemaVersion: "nirnay/version-compare/v1",
      baseline,
      amended,
      changes
    }
  };
}

export function generateInspectionReport(notes: string): InspectionReport {
  const siteMatch = notes.match(/Site:\s*(.+)/i);
  const piMatch = notes.match(/PI:\s*(.+)/i);
  const dateMatch = notes.match(/Date:\s*(.+)/i);
  const observations = notes
    .split("\n")
    .map((line) => line.trim())
    .filter((line) => line.startsWith("-"))
    .map((line) => line.replace(/^-+\s*/, ""));

  const findings: InspectionFinding[] = [];

  if (/superseded version/i.test(notes)) {
    findings.push({
      level: "Critical",
      title: "Outdated informed consent version in use",
      evidence:
        "Three subject files referenced consent form version 2.1 instead of approved version 2.3.",
      action:
        "Quarantine impacted subject files, assess re-consent requirement, and document CAPA within 48 hours."
    });
  }

  if (/24-hour notification/i.test(notes) || /updated late/i.test(notes)) {
    findings.push({
      level: "Major",
      title: "Delayed SAE notification evidence",
      evidence:
        "SAE log for subject AC-204 was updated late and sponsor notification evidence was missing.",
      action:
        "Reconstruct the notification timeline and retrain the site safety reporting team."
    });
  }

  if (/temperature log/i.test(notes)) {
    findings.push({
      level: "Minor",
      title: "Incomplete investigational product temperature log",
      evidence: "Temperature entries were absent on 08 Apr and 09 Apr.",
      action:
        "Close the log gap, verify storage excursions, and strengthen daily pharmacy checks."
    });
  }

  const evidenceSummary = findings.map(
    (finding) => `${finding.level}: ${finding.title} - ${finding.evidence}`
  );
  const recommendedAction = findings.map((finding) => finding.action);

  const formalReport = [
    "CDSCO Inspection Report Draft",
    `Site: ${siteMatch?.[1] ?? "Not captured"}`,
    `Principal Investigator: ${piMatch?.[1] ?? "Not captured"}`,
    `Inspection Date: ${dateMatch?.[1] ?? "Not captured"}`,
    "",
    "Observations:",
    ...observations.map((item) => `- ${item}`),
    "",
    "Findings:",
    ...findings.map((item) => `- [${item.level}] ${item.title}: ${item.evidence}`),
    "",
    "Recommended Actions:",
    ...recommendedAction.map((item) => `- ${item}`)
  ].join("\n");

  return {
    siteDetails: {
      siteName: siteMatch?.[1] ?? "Not captured",
      principalInvestigator: piMatch?.[1] ?? "Not captured",
      inspectionDate: dateMatch?.[1] ?? "Not captured"
    },
    observations,
    findings,
    evidenceSummary,
    recommendedAction,
    formalReport,
    exportPayload: {
      generatedAt: MOCK_GENERATED_AT,
      schemaVersion: "nirnay/inspection-report/v1",
      siteDetails: {
        siteName: siteMatch?.[1] ?? "Not captured",
        principalInvestigator: piMatch?.[1] ?? "Not captured",
        inspectionDate: dateMatch?.[1] ?? "Not captured"
      },
      findings
    }
  };
}

export function createAuditEntry(input: {
  id: string;
  module: string;
  action: string;
  actor: "AI" | "Reviewer" | "System";
  confidence: number;
  timestamp: string;
  sourceReference: string;
  status: AuditEntry["status"];
  note: string;
}): AuditEntry {
  return {
    id: input.id,
    module: input.module,
    action: input.action,
    actor: input.actor,
    confidence: input.confidence,
    timestamp: input.timestamp,
    sourceReference: input.sourceReference,
    status: input.status,
    note: input.note
  };
}
