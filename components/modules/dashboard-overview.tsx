"use client";

import { useRef, useState } from "react";
import { Badge } from "@/components/ui/badge";
import { SectionCard } from "@/components/ui/section-card";
import {
  INTELLIGENCE_MODULES,
  LIVE_REVIEW_SIGNALS,
  PRODUCT_TOUR_STEPS,
  RISK_CONTROL_ITEMS
} from "@/lib/mock-data";
import { DashboardMetric, NavKey, SourceDocument } from "@/lib/types";

const reviewLaneByType: Record<SourceDocument["documentType"], string> = {
  "SUGAM Application": "Completeness lane",
  "SAE Narrative": "Safety lane",
  "Meeting Transcript": "Intelligence lane",
  "Inspection Notes": "Inspection lane",
  "Protocol Amendment": "Comparison lane"
};

export function DashboardOverview({
  metrics,
  documents,
  onNavigate
}: {
  metrics: DashboardMetric[];
  documents: SourceDocument[];
  onNavigate: (target: NavKey) => void;
}) {
  const [tourIndex, setTourIndex] = useState(0);
  const tourRef = useRef<HTMLElement | null>(null);
  const activeTour = PRODUCT_TOUR_STEPS[tourIndex];

  function openTour() {
    setTourIndex(0);
    tourRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  return (
    <div className="dashboard-cockpit">
      <section className="cockpit-hero">
        <div className="cockpit-hero__copy">
          <span className="cockpit-hero__eyebrow">Regulatory Intelligence Cockpit</span>
          <h1>Nirnay</h1>
          <p>
            AI-assisted regulatory review workbench for structured evidence,
            protected data, and audit-ready decisions.
          </p>

          <div className="cockpit-hero__actions">
            <button className="button" onClick={() => onNavigate("document-intake")} type="button">
              Start Review
            </button>
            <button className="button button--secondary" onClick={openTour} type="button">
              Take Product Tour
            </button>
          </div>

          <div className="cockpit-trustline">
            <span className="status-dot status-dot--green" />
            <p>Assistive AI only. Final decision remains with the authorised reviewer.</p>
          </div>

          <div className="hero-flow">
            {[
              "Document Intake",
              "Anonymisation",
              "Intelligence",
              "Human Review",
              "Audit Packet"
            ].map((step, index) => (
              <div key={step} className="hero-flow__node">
                <span>{`0${index + 1}`}</span>
                <strong>{step}</strong>
              </div>
            ))}
          </div>
        </div>

        <div className="command-panel">
          <div className="command-panel__header">
            <div>
              <span className="command-panel__kicker">Command Surface</span>
              <strong>Live reviewer operating picture</strong>
            </div>
            <Badge tone="cyan">Stage 1 Demo</Badge>
          </div>

          <div className="command-panel__grid">
            {metrics.map((metric) => (
              <article key={metric.label} className={`command-kpi command-kpi--${metric.tone}`}>
                <span>{metric.label}</span>
                <strong>{metric.value}</strong>
                <p>{metric.delta}</p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <SectionCard
        title="Live Review Board"
        description="Compact regulatory signals for the current review window."
      >
        <div className="review-board">
          <div className="review-board__signals">
            {LIVE_REVIEW_SIGNALS.map((signal) => (
              <button
                key={signal.id}
                className={`signal-card signal-card--${signal.tone}`}
                onClick={() => signal.navTarget && onNavigate(signal.navTarget)}
                type="button"
              >
                <div className="signal-card__header">
                  <span className={`status-dot status-dot--${signal.tone}`} />
                  <small>{signal.status}</small>
                </div>
                <strong>{signal.title}</strong>
                <div className="signal-card__metric">{signal.metric}</div>
                <p>{signal.summary}</p>
              </button>
            ))}
          </div>

          <div className="review-board__table">
            <div className="review-board__table-header">
              <strong>Current review queue</strong>
              <span>Source-linked packets staged for action</span>
            </div>
            <div className="table-wrap">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Packet</th>
                    <th>Lane</th>
                    <th>Type</th>
                    <th>Confidence</th>
                  </tr>
                </thead>
                <tbody>
                  {documents.map((document) => (
                    <tr key={document.id}>
                      <td>
                        <strong>{document.name}</strong>
                        <p>{document.source}</p>
                      </td>
                      <td>{reviewLaneByType[document.documentType]}</td>
                      <td>
                        <Badge tone="blue">{document.documentType}</Badge>
                      </td>
                      <td>{Math.round(document.confidence * 100)}%</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </SectionCard>

      <SectionCard
        title="Intelligence Modules"
        description="Operational modules tuned for regulatory evidence handling rather than conversational AI."
      >
        <div className="intelligence-grid">
          {INTELLIGENCE_MODULES.map((module) => (
            <button
              key={module.id}
              className={`intel-card intel-card--${module.tone} ${
                activeTour.route === module.navTarget ? "intel-card--active" : ""
              }`}
              onClick={() => module.navTarget && onNavigate(module.navTarget)}
              type="button"
            >
              <div className="intel-card__header">
                <span>{module.code}</span>
                <small>{module.status}</small>
              </div>
              <strong>{module.title}</strong>
              <p>{module.summary}</p>
              <div className="intel-card__detail">{module.detail}</div>
            </button>
          ))}
        </div>
      </SectionCard>

      <SectionCard
        title="Risk Control Layer"
        description="Authority, confidence, and traceability remain visible at every stage."
      >
        <div className="risk-layer">
          <div className="risk-layer__quote">
            <span className="risk-layer__eyebrow">Decision Discipline</span>
            <strong>When confidence is low, Nirnay does not guess. It escalates.</strong>
            <p>
              The system surfaces uncertainty, keeps the reviewer in control, and captures every
              action for later audit and supervisory review.
            </p>
          </div>

          <div className="risk-layer__grid">
            {RISK_CONTROL_ITEMS.map((item) => (
              <article key={item.id} className={`risk-card risk-card--${item.tone}`}>
                <div className="risk-card__header">
                  <span className={`status-dot status-dot--${item.tone}`} />
                  <small>{item.metric}</small>
                </div>
                <strong>{item.title}</strong>
                <p>{item.detail}</p>
              </article>
            ))}
          </div>
        </div>
      </SectionCard>

      <SectionCard
        title="Product Tour"
        description="Walkthrough of the review flow from incoming packet to audit-ready packet."
      >
        <section className="tour-panel" ref={tourRef}>
          <div className="tour-panel__sidebar">
            {PRODUCT_TOUR_STEPS.map((step, index) => (
              <button
                key={step.id}
                className={`tour-step ${tourIndex === index ? "tour-step--active" : ""}`}
                onClick={() => setTourIndex(index)}
                type="button"
              >
                <span>{step.phase}</span>
                <strong>{step.title}</strong>
                <p>{step.summary}</p>
              </button>
            ))}
          </div>

          <div className="tour-panel__content" key={activeTour.id}>
            <div className="tour-panel__content-head">
              <div>
                <span className="tour-panel__phase">{activeTour.phase}</span>
                <h3>{activeTour.title}</h3>
                <p>{activeTour.detail}</p>
              </div>
              <button className="button" onClick={() => onNavigate(activeTour.route)} type="button">
                Open Module
              </button>
            </div>

            <div className="tour-signal">
              <span className="status-dot status-dot--cyan" />
              <strong>{activeTour.signal}</strong>
            </div>

            <div className="tour-detail-grid">
              <div className="tour-detail-card">
                <span>Safeguards</span>
                <ul className="list-clean">
                  {activeTour.safeguards.map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              </div>
              <div className="tour-detail-card">
                <span>Outputs</span>
                <ul className="list-clean">
                  {activeTour.outputs.map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              </div>
            </div>

            <div className="tour-panel__controls">
              <button
                className="button button--secondary"
                disabled={tourIndex === 0}
                onClick={() => setTourIndex((current) => Math.max(0, current - 1))}
                type="button"
              >
                Previous
              </button>
              <button
                className="button"
                disabled={tourIndex === PRODUCT_TOUR_STEPS.length - 1}
                onClick={() =>
                  setTourIndex((current) => Math.min(PRODUCT_TOUR_STEPS.length - 1, current + 1))
                }
                type="button"
              >
                Next Step
              </button>
            </div>
          </div>
        </section>
      </SectionCard>
    </div>
  );
}
