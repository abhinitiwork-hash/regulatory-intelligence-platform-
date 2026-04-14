"use client";

import { useMemo, useState } from "react";
import { ChevronDown, Download, FileJson2, LoaderCircle } from "lucide-react";
import { INSPECTION_SEED } from "@/lib/demo-data";
import { InspectionFindingItem } from "@/lib/demo-types";
import { useNirnay } from "@/components/providers/nirnay-provider";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { downloadFile, sleep } from "@/lib/utils";

const progressSteps = ["Parsing notes", "Structuring findings", "Drafting report"] as const;

export function InspectionReportPage() {
  const { addAuditEvent, addToast } = useNirnay();
  const [notes, setNotes] = useState(INSPECTION_SEED.notes);
  const [progressIndex, setProgressIndex] = useState(-1);
  const [generated, setGenerated] = useState(false);
  const [reportText, setReportText] = useState("");
  const [findings, setFindings] = useState<InspectionFindingItem[]>(INSPECTION_SEED.findings);
  const [mappingOpen, setMappingOpen] = useState(true);

  const reportPayload = useMemo(() => {
    return {
      siteDetails: {
        siteName: "Apex Care Hospital, Bengaluru",
        principalInvestigator: "Dr. Kavita Menon",
        inspectionDate: "12 Apr 2026"
      },
      findings,
      notes
    };
  }, [findings, notes]);

  async function generateReport() {
    setGenerated(false);

    for (let index = 0; index < progressSteps.length; index += 1) {
      setProgressIndex(index);
      await sleep(500);
    }

    const report = [
      "CDSCO INSPECTION REPORT DRAFT",
      "Site: Apex Care Hospital, Bengaluru",
      "Principal Investigator: Dr. Kavita Menon",
      "Inspection Date: 12 Apr 2026",
      "",
      "Observations:",
      ...notes
        .split("\n")
        .filter((line) => line.trim().startsWith("-"))
        .map((line) => line.trim()),
      "",
      "Findings:",
      ...findings.map((finding) => `- [${finding.level}] ${finding.title}: ${finding.evidence}`),
      "",
      "Recommended actions:",
      ...findings.map((finding) => `- ${finding.action}`)
    ].join("\n");

    setReportText(report);
    setGenerated(true);
    addAuditEvent({
      module: "Inspection Report",
      action: "Inspection report generated",
      confidence: 0.9,
      reviewerAction: "Draft ready for field review",
      finalStatus: "Completed",
      sourceReference: "site_visit_notes_photo.jpg",
      note: "Generated report created from rough inspection notes."
    });
    addToast({
      title: "Inspection report generated",
      description: "Draft report is ready for inline review and export.",
      tone: "success"
    });
  }

  function exportText() {
    downloadFile(reportText || "Generate report first.", "nirnay-inspection-report.txt", "text/plain");
  }

  function exportJson() {
    downloadFile(
      JSON.stringify({ ...reportPayload, reportText }, null, 2),
      "nirnay-inspection-report.json",
      "application/json"
    );
  }

  return (
    <div className="page-grid">
      <section className="surface p-6">
        <div className="flex flex-wrap items-end justify-between gap-4">
          <div>
            <p className="eyebrow">Inspection Report Generator</p>
            <h1 className="mt-3 text-3xl font-semibold tracking-tight text-nirnay-navy">
              Rough notes to formal inspection report
            </h1>
          </div>
          <div className="flex flex-wrap gap-3">
            <Button onClick={generateReport}>
              {progressIndex >= 0 && !generated ? (
                <>
                  <LoaderCircle className="h-4 w-4 animate-spin" />
                  {progressSteps[progressIndex]}
                </>
              ) : (
                "Generate report"
              )}
            </Button>
            <Button onClick={exportText} variant="secondary">
              <Download className="h-4 w-4" />
              Export text
            </Button>
            <Button onClick={exportJson} variant="secondary">
              <FileJson2 className="h-4 w-4" />
              Export JSON
            </Button>
          </div>
        </div>
        <div className="mt-6 grid gap-3 md:grid-cols-3">
          {progressSteps.map((step, index) => (
            <div
              className={`rounded-3xl border p-4 ${
                progressIndex >= index
                  ? "border-[rgba(24,166,184,0.22)] bg-[rgba(24,166,184,0.08)]"
                  : "border-[rgba(11,63,117,0.08)] bg-white"
              }`}
              key={step}
            >
              <p className="eyebrow">{step}</p>
              <p className="mt-3 text-sm text-nirnay-slate">
                {index === 0
                  ? "Extract structure from rough field notes."
                  : index === 1
                    ? "Group evidence into severity-tagged findings."
                    : "Prepare formal report text for review."}
              </p>
            </div>
          ))}
        </div>
      </section>

      <section className="grid gap-5 xl:grid-cols-[420px_minmax(0,1fr)]">
        <div className="surface p-6">
          <p className="eyebrow">Raw notes input</p>
          <textarea
            className="field-shell mt-4 min-h-[420px] w-full resize-y"
            onChange={(event) => setNotes(event.target.value)}
            value={notes}
          />
        </div>

        <div className="grid gap-5">
          <div className="surface p-6">
            <div className="flex items-center justify-between gap-4">
              <div>
                <p className="eyebrow">Formatted output</p>
                <p className="mt-3 text-2xl font-semibold tracking-tight text-nirnay-navy">
                  Inline-editable inspection report
                </p>
              </div>
              {generated ? (
                <Badge className="border-[rgba(46,125,50,0.2)] bg-[rgba(46,125,50,0.08)] text-[var(--nirnay-green)]">
                  Draft ready
                </Badge>
              ) : null}
            </div>
            <textarea
              className="field-shell mt-4 min-h-[340px] w-full resize-y font-mono leading-7"
              onChange={(event) => setReportText(event.target.value)}
              value={reportText}
            />
          </div>

          <div className="surface p-6">
            <p className="eyebrow">Findings</p>
            <div className="mt-5 grid gap-3">
              {findings.map((finding) => (
                <div
                  className="grid gap-4 rounded-3xl border border-[rgba(11,63,117,0.08)] p-4 md:grid-cols-[160px_minmax(0,1fr)]"
                  key={finding.id}
                >
                  <select
                    className="field-shell"
                    onChange={(event) =>
                      setFindings((current) =>
                        current.map((item) =>
                          item.id === finding.id
                            ? {
                                ...item,
                                level: event.target.value as "Critical" | "Major" | "Minor"
                              }
                            : item
                        )
                      )
                    }
                    value={finding.level}
                  >
                    <option>Critical</option>
                    <option>Major</option>
                    <option>Minor</option>
                  </select>
                  <div>
                    <p className="text-sm font-semibold text-nirnay-navy">{finding.title}</p>
                    <p className="mt-2 text-sm leading-7 text-nirnay-slate">{finding.evidence}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="surface p-6">
            <button
              className="flex w-full items-center justify-between gap-3"
              onClick={() => setMappingOpen((current) => !current)}
              type="button"
            >
              <div className="text-left">
                <p className="eyebrow">Evidence mapping</p>
                <p className="mt-3 text-2xl font-semibold tracking-tight text-nirnay-navy">
                  Collapsible source-to-finding mapping
                </p>
              </div>
              <ChevronDown
                className={`h-5 w-5 text-nirnay-slate transition ${mappingOpen ? "rotate-180" : ""}`}
              />
            </button>
            {mappingOpen ? (
              <div className="mt-5 grid gap-3">
                {findings.map((finding) => (
                  <div className="surface-subtle p-4" key={finding.id}>
                    <p className="text-sm font-semibold text-nirnay-navy">{finding.title}</p>
                    <p className="mt-3 text-sm leading-7 text-nirnay-slate">{finding.evidence}</p>
                  </div>
                ))}
              </div>
            ) : null}
          </div>
        </div>
      </section>
    </div>
  );
}
