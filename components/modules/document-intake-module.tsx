import type { ChangeEvent } from "react";
import { Badge } from "@/components/ui/badge";
import { ConfidenceMeter } from "@/components/ui/confidence-meter";
import { SectionCard } from "@/components/ui/section-card";
import { IntakeClassification, SourceDocument } from "@/lib/types";

export function DocumentIntakeModule({
  documents,
  activeDocument,
  classification,
  intakeError,
  onFileChange,
  onSelectSample
}: {
  documents: SourceDocument[];
  activeDocument: SourceDocument | null;
  classification: IntakeClassification | null;
  intakeError: string | null;
  onFileChange: (event: ChangeEvent<HTMLInputElement>) => void;
  onSelectSample: (document: SourceDocument) => void;
}) {
  return (
    <div className="module-stack">
      <SectionCard
        title="Document Intake"
        description="Accepts PDF, DOCX, TXT, and image placeholders, then routes each packet into the correct review workflow."
      >
        <div className="upload-grid">
          <label className="upload-dropzone">
            <input
              accept=".pdf,.docx,.txt,image/*"
              className="sr-only"
              onChange={onFileChange}
              type="file"
            />
            <span className="upload-dropzone__eyebrow">Upload packet</span>
            <strong>Drop a document here or browse</strong>
            <p>Supported: PDF, DOCX, TXT, JPG, PNG. Binary files use placeholder extraction in this MVP.</p>
          </label>

          <div className="callout callout--slate">
            <strong>Ingestion architecture</strong>
            <p>
              File upload works today with mock routing. OCR, parser, and case metadata APIs plug in
              at this boundary later.
            </p>
            <div className="token-list">
              <Badge tone="slate">Classifier</Badge>
              <Badge tone="slate">OCR Adapter</Badge>
              <Badge tone="slate">SUGAM Sync Ready</Badge>
            </div>
          </div>
        </div>

        {intakeError ? (
          <div className="callout callout--red">
            <strong>Upload validation</strong>
            <p>{intakeError}</p>
          </div>
        ) : null}

        <div className="sample-grid">
          {documents.map((document) => (
            <button
              key={document.id}
              className={`sample-card ${
                activeDocument?.id === document.id ? "sample-card--active" : ""
              }`}
              onClick={() => onSelectSample(document)}
              type="button"
            >
              <span>{document.format}</span>
              <strong>{document.name}</strong>
              <p>{document.description}</p>
            </button>
          ))}
        </div>
      </SectionCard>

      {activeDocument && classification ? (
        <div className="two-column">
          <SectionCard
            title="Classified Packet"
            description="Current routing recommendation for the loaded document."
          >
            <div className="detail-grid">
              <div className="detail-card">
                <span>Document name</span>
                <strong>{activeDocument.name}</strong>
              </div>
              <div className="detail-card">
                <span>Detected type</span>
                <strong>{classification.documentType}</strong>
              </div>
              <div className="detail-card">
                <span>Source</span>
                <strong>{activeDocument.source}</strong>
              </div>
              <div className="detail-card">
                <span>Format</span>
                <strong>{activeDocument.format}</strong>
              </div>
            </div>
            <ConfidenceMeter label="Routing confidence" value={classification.confidence} />
            <ul className="list-clean">
              {classification.rationale.map((reason) => (
                <li key={reason}>{reason}</li>
              ))}
            </ul>
          </SectionCard>

          <SectionCard
            title="Reviewer Notes"
            description="Presentation-friendly view of what the intake service captured."
          >
            <div className="callout callout--blue">
              <strong>Classification output</strong>
              <p>The packet is staged for the {classification.documentType} workflow.</p>
            </div>
            <pre className="code-block">{JSON.stringify(classification, null, 2)}</pre>
            {activeDocument.ingestionNote ? (
              <div className="callout callout--amber">
                <strong>MVP placeholder</strong>
                <p>{activeDocument.ingestionNote}</p>
              </div>
            ) : null}
          </SectionCard>
        </div>
      ) : (
        <SectionCard
          title="No document loaded"
          description="Load a sample or upload a packet to start the regulated review workflow."
        >
          <div className="empty-state">
            <strong>Awaiting reviewer intake</strong>
            <p>The workbench will classify the incoming document and expose the downstream modules.</p>
          </div>
        </SectionCard>
      )}
    </div>
  );
}
