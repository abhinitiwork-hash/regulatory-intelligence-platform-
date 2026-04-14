"use client";

import type { ReactNode } from "react";
import { useMemo, useState } from "react";
import {
  AlertTriangle,
  Download,
  ShieldCheck,
  ShieldX
} from "lucide-react";
import { REDACTION_SAMPLE } from "@/lib/demo-data";
import { RedactionEntity } from "@/lib/demo-types";
import { useNirnay } from "@/components/providers/nirnay-provider";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Drawer } from "@/components/ui/drawer";
import { downloadFile, formatPercent } from "@/lib/utils";

function buildRedactedText(
  source: string,
  entities: RedactionEntity[],
  showCategories: Record<"PII" | "PHI", boolean>
) {
  let redacted = source;

  entities.forEach((entity) => {
    const shouldReplace = entity.approved && showCategories[entity.category];

    redacted = redacted.replaceAll(entity.value, shouldReplace ? entity.replacement : entity.value);
  });

  return redacted;
}

function renderHighlightedText(
  text: string,
  entities: RedactionEntity[],
  showCategories: Record<"PII" | "PHI", boolean>
) {
  const sorted = [...entities]
    .map((entity) => ({
      ...entity,
      index: text.indexOf(entity.approved && showCategories[entity.category] ? entity.replacement : entity.value)
    }))
    .filter((entity) => entity.index >= 0)
    .sort((left, right) => left.index - right.index);

  const nodes: ReactNode[] = [];
  let cursor = 0;

  sorted.forEach((entity) => {
    const value = entity.approved && showCategories[entity.category] ? entity.replacement : entity.value;
    const nextIndex = text.indexOf(value, cursor);

    if (nextIndex < 0) {
      return;
    }

    if (nextIndex > cursor) {
      nodes.push(<span key={`text-${cursor}`}>{text.slice(cursor, nextIndex)}</span>);
    }

    nodes.push(
      <span
        className={
          entity.category === "PHI"
            ? "rounded-lg bg-[rgba(198,40,40,0.12)] px-1.5 py-0.5 text-[var(--nirnay-red)]"
            : "rounded-lg bg-[rgba(24,166,184,0.12)] px-1.5 py-0.5 text-[var(--nirnay-blue)]"
        }
        key={entity.id}
      >
        {value}
      </span>
    );

    cursor = nextIndex + value.length;
  });

  if (cursor < text.length) {
    nodes.push(<span key={`text-end-${cursor}`}>{text.slice(cursor)}</span>);
  }

  return nodes;
}

