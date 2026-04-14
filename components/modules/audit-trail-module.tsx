import { Badge } from "@/components/ui/badge";
import { SectionCard } from "@/components/ui/section-card";
import { AuditEntry } from "@/lib/types";

export function AuditTrailModule({ entries }: { entries: AuditEntry[] }) {
  return (
    <div className="module-stack">
      <SectionCard
        title="Audit Trail"
        description="Every AI output and reviewer action is time-stamped, source-linked, and clearly marked as assistive."
      >
        <div className="callout callout--slate">
          <strong>Assistive AI only</strong>
          <p>
            Nirnay Portal does not take final regulatory action. Reviewer decisions remain explicit,
            visible, and attributable.
          </p>
        </div>

        <div className="table-wrap">
          <table className="data-table">
            <thead>
              <tr>
                <th>Timestamp</th>
                <th>Module</th>
                <th>Actor</th>
                <th>Action</th>
                <th>Confidence</th>
                <th>Status</th>
                <th>Source reference</th>
              </tr>
            </thead>
            <tbody>
              {entries.map((entry) => (
                <tr key={entry.id}>
                  <td>{entry.timestamp}</td>
                  <td>{entry.module}</td>
                  <td>{entry.actor}</td>
                  <td>
                    <strong>{entry.action}</strong>
                    <p>{entry.note}</p>
                  </td>
                  <td>{Math.round(entry.confidence * 100)}%</td>
                  <td>
                    <Badge
                      tone={
                        entry.status === "Accepted"
                          ? "green"
                          : entry.status === "Overridden"
                            ? "amber"
                            : entry.status === "Edited"
                              ? "blue"
                              : "slate"
                      }
                    >
                      {entry.status}
                    </Badge>
                  </td>
                  <td>{entry.sourceReference}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </SectionCard>
    </div>
  );
}

