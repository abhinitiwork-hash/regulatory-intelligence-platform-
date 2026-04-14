"use client";

import { useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import {
  ArrowRight,
  ChevronDown,
  Clock3,
  Filter,
  Flame,
  Layers3
} from "lucide-react";
import {
  DASHBOARD_METRICS,
  MODULE_SHORTCUTS
} from "@/lib/demo-data";
import { DemoDocument } from "@/lib/demo-types";
import { useNirnay } from "@/components/providers/nirnay-provider";
import { AnimatedCounter } from "@/components/ui/animated-counter";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Drawer } from "@/components/ui/drawer";
import { cn } from "@/lib/utils";

const riskLevels = ["All", "Critical", "High", "Medium", "Low"] as const;

function routeForModule(module: string) {
  if (module === "Summarisation") {
    return "/document-intake";
  }

  return `/${module.toLowerCase().replace(/\s+/g, "-")}`;
}

export function DashboardPage() {
  const router = useRouter();
  const { documents, auditEvents, priorityItems } = useNirnay();
  const [selectedType, setSelectedType] = useState<string>("All");
  const [selectedRisk, setSelectedRisk] = useState<(typeof riskLevels)[number]>("All");
  const [selectedStage, setSelectedStage] = useState<string>("All");
  const [expandedPriority, setExpandedPriority] = useState<string | null>(priorityItems[0]?.id ?? null);
  const [activeDocument, setActiveDocument] = useState<DemoDocument | null>(null);

  const filteredDocuments = useMemo(() => {
    return documents.filter((document) => {
      const matchesType = selectedType === "All" || document.documentType === selectedType;
      const matchesRisk = selectedRisk === "All" || document.riskLevel === selectedRisk;
      const matchesStage = selectedStage === "All" || document.stage === selectedStage;

      return matchesType && matchesRisk && matchesStage;
    });
  }, [documents, selectedRisk, selectedStage, selectedType]);

  const riskHeat = useMemo(() => {
    return {
      Critical: documents.filter((item) => item.riskLevel === "Critical").length,
      High: documents.filter((item) => item.riskLevel === "High").length,
      Medium: documents.filter((item) => item.riskLevel === "Medium").length,
      Low: documents.filter((item) => item.riskLevel === "Low").length
    };
  }, [documents]);

  return (
    <div className="page-grid">
      <section className="surface-dark overflow-hidden p-6 md:p-8">
        <div className="grid gap-6 xl:grid-cols-[minmax(0,1.1fr)_420px]">
          <div>
            <Badge className="border-white/12 bg-white/8 text-white/72">Live Review Board</Badge>
            <h1 className="mt-5 text-4xl font-semibold tracking-[-0.06em] text-white md:text-5xl">
              High-information review cockpit with no dead paths
            </h1>
            <p className="mt-4 max-w-3xl text-sm leading-7 text-white/74 md:text-base">
              Filters, queues, priorities, and activity are connected to the live module routes so
              you can present the entire system without landing on a static screen.
            </p>

            <div className="mt-8 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {DASHBOARD_METRICS.map((metric) => (
                <div
                  className="rounded-3xl border border-white/8 bg-[rgba(4,14,28,0.2)] p-4"
                  key={metric.id}
                >
                  <p className="text-sm text-white/58">{metric.label}</p>
                  <p className="mt-3 text-3xl font-semibold tracking-[-0.06em] text-white">
                    <AnimatedCounter suffix={metric.suffix} value={metric.value} />
                  </p>
                  <p className="mt-2 text-sm leading-6 text-white/62">{metric.detail}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="rounded-[1.75rem] border border-white/10 bg-white/6 p-5">
            <div className="flex items-center justify-between">
              <div>
                <p className="eyebrow-light">Today’s priority items</p>
                <p className="mt-2 text-lg font-semibold text-white">Expandable reviewer queue</p>
              </div>
              <Flame className="h-5 w-5 text-[var(--nirnay-amber)]" />
            </div>

            <div className="mt-5 grid gap-3">
              {priorityItems.map((item) => (
                <button
                  className={cn(
                    "rounded-3xl border p-4 text-left transition",
                    expandedPriority === item.id
                      ? "border-[rgba(24,166,184,0.28)] bg-white/10"
                      : "border-white/8 bg-white/5 hover:bg-white/8"
                  )}
                  key={item.id}
                  onClick={() =>
                    setExpandedPriority((current) => (current === item.id ? null : item.id))
                  }
                  type="button"
                >
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <p className="font-mono text-[11px] uppercase tracking-[0.12em] text-white/48">
                        {item.riskLevel}
                      </p>
                      <p className="mt-2 text-sm font-semibold text-white">{item.title}</p>
                    </div>
                    <ChevronDown
                      className={cn(
                        "mt-1 h-4 w-4 text-white/56 transition",
                        expandedPriority === item.id && "rotate-180"
                      )}
                    />
                  </div>
                  {expandedPriority === item.id ? (
                    <motion.div
                      animate={{ opacity: 1, height: "auto" }}
                      className="mt-4 space-y-3 text-sm leading-6 text-white/72"
                      initial={{ opacity: 0, height: 0 }}
                    >
                      <p>{item.summary}</p>
                      <p>
                        <span className="font-semibold text-white">Next step:</span> {item.nextStep}
                      </p>
                      <Button
                        className="border-white/10 bg-white/10 text-white shadow-none hover:bg-white/16"
                        onClick={(event) => {
                          event.stopPropagation();
                          router.push(item.route);
                        }}
                        variant="primary"
                      >
                        Open Item
                        <ArrowRight className="h-4 w-4" />
                      </Button>
                    </motion.div>
                  ) : null}
                </button>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section className="grid gap-5 xl:grid-cols-[minmax(0,1.05fr)_360px]">
        <div className="surface p-6">
          <div className="flex flex-wrap items-end justify-between gap-4">
            <div>
              <p className="eyebrow">Review Queue</p>
              <h2 className="mt-3 text-3xl font-semibold tracking-tight text-nirnay-navy">
                Pending reviewer actions and recent documents
              </h2>
            </div>
            <Badge className="border-[rgba(11,63,117,0.18)] bg-[rgba(11,63,117,0.06)] text-nirnay-blue">
              Click a row for detail
            </Badge>
          </div>

          <div className="mt-6 flex flex-wrap gap-3">
            <select
              className="field-shell min-w-[180px]"
              onChange={(event) => setSelectedType(event.target.value)}
              value={selectedType}
            >
              {["All", ...new Set(documents.map((item) => item.documentType))].map((option) => (
                <option key={option}>{option}</option>
              ))}
            </select>
            <select
              className="field-shell min-w-[160px]"
              onChange={(event) => setSelectedRisk(event.target.value as (typeof riskLevels)[number])}
              value={selectedRisk}
            >
              {riskLevels.map((option) => (
                <option key={option}>{option}</option>
              ))}
            </select>
            <select
              className="field-shell min-w-[180px]"
              onChange={(event) => setSelectedStage(event.target.value)}
              value={selectedStage}
            >
              {["All", ...new Set(documents.map((item) => item.stage))].map((option) => (
                <option key={option}>{option}</option>
              ))}
            </select>
            <Button
              onClick={() => {
                setSelectedType("All");
                setSelectedRisk("All");
                setSelectedStage("All");
              }}
              variant="secondary"
            >
              <Filter className="h-4 w-4" />
              Reset filters
            </Button>
          </div>

          <div className="table-shell mt-6">
            <div className="grid grid-cols-[minmax(0,1.1fr)_160px_140px_130px] gap-4 border-b border-[rgba(11,63,117,0.08)] px-5 py-4 font-mono text-[11px] uppercase tracking-[0.14em] text-nirnay-slate">
              <span>Document</span>
              <span>Stage</span>
              <span>Risk</span>
              <span>Status</span>
            </div>
            <div className="divide-y divide-[rgba(11,63,117,0.08)]">
              {filteredDocuments.map((document) => (
                <button
                  className="grid w-full grid-cols-[minmax(0,1.1fr)_160px_140px_130px] gap-4 px-5 py-4 text-left transition hover:bg-[rgba(11,63,117,0.03)]"
                  key={document.id}
                  onClick={() => setActiveDocument(document)}
                  type="button"
                >
                  <div>
                    <p className="text-sm font-semibold text-nirnay-navy">{document.name}</p>
                    <p className="mt-2 text-sm leading-6 text-nirnay-slate">{document.summary}</p>
                  </div>
                  <div className="text-sm text-nirnay-slate">{document.stage}</div>
                  <div className="text-sm text-nirnay-slate">{document.riskLevel}</div>
                  <div className="text-sm text-nirnay-slate">{document.status}</div>
                </button>
              ))}
            </div>
          </div>
        </div>

        <div className="grid gap-5">
          <div className="surface p-5">
            <div className="flex items-center justify-between">
              <div>
                <p className="eyebrow">Risk Heat</p>
                <p className="mt-2 text-xl font-semibold tracking-tight text-nirnay-navy">
                  Current document distribution
                </p>
              </div>
              <Flame className="h-5 w-5 text-[var(--nirnay-amber)]" />
            </div>
            <div className="mt-5 grid gap-3">
              {Object.entries(riskHeat).map(([level, count]) => (
                <div className="rounded-2xl border border-[rgba(11,63,117,0.08)] p-4" key={level}>
                  <div className="flex items-center justify-between">
                    <p className="text-sm font-semibold text-nirnay-navy">{level}</p>
                    <p className="text-sm text-nirnay-slate">{count}</p>
                  </div>
                  <div className="mt-3 h-2 rounded-full bg-[rgba(11,63,117,0.06)]">
                    <div
                      className={cn(
                        "h-2 rounded-full",
                        level === "Critical" && "bg-[var(--nirnay-red)]",
                        level === "High" && "bg-[var(--nirnay-amber)]",
                        level === "Medium" && "bg-[var(--nirnay-cyan)]",
                        level === "Low" && "bg-[var(--nirnay-green)]"
                      )}
                      style={{ width: `${Math.max(12, count * 20)}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="surface p-5">
            <div className="flex items-center justify-between">
              <div>
                <p className="eyebrow">Activity Timeline</p>
                <p className="mt-2 text-xl font-semibold tracking-tight text-nirnay-navy">
                  Latest AI and reviewer events
                </p>
              </div>
              <Clock3 className="h-5 w-5 text-nirnay-cyan" />
            </div>
            <div className="mt-5 grid gap-4">
              {auditEvents.slice(0, 5).map((event) => (
                <div className="rounded-2xl border border-[rgba(11,63,117,0.08)] p-4" key={event.id}>
                  <div className="flex items-center justify-between gap-3">
                    <p className="text-sm font-semibold text-nirnay-navy">{event.module}</p>
                    <p className="text-xs text-nirnay-slate">{event.timestamp}</p>
                  </div>
                  <p className="mt-2 text-sm text-nirnay-slate">{event.action}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section className="surface p-6">
        <div className="flex items-center justify-between gap-4">
          <div>
            <p className="eyebrow">Module Shortcuts</p>
            <h2 className="mt-3 text-3xl font-semibold tracking-tight text-nirnay-navy">
              Open any workflow directly
            </h2>
          </div>
          <Layers3 className="h-5 w-5 text-nirnay-cyan" />
        </div>

        <div className="mt-6 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {MODULE_SHORTCUTS.map((shortcut) => (
            <button
              className="surface-subtle p-5 text-left transition hover:-translate-y-1"
              key={shortcut.id}
              onClick={() => router.push(shortcut.route)}
              type="button"
            >
              <Badge>{shortcut.badge}</Badge>
              <h3 className="mt-5 text-xl font-semibold tracking-tight text-nirnay-navy">
                {shortcut.title}
              </h3>
              <p className="mt-3 text-sm leading-7 text-nirnay-slate">{shortcut.description}</p>
              <div className="mt-5 flex items-center gap-2 text-sm font-semibold text-nirnay-blue">
                Open module
                <ArrowRight className="h-4 w-4" />
              </div>
            </button>
          ))}
        </div>
      </section>

      <Drawer
        description={activeDocument?.summary}
        onClose={() => setActiveDocument(null)}
        open={Boolean(activeDocument)}
        title={activeDocument?.name ?? "Document detail"}
      >
        {activeDocument ? (
          <div className="space-y-5">
            <div className="grid gap-3 md:grid-cols-2">
              {Object.entries(activeDocument.metadata).map(([key, value]) => (
                <div className="surface-subtle p-4" key={key}>
                  <p className="eyebrow">{key}</p>
                  <p className="mt-3 text-sm font-semibold text-nirnay-navy">{value}</p>
                </div>
              ))}
            </div>
            <div className="surface-subtle p-4">
              <p className="eyebrow">Preview</p>
              <p className="mt-3 text-sm leading-7 text-nirnay-slate">{activeDocument.preview}</p>
            </div>
            <div className="flex flex-wrap gap-3">
              <Button onClick={() => router.push(routeForModule(activeDocument.assignedModule))}>
                Open Assigned Module
              </Button>
              <Button onClick={() => router.push("/audit-trail")} variant="secondary">
                Inspect Audit Entries
              </Button>
            </div>
          </div>
        ) : null}
      </Drawer>
    </div>
  );
}