export function AnonymisationPage() {
  const { documents, addAuditEvent, addToast } = useNirnay();
  const [selectedDocumentId, setSelectedDocumentId] = useState("doc-002");
  const [entities, setEntities] = useState<RedactionEntity[]>(REDACTION_SAMPLE.entities);
  const [showCategories, setShowCategories] = useState<Record<"PII" | "PHI", boolean>>({
    PII: true,
    PHI: true
  });
  const [validationSummary, setValidationSummary] = useState<string | null>(null);
  const [queueOpen, setQueueOpen] = useState(false);

  const selectedDocument =
    documents.find((document) => document.id === selectedDocumentId) ?? documents[1] ?? documents[0];

  const redactedText = useMemo(
    () => buildRedactedText(REDACTION_SAMPLE.originalText, entities, showCategories),
    [entities, showCategories]
  );

  const lowConfidence = entities.filter((entity) => entity.confidence < 0.9);

  function toggleEntityApproval(id: string) {
    setEntities((current) =>
      current.map((entity) =>
        entity.id === id ? { ...entity, approved: !entity.approved } : entity
      )
    );
  }

  function validateRedaction() {
    const approved = entities.filter((entity) => entity.approved).length;
    const rejected = entities.length - approved;
    const summary = `${approved} redactions approved, ${rejected} held back, ${lowConfidence.length} entities under the low-confidence threshold.`;

    setValidationSummary(summary);
    addAuditEvent({
      module: "Anonymisation",
      action: "Redaction validation completed",
      confidence: 0.95,
      reviewerAction: "Validation summary reviewed",
      finalStatus: "Completed",
      sourceReference: selectedDocument.name,
      note: summary
    });
    addToast({
      title: "Validation complete",
      description: summary,
      tone: "success"
    });
  }

  function exportJson() {
    const payload = {
      sourceReference: selectedDocument.name,
      generatedAt: new Date().toISOString(),
      redactedText,
      entities,
      categoriesEnabled: showCategories
    };

    downloadFile(JSON.stringify(payload, null, 2), "nirnay-anonymised-output.json", "application/json");
    addAuditEvent({
      module: "Anonymisation",
      action: "Anonymised JSON exported",
      confidence: 0.95,
      reviewerAction: "Exported for downstream handling",
      finalStatus: "Completed",
      sourceReference: selectedDocument.name,
      note: "Reviewer downloaded anonymised JSON payload."
    });
    addToast({
      title: "JSON exported",
      description: "Anonymised payload downloaded for the demo workflow.",
      tone: "info"
    });
  }

  return (
    <div className="page-grid">
      <section className="surface p-6">
        <div className="flex flex-wrap items-end justify-between gap-4">
          <div>
            <p className="eyebrow">Anonymisation</p>
            <h1 className="mt-3 text-3xl font-semibold tracking-tight text-nirnay-navy">
              Reviewer-controlled sensitive data protection
            </h1>
          </div>
          <div className="flex flex-wrap gap-3">
            <Button onClick={validateRedaction}>
              <ShieldCheck className="h-4 w-4" />
              Validate redaction
            </Button>
            <Button onClick={exportJson} variant="secondary">
              <Download className="h-4 w-4" />
              Export anonymised JSON
            </Button>
            <Button onClick={() => setQueueOpen(true)} variant="secondary">
              <AlertTriangle className="h-4 w-4" />
              Escalate low-confidence entities
            </Button>
          </div>
        </div>

        <div className="mt-6 flex flex-wrap gap-3">
          <select
            className="field-shell min-w-[240px]"
            onChange={(event) => setSelectedDocumentId(event.target.value)}
            value={selectedDocumentId}
          >
            {documents.map((document) => (
              <option key={document.id} value={document.id}>
                {document.name}
              </option>
            ))}
          </select>
          <button
            className={`status-pill ${showCategories.PII ? "border-[rgba(24,166,184,0.22)] bg-[rgba(24,166,184,0.08)] text-nirnay-blue" : "border-[rgba(11,63,117,0.12)] bg-white text-nirnay-slate"}`}
            onClick={() =>
              setShowCategories((current) => ({ ...current, PII: !current.PII }))
            }
            type="button"
          >
            PII {showCategories.PII ? "On" : "Off"}
          </button>
          <button
            className={`status-pill ${showCategories.PHI ? "border-[rgba(198,40,40,0.18)] bg-[rgba(198,40,40,0.08)] text-[var(--nirnay-red)]" : "border-[rgba(11,63,117,0.12)] bg-white text-nirnay-slate"}`}
            onClick={() =>
              setShowCategories((current) => ({ ...current, PHI: !current.PHI }))
            }
            type="button"
          >
            PHI {showCategories.PHI ? "On" : "Off"}
          </button>
          {validationSummary ? (
            <Badge className="border-[rgba(46,125,50,0.2)] bg-[rgba(46,125,50,0.08)] text-[var(--nirnay-green)]">
              {validationSummary}
            </Badge>
          ) : null}
        </div>
      </section>

      <section className="grid gap-5 xl:grid-cols-[minmax(0,1fr)_380px]">
        <div className="grid gap-5">
          <div className="surface p-6">
            <div className="grid gap-5 xl:grid-cols-2">
              <div>
                <p className="eyebrow">Original text</p>
                <div className="mt-4 rounded-3xl border border-[rgba(11,63,117,0.08)] bg-white p-5 text-sm leading-8 text-nirnay-graphite">
                  {renderHighlightedText(REDACTION_SAMPLE.originalText, entities, {
                    PII: true,
                    PHI: true
                  })}
                </div>
              </div>
              <div>
                <p className="eyebrow">Redacted text</p>
                <div className="mt-4 rounded-3xl border border-[rgba(11,63,117,0.08)] bg-[rgba(11,63,117,0.03)] p-5 text-sm leading-8 text-nirnay-graphite">
                  {renderHighlightedText(redactedText, entities, showCategories)}
                </div>
              </div>
            </div>
          </div>

          <div className="surface p-6">
            <div className="flex items-center justify-between gap-4">
              <div>
                <p className="eyebrow">Entity Ledger</p>
                <h2 className="mt-3 text-2xl font-semibold tracking-tight text-nirnay-navy">
                  Manual approval and rejection controls
                </h2>
              </div>
              <Badge>{selectedDocument.name}</Badge>
            </div>

            <div className="mt-6 grid gap-3">
              {entities.map((entity) => (
                <div
                  className="grid gap-4 rounded-3xl border border-[rgba(11,63,117,0.08)] p-4 md:grid-cols-[minmax(0,1fr)_130px_120px_160px]"
                  key={entity.id}
                >
                  <div>
                    <p className="text-sm font-semibold text-nirnay-navy">{entity.label}</p>
                    <p className="mt-1 text-sm text-nirnay-slate">
                      {entity.value} → {entity.replacement}
                    </p>
                  </div>
                  <Badge
                    className={
                      entity.category === "PHI"
                        ? "border-[rgba(198,40,40,0.18)] bg-[rgba(198,40,40,0.08)] text-[var(--nirnay-red)]"
                        : "border-[rgba(24,166,184,0.18)] bg-[rgba(24,166,184,0.08)] text-nirnay-blue"
                    }
                  >
                    {entity.category}
                  </Badge>
                  <Badge>{formatPercent(entity.confidence)}</Badge>
                  <div className="flex gap-2">
                    <Button
                      className="flex-1"
                      onClick={() => toggleEntityApproval(entity.id)}
                      variant={entity.approved ? "primary" : "secondary"}
                    >
                      {entity.approved ? (
                        <>
                          <ShieldCheck className="h-4 w-4" />
                          Approved
                        </>
                      ) : (
                        <>
                          <ShieldX className="h-4 w-4" />
                          Rejected
                        </>
                      )}
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="surface p-6">
          <p className="eyebrow">Validation state</p>
          <h2 className="mt-3 text-2xl font-semibold tracking-tight text-nirnay-navy">
            Redaction summary
          </h2>
          <div className="mt-6 grid gap-3">
            <div className="rounded-3xl border border-[rgba(11,63,117,0.08)] p-4">
              <p className="text-sm text-nirnay-slate">Entities detected</p>
              <p className="mt-3 text-3xl font-semibold tracking-[-0.06em] text-nirnay-navy">
                {entities.length}
              </p>
            </div>
            <div className="rounded-3xl border border-[rgba(11,63,117,0.08)] p-4">
              <p className="text-sm text-nirnay-slate">Low-confidence entities</p>
              <p className="mt-3 text-3xl font-semibold tracking-[-0.06em] text-[var(--nirnay-amber)]">
                {lowConfidence.length}
              </p>
            </div>
            <div className="rounded-3xl border border-[rgba(11,63,117,0.08)] p-4">
              <p className="text-sm text-nirnay-slate">Approved by reviewer</p>
              <p className="mt-3 text-3xl font-semibold tracking-[-0.06em] text-[var(--nirnay-green)]">
                {entities.filter((entity) => entity.approved).length}
              </p>
            </div>
          </div>
        </div>
      </section>

      <Drawer
        description="Entities below the low-confidence threshold are routed for manual reviewer attention."
        onClose={() => setQueueOpen(false)}
        open={queueOpen}
        title="Escalation queue"
      >
        <div className="space-y-4">
          {lowConfidence.map((entity) => (
            <div className="surface-subtle p-4" key={entity.id}>
              <div className="flex items-center justify-between gap-3">
                <div>
                  <p className="text-sm font-semibold text-nirnay-navy">{entity.label}</p>
                  <p className="mt-2 text-sm text-nirnay-slate">{entity.value}</p>
                </div>
                <Badge className="border-[rgba(245,166,35,0.22)] bg-[rgba(245,166,35,0.1)] text-[var(--nirnay-amber)]">
                  {formatPercent(entity.confidence)}
                </Badge>
              </div>
              <div className="mt-4 flex gap-3">
                <Button
                  onClick={() => {
                    toggleEntityApproval(entity.id);
                    addToast({
                      title: "Escalation reviewed",
                      description: `${entity.label} moved through manual reviewer approval.`,
                      tone: "success"
                    });
                  }}
                >
                  Approve after review
                </Button>
                <Button
                  onClick={() => {
                    setShowCategories((current) => ({ ...current, [entity.category]: false }));
                    addToast({
                      title: "Category toggle updated",
                      description: `${entity.category} masking disabled to force manual inspection.`,
                      tone: "warning"
                    });
                  }}
                  variant="secondary"
                >
                  Pause category masking
                </Button>
              </div>
            </div>
          ))}
        </div>
      </Drawer>
    </div>
  );
}
