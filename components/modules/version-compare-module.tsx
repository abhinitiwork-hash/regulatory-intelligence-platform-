import { Badge } from "@/components/ui/badge";
import { ConfidenceMeter } from "@/components/ui/confidence-meter";
import { SectionCard } from "@/components/ui/section-card";
import { VersionCompareResult } from "@/lib/types";

export function VersionCompareModule({
  result,
  onLogEscalation
}: {
  result: VersionCompareResult;
  onLogEscalation: () => void;
}) {
  return (
    <div className="module-stack">
      <SectionCard
        title="Version Compare"
        description="Substantive changes are highlighted with the likely regulatory impact and ready-to-log rationale."
        actions={
          <button className="button" onClick={onLogEscalation} type="button">
            Escalate amendment review
          </button>
        }
      >
        <div className="callout callout--blue">
          <strong>Comparison summary</strong>
          <p>{result.summary}</p>
        </div>
        <div className="compare-header">
          <div>
            <span>Baseline</span>
            <strong>{result.baselineLabel}</strong>
          </div>
          <div>
            <span>Amended</span>
            <strong>{result.amendedLabel}</strong>
          </div>
        </div>
      </SectionCard>

      <div className="compare-grid">
        {result.changes.map((change) => (
          <SectionCard
            key={change.id}
            title={change.area}
            description="AI-assisted delta explanation"
          >
            <Badge tone={change.significance === "Substantive" ? "amber" : "slate"}>
              {change.significance}
            </Badge>
            <div className="compare-pair">
              <div className="compare-pair__block">
                <span>Before</span>
                <p>{change.before}</p>
              </div>
              <div className="compare-pair__block">
                <span>After</span>
                <p>{change.after}</p>
              </div>
            </div>
            <p className="impact-copy">{change.impact}</p>
            <ConfidenceMeter value={change.confidence} label="Impact confidence" />
          </SectionCard>
        ))}
      </div>
    </div>
  );
}

