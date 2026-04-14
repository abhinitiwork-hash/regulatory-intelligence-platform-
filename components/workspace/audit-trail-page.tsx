"use client";

import { useMemo, useState } from "react";
import { ArrowDownWideNarrow, Download, Search } from "lucide-react";
import { DemoAuditEvent } from "@/lib/demo-types";
import { useNirnay } from "@/components/providers/nirnay-provider";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Drawer } from "@/components/ui/drawer";
import { downloadFile } from "@/lib/utils";

export function AuditTrailPage() {
  const { auditEvents, addToast } = useNirnay();
  const [search, setSearch] = useState("");
  const [moduleFilter, setModuleFilter] = useState("All");
  const [statusFilter, setStatusFilter] = useState("All");
  const [sortBy, setSortBy] = useState<"Newest" | "Confidence" | "Module">("Newest");
  const [selectedEvent, setSelectedEvent] = useState<DemoAuditEvent | null>(null);

  const filteredEvents = useMemo(() => {
    const next = auditEvents
      .filter((event) => {
        const haystack = `${event.module} ${event.action} ${event.sourceReference} ${event.note}`.toLowerCase();
        const matchesSearch = haystack.includes(search.toLowerCase());
        const matchesModule = moduleFilter === "All" || event.module === moduleFilter;
        const matchesStatus = statusFilter === "All" || event.finalStatus === statusFilter;

        return matchesSearch && matchesModule && matchesStatus;
      })
      .sort((left, right) => {
        if (sortBy === "Confidence") {
          return right.confidence - left.confidence;
        }

        if (sortBy === "Module") {
          return left.module.localeCompare(right.module);
        }

        return right.timestamp.localeCompare(left.timestamp);
      });

    return next;
  }, [auditEvents, moduleFilter, search, sortBy, statusFilter]);

  function exportJson() {
    downloadFile(
      JSON.stringify(filteredEvents, null, 2),
      "nirnay-audit-log.json",
      "application/json"
    );
    addToast({
      title: "Audit log exported",
      description: "Filtered audit data downloaded as JSON.",
      tone: "success"
    });
  }

  function exportCsv() {
    const content = [
      ["timestamp", "module", "action", "confidence", "reviewerAction", "finalStatus", "sourceReference"].join(","),
      ...filteredEvents.map((event) =>
        [
          event.timestamp,
          event.module,
          event.action,
          event.confidence.toFixed(2),
          event.reviewerAction,
          event.finalStatus,
          event.sourceReference
        ]
          .map((item) => `"${item.replaceAll('"', '""')}"`)
          .join(",")
      )
    ].join("\n");

    downloadFile(content, "nirnay-audit-log.csv", "text/csv");
    addToast({
      title: "Audit log exported",
      description: "Filtered audit data downloaded as CSV.",
      tone: "success"
    });
  }

  return (
    <div className="page-grid">
      <section className="surface p-6">
        <div className="flex flex-wrap items-end justify-between gap-4">
          <div>
            <p className="eyebrow">Audit Trail</p>
            <h1 className="mt-3 text-3xl font-semibold tracking-tight text-nirnay-navy">
              Searchable, filterable record of AI and reviewer actions
            </h1>
          </div>
          <div className="flex flex-wrap gap-3">
            <Button onClick={exportJson}>Export JSON</Button>
            <Button onClick={exportCsv} variant="secondary">
              <Download className="h-4 w-4" />
              Export CSV
            </Button>
          </div>
        </div>

        <div className="mt-6 grid gap-3 md:grid-cols-[minmax(0,1fr)_180px_160px_160px]">
          <label className="field-shell flex items-center gap-3">
            <Search className="h-4 w-4 text-nirnay-slate" />
            <input
              className="w-full bg-transparent outline-none"
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Search module, action, source, note"
              value={search}
            />
          </label>
          <select className="field-shell" onChange={(event) => setModuleFilter(event.target.value)} value={moduleFilter}>
            {["All", ...new Set(auditEvents.map((event) => event.module))].map((option) => (
              <option key={option}>{option}</option>
            ))}
          </select>
          <select className="field-shell" onChange={(event) => setStatusFilter(event.target.value)} value={statusFilter}>
            {["All", ...new Set(auditEvents.map((event) => event.finalStatus))].map((option) => (
              <option key={option}>{option}</option>
            ))}
          </select>
          <button
            className="field-shell flex items-center justify-center gap-2"
            onClick={() =>
              setSortBy((current) =>
                current === "Newest" ? "Confidence" : current === "Confidence" ? "Module" : "Newest"
              )
            }
            type="button"
          >
            <ArrowDownWideNarrow className="h-4 w-4 text-nirnay-slate" />
            {sortBy}
          </button>
        </div>
      </section>

      <section className="table-shell">
        <div className="grid grid-cols-[180px_150px_minmax(0,1.1fr)_120px_150px_140px] gap-4 border-b border-[rgba(11,63,117,0.08)] px-5 py-4 font-mono text-[11px] uppercase tracking-[0.14em] text-nirnay-slate">
          <span>Timestamp</span>
          <span>Module</span>
          <span>Action</span>
          <span>Confidence</span>
          <span>Reviewer action</span>
          <span>Status</span>
        </div>
        <div className="divide-y divide-[rgba(11,63,117,0.08)]">
          {filteredEvents.map((event) => (
            <button
              className="grid w-full grid-cols-[180px_150px_minmax(0,1.1fr)_120px_150px_140px] gap-4 px-5 py-4 text-left transition hover:bg-[rgba(11,63,117,0.03)]"
              key={event.id}
              onClick={() => setSelectedEvent(event)}
              type="button"
            >
              <span className="text-sm text-nirnay-slate">{event.timestamp}</span>
              <span className="text-sm font-medium text-nirnay-navy">{event.module}</span>
              <span>
                <p className="text-sm font-semibold text-nirnay-navy">{event.action}</p>
                <p className="mt-2 text-sm leading-6 text-nirnay-slate">{event.note}</p>
              </span>
              <span className="text-sm text-nirnay-slate">{Math.round(event.confidence * 100)}%</span>
              <span className="text-sm text-nirnay-slate">{event.reviewerAction}</span>
              <span>
                <Badge>{event.finalStatus}</Badge>
              </span>
            </button>
          ))}
        </div>
      </section>

      <Drawer
        description={selectedEvent?.note}
        onClose={() => setSelectedEvent(null)}
        open={Boolean(selectedEvent)}
        title={selectedEvent?.action ?? "Audit detail"}
      >
        {selectedEvent ? (
          <div className="space-y-4">
            <div className="grid gap-4 md:grid-cols-2">
              {[
                ["Timestamp", selectedEvent.timestamp],
                ["Module", selectedEvent.module],
                ["Confidence", `${Math.round(selectedEvent.confidence * 100)}%`],
                ["Source reference", selectedEvent.sourceReference],
                ["Reviewer action", selectedEvent.reviewerAction],
                ["Final status", selectedEvent.finalStatus]
              ].map(([label, value]) => (
                <div className="surface-subtle p-4" key={label}>
                  <p className="eyebrow">{label}</p>
                  <p className="mt-3 text-sm font-semibold text-nirnay-navy">{value}</p>
                </div>
              ))}
            </div>
            <div className="surface-subtle p-4">
              <p className="eyebrow">Narrative note</p>
              <p className="mt-3 text-sm leading-7 text-nirnay-slate">{selectedEvent.note}</p>
            </div>
          </div>
        ) : null}
      </Drawer>
    </div>
  );
}
