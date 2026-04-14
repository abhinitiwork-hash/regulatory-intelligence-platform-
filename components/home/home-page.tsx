"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import {
  ArrowRight,
  ChevronDown,
  FileScan,
  Shield,
  Sparkles,
  Waypoints
} from "lucide-react";
import { useEffect, useState } from "react";
import {
  DASHBOARD_METRICS,
  TRUST_CONTROLS,
  WHAT_NIRNAY_DOES
} from "@/lib/demo-data";
import { AnimatedCounter } from "@/components/ui/animated-counter";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Modal } from "@/components/ui/modal";
import { TourExperience } from "@/components/tour/tour-experience";
import { cn } from "@/lib/utils";

const flowSteps = [
  "Intake",
  "Anonymisation",
  "Intelligence",
  "Human Review",
  "Audit Output"
];

export function HomePage() {
  const router = useRouter();
  const [scrolled, setScrolled] = useState(false);
  const [tourOpen, setTourOpen] = useState(false);
  const [selectedCapability, setSelectedCapability] = useState<(typeof WHAT_NIRNAY_DOES)[number] | null>(
    null
  );
  const [governanceExpanded, setGovernanceExpanded] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 18);

    onScroll();
    window.addEventListener("scroll", onScroll);

    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <>
      <div className="relative min-h-screen overflow-x-clip">
        <header
          className={cn(
            "fixed inset-x-0 top-0 z-40 transition",
            scrolled ? "px-4 py-3 md:px-6" : "px-4 py-5 md:px-6"
          )}
        >
          <div
            className={cn(
              "mx-auto flex w-full max-w-[1400px] items-center justify-between gap-4 rounded-full border px-4 py-3 transition md:px-6",
              scrolled
                ? "border-[rgba(11,63,117,0.14)] bg-white/78 shadow-[0_18px_40px_rgba(7,30,61,0.1)] backdrop-blur-xl"
                : "border-transparent bg-transparent"
            )}
          >
            <Link className="text-2xl font-semibold tracking-[-0.08em] text-nirnay-navy" href="/">
              Nirnay
            </Link>
            <nav className="hidden items-center gap-5 text-sm font-medium text-nirnay-slate md:flex">
              <a href="#what-it-does">Capabilities</a>
              <a href="#trust">Governance</a>
              <a href="#tour">Tour</a>
              <Link href="/dashboard">Dashboard</Link>
            </nav>
            <div className="flex items-center gap-2">
              <Button onClick={() => setTourOpen(true)} variant="secondary">
                Take Product Tour
              </Button>
              <Button onClick={() => router.push("/dashboard")}>Start Review</Button>
            </div>
          </div>
        </header>

        <main className="page-shell pt-28 md:pt-32">
          <div className="grid gap-6">
            <section className="surface-dark relative overflow-hidden p-6 md:p-8 lg:p-10">
              <div className="absolute inset-y-0 right-[-10%] hidden w-[48%] bg-[radial-gradient(circle_at_center,rgba(24,166,184,0.18)_0,transparent_58%)] lg:block" />
              <div className="grid gap-8 lg:grid-cols-[minmax(0,1.05fr)_440px]">
                <motion.div
                  animate={{ opacity: 1, y: 0 }}
                  initial={{ opacity: 0, y: 18 }}
                  transition={{ duration: 0.45 }}
                >
                  <Badge className="border-white/12 bg-white/8 text-white/72">Regulatory Intelligence Cockpit</Badge>
                  <h1 className="mt-6 max-w-4xl text-5xl font-semibold tracking-[-0.08em] text-white md:text-7xl">
                    Nirnay
                  </h1>
                  <p className="mt-5 max-w-3xl text-base leading-8 text-white/76 md:text-lg">
                    AI-assisted regulatory review workbench for structured evidence,
                    protected data, and audit-ready decisions.
                  </p>

                  <div className="mt-8 flex flex-wrap gap-3">
                    <Button onClick={() => router.push("/dashboard")}>
                      Start Review
                      <ArrowRight className="h-4 w-4" />
                    </Button>
                    <Button onClick={() => setTourOpen(true)} variant="secondary">
                      Take Product Tour
                    </Button>
                  </div>

                  <div className="mt-8 inline-flex items-center gap-3 rounded-full border border-white/12 bg-white/8 px-4 py-2 text-sm text-white/72">
                    <Shield className="h-4 w-4 text-nirnay-cyan" />
                    Assistive AI only. Final decision remains with the authorised reviewer.
                  </div>

                  <div className="mt-10 grid gap-3 md:grid-cols-5">
                    {flowSteps.map((step, index) => (
                      <div
                        className="rounded-2xl border border-white/10 bg-white/6 p-4"
                        key={step}
                      >
                        <p className="font-mono text-[11px] uppercase tracking-[0.14em] text-white/45">
                          {`0${index + 1}`}
                        </p>
                        <p className="mt-3 text-sm font-semibold text-white">{step}</p>
                      </div>
                    ))}
                  </div>
                </motion.div>

                <motion.div
                  animate={{ opacity: 1, x: 0 }}
                  className="rounded-[1.75rem] border border-white/10 bg-white/6 p-5"
                  initial={{ opacity: 0, x: 18 }}
                  transition={{ duration: 0.45, delay: 0.05 }}
                >
                  <div className="mb-5 flex items-center justify-between">
                    <div>
                      <p className="eyebrow-light">Command center</p>
                      <h2 className="mt-2 text-xl font-semibold text-white">
                        Reviewer operating picture
                      </h2>
                    </div>
                    <Waypoints className="h-5 w-5 text-nirnay-cyan" />
                  </div>
                  <div className="grid gap-3 sm:grid-cols-2">
                    {DASHBOARD_METRICS.map((metric) => (
                      <div
                        className="rounded-2xl border border-white/8 bg-[rgba(4,14,28,0.22)] p-4"
                        key={metric.id}
                      >
                        <p className="text-sm text-white/60">{metric.label}</p>
                        <p className="mt-3 text-3xl font-semibold tracking-[-0.06em] text-white">
                          <AnimatedCounter suffix={metric.suffix} value={metric.value} />
                        </p>
                        <p className="mt-2 text-sm leading-6 text-white/64">{metric.detail}</p>
                      </div>
                    ))}
                  </div>
                </motion.div>
              </div>
            </section>

            <motion.section
              className="surface p-6 md:p-8"
              id="what-it-does"
              initial={{ opacity: 0, y: 18 }}
              transition={{ duration: 0.35 }}
              viewport={{ once: true, margin: "-80px" }}
              whileInView={{ opacity: 1, y: 0 }}
            >
              <div className="flex flex-wrap items-end justify-between gap-4">
                <div className="space-y-3">
                  <p className="eyebrow">What Nirnay Does</p>
                  <h2 className="text-3xl font-semibold tracking-tight text-nirnay-navy md:text-4xl">
                    Built for regulated review, not chat
                  </h2>
                  <p className="max-w-3xl text-sm leading-7 text-nirnay-slate md:text-base">
                    Each capability opens a detail surface, so nothing on the home page is static.
                  </p>
                </div>
                <Badge className="border-[rgba(24,166,184,0.22)] bg-[rgba(24,166,184,0.08)] text-nirnay-blue">
                  Interactive details
                </Badge>
              </div>

              <div className="mt-8 grid gap-4 md:grid-cols-3">
                {WHAT_NIRNAY_DOES.map((item, index) => (
                  <motion.button
                    className="surface-subtle cursor-pointer p-5 text-left"
                    key={item.id}
                    onClick={() => setSelectedCapability(item)}
                    transition={{ duration: 0.22, delay: index * 0.04 }}
                    viewport={{ once: true }}
                    whileHover={{ y: -4 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    initial={{ opacity: 0, y: 14 }}
                  >
                    <div className="flex items-center justify-between">
                      <span className="rounded-2xl bg-[rgba(24,166,184,0.08)] p-3 text-nirnay-blue">
                        {index === 0 ? (
                          <Shield className="h-5 w-5" />
                        ) : index === 1 ? (
                          <FileScan className="h-5 w-5" />
                        ) : (
                          <Sparkles className="h-5 w-5" />
                        )}
                      </span>
                      <ArrowRight className="h-4 w-4 text-nirnay-slate" />
                    </div>
                    <h3 className="mt-6 text-xl font-semibold tracking-tight text-nirnay-navy">
                      {item.title}
                    </h3>
                    <p className="mt-3 text-sm leading-7 text-nirnay-slate">{item.summary}</p>
                  </motion.button>
                ))}
              </div>
            </motion.section>

            <motion.section
              className="surface p-6 md:p-8"
              id="trust"
              initial={{ opacity: 0, y: 18 }}
              transition={{ duration: 0.35 }}
              viewport={{ once: true, margin: "-80px" }}
              whileInView={{ opacity: 1, y: 0 }}
            >
              <div className="flex flex-wrap items-center justify-between gap-4">
                <div>
                  <p className="eyebrow">Why Reviewers Can Trust It</p>
                  <h2 className="mt-3 text-3xl font-semibold tracking-tight text-nirnay-navy">
                    Governance controls are visible, not buried
                  </h2>
                </div>
                <Button
                  onClick={() => setGovernanceExpanded((current) => !current)}
                  variant="secondary"
                >
                  {governanceExpanded ? "Collapse controls" : "Expand controls"}
                  <ChevronDown
                    className={cn("h-4 w-4 transition", governanceExpanded && "rotate-180")}
                  />
                </Button>
              </div>

              <div className="mt-6 grid gap-4 md:grid-cols-2">
                {TRUST_CONTROLS.map((control) => (
                  <motion.div
                    animate={{ opacity: 1, height: "auto" }}
                    className="surface-subtle overflow-hidden p-5"
                    initial={false}
                    key={control.id}
                  >
                    <h3 className="text-lg font-semibold tracking-tight text-nirnay-navy">
                      {control.title}
                    </h3>
                    <p className="mt-3 text-sm leading-7 text-nirnay-slate">
                      {governanceExpanded
                        ? control.detail
                        : `${control.detail.split(".")[0]}.`}
                    </p>
                  </motion.div>
                ))}
              </div>
            </motion.section>

            <motion.section
              className="surface p-6 md:p-8"
              id="tour"
              initial={{ opacity: 0, y: 18 }}
              transition={{ duration: 0.35 }}
              viewport={{ once: true, margin: "-80px" }}
              whileInView={{ opacity: 1, y: 0 }}
            >
              <div className="flex flex-wrap items-end justify-between gap-4">
                <div>
                  <p className="eyebrow">Product Tour</p>
                  <h2 className="mt-3 text-3xl font-semibold tracking-tight text-nirnay-navy">
                    Run the guided walkthrough or jump straight into the live dashboard
                  </h2>
                </div>
                <div className="flex gap-3">
                  <Button onClick={() => setTourOpen(true)} variant="secondary">
                    Launch Overlay Tour
                  </Button>
                  <Link className="action-button" href="/tour">
                    Open Tour Page
                  </Link>
                </div>
              </div>
            </motion.section>
          </div>
        </main>
      </div>

      <Modal
        description="A real multi-step walkthrough tied to live module routes."
        onClose={() => setTourOpen(false)}
        open={tourOpen}
        title="Nirnay product tour"
      >
        <TourExperience embedded onFinish={() => setTourOpen(false)} />
      </Modal>

      <Modal
        description={selectedCapability?.summary}
        onClose={() => setSelectedCapability(null)}
        open={Boolean(selectedCapability)}
        title={selectedCapability?.title ?? "Capability detail"}
      >
        <div className="space-y-4">
          <p className="text-sm leading-7 text-nirnay-slate">{selectedCapability?.details}</p>
          <div className="grid gap-3 md:grid-cols-2">
            <div className="surface-subtle p-4">
              <p className="eyebrow">Live relevance</p>
              <p className="mt-3 text-sm leading-7 text-nirnay-slate">
                This capability maps directly into the route-based demo pages and contributes to
                the shared audit trail.
              </p>
            </div>
            <div className="surface-subtle p-4">
              <p className="eyebrow">Next action</p>
              <div className="mt-4">
                <Button onClick={() => router.push("/dashboard")}>Enter Dashboard</Button>
              </div>
            </div>
          </div>
        </div>
      </Modal>
    </>
  );
}
