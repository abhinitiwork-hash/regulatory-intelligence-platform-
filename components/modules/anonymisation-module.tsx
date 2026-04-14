import { Badge } from "@/components/ui/badge";
import { ConfidenceMeter } from "@/components/ui/confidence-meter";
import { SectionCard } from "@/components/ui/section-card";
import { AnonymisationResult } from "@/lib/types";

export function AnonymisationModule({
  result,
  onExport
}: {
  result: AnonymisationResult | null;
  onExport: () => void;
}) {
  if (!result) {
    return (
      <SectionCard
        title="Anonymisation"
        description="Load source text to inspect detected PII and PHI entities."
      >
        <div className="empty-state">
          <strong>No text available</strong>
          <p>Upload a TXT narrative or use a seeded sample to generate redaction output.</p>
        </div>
      </SectionCard>
    );
  }

  const downloadHref = `data:application/json;charset=utf-8,${encodeURIComponent(
    JSON.stringify(result.exportPayload, null, 2)
  )}`;

  return (
    <div className="module-stack">
      <SectionCard
        title="Anonymisation"
        description="PII and PHI entities are detected first so reviewer-approved redactions flow into all later modules."
        actions={
          <a className="button button--secondary" download="anonymised-output.json" href={downloadHref} onClick={onExport}>
            Export anonymised JSON
          </a>
        }
      >
        <div className="summary-strip">
          <div className="summary-strip__item">
            <span>Source</span>
            <strong>{result.sourceReference}</strong>
          </div>
          <div className="summary-strip__item">
            <span>Entities detected</span>
            <strong>{result.entities.length}</strong>
          </div>
          <div className="summary-strip__item">
            <span>Redaction mode</span>
            <strong>Deterministic tokenisation</strong>
          </div>
        </div>

        <ConfidenceMeter value={result.confidence} />

        <div className="token-list">
          {result.entities.map((entity) => (
            <Badge key={`${entity.label}-${entity.value}`} tone={entity.category === "PHI" ? "red" : "blue"}>
              {entity.label} · {Math.round(entity.confidence * 100)}%
            </Badge>
          ))}
        </div>

        <div className="two-column">
          <div className="text-panel">
            <span>Original text</span>
            <p>{result.originalText}</p>
          </div>
          <div className="text-panel text-panel--redacted">
            <span>Redacted text</span>
            <p>{result.redactedText}</p>
          </div>
        </div>
      </SectionCard>

      <div className="two-column">
        <SectionCard
          title="Entity Ledger"
          description="Confidence and masking label for each detected identifier."
        >
          <div className="table-wrap">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Entity</th>
                  <th>Label</th>
                  <th>Redacted token</th>
                  <th>Confidence</th>
                </tr>
              </thead>
              <tbody>
                {result.entities.map((entity) => (
                  <tr key={`${entity.label}-${entity.value}`}>
                    <td>{entity.value}</td>
                    <td>
                      <Badge tone={entity.category === "PHI" ? "red" : "blue"}>{entity.label}</Badge>
                    </td>
                    <td>{entity.redactedValue}</td>
                    <td>{Math.round(entity.confidence * 100)}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </SectionCard>

        <SectionCard
          title="Sample JSON Output"
          description="Structured export payload for downstream storage or API submission."
        >
          <pre className="code-block">{JSON.stringify(result.exportPayload, null, 2)}</pre>
        </SectionCard>
      </div>
    </div>
  );
}

