import { Badge } from "@/components/ui/badge";
import { SectionCard } from "@/components/ui/section-card";
import { CompletenessResult } from "@/lib/types";

export function CompletenessCheckModule({
  result,
  onLogReviewerAction
}: {
  result: CompletenessResult;
  onLogReviewerAction: () => void;
}) {
  return (
    <div className="module-stack">
      <SectionCard
        title="Completeness Check"
        description="Mandatory fields are assessed against a seed regulatory form object and prioritised by reviewer urgency."
        actions={
          <button className="button" onClick={onLogReviewerAction} type="button">
            Log reviewer follow-up
          </button>
        }
      >
        <div className="summary-strip">
          <div className="summary-strip__item">
            <span>Completeness score</span>
            <strong>{result.completenessScore}%</strong>
          </div>
          <div className="summary-strip__item">
            <span>Critical gaps</span>
            <strong>{result.summary.critical}</strong>
          </div>
          <div className="summary-strip__item">
            <span>Major gaps</span>
            <strong>{result.summary.major}</strong>
          </div>
          <div className="summary-strip__item">
            <span>Minor gaps</span>
            <strong>{result.summary.minor}</strong>
          </div>
        </div>

        <div className="table-wrap">
          <table className="data-table">
            <thead>
              <tr>
                <th>Section</th>
                <th>Field</th>
                <th>Status</th>
                <th>Gap level</th>
                <th>Reviewer action needed</th>
              </tr>
            </thead>
            <tbody>
              {result.fields.map((field) => (
                <tr key={field.field}>
                  <td>{field.section}</td>
                  <td>
                    <strong>{field.field}</strong>
                    <p>{field.value}</p>
                  </td>
                  <td>{field.status}</td>
                  <td>
                    <Badge
                      tone={
                        field.gapLevel === "Critical"
                          ? "red"
                          : field.gapLevel === "Major"
                            ? "amber"
                            : field.gapLevel === "Minor"
                              ? "blue"
                              : "green"
                      }
                    >
                      {field.gapLevel}
                    </Badge>
                  </td>
                  <td>{field.actionNeeded}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </SectionCard>

      <div className="two-column">
        <SectionCard
          title="Reviewer Action Required"
          description="Clear next steps for the regulatory reviewer."
        >
          <div className="bullet-grid">
            <div className="bullet-card">
              <strong>Critical</strong>
              <p>Block progression until ethics approval number and core identifiers are attached.</p>
            </div>
            <div className="bullet-card">
              <strong>Major</strong>
              <p>Request missing indemnity, consent version, and supporting product documentation.</p>
            </div>
            <div className="bullet-card">
              <strong>Minor</strong>
              <p>Capture operational contacts before final reviewer sign-off.</p>
            </div>
          </div>
        </SectionCard>

        <SectionCard
          title="Sample JSON Output"
          description="Structured checklist payload for future workflow APIs."
        >
          <pre className="code-block">{JSON.stringify(result.exportPayload, null, 2)}</pre>
        </SectionCard>
      </div>
    </div>
  );
}

