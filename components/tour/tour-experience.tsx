"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { AnimatePresence, motion } from "framer-motion";
import { ArrowRight, CheckCircle2, ChevronLeft, PlayCircle, SkipForward } from "lucide-react";
import { useState } from "react";
import { TOUR_STEPS } from "@/lib/demo-data";
import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

export function TourExperience({
  embedded = false,
  onFinish
}: {
  embedded?: boolean;
  onFinish?: () => void;
}) {
  const router = useRouter();
  const [step, setStep] = useState(0);
  const active = TOUR_STEPS[step];

  function finish() {
    onFinish?.();
    router.push("/dashboard");
  }

  return (
    <div className={cn("grid gap-6", embedded ? "min-h-[520px]" : "page-shell min-h-screen py-8")}>
      {!embedded ? (
        <div className="flex items-center justify-between gap-4">
          <div className="space-y-2">
            <p className="eyebrow">Product Tour</p>
            <h1 className="text-4xl font-semibold tracking-tight text-nirnay-navy md:text-5xl">
              Guided walk-through of the Nirnay review flow
            </h1>
            <p className="max-w-3xl text-sm leading-7 text-nirnay-slate md:text-base">
              This is a real multi-step tour, not a static carousel. Each step can launch a live
              module so the presentation never stalls.
            </p>
          </div>
          <Badge className="border-[rgba(24,166,184,0.22)] bg-[rgba(24,166,184,0.08)] text-nirnay-blue">
            Live demo path
          </Badge>
        </div>
      ) : null}

      <div className="grid gap-5 lg:grid-cols-[280px_minmax(0,1fr)]">
        <div className="surface p-4 md:p-5">
          <div className="mb-4 flex items-center justify-between">
            <div>
              <p className="eyebrow">Stepper</p>
              <p className="mt-2 text-sm text-nirnay-slate">{`${step + 1} of ${TOUR_STEPS.length}`}</p>
            </div>
            <PlayCircle className="h-5 w-5 text-nirnay-cyan" />
          </div>
          <div className="grid gap-2">
            {TOUR_STEPS.map((tourStep, index) => (
              <button
                className={cn(
                  "rounded-2xl border px-4 py-4 text-left transition",
                  step === index
                    ? "border-[rgba(24,166,184,0.28)] bg-[rgba(24,166,184,0.08)]"
                    : "border-[rgba(11,63,117,0.1)] bg-white/90 hover:border-[rgba(11,63,117,0.18)] hover:bg-[rgba(11,63,117,0.03)]"
                )}
                key={tourStep.id}
                onClick={() => setStep(index)}
                type="button"
              >
                <p className="font-mono text-[11px] uppercase tracking-[0.12em] text-nirnay-blue">
                  Step {index + 1}
                </p>
                <p className="mt-2 text-base font-semibold text-nirnay-navy">{tourStep.title}</p>
                <p className="mt-2 text-sm leading-6 text-nirnay-slate">{tourStep.signal}</p>
              </button>
            ))}
          </div>
        </div>

        <AnimatePresence mode="wait">
          <motion.div
            animate={{ opacity: 1, y: 0 }}
            className="surface overflow-hidden"
            exit={{ opacity: 0, y: 10 }}
            initial={{ opacity: 0, y: 10 }}
            key={active.id}
            transition={{ duration: 0.22 }}
          >
            <div className="grid gap-0 lg:grid-cols-[minmax(0,1fr)_360px]">
              <div className="p-6 md:p-8">
                <div className="mb-6 flex flex-wrap items-center gap-3">
                  <Badge>{active.title}</Badge>
                  <Badge className="border-[rgba(245,166,35,0.24)] bg-[rgba(245,166,35,0.1)] text-[var(--nirnay-amber)]">
                    Reviewer controlled
                  </Badge>
                </div>

                <h2 className="text-3xl font-semibold tracking-tight text-nirnay-navy md:text-4xl">
                  {active.signal}
                </h2>
                <p className="mt-4 max-w-3xl text-sm leading-7 text-nirnay-slate md:text-base">
                  {active.detail}
                </p>

                <div className="mt-8 grid gap-4 md:grid-cols-3">
                  {active.outputs.map((output) => (
                    <div
                      className="surface-subtle border-[rgba(11,63,117,0.08)] p-4"
                      key={output}
                    >
                      <p className="eyebrow">Output</p>
                      <p className="mt-3 text-sm font-semibold text-nirnay-navy">{output}</p>
                    </div>
                  ))}
                </div>

                <div className="mt-8 flex flex-wrap gap-3">
                  <Button onClick={() => router.push(active.route)}>Open Live Module</Button>
                  <Link className="ghost-button" href="/dashboard">
                    Jump to Dashboard
                  </Link>
                </div>
              </div>

              <div className="bg-[linear-gradient(180deg,rgba(7,30,61,0.98)_0%,rgba(11,63,117,0.96)_100%)] p-6 text-white">
                <p className="eyebrow-light">Highlighted area</p>
                <div className="mt-4 rounded-[1.75rem] border border-white/10 bg-white/6 p-4">
                  <div className="flex items-center justify-between">
                    <span className="font-mono text-[11px] uppercase tracking-[0.14em] text-white/50">
                      {active.title}
                    </span>
                    <CheckCircle2 className="h-4 w-4 text-nirnay-cyan" />
                  </div>
                  <div className="mt-4 grid gap-3">
                    <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                      <p className="text-sm font-semibold">Key reviewer surface</p>
                      <p className="mt-2 text-sm leading-6 text-white/70">
                        The demo highlights the actual controls the reviewer interacts with on this
                        module, so the walkthrough maps directly to the live product.
                      </p>
                    </div>
                    <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-1">
                      {active.outputs.map((item) => (
                        <div
                          className="rounded-2xl border border-white/10 bg-[rgba(255,255,255,0.04)] p-3"
                          key={item}
                        >
                          <p className="font-mono text-[11px] uppercase tracking-[0.12em] text-white/45">
                            Surface
                          </p>
                          <p className="mt-2 text-sm text-white/78">{item}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                <div className="mt-6 flex flex-wrap gap-3">
                  <Button
                    className="bg-white text-nirnay-blue hover:bg-white"
                    onClick={() => setStep((current) => Math.max(0, current - 1))}
                    variant="primary"
                  >
                    <ChevronLeft className="h-4 w-4" />
                    Back
                  </Button>
                  {step < TOUR_STEPS.length - 1 ? (
                    <Button
                      className="border-white/12 bg-white/8 text-white shadow-none hover:bg-white/12"
                      onClick={() => setStep((current) => Math.min(TOUR_STEPS.length - 1, current + 1))}
                      variant="primary"
                    >
                      Next
                      <ArrowRight className="h-4 w-4" />
                    </Button>
                  ) : (
                    <Button
                      className="border-white/12 bg-white/8 text-white shadow-none hover:bg-white/12"
                      onClick={finish}
                      variant="primary"
                    >
                      Finish
                    </Button>
                  )}
                  <Button
                    className="border-white/10 bg-transparent text-white shadow-none hover:bg-white/8"
                    onClick={finish}
                    variant="primary"
                  >
                    <SkipForward className="h-4 w-4" />
                    Skip
                  </Button>
                </div>
              </div>
            </div>
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  );
}
