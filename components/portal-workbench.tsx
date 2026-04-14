"use client";

import { ChangeEvent, useState } from "react";
import { AuditTrailModule } from "@/components/modules/audit-trail-module";
import { AnonymisationModule } from "@/components/modules/anonymisation-module";
import { CompletenessCheckModule } from "@/components/modules/completeness-check-module";
import { DashboardOverview } from "@/components/modules/dashboard-overview";
import { DocumentIntakeModule } from "@/components/modules/document-intake-module";
import { InspectionReportModule } from "@/components/modules/inspection-report-module";
import { SaeReviewModule } from "@/components/modules/sae-review-module";
import { VersionCompareModule } from "@/components/modules/version-compare-module";
import { Sidebar } from "@/components/sidebar";
import {
  DASHBOARD_METRICS,
  INITIAL_AUDIT_TRAIL,
  NAV_ITEMS,
  SAMPLE_ANONYMISATION_TEXT,
  SAMPLE_DOCUMENTS,
  SAMPLE_INSPECTION_NOTES,
  SAMPLE_SAE_NARRATIVE
} from "@/lib/mock-data";
import {
  classifyDocument,
  compareProtocolVersions,
  createAuditEntry,
  generateAnonymisationResult,
  generateInspectionReport,
  parseSaeNarrative,
  runCompletenessCheck
} from "@/lib/mock-engine";
import {
  AuditEntry,
  InspectionReport,
  NavKey,
  SaeReviewResult,
  SourceDocument
} from "@/lib/types";

const defaultDocument = SAMPLE_DOCUMENTS[0];

function buildTimestamp() {
  return new Intl.DateTimeFormat("en-IN", {
    dateStyle: "medium",
    timeStyle: "short",
    timeZone: "Asia/Kolkata"
  }).format(new Date());
}

function nextAuditId(entries: AuditEntry[]) {
  return `audit-${entries.length + 1}`;
}

