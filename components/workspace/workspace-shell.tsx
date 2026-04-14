"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import type { ReactNode } from "react";
import { Home, LayoutDashboard, ShieldCheck } from "lucide-react";
import { useNirnay } from "@/components/providers/nirnay-provider";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { DemoFlowBanner } from "@/components/workspace/demo-flow-banner";
import { cn } from "@/lib/utils";

const navItems = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/document-intake", label: "Document Intake" },
  { href: "/anonymisation", label: "Anonymisation" },
  { href: "/sae-review", label: "SAE Review" },
  { href: "/completeness-check", label: "Completeness Check" },
  { href: "/version-compare", label: "Version Compare" },
  { href: "/inspection-report", label: "Inspection Report" },
  { href: "/audit-trail", label: "Audit Trail" },
  { href: "/risk-controls", label: "Risk Controls" }
];

export function WorkspaceShell({ children }: { children: ReactNode }) {
  const pathname = usePathname();
  const { reviewerName, documents } = useNirnay();
  const pending = documents.filter((item) => item.status !== "Completed").length;

  return (
    <div className="min-h-screen bg-[linear-gradient(180deg,#EEF8FC_0%,#E6F1F7_100%)]">
      <div className="grid min-h-screen lg:grid-cols-[292px_minmax(0,1fr)]">
        <aside className="border-r border-white/8 bg-[linear-gradient(180deg,#071E3D_0%,#0B3F75_100%)] px-5 py-6 text-white">
          <div className="space-y-3 px-2">
            <p className="eyebrow-light">Nirnay Portal</p>
            <div>
              <h1 className="text-4xl font-semibold tracking-[-0.08em]">Nirnay</h1>
              <p className="mt-3 max-w-xs text-sm leading-6 text-white/70">
                AI-assisted regulatory review workbench for structured evidence and audit-ready
                decisions.
              </p>
            </div>
          </div>

          <div className="mt-6 grid gap-2">
            <Link
              className="rounded-2xl border border-white/10 bg-white/6 px-4 py-3 text-sm font-semibold text-white transition hover:bg-white/10"
              href="/"
            >
              <span className="flex items-center gap-2">
                <Home className="h-4 w-4" />
                Home
              </span>
            </Link>
            <Link
              className="rounded-2xl border border-white/10 bg-white/6 px-4 py-3 text-sm font-semibold text-white transition hover:bg-white/10"
              href="/tour"
            >
              <span className="flex items-center gap-2">
                <LayoutDashboard className="h-4 w-4" />
                Product Tour
              </span>
            </Link>
          </div>

          <nav className="mt-8 grid gap-2">
            {navItems.map((item) => (
              <Link
                className={cn(
                  "rounded-2xl border px-4 py-3 text-sm transition",
                  pathname === item.href
                    ? "border-[rgba(24,166,184,0.32)] bg-white/10 text-white"
                    : "border-transparent bg-transparent text-white/78 hover:border-white/10 hover:bg-white/6 hover:text-white"
                )}
                href={item.href}
                key={item.href}
              >
                {item.label}
              </Link>
            ))}
          </nav>

          <div className="mt-8 surface-subtle border-white/10 bg-white/7 p-4 text-white shadow-none">
            <p className="eyebrow-light">Reviewer Status</p>
            <p className="mt-3 text-base font-semibold">{reviewerName}</p>
            <p className="mt-2 text-sm leading-6 text-white/70">
              {pending} packets remain active across the review cockpit.
            </p>
            <Badge className="mt-4 border-white/14 bg-white/10 text-white/80">
              Assistive AI only
            </Badge>
          </div>
        </aside>

        <div className="min-w-0">
          <header className="sticky-header mx-4 mt-4 flex items-center justify-between gap-4 px-5 py-4 md:mx-6 lg:mx-8">
            <div>
              <p className="eyebrow">Operational Header</p>
              <h2 className="mt-2 text-2xl font-semibold tracking-tight text-nirnay-navy">
                Regulatory intelligence cockpit
              </h2>
            </div>
            <div className="flex items-center gap-3">
              <Badge>{reviewerName}</Badge>
              <Link href="/audit-trail">
                <Button variant="secondary">
                  <ShieldCheck className="h-4 w-4" />
                  Open Audit Trail
                </Button>
              </Link>
            </div>
          </header>
          <div className="page-shell pt-5">
            <DemoFlowBanner />
            {children}
          </div>
        </div>
      </div>
    </div>
  );
}
