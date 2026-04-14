"use client";

import { useState } from "react";
import { ChevronDown, Scale, ShieldCheck } from "lucide-react";
import { RISK_CONTROL_TOPICS } from "@/lib/demo-data";
import { useNirnay } from "@/components/providers/nirnay-provider";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

export function RiskControlsPage() {
  const { addToast } = useNirnay();
  const [openId, setOpenId] = useState(RISK_CONTROL_TOPICS[0]?.id ?? "");

  return (
    <div className="page-grid">
      <section className="surface-dark p-6 md:p-8">
        <Badge className="border-white/12 bg-white/8 text-white/72">Reviewer Questions / Risk Controls</Badge>
        <h1 className="mt-5 text-4xl font-semibold tracking-[-0.06em] text-white">
          Assistive AI only. Final decision remains with the authorised reviewer.
        </h1>
        <p className="mt-4 max-w-4xl text-sm leading-8 text-white/74 md:text-base">
          This screen is designed for official scrutiny. It answers the accountability, privacy,
          quality, and integration concerns that a CDSCO-style review panel is likely to raise.
        </p>
      </section>

      <section className="grid gap-5 xl:grid-cols-[320px_minmax(0,1fr)]">
        <div className="surface p-6">
          <p className="eyebrow">Concern Index</p>
          <div className="mt-5 grid gap-3">
            {RISK_CONTROL_TOPICS.map((topic) => (
              <button
                className={`rounded-3xl border px-4 py-4 text-left transition ${
                  openId === topic.id
                    ? "border-[rgba(24,166,184,0.28)] bg-[rgba(24,166,184,0.08)]"
                    : "border-[rgba(11,63,117,0.08)] bg-white"
                }`}
                key={topic.id}
                onClick={() => setOpenId(topic.id)}
                type="button"
              >
                <p className="text-sm font-semibold text-nirnay-navy">{topic.title}</p>
                <p className="mt-2 text-sm leading-6 text-nirnay-slate">{topic.concern}</p>
              </button>
            ))}
          </div>
        </div>

        <div className="grid gap-4">
          {RISK_CONTROL_TOPICS.map((topic) => {
            const open = topic.id === openId;

            return (
              <div className="surface p-6" key={topic.id}>
                <button
                  className="flex w-full items-start justify-between gap-4 text-left"
                  onClick={() => setOpenId((current) => (current === topic.id ? "" : topic.id))}
                  type="button"
                >
                  <div>
                    <div className="flex flex-wrap items-center gap-2">
                      <Badge>{topic.title}</Badge>
                      <Badge className="border-[rgba(11,63,117,0.12)] bg-[rgba(11,63,117,0.04)] text-nirnay-slate">
                        Official concern
                      </Badge>
                    </div>
                    <h2 className="mt-4 text-2xl font-semibold tracking-tight text-nirnay-navy">
                      {topic.concern}
                    </h2>
                  </div>
                  <ChevronDown
                    className={`mt-1 h-5 w-5 text-nirnay-slate transition ${open ? "rotate-180" : ""}`}
                  />
                </button>

                {open ? (
                  <div className="mt-6 grid gap-4">
                    {topic.mitigation.map((item) => (
                      <div className="surface-subtle p-4" key={item}>
                        <div className="flex items-start gap-3">
                          <ShieldCheck className="mt-1 h-5 w-5 text-nirnay-cyan" />
                          <p className="text-sm leading-7 text-nirnay-slate">{item}</p>
                        </div>
                      </div>
                    ))}

                    <div className="flex flex-wrap gap-3">
                      <Button
                        onClick={() =>
                          addToast({
                            title: "Governance brief ready",
                            description:
                              "This mitigation set is prepared for official Q&A and oversight discussion.",
                            tone: "info"
                          })
                        }
                        variant="secondary"
                      >
                        <Scale className="h-4 w-4" />
                        Suitable for official Q&A
                      </Button>
                    </div>
                  </div>
                ) : null}
              </div>
            );
          })}
        </div>
      </section>
    </div>
  );
}
