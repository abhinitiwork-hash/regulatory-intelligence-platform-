export type NavKey =
  | "dashboard"
  | "document-intake"
  | "anonymisation"
  | "sae-review"
  | "completeness-check"
  | "version-compare"
  | "inspection-report"
  | "audit-trail";

export type DocumentType =
  | "SUGAM Application"
  | "SAE Narrative"
  | "Meeting Transcript"
  | "Inspection Notes"
  | "Protocol Amendment";

export type GapLevel = "Critical" | "Major" | "Minor" | "Complete";

export type SeverityClassification =
  | "Death"
  | "Life-threatening"
  | "Hospitalisation"
  | "Disability"
  | "Medically significant"
  | "Non-serious";

export type ReviewerAction = "Pending" | "Accepted" | "Edited" | "Overridden";

export interface NavItem {
  id: NavKey;
  label: string;
  shortLabel: string;
  description: string;
}

export interface DashboardMetric {
  label: string;
  value: string;
  delta: string;
  tone: "blue" | "slate" | "amber" | "green" | "cyan";
}

export interface ReviewBoardSignal {
  id: string;
  title: string;
  status: string;
  metric: string;
  summary: string;
  tone: "blue" | "slate" | "amber" | "green" | "cyan" | "red";
  navTarget?: NavKey;
}

export interface IntelligenceModulePreview {
  id: string;
  code: string;
  title: string;
  summary: string;
  detail: string;
  status: string;
  tone: "blue" | "slate" | "amber" | "green" | "cyan";
  navTarget?: NavKey;
}

export interface RiskControlItem {
  id: string;
  title: string;
  metric: string;
  detail: string;
  tone: "blue" | "slate" | "amber" | "green" | "cyan" | "red";
}

export interface ProductTourStep {
  id: string;
  phase: string;
  title: string;
  summary: string;
  detail: string;
  signal: string;
  route: NavKey;
  safeguards: string[];
  outputs: string[];
}

export interface SourceDocument {
  id: string;
  name: string;
  format: string;
  source: string;
  description: string;
  documentType: DocumentType;
  confidence: number;
  extractedText?: string;
  ingestionNote?: string;
}

export interface IntakeClassification {
  documentType: DocumentType;
  confidence: number;
  rationale: string[];
}

export interface EntityDetection {
  label: string;
  category: "PII" | "PHI";
  value: string;
  redactedValue: string;
  confidence: number;
}

export interface AnonymisationResult {
  sourceReference: string;
  originalText: string;
  redactedText: string;
  entities: EntityDetection[];
  confidence: number;
  exportPayload: Record<string, unknown>;
}

export interface SaeReviewResult {
  patientProfile: string;
  event: string;
  seriousnessCriteria: string[];
  severity: SeverityClassification;
  causality: string;
  actionTaken: string;
  outcome: string;
  missingInfo: string[];
  confidence: number;
  sourceNarrative: string;
  exportPayload: Record<string, unknown>;
}

export interface RegulatoryFieldCheck {
  section: string;
  field: string;
  value: string;
  mandatory: boolean;
  gapLevel: GapLevel;
  status: "Present" | "Missing";
  actionNeeded: string;
}

export interface CompletenessResult {
  formName: string;
  completenessScore: number;
  fields: RegulatoryFieldCheck[];
  summary: {
    critical: number;
    major: number;
    minor: number;
  };
  exportPayload: Record<string, unknown>;
}

export interface VersionChange {
  id: string;
  area: string;
  before: string;
  after: string;
  impact: string;
  significance: "Substantive" | "Administrative";
  confidence: number;
}

export interface VersionCompareResult {
  baselineLabel: string;
  amendedLabel: string;
  summary: string;
  changes: VersionChange[];
  exportPayload: Record<string, unknown>;
}

export interface InspectionFinding {
  level: "Critical" | "Major" | "Minor";
  title: string;
  evidence: string;
  action: string;
}

export interface InspectionReport {
  siteDetails: {
    siteName: string;
    principalInvestigator: string;
    inspectionDate: string;
  };
  observations: string[];
  findings: InspectionFinding[];
  evidenceSummary: string[];
  recommendedAction: string[];
  formalReport: string;
  exportPayload: Record<string, unknown>;
}

export interface AuditEntry {
  id: string;
  module: string;
  action: string;
  actor: "AI" | "Reviewer" | "System";
  confidence: number;
  timestamp: string;
  sourceReference: string;
  status: ReviewerAction | "Generated" | "Logged";
  note: string;
}
