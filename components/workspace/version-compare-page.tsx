"use client";

import { useMemo, useState } from "react";
import { FileOutput, Filter, Scale3d } from "lucide-react";
import { VERSION_CHANGES } from "@/lib/demo-data";
import { VersionChangeItem } from "@/lib/demo-types";
import { useNirnay } from "@/components/providers/nirnay-provider";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Drawer } from "@/components/ui/drawer";

const filters = [
  "All changes",
  "Safety-impacting",
  "Eligibility",
  "Endpoint",
  "Consent language"
] as const;

export function VersionComparePage() {
  const { addAuditEvent, addToast } = useNirnay();
  const [activeFilter, setActiveFilter] = useState<(typeof filters)[number]>("All changes");
  const [selectedChange, setSelectedChange] = useState<VersionChangeItem | null>(null);
  const [summary, setSummary] = useState<string | null>(null);

  const filteredChanges = useMemo(() => {
    if (activeFilter === "All changes") {
      return VERSION_CHANGES;
    }

    if (activeFilter === "Safety-impacting") {
      return VERSION_CHANGES.filter((change) => change.impactLevel === "High");
    }

    if (activeFilter === "Consent language") {
      return VERSION_CHANGES.filter((change) => change.area === "Consent Language");
    }

    return VERSION_CHANGES.filter((change) => change.area === activeFilter);
  }, [activeFilter]);

  function createSummary() {
    const content = [
      "NIRNAY REVIEWER SUMMARY",
      "Protocol v2.1 → Protocol v3.0",
      "",
      ...filteredChanges.map(
        (change) =>
          `- ${change.area}: ${change.classification}. ${change.impact}`
      )
    ].join("\n");

    setSummary(content);
    addAuditEvent({
      module: "Version Compare",
      action: "Reviewer summary created",
      confidence: 0.95,
      reviewerAction: "Impact rationale prepared",
      finalStatus: "Completed",
      sourceReference: "protocol_amendment_3_redline.pdf",
      note: `${filteredChanges.length} changes captured in reviewer summary.`
    });
    addToast({
      title: "Reviewer summary created",
      description: "Protocol impact summary is ready below the comparison grid.",
      tone: "success"
    });
  }

  return (
    <div className="page-grid">
      <section className="surface p-6">
        <div className="flex flex-wrap items-end justify-between gap-4">
          <div>
            <p className="eyebrow">Version Compare</p>
            <h1 className="mt-3 text-3xl font-semibold tracking-tight text-nirnay-navy">
              Substantive change detection with impact explanation
            </h1>
          </div>
          <Button onClick={createSummary}>
            <FileOutput className="h-4 w-4" />
            Create reviewer summary
          </Button>
        </div>
        <div className="mt-6 flex flex-wrap gap-3">
          {filters.map((filter) => (
            <button
              className={`rounded-full border px-4 py-2 text-sm font-semibold transition ${
                activeFilter === filter
                  ? "border-[rgba(24,166,184,0.28)] bg-[rgba(24,166,184,0.08)] text-nirnay-blue"
                  : "border-[rgba(11,63,117,0.1)] bg-white text-nirnay-slate"
              }`}
              key={filter}
              onClick={() => setActiveFilter(filter)}
              type="button"
            >
              {filter}
            </button>
          ))}
          <Badge className="border-[rgba(11,63,117,0.12)] bg-[rgba(11,63,117,0.04)] text-nirnay-slate">
            <Filter className="h-3.5 w-3.5" />
            Filtered view
          </Badge>
        </div>
      </section>

      <section className="grid gap-5 xl:grid-cols-[minmax(0,1fr)_360px]">
        <div className="surface p-6">
          <div className="grid gap-4">
            {filteredChanges.map((change) => (
              <button
                className="surface-subtle p-5 text-left"
                key={change.id}
                onClick={() => setSelectedChange(change)}
                type="button"
              >
                <div className="flex flex-wrap items-center justify-between gap-3">
                  <div className="flex gap-2">
                    <Badge>{change.area}</Badge>
                    <Badge
                      className={
                        change.classification === "Substantive"
                          ? "border-[rgba(245,166,35,0.22)] bg-[rgba(245,166,35,0.1)] text-[var(--nirnay-amber)]"
                          : "border-[rgba(11,63,117,0.12)] bg-[rgba(11,63,117,0.04)] text-nirnay-slate"
                      }
                    >
                      {change.classification}
                    </Badge>
                  </div>
                  <Badge>{change.impactLevel}</Badge>
                </div>
                <div className="mt-5 grid gap-4 md:grid-cols-2">
                  <div className="rounded-2xl border border-[rgba(11,63,117,0.08)] bg-white p-4">
                    <p className="eyebrow">Before</p>
                    <p className="mt-3 text-sm leading-7 text-nirnay-slate">{change.before}</p>
                  </div>
                  <div className="rounded-2xl border border-[rgba(11,63,117,0.08)] bg-[rgba(24,166,184,0.05)] p-4">
                    <p className="eyebrow">After</p>
                    <p className="mt-3 text-sm leading-7 text-nirnay-slate">{change.after}</p>
                  </div>
                </div>
              </button>
            ))}
          </div>
        </div>

        <div className="surface p-6">
          <div className="flex items-center justify-between gap-3">
            <div>
              <p className="eyebrow">Impact board</p>
              <p className="mt-3 text-2xl font-semibold tracking-tight text-nirnay-navy">
                Regulatory significance snapshot
              </p>
            </div>
            <Scale3d className="h-5 w-5 text-nirnay-cyan" />
          </div>
          <div className="mt-6 grid gap-3">
            <div className="surface-subtle p-4">
              <p className="text-sm text-nirnay-slate">Visible changes</p>
              <p className="mt-3 text-3xl font-semibold tracking-[-0.06em] text-nirnay-navy">
                {filteredChanges.length}
              </p>
            </div>
            <div className="surface-subtle p-4">
              <p className="text-sm text-nirnay-slate">Substantive changes</p>
              <p className="mt-3 text-3xl font-semibold tracking-[-0.06em] text-[var(--nirnay-amber)]">
                {filteredChanges.filter((change) => change.classification === "Substantive").length}
              </p>
            </div>
            <div className="surface-subtle p-4">
              <p className="text-sm text-nirnay-slate">Safety impacting</p>
              <p className="mt-3 text-3xl font-semibold tracking-[-0.06em] text-[var(--nirnay-red)]">
                {filteredChanges.filter((change) => change.impactLevel === "High").length}
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className="surface p-6">
        <p className="eyebrow">Reviewer summary output</p>
        {summary ? (
          <pre className="mt-4 overflow-x-auto rounded-3xl bg-[rgba(7,30,61,0.98)] p-5 text-sm leading-7 text-white/80">
            {summary}
          </pre>
        ) : (
          <p className="mt-4 text-sm leading-7 text-nirnay-slate">
            Use the header action to create a summary from the active filtered set of protocol changes.
          </p>
        )}
      </section>

      <Drawer
        description={selectedChange?.impact}
        onClose={() => setSelectedChange(null)}
        open={Boolean(selectedChange)}
        title={selectedChange?.area ?? "Change detail"}
      >
        {selectedChange ? (
          <div className="space-y-5">
            <div className="grid gap-4">
              <div className="surface-subtle p-4">
                <p className="eyebrow">Administrative vs substantive</p>
                <p className="mt-3 text-sm font-semibold text-nirnay-navy">
                  {selectedChange.classification}
                </p>
              </div>
              <div className="surface-subtle p-4">
                <p className="eyebrow">Regulatory impact</p>
                <p className="mt-3 text-sm leading-7 text-nirnay-slate">
                  {selectedChange.impact}
                </p>
              </div>
            </div>
          </div>
        ) : null}
      </Drawer>
    </div>
  );
}
