"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { ArrowRight, ShieldCheck } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

const flow = [
  {
    route: "/dashboard",
    label: "1. Dashboard",
    purpose: "Open with a live operating picture and today’s priority items."
  },
  {
    route: "/document-intake",
    label: "2. Document Intake",
    purpose: "Show packet upload, classification, metadata, and routing."
  },
  {
    route: "/anonymisation",
    label: "3. Anonymisation",
    purpose: "Create the privacy and redaction moment with validation and escalation."
  },
  {
    route: "/sae-review",
    label: "4. SAE Review",
    purpose: "Demonstrate structured extraction, evidence, override, and packet generation."
  },
  {
    route: "/completeness-check",
    label: "5. Completeness",
    purpose: "Show dynamic gap resolution and deficiency memo generation."
  },
  {
    route: "/version-compare",
    label: "6. Version Compare",
    purpose: "Highlight substantive protocol change detection and reviewer summary."
  },
  {
    route: "/inspection-report",
    label: "7. Inspection Report",
    purpose: "Convert rough notes into a formal, exportable inspection draft."
  },
  {
    route: "/audit-trail",
    label: "8. Audit Trail",
    purpose: "Land the trust story with full traceability and export."
  },
  {
    route: "/risk-controls",
    label: "9. Risk Controls",
    purpose: "Close with official-facing mitigations and accountability language."
  }
];

export function DemoFlowBanner() {
  const pathname = usePathname();
  const currentIndex = flow.findIndex((item) => item.route === pathname);
  const current = flow[currentIndex];
  const next = flow[currentIndex + 1];

  if (!current) {
    return null;
  }

  return (
    <section className="surface mb-5 px-5 py-4">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div className="space-y-2">
          <div className="flex flex-wrap items-center gap-2">
            <Badge>3-minute judging path</Badge>
            <Badge className="border-[rgba(46,125,50,0.2)] bg-[rgba(46,125,50,0.08)] text-[var(--nirnay-green)]">
              Step {currentIndex + 1} of {flow.length}
            </Badge>
          </div>
          <h3 className="text-xl font-semibold tracking-tight text-nirnay-navy">{current.label}</h3>
          <p className="max-w-3xl text-sm leading-7 text-nirnay-slate">{current.purpose}</p>
          <div className="flex items-center gap-2 text-sm text-nirnay-slate">
            <ShieldCheck className="h-4 w-4 text-nirnay-cyan" />
            Assistive AI only. Reviewer action and audit trace remain visible.
          </div>
        </div>
        {next ? (
          <Link href={next.route}>
            <Button>
              Next demo step
              <ArrowRight className="h-4 w-4" />
            </Button>
          </Link>
        ) : null}
      </div>
    </section>
  );
}
