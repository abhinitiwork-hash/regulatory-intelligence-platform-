import { SectionCard } from "@/components/ui/section-card";
import { InspectionReport } from "@/lib/types";

export function InspectionReportModule({
  notes,
  report,
  error,
  onNotesChange,
  onGenerate
}: {
  notes: string;
  report: InspectionReport | null;
  error: string | null;
  onNotesChange: (value: string) => void;
  onGenerate: () => void;
}) {
  return (
    <div className="module-stack">
      <SectionCard
        title="Inspection Report Generator"
        description="Converts rough unstructured notes and handwritten-note placeholders into a formal, reviewer-ready inspection report."
        actions={
          <button className="button" onClick={onGenerate} type="button">
            Generate report
          </button>
        }
      >
        <label className="field">
          <span>Rough notes input</span>
          <textarea onChange={(event) => onNotesChange(event.target.value)} rows={10} value={notes} />
        </label>
        {error ? (
          <div className="callout callout--red">
            <strong>Generation blocked</strong>
            <p>{error}</p>
          </div>
        ) : null}
      </SectionCard>

      {report ? (
        <div className="two-column">
          <SectionCard
            title="Formal Inspection Report"
            description="Generated draft with site details, findings, evidence, and recommended action."
          >
            <div className="detail-grid">
              <div className="detail-card">
                <span>Site</span>
                <strong>{report.siteDetails.siteName}</strong>
              </div>
              <div className="detail-card">
                <span>Principal investigator</span>
                <strong>{report.siteDetails.principalInvestigator}</strong>
              </div>
              <div className="detail-card">
                <span>Inspection date</span>
                <strong>{report.siteDetails.inspectionDate}</strong>
              </div>
            </div>
            <pre className="code-block code-block--report">{report.formalReport}</pre>
          </SectionCard>

          <SectionCard
            title="Findings and Evidence"
            description="Structured findings grouped by criticality."
          >
            <div className="finding-list">
              {report.findings.map((finding) => (
                <div key={finding.title} className={`finding finding--${finding.level.toLowerCase()}`}>
                  <strong>
                    {finding.level}: {finding.title}
                  </strong>
                  <p>{finding.evidence}</p>
                  <small>{finding.action}</small>
                </div>
              ))}
            </div>
            <pre className="code-block">{JSON.stringify(report.exportPayload, null, 2)}</pre>
          </SectionCard>
        </div>
      ) : (
        <SectionCard
          title="No report generated"
          description="Add notes and run the generator to produce a formal inspection report."
        >
          <div className="empty-state">
            <strong>Awaiting source notes</strong>
            <p>The generated report will appear here with findings, evidence summary, and CAPA-ready actions.</p>
          </div>
        </SectionCard>
      )}
    </div>
  );
}