export function PortalWorkbench() {
  const [selectedNav, setSelectedNav] = useState<NavKey>("dashboard");
  const [documents, setDocuments] = useState<SourceDocument[]>(SAMPLE_DOCUMENTS);
  const [activeDocument, setActiveDocument] = useState<SourceDocument | null>(defaultDocument);
  const [classification, setClassification] = useState(() =>
    classifyDocument(defaultDocument.name)
  );
  const [uploadedText, setUploadedText] = useState("");
  const [intakeError, setIntakeError] = useState<string | null>(null);
  const [anonymisationResult, setAnonymisationResult] = useState(() =>
    generateAnonymisationResult(SAMPLE_ANONYMISATION_TEXT, defaultDocument.name)
  );
  const [saeReview, setSaeReview] = useState<SaeReviewResult>(() =>
    parseSaeNarrative(SAMPLE_SAE_NARRATIVE)
  );
  const [inspectionNotes, setInspectionNotes] = useState(SAMPLE_INSPECTION_NOTES);
  const [inspectionError, setInspectionError] = useState<string | null>(null);
  const [inspectionReport, setInspectionReport] = useState<InspectionReport | null>(() =>
    generateInspectionReport(SAMPLE_INSPECTION_NOTES)
  );
  const [auditEntries, setAuditEntries] = useState(INITIAL_AUDIT_TRAIL);

  const completenessResult = runCompletenessCheck();
  const versionCompareResult = compareProtocolVersions();

  function appendAudit(entry: Omit<AuditEntry, "id">) {
    setAuditEntries((current) => [
      createAuditEntry({
        ...entry,
        id: nextAuditId(current)
      }),
      ...current
    ]);
  }

  function syncDocumentContext(document: SourceDocument) {
    setActiveDocument(document);
    setClassification(classifyDocument(document.name));

    const sourceText = document.extractedText || uploadedText || SAMPLE_ANONYMISATION_TEXT;
    setAnonymisationResult(generateAnonymisationResult(sourceText, document.name));

    if (document.documentType === "SAE Narrative" || document.name.toLowerCase().includes("sae")) {
      setSaeReview(parseSaeNarrative(document.extractedText || SAMPLE_SAE_NARRATIVE));
    }
  }

  function handleSampleSelect(document: SourceDocument) {
    setIntakeError(null);
    syncDocumentContext(document);
    setSelectedNav("document-intake");

    appendAudit({
      module: "Document Intake",
      action: "Sample packet loaded",
      actor: "System",
      confidence: document.confidence,
      timestamp: buildTimestamp(),
      sourceReference: document.name,
      status: "Logged",
      note: `Loaded seeded ${document.documentType} packet for demo review.`
    });
  }

  function handleFileChange(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];

    if (!file) {
      return;
    }

    const allowed = /\.(pdf|docx|txt|png|jpg|jpeg)$/i.test(file.name);

    if (!allowed) {
      setIntakeError("Unsupported format. Upload PDF, DOCX, TXT, JPG, or PNG.");
      return;
    }

    setIntakeError(null);

    const classificationResult = classifyDocument(file.name);
    const draftDocument: SourceDocument = {
      id: `uploaded-${Date.now()}`,
      name: file.name,
      format: file.name.split(".").pop()?.toUpperCase() ?? "FILE",
      source: "Local upload",
      description: "User-uploaded document in the Nirnay Portal workbench.",
      documentType: classificationResult.documentType,
      confidence: classificationResult.confidence,
      ingestionNote:
        file.type.startsWith("image/") || !file.name.toLowerCase().endsWith(".txt")
          ? "Binary document accepted. OCR/parser integration would extract text in production."
          : undefined
    };

    setClassification(classificationResult);
    setActiveDocument(draftDocument);
    setDocuments((current) => [draftDocument, ...current.filter((item) => item.id !== draftDocument.id)]);
    setSelectedNav("document-intake");

    appendAudit({
      module: "Document Intake",
      action: "Uploaded packet classified",
      actor: "AI",
      confidence: classificationResult.confidence,
      timestamp: buildTimestamp(),
      sourceReference: file.name,
      status: "Generated",
      note: `Detected ${classificationResult.documentType} from uploaded source reference.`
    });

    if (file.name.toLowerCase().endsWith(".txt")) {
      const reader = new FileReader();

      reader.onload = () => {
        const text = typeof reader.result === "string" ? reader.result : "";

        setUploadedText(text);

        const enrichedDocument = {
          ...draftDocument,
          extractedText: text
        };

        setActiveDocument(enrichedDocument);
        setDocuments((current) =>
          current.map((item) => (item.id === draftDocument.id ? enrichedDocument : item))
        );

        // Backend integration point: replace this with OCR/parser service output for PDF/DOCX/image inputs.
        setAnonymisationResult(generateAnonymisationResult(text || SAMPLE_ANONYMISATION_TEXT, file.name));

        if (classificationResult.documentType === "SAE Narrative") {
          setSaeReview(parseSaeNarrative(text || SAMPLE_SAE_NARRATIVE));
        }
      };

      reader.readAsText(file);
      return;
    }

    setUploadedText("");
    setAnonymisationResult(generateAnonymisationResult(SAMPLE_ANONYMISATION_TEXT, file.name));
  }

  function handleAnonymisationExport() {
    appendAudit({
      module: "Anonymisation",
      action: "Anonymised JSON exported",
      actor: "Reviewer",
      confidence: anonymisationResult?.confidence ?? 1,
      timestamp: buildTimestamp(),
      sourceReference: activeDocument?.name ?? "Unknown source",
      status: "Accepted",
      note: "Reviewer exported the anonymised payload for downstream handling."
    });
  }

  function handleSaeFieldChange(
    field:
      | "patientProfile"
      | "event"
      | "causality"
      | "actionTaken"
      | "outcome"
      | "missingInfo",
    value: string | string[]
  ) {
    setSaeReview((current) => {
      if (field === "missingInfo") {
        return {
          ...current,
          missingInfo: Array.isArray(value) ? value : current.missingInfo,
          exportPayload: {
            ...current.exportPayload,
            missingInfo: Array.isArray(value) ? value : current.missingInfo
          }
        };
      }

      return {
        ...current,
        [field]: typeof value === "string" ? value : current[field],
        exportPayload: {
          ...current.exportPayload,
          [field]: typeof value === "string" ? value : current[field]
        }
      };
    });
  }

  function handleSaeAccept() {
    appendAudit({
      module: "SAE Review",
      action: "AI extraction accepted",
      actor: "Reviewer",
      confidence: saeReview.confidence,
      timestamp: buildTimestamp(),
      sourceReference: activeDocument?.name ?? "SAE narrative",
      status: "Accepted",
      note: `Reviewer accepted severity classification as ${saeReview.severity}.`
    });
  }

  function handleSaeSave() {
    appendAudit({
      module: "SAE Review",
      action: "Reviewer edits saved",
      actor: "Reviewer",
      confidence: 1,
      timestamp: buildTimestamp(),
      sourceReference: activeDocument?.name ?? "SAE narrative",
      status: "Edited",
      note: "Structured SAE fields were revised before final reviewer determination."
    });
  }

  function handleSaeOverride(severity: SaeReviewResult["severity"]) {
    setSaeReview((current) => ({
      ...current,
      severity,
      exportPayload: {
        ...current.exportPayload,
        severity,
        reviewerOverride: true
      }
    }));

    appendAudit({
      module: "SAE Review",
      action: "Severity overridden",
      actor: "Reviewer",
      confidence: 1,
      timestamp: buildTimestamp(),
      sourceReference: activeDocument?.name ?? "SAE narrative",
      status: "Overridden",
      note: `Reviewer set final seriousness disposition to ${severity}.`
    });
  }

  function handleCompletenessLog() {
    appendAudit({
      module: "Completeness Check",
      action: "Reviewer follow-up logged",
      actor: "Reviewer",
      confidence: 1,
      timestamp: buildTimestamp(),
      sourceReference: "CT-23-2026-1148",
      status: "Logged",
      note: "Reviewer marked missing regulatory fields for sponsor clarification."
    });
  }

  function handleVersionEscalation() {
    appendAudit({
      module: "Version Compare",
      action: "Amendment review escalated",
      actor: "Reviewer",
      confidence: 1,
      timestamp: buildTimestamp(),
      sourceReference: "protocol_amendment_3_redline.pdf",
      status: "Logged",
      note: "Substantive protocol deltas routed for formal amendment review."
    });
  }

  function handleGenerateInspectionReport() {
    if (!inspectionNotes.trim()) {
      setInspectionError("Add rough inspection notes before generating a report draft.");
      setInspectionReport(null);
      return;
    }

    setInspectionError(null);
    const report = generateInspectionReport(inspectionNotes);
    setInspectionReport(report);

    appendAudit({
      module: "Inspection Report",
      action: "Inspection report generated",
      actor: "AI",
      confidence: report.findings.length ? 0.9 : 0.72,
      timestamp: buildTimestamp(),
      sourceReference: activeDocument?.name ?? "Inspection notes",
      status: "Generated",
      note: "Draft report assembled from unstructured site inspection notes."
    });
  }

  return (
    <main className="shell">
      <Sidebar items={NAV_ITEMS} onSelect={setSelectedNav} selected={selectedNav} />

      <section className="workspace">
        <header className="workspace__header">
          <div>
            <span className="workspace__eyebrow">Nirnay Portal</span>
            <h2>Regulatory intelligence cockpit</h2>
            <p>
              Privacy, traceability, and reviewer control across document intake,
              safety assessment, regulatory completeness, and inspection workflows.
            </p>
          </div>
          <div className="workspace__status">
            <div>
              <span>Current case</span>
              <strong>{activeDocument?.name ?? "No document selected"}</strong>
            </div>
            <div>
              <span>Mode</span>
              <strong>Assistive AI · Reviewer controlled</strong>
            </div>
          </div>
        </header>

        {selectedNav === "dashboard" ? (
          <DashboardOverview
            documents={documents}
            metrics={DASHBOARD_METRICS}
            onNavigate={setSelectedNav}
          />
        ) : null}

        {selectedNav === "document-intake" ? (
          <DocumentIntakeModule
            activeDocument={activeDocument}
            classification={classification}
            documents={documents}
            intakeError={intakeError}
            onFileChange={handleFileChange}
            onSelectSample={handleSampleSelect}
          />
        ) : null}

        {selectedNav === "anonymisation" ? (
          <AnonymisationModule onExport={handleAnonymisationExport} result={anonymisationResult} />
        ) : null}

        {selectedNav === "sae-review" ? (
          <SaeReviewModule
            onAccept={handleSaeAccept}
            onFieldChange={handleSaeFieldChange}
            onOverride={handleSaeOverride}
            onSaveEdits={handleSaeSave}
            review={saeReview}
          />
        ) : null}

        {selectedNav === "completeness-check" ? (
          <CompletenessCheckModule
            onLogReviewerAction={handleCompletenessLog}
            result={completenessResult}
          />
        ) : null}

        {selectedNav === "version-compare" ? (
          <VersionCompareModule
            onLogEscalation={handleVersionEscalation}
            result={versionCompareResult}
          />
        ) : null}

        {selectedNav === "inspection-report" ? (
          <InspectionReportModule
            error={inspectionError}
            notes={inspectionNotes}
            onGenerate={handleGenerateInspectionReport}
            onNotesChange={setInspectionNotes}
            report={inspectionReport}
          />
        ) : null}

        {selectedNav === "audit-trail" ? <AuditTrailModule entries={auditEntries} /> : null}
      </section>
    </main>
  );
}
