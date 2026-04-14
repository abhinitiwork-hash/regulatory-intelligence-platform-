"use client";

import { useMemo, useRef, useState } from "react";
import { FileWarning, SendToBack } from "lucide-react";
import { COMPLETENESS_ISSUES } from "@/lib/demo-data";
import { useNirnay } from "@/components/providers/nirnay-provider";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

const sectionSeed = {
  Administrative: [
    "Application ID: CT-23-2026-1148",
    "Sponsor Name: Helix Biotech Pvt Ltd",
    "Study Title: HBT-17 Phase II Autoimmune Dermatitis"
  ],
  Ethics: [
    "Ethics Committee Approval Number: Not provided",
    "Informed Consent Version: Not provided"
  ],
  Insurance: ["Indemnity Document Reference: Not provided"],
  Safety: [
    "Medical Monitor Name: Dr. Sonia Kapoor",
    "SAE Reporting Contact: Not provided"
  ]
};

function severityLabel(value: string) {
  if (value === "Critical") {
    return "Critical";
  }

  if (value === "High") {
    return "Major";
  }

  return "Minor";
}

export function CompletenessPage() {
  const { addAuditEvent, addToast } = useNirnay();
  const [issues, setIssues] = useState(
    COMPLETENESS_ISSUES.map((issue) => ({
      ...issue,
      status: issue.status === "Open" ? "Unresolved" : issue.status
    }))
  );
  const [memo, setMemo] = useState<string | null>(null);
  const sectionRefs = {
    Administrative: useRef<HTMLDivElement | null>(null),
    Ethics: useRef<HTMLDivElement | null>(null),
    Insurance: useRef<HTMLDivElement | null>(null),
    Safety: useRef<HTMLDivElement | null>(null)
  };

  const completionPercent = useMemo(() => {
    const done = issues.filter((issue) => issue.status !== "Unresolved").length;
    return Math.round((done / issues.length) * 100);
  }, [issues]);

  function generateMemo() {
    const unresolved = issues.filter((issue) => issue.status === "Unresolved");
    const content = [
      "NIRNAY DEFICIENCY MEMO",
      "",
      ...unresolved.map(
        (issue, index) =>
          `${index + 1}. [${severityLabel(issue.gapLevel)}] ${issue.field} - ${issue.action}${
            issue.comment ? ` Reviewer comment: ${issue.comment}` : ""
          }`
      )
    ].join("\n");

    setMemo(content);
    addAuditEvent({
      module: "Completeness Check",
      action: "Deficiency memo generated",
      confidence: 0.97,
      reviewerAction: "Memo ready for sponsor communication",
      finalStatus: "Completed",
      sourceReference: "CT-23-2026-1148",
      note: `${unresolved.length} unresolved items included in deficiency memo.`
    });
    addToast({
      title: "Deficiency memo generated",
      description: "Live memo panel updated from unresolved issues.",
      tone: "success"
    });
  }

  return (
    <div className="page-grid">
      <section className="surface p-6">
        <div className="flex flex-wrap items-end justify-between gap-4">
          <div>
            <p className="eyebrow">Completeness Check</p>
            <h1 className="mt-3 text-3xl font-semibold tracking-tight text-nirnay-navy">
              Dynamic deficiency management for regulatory forms
            </h1>
          </div>
          <div className="flex gap-3">
            <Button onClick={generateMemo}>
              <FileWarning className="h-4 w-4" />
              Generate deficiency memo
            </Button>
          </div>
        </div>
        <div className="mt-6 grid gap-4 md:grid-cols-4">
          <div className="surface-subtle p-4">
            <p className="text-sm text-nirnay-slate">Completion percentage</p>
            <p className="mt-3 text-3xl font-semibold tracking-[-0.06em] text-nirnay-navy">
              {completionPercent}%
            </p>
          </div>
          <div className="surface-subtle p-4">
            <p className="text-sm text-nirnay-slate">Critical</p>
            <p className="mt-3 text-3xl font-semibold tracking-[-0.06em] text-[var(--nirnay-red)]">
              {issues.filter((issue) => issue.gapLevel === "Critical").length}
            </p>
          </div>
          <div className="surface-subtle p-4">
            <p className="text-sm text-nirnay-slate">Major</p>
            <p className="mt-3 text-3xl font-semibold tracking-[-0.06em] text-[var(--nirnay-amber)]">
              {issues.filter((issue) => issue.gapLevel === "High").length}
            </p>
          </div>
          <div className="surface-subtle p-4">
            <p className="text-sm text-nirnay-slate">Minor</p>
            <p className="mt-3 text-3xl font-semibold tracking-[-0.06em] text-nirnay-cyan">
              {issues.filter((issue) => issue.gapLevel === "Medium").length}
            </p>
          </div>
        </div>
      </section>

      <section className="grid gap-5 xl:grid-cols-[420px_minmax(0,1fr)]">
        <div className="surface p-6">
          <div className="flex items-center justify-between gap-3">
            <div>
              <p className="eyebrow">Issue register</p>
              <p className="mt-3 text-2xl font-semibold tracking-tight text-nirnay-navy">
                Jump from issue to source section
              </p>
            </div>
            <SendToBack className="h-5 w-5 text-nirnay-cyan" />
          </div>

          <div className="mt-6 grid gap-3">
            {issues.map((issue) => (
              <button
                className="surface-subtle p-4 text-left"
                key={issue.id}
                onClick={() =>
                  sectionRefs[issue.section as keyof typeof sectionRefs].current?.scrollIntoView({
                    behavior: "smooth",
                    block: "center"
                  })
                }
                type="button"
              >
                <div className="flex items-center justify-between gap-3">
                  <p className="text-sm font-semibold text-nirnay-navy">{issue.field}</p>
                  <Badge>{severityLabel(issue.gapLevel)}</Badge>
                </div>
                <p className="mt-2 text-sm leading-6 text-nirnay-slate">{issue.action}</p>
              </button>
            ))}
          </div>
        </div>

        <div className="grid gap-5">
          {Object.entries(sectionSeed).map(([section, values]) => (
            <div className="surface p-6" key={section} ref={sectionRefs[section as keyof typeof sectionRefs]}>
              <div className="flex items-center justify-between gap-3">
                <div>
                  <p className="eyebrow">Source section</p>
                  <h2 className="mt-3 text-2xl font-semibold tracking-tight text-nirnay-navy">
                    {section}
                  </h2>
                </div>
                <Badge>{values.length} fields</Badge>
              </div>

              <div className="mt-6 grid gap-3">
                {values.map((value) => {
                  const linkedIssue = issues.find((issue) => value.startsWith(issue.field));

                  return (
                    <div className="surface-subtle p-4" key={value}>
                      <p className="text-sm text-nirnay-slate">{value}</p>
                      {linkedIssue ? (
                        <div className="mt-4 grid gap-3 md:grid-cols-[160px_minmax(0,1fr)]">
                          <select
                            className="field-shell"
                            onChange={(event) =>
                              setIssues((current) =>
                                current.map((issue) =>
                                  issue.id === linkedIssue.id
                                    ? {
                                        ...issue,
                                        status: event.target.value as "Unresolved" | "Resolved" | "Accepted"
                                      }
                                    : issue
                                )
                              )
                            }
                            value={linkedIssue.status}
                          >
                            <option>Unresolved</option>
                            <option>Resolved</option>
                            <option>Accepted</option>
                          </select>
                          <textarea
                            className="field-shell min-h-[96px] resize-y"
                            onChange={(event) =>
                              setIssues((current) =>
                                current.map((issue) =>
                                  issue.id === linkedIssue.id
                                    ? { ...issue, comment: event.target.value }
                                    : issue
                                )
                              )
                            }
                            placeholder="Add reviewer comment"
                            value={linkedIssue.comment}
                          />
                        </div>
                      ) : null}
                    </div>
                  );
                })}
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className="surface p-6">
        <p className="eyebrow">Memo output</p>
        {memo ? (
          <pre className="mt-4 overflow-x-auto rounded-3xl bg-[rgba(7,30,61,0.98)] p-5 text-sm leading-7 text-white/80">
            {memo}
          </pre>
        ) : (
          <p className="mt-4 text-sm leading-7 text-nirnay-slate">
            Generate the deficiency memo once the reviewer has updated issue states and comments.
          </p>
        )}
      </section>
    </div>
  );
}
