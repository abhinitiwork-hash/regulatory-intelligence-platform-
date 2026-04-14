export type DemoRoute =
  | "/"
  | "/tour"
  | "/dashboard"
  | "/document-intake"
  | "/anonymisation"
  | "/sae-review"
  | "/completeness-check"
  | "/version-compare"
  | "/inspection-report"
  | "/audit-trail"
  | "/risk-controls";

export type RiskLevel = "Low" | "Medium" | "High" | "Critical";
export type DemoStatus =
  | "Queued"
  | "Classifying"
  | "Ready for Review"
  | "In Review"
  | "Escalated"
  | "Completed";

export type DemoStage =
  | "Document Intake"
  | "Anonymisation"
  | "Intelligence"
  | "Human Review"
  | "Audit Output";

export interface ReviewerUser {
  id: string;
  name: string;
  role: string;
  focus: string;
}

export interface DemoDocument {
  id: string;
  name: string;
  format: "PDF" | "DOCX" | "TXT" | "IMG";
  documentType:
    | "SUGAM Application"
    | "SAE Narrative"
    | "Meeting Transcript"
    | "Inspection Notes"
    | "Protocol Amendment";
  source: string;
  stage: DemoStage;
  status: DemoStatus;
  riskLevel: RiskLevel;
  confidence: number;
  updatedAt: string;
  assignedModule: string;
  reviewer: string;
  summary: string;
  preview: string;
  metadata: Record<string, string>;
  tags: string[];
}

export interface DemoMetric {
  id: string;
  label: string;
  value: number;
  suffix?: string;
  detail: string;
}

export interface DemoPriorityItem {
  id: string;
  title: string;
  riskLevel: RiskLevel;
  owner: string;
  summary: string;
  nextStep: string;
  route: DemoRoute;
}

export interface ModuleShortcut {
  id: string;
  title: string;
  description: string;
  route: DemoRoute;
  badge: string;
}

export interface RedactionEntity {
  id: string;
  label:
    | "Patient Name"
    | "Age"
    | "Initials"
    | "Phone"
    | "Address"
    | "Hospital ID"
    | "Investigator Name"
    | "Site Name"
    | "Sponsor Name";
  category: "PII" | "PHI";
  value: string;
  replacement: string;
  confidence: number;
  approved: boolean;
}

export interface EvidenceSnippet {
  id: string;
  label: string;
  snippet: string;
  confidence: number;
}

export interface SaeField {
  key:
    | "patientProfile"
    | "event"
    | "seriousnessCriteria"
    | "severity"
    | "causality"
    | "actionTaken"
    | "outcome";
  label: string;
  value: string;
  evidence: EvidenceSnippet[];
}

export interface CompletenessIssue {
  id: string;
  section: string;
  field: string;
  gapLevel: RiskLevel;
  status: "Open" | "Resolved" | "Accepted";
  comment: string;
  value: string;
  action: string;
}

export interface VersionChangeItem {
  id: string;
  area: "Eligibility" | "Safety" | "Endpoint" | "Consent Language" | "Administrative";
  classification: "Substantive" | "Administrative";
  impactLevel: RiskLevel;
  before: string;
  after: string;
  impact: string;
}

export interface InspectionFindingItem {
  id: string;
  level: "Critical" | "Major" | "Minor";
  title: string;
  evidence: string;
  action: string;
}

export interface DemoAuditEvent {
  id: string;
  timestamp: string;
  module: string;
  action: string;
  confidence: number;
  reviewerAction: string;
  finalStatus: string;
  sourceReference: string;
  note: string;
}

export interface RiskControlTopic {
  id: string;
  title: string;
  concern: string;
  mitigation: string[];
}

export interface TourStep {
  id: string;
  title: string;
  route: DemoRoute;
  signal: string;
  detail: string;
  outputs: string[];
}

export interface IntakeSynopsis {
  headline: string;
  confidence: number;
  summary: string;
  keySignals: string[];
  reviewerPrompts: string[];
  nextAction: string;
}

export interface JudgingFlowStep {
  id: string;
  route: DemoRoute;
  label: string;
  purpose: string;
  requirement: string;
  strongMoment: string;
}

export interface ToastItem {
  id: string;
  title: string;
  description: string;
  tone: "info" | "success" | "warning" | "danger";
}
