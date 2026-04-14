import { Badge } from "@/components/ui/badge";
import { ConfidenceMeter } from "@/components/ui/confidence-meter";
import { SectionCard } from "@/components/ui/section-card";
import { SaeReviewResult, SeverityClassification } from "@/lib/types";

export function SaeReviewModule({
  review,
  onFieldChange,
  onAccept,
  onSaveEdits,
  onOverride
}: {
  review: SaeReviewResult;
  onFieldChange: (
    field:
      | "patientProfile"
      | "event"
      | "causality"
      | "actionTaken"
      | "outcome"
      | "missingInfo",
    value: string | string[]
  ) => void;
  onAccept: () => void;
  onSaveEdits: () => void;
  onOverride: (severity: SeverityClassification) => void;
}) {
  return (
    <div className="module-stack">
      <SectionCard
        title="SAE Review"
        description="AI extraction is visible, editable, and always subject to reviewer override."
        actions={
          <div className="button-group">
            <button className="button button--secondary" onClick={onAccept} type="button">
              Accept AI output
            </button>
            <button className="button" onClick={onSaveEdits} type="button">
              Save reviewer edits
            </button>
          </div>
        }
      >
        <div className="two-column">
          <div className="text-panel">
            <span>Source SAE narrative</span>
            <p>{review.sourceNarrative}</p>
          </div>
          <div className="panel-stack">
            <div className="summary-strip">
              <div className="summary-strip__item">
                <span>Current severity</span>
                <strong>{review.severity}</strong>
              </div>
              <div className="summary-strip__item">
                <span>Missing fields</span>
                <strong>{review.missingInfo.length}</strong>
              </div>
            </div>
            <ConfidenceMeter value={review.confidence} />
            <div className="token-list">
              {review.seriousnessCriteria.map((criterion) => (
                <Badge key={criterion} tone="amber">
                  {criterion}
                </Badge>
              ))}
            </div>
          </div>
        </div>
      </SectionCard>

      <div className="two-column">
        <SectionCard
          title="Structured Extraction"
          description="Reviewer edits are intentionally first-class, not hidden behind a chat action."
        >
          <div className="form-grid">
            <label className="field">
              <span>Patient profile</span>
              <textarea
                onChange={(event) => onFieldChange("patientProfile", event.target.value)}
                rows={3}
                value={review.patientProfile}
              />
            </label>
            <label className="field">
              <span>Event</span>
              <textarea
                onChange={(event) => onFieldChange("event", event.target.value)}
                rows={4}
                value={review.event}
              />
            </label>
            <label className="field">
              <span>Causality</span>
              <textarea
                onChange={(event) => onFieldChange("causality", event.target.value)}
                rows={3}
                value={review.causality}
              />
            </label>
            <label className="field">
              <span>Action taken</span>
              <textarea
                onChange={(event) => onFieldChange("actionTaken", event.target.value)}
                rows={3}
                value={review.actionTaken}
              />
            </label>
            <label className="field">
              <span>Outcome</span>
              <textarea
                onChange={(event) => onFieldChange("outcome", event.target.value)}
                rows={3}
                value={review.outcome}
              />
            </label>
            <label className="field">
              <span>Missing info</span>
              <textarea
                onChange={(event) =>
                  onFieldChange(
                    "missingInfo",
                    event.target.value
                      .split("\n")
                      .map((item) => item.trim())
                      .filter(Boolean)
                  )
                }
                rows={4}
                value={review.missingInfo.join("\n")}
              />
            </label>
          </div>
        </SectionCard>

        <SectionCard
          title="Severity Override"
          description="Reviewer remains responsible for the final seriousness disposition."
        >
          <div className="override-list">
            {[
              "Death",
              "Life-threatening",
              "Hospitalisation",
              "Disability",
              "Medically significant",
              "Non-serious"
            ].map((severity) => (
              <button
                key={severity}
                className={`override-option ${
                  review.severity === severity ? "override-option--active" : ""
                }`}
                onClick={() => onOverride(severity as SeverityClassification)}
                type="button"
              >
                {severity}
              </button>
            ))}
          </div>
          <pre className="code-block">{JSON.stringify(review.exportPayload, null, 2)}</pre>
        </SectionCard>
      </div>
    </div>
  );
}
