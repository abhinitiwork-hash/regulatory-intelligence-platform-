"use client";

import { useMemo, useState } from "react";
import {
  ChevronDown,
  FileOutput,
  Save,
  ShieldAlert
} from "lucide-react";
import { SAE_REVIEW_SEED } from "@/lib/demo-data";
import { useNirnay } from "@/components/providers/nirnay-provider";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

const tabs = ["Summary", "Evidence", "Triage", "Reviewer Notes"] as const;
const severityOptions = [
  "Death",
  "Life-threatening",
  "Hospitalisation",
  "Disability",
  "Medically significant",
  "Non-serious"
];

export function SaeReviewPage() {
  const { addAuditEvent, addToast } = useNirnay();
  const [activeTab, setActiveTab] = useState<(typeof tabs)[number]>("Summary");
  const [fields, setFields] = useState(SAE_REVIEW_SEED.fields);
  const [severity, setSeverity] = useState("Hospitalisation");
  const [missingInfo, setMissingInfo] = useState(
    SAE_REVIEW_SEED.missingInfo.map((item) => ({ item, resolved: false }))
  );
  const [reviewerNotes, setReviewerNotes] = useState(
    "Hospitalisation basis confirmed. Causality remains possibly related pending concomitant medication history."
  );
  const [openEvidence, setOpenEvidence] = useState<string | null>(SAE_REVIEW_SEED.fields[0]?.key ?? null);
  const [reviewPacket, setReviewPacket] = useState<string | null>(null);

  const dynamicMissing = useMemo(() => {
    const emptyFields = fields
      .filter((field) => !field.value.trim())
      .map((field) => `${field.label} requires reviewer input`);

    return [
      ...missingInfo.filter((item) => !item.resolved).map((item) => item.item),
      ...emptyFields
    ];
  }, [fields, missingInfo]);

  function saveEdits() {
    addAuditEvent({
      module: "SAE Review",
      action: "Reviewer edits saved",
      confidence: 1,
      reviewerAction: "Structured fields updated",
      finalStatus: "Completed",
      sourceReference: "SAE_narrative_subject_204.txt",
      note: `Reviewer maintained final severity as ${severity}.`
    });
    addToast({
      title: "SAE edits saved",
      description: "Structured review fields were updated and logged.",
      tone: "success"
    });
  }

  function generatePacket() {
    const packet = [
      "NIRNAY SAE REVIEW PACKET",
      "Source: SAE_narrative_subject_204.txt",
      `Final severity: ${severity}`,
      "",
      ...fields.map((field) => `${field.label}: ${field.value}`),
      "",
      `Missing information: ${dynamicMissing.join(", ") || "None"}`,
      "",
      `Reviewer notes: ${reviewerNotes}`
    ].join("\n");

    setReviewPacket(packet);
    addAuditEvent({
      module: "SAE Review",
      action: "Review packet generated",
      confidence: 0.94,
      reviewerAction: "Packet ready for supervisory review",
      finalStatus: "Completed",
      sourceReference: "SAE_narrative_subject_204.txt",
      note: "Formatted SAE review packet created from structured fields."
    });
    addToast({
      title: "Review packet generated",
      description: "Formatted output panel is ready for presentation or export.",
      tone: "success"
    });
    setActiveTab("Reviewer Notes");
  }

  return (
    <div className="page-grid">
      <section className="surface p-6">
        <div className="flex flex-wrap items-end justify-between gap-4">
          <div>
            <p className="eyebrow">SAE Review</p>
            <h1 className="mt-3 text-3xl font-semibold tracking-tight text-nirnay-navy">
              Structured safety review with reviewer override
            </h1>
            <p className="mt-3 max-w-3xl text-sm leading-7 text-nirnay-slate">
              Tabs, evidence snippets, editable structured fields, and a review packet generator are
              all live in this screen.
            </p>
          </div>
          <div className="flex flex-wrap gap-3">
            <Button onClick={saveEdits}>
              <Save className="h-4 w-4" />
              Save edits
            </Button>
            <Button onClick={generatePacket} variant="secondary">
              <FileOutput className="h-4 w-4" />
              Generate review packet
            </Button>
          </div>
        </div>

        <div className="mt-6 flex flex-wrap gap-3">
          {tabs.map((tab) => (
            <button
              className={cn(
                "rounded-full border px-4 py-2 text-sm font-semibold transition",
                activeTab === tab
                  ? "border-[rgba(24,166,184,0.28)] bg-[rgba(24,166,184,0.08)] text-nirnay-blue"
                  : "border-[rgba(11,63,117,0.1)] bg-white text-nirnay-slate hover:border-[rgba(11,63,117,0.18)]"
              )}
              key={tab}
              onClick={() => setActiveTab(tab)}
              type="button"
            >
              {tab}
            </button>
          ))}
        </div>
      </section>

      <section className="grid gap-5 xl:grid-cols-[minmax(0,1fr)_360px]">
        <div className="surface p-6">
          {activeTab === "Summary" ? (
            <div className="grid gap-4">
              {fields.map((field) => (
                <div className="surface-subtle p-4" key={field.key}>
                  <p className="eyebrow">{field.label}</p>
                  <textarea
                    className="field-shell mt-3 min-h-[110px] w-full resize-y"
                    onChange={(event) =>
                      setFields((current) =>
                        current.map((item) =>
                          item.key === field.key ? { ...item, value: event.target.value } : item
                        )
                      )
                    }
                    value={field.value}
                  />
                </div>
              ))}
            </div>
          ) : null}

          {activeTab === "Evidence" ? (
            <div className="grid gap-3">
              {fields.map((field) => (
                <button
                  className="surface-subtle p-4 text-left"
                  key={field.key}
                  onClick={() =>
                    setOpenEvidence((current) => (current === field.key ? null : field.key))
                  }
                  type="button"
                >
                  <div className="flex items-center justify-between gap-3">
                    <div>
                      <p className="text-sm font-semibold text-nirnay-navy">{field.label}</p>
                      <p className="mt-2 text-sm text-nirnay-slate">{field.value}</p>
                    </div>
                    <ChevronDown
                      className={cn(
                        "h-4 w-4 text-nirnay-slate transition",
                        openEvidence === field.key && "rotate-180"
                      )}
                    />
                  </div>
                  {openEvidence === field.key ? (
                    <div className="mt-4 grid gap-3 border-t border-[rgba(11,63,117,0.08)] pt-4">
                      {field.evidence.map((evidence) => (
                        <div
                          className="rounded-2xl border border-[rgba(11,63,117,0.08)] bg-white px-4 py-3"
                          key={evidence.id}
                        >
                          <div className="flex items-center justify-between gap-3">
                            <p className="text-sm font-semibold text-nirnay-navy">{evidence.label}</p>
                            <Badge>{Math.round(evidence.confidence * 100)}%</Badge>
                          </div>
                          <p className="mt-3 text-sm leading-7 text-nirnay-slate">
                            {evidence.snippet}
                          </p>
                        </div>
                      ))}
                    </div>
                  ) : null}
                </button>
              ))}
            </div>
          ) : null}

          {activeTab === "Triage" ? (
            <div className="grid gap-5">
              <div className="surface-subtle p-4">
                <p className="eyebrow">Final severity</p>
                <select
                  className="field-shell mt-3 w-full"
                  onChange={(event) => setSeverity(event.target.value)}
                  value={severity}
                >
                  {severityOptions.map((option) => (
                    <option key={option}>{option}</option>
                  ))}
                </select>
              </div>

              <div className="surface-subtle p-4">
                <p className="eyebrow">Missing information panel</p>
                <div className="mt-4 grid gap-3">
                  {missingInfo.map((item) => (
                    <label
                      className="flex items-start gap-3 rounded-2xl border border-[rgba(11,63,117,0.08)] bg-white px-4 py-3"
                      key={item.item}
                    >
                      <input
                        checked={item.resolved}
                        className="mt-1"
                        onChange={(event) =>
                          setMissingInfo((current) =>
                            current.map((entry) =>
                              entry.item === item.item
                                ? { ...entry, resolved: event.target.checked }
                                : entry
                            )
                          )
                        }
                        type="checkbox"
                      />
                      <span className="text-sm leading-7 text-nirnay-slate">{item.item}</span>
                    </label>
                  ))}
                </div>
              </div>
            </div>
          ) : null}

          {activeTab === "Reviewer Notes" ? (
            <div className="grid gap-5">
              <div className="surface-subtle p-4">
                <p className="eyebrow">Reviewer notes</p>
                <textarea
                  className="field-shell mt-3 min-h-[180px] w-full resize-y"
                  onChange={(event) => setReviewerNotes(event.target.value)}
                  value={reviewerNotes}
                />
              </div>
              <div className="surface-subtle p-4">
                <p className="eyebrow">Generated review packet</p>
                {reviewPacket ? (
                  <pre className="mt-3 overflow-x-auto rounded-2xl bg-[rgba(7,30,61,0.98)] p-4 text-sm leading-7 text-white/80">
                    {reviewPacket}
                  </pre>
                ) : (
                  <p className="mt-3 text-sm leading-7 text-nirnay-slate">
                    Generate the review packet from the header action to populate this output panel.
                  </p>
                )}
              </div>
            </div>
          ) : null}
        </div>

        <div className="surface p-6">
          <p className="eyebrow">Live triage state</p>
          <h2 className="mt-3 text-2xl font-semibold tracking-tight text-nirnay-navy">
            Reviewer-facing summary
          </h2>
          <div className="mt-6 grid gap-3">
            <div className="rounded-3xl border border-[rgba(11,63,117,0.08)] p-4">
              <p className="text-sm text-nirnay-slate">Current severity</p>
              <p className="mt-3 text-3xl font-semibold tracking-[-0.06em] text-[var(--nirnay-red)]">
                {severity}
              </p>
            </div>
            <div className="rounded-3xl border border-[rgba(11,63,117,0.08)] p-4">
              <p className="text-sm text-nirnay-slate">Outstanding missing items</p>
              <p className="mt-3 text-3xl font-semibold tracking-[-0.06em] text-[var(--nirnay-amber)]">
                {dynamicMissing.length}
              </p>
            </div>
            <div className="rounded-3xl border border-[rgba(11,63,117,0.08)] bg-[rgba(11,63,117,0.03)] p-4">
              <div className="flex items-start gap-3">
                <ShieldAlert className="mt-1 h-5 w-5 text-nirnay-cyan" />
                <p className="text-sm leading-7 text-nirnay-slate">
                  Reviewer can accept, edit, or override AI output. All actions are logged and stay
                  visible in the audit trail.
                </p>
              </div>
            </div>
          </div>
          <div className="mt-5 rounded-3xl border border-[rgba(11,63,117,0.08)] p-4">
            <p className="eyebrow">Dynamic missing information</p>
            <ul className="mt-4 grid gap-3 text-sm leading-7 text-nirnay-slate">
              {dynamicMissing.map((item) => (
                <li className="rounded-2xl bg-[rgba(245,166,35,0.08)] px-3 py-2" key={item}>
                  {item}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </section>
    </div>
  );
}
