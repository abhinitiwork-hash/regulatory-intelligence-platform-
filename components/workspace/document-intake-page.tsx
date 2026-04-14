"use client";

import { DragEvent, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { AnimatePresence, motion } from "framer-motion";
import {
  ArrowRight,
  CheckCircle2,
  FilePlus2,
  FileSearch,
  LoaderCircle,
  UploadCloud
} from "lucide-react";
import { useNirnay } from "@/components/providers/nirnay-provider";
import { Button } from "@/components/ui/button";
import { Drawer } from "@/components/ui/drawer";
import { Badge } from "@/components/ui/badge";
import { sleep } from "@/lib/utils";

export function DocumentIntakePage() {
  const router = useRouter();
  const { documents, uploadDocument, updateDocument, addAuditEvent, addToast } = useNirnay();
  const [selectedId, setSelectedId] = useState(documents[0]?.id ?? "");
  const [drawerId, setDrawerId] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [classificationState, setClassificationState] = useState<{
    phase: "idle" | "classifying" | "complete";
    progress: number;
    documentId?: string;
  }>({ phase: "idle", progress: 0 });

  const selectedDocument = documents.find((document) => document.id === selectedId) ?? documents[0];
  const drawerDocument = documents.find((document) => document.id === drawerId) ?? null;

  async function runClassification(documentId: string) {
    const currentDocument = documents.find((document) => document.id === documentId);
    setClassificationState({ phase: "classifying", progress: 10, documentId });
    updateDocument(documentId, { status: "Classifying" });

    for (const progress of [28, 46, 68, 82, 100]) {
      await sleep(280);
      setClassificationState({ phase: "classifying", progress, documentId });
    }

    updateDocument(documentId, {
      status: "Ready for Review"
    });
    addAuditEvent({
      module: "Document Intake",
      action: "Classification completed",
      confidence: currentDocument?.confidence ?? 0.92,
      reviewerAction: "Review routing metadata",
      finalStatus: "Generated",
      sourceReference: currentDocument?.name ?? "Document",
      note: "Classifier completed document routing with metadata extraction."
    });
    addToast({
      title: "Classification complete",
      description: "Routing metadata is ready and the packet can move to the next workflow.",
      tone: "success"
    });
    setClassificationState({ phase: "complete", progress: 100, documentId });
  }

  function onDrop(event: DragEvent<HTMLLabelElement>) {
    event.preventDefault();
    setIsDragging(false);
    const file = event.dataTransfer.files?.[0];

    if (!file) {
      return;
    }

    const uploaded = uploadDocument(file);
    setSelectedId(uploaded.id);
    setDrawerId(uploaded.id);
    addAuditEvent({
      module: "Document Intake",
      action: "Document uploaded",
      confidence: 0.88,
      reviewerAction: "Queued for classification",
      finalStatus: "Logged",
      sourceReference: uploaded.name,
      note: "Local file upload accepted into the demo queue."
    });
    addToast({
      title: "Document uploaded",
      description: `${uploaded.name} is now in the intake queue and ready for classification.`,
      tone: "info"
    });
  }

  async function handleSendToAnonymisation() {
    if (!selectedDocument) {
      return;
    }

    updateDocument(selectedDocument.id, {
      stage: "Anonymisation",
      status: "In Review"
    });
    addAuditEvent({
      module: "Document Intake",
      action: "Sent to anonymisation",
      confidence: selectedDocument.confidence,
      reviewerAction: "Routing accepted",
      finalStatus: "Completed",
      sourceReference: selectedDocument.name,
      note: "Packet forwarded to anonymisation workflow."
    });
    addToast({
      title: "Sent to anonymisation",
      description: `${selectedDocument.name} moved into the protected-data workflow.`,
      tone: "success"
    });
    router.push("/anonymisation");
  }

  const documentsByStatus = useMemo(() => {
    return {
      queued: documents.filter((document) => document.status === "Queued").length,
      inReview: documents.filter((document) => document.status === "In Review").length,
      ready: documents.filter((document) => document.status === "Ready for Review").length
    };
  }, [documents]);

  return (
    <div className="page-grid">
      <section className="surface p-6 md:p-7">
        <div className="grid gap-5 xl:grid-cols-[minmax(0,1.1fr)_360px]">
          <label
            className={`surface-dark cursor-pointer p-6 transition ${isDragging ? "ring-2 ring-white/50" : ""}`}
            onDragEnter={() => setIsDragging(true)}
            onDragLeave={() => setIsDragging(false)}
            onDragOver={(event) => event.preventDefault()}
            onDrop={onDrop}
          >
            <input
              accept=".pdf,.docx,.txt,.png,.jpg,.jpeg"
              className="hidden"
              onChange={(event) => {
                const file = event.target.files?.[0];

                if (!file) {
                  return;
                }

                const uploaded = uploadDocument(file);
                setSelectedId(uploaded.id);
                setDrawerId(uploaded.id);
                addToast({
                  title: "Upload ready",
                  description: `${uploaded.name} added to the intake queue.`,
                  tone: "info"
                });
              }}
              type="file"
            />
            <p className="eyebrow-light">Document Intake</p>
            <div className="mt-5 flex items-center gap-3 text-white">
              <span className="rounded-2xl bg-white/10 p-3">
                <UploadCloud className="h-6 w-6" />
              </span>
              <div>
                <p className="text-xl font-semibold">Drop a packet or browse for upload</p>
                <p className="mt-2 text-sm text-white/68">
                  PDF, DOCX, TXT, JPG, and PNG are accepted for the live demo.
                </p>
              </div>
            </div>
            <div className="mt-8 grid gap-3 md:grid-cols-3">
              <div className="rounded-2xl border border-white/10 bg-white/6 p-4">
                <p className="text-sm text-white/60">Queued</p>
                <p className="mt-3 text-3xl font-semibold text-white">{documentsByStatus.queued}</p>
              </div>
              <div className="rounded-2xl border border-white/10 bg-white/6 p-4">
                <p className="text-sm text-white/60">Ready</p>
                <p className="mt-3 text-3xl font-semibold text-white">{documentsByStatus.ready}</p>
              </div>
              <div className="rounded-2xl border border-white/10 bg-white/6 p-4">
                <p className="text-sm text-white/60">In review</p>
                <p className="mt-3 text-3xl font-semibold text-white">{documentsByStatus.inReview}</p>
              </div>
            </div>
          </label>

          <div className="surface-subtle p-5">
            <p className="eyebrow">Workflow State</p>
            <h2 className="mt-3 text-2xl font-semibold tracking-tight text-nirnay-navy">
              Classification run status
            </h2>
            <div className="mt-6 grid gap-3">
              {[
                {
                  title: "Start",
                  done: classificationState.phase !== "idle"
                },
                {
                  title: "Progress",
                  done: classificationState.phase === "classifying" || classificationState.phase === "complete"
                },
                {
                  title: "Result",
                  done: classificationState.phase === "complete"
                },
                {
                  title: "Next step",
                  done: classificationState.phase === "complete"
                }
              ].map((step) => (
                <div
                  className="flex items-center justify-between rounded-2xl border border-[rgba(11,63,117,0.08)] px-4 py-3"
                  key={step.title}
                >
                  <span className="text-sm font-medium text-nirnay-navy">{step.title}</span>
                  {step.done ? (
                    <CheckCircle2 className="h-4 w-4 text-nirnay-green" />
                  ) : (
                    <span className="h-4 w-4 rounded-full border border-[rgba(11,63,117,0.12)]" />
                  )}
                </div>
              ))}
            </div>

            <div className="mt-6 rounded-2xl border border-[rgba(11,63,117,0.08)] bg-[rgba(11,63,117,0.03)] p-4">
              <div className="flex items-center justify-between gap-3">
                <span className="text-sm font-semibold text-nirnay-navy">Classifier progress</span>
                <span className="text-sm text-nirnay-slate">{classificationState.progress}%</span>
              </div>
              <div className="mt-3 h-2 rounded-full bg-[rgba(11,63,117,0.08)]">
                <div
                  className="h-2 rounded-full bg-[var(--nirnay-cyan)] transition-all"
                  style={{ width: `${classificationState.progress}%` }}
                />
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="grid gap-5 xl:grid-cols-[minmax(0,1.08fr)_380px]">
        <div className="surface p-6">
          <div className="flex flex-wrap items-end justify-between gap-4">
            <div>
              <p className="eyebrow">Seeded Intake Queue</p>
              <h2 className="mt-3 text-3xl font-semibold tracking-tight text-nirnay-navy">
                Select a packet and run the intake flow
              </h2>
            </div>
            <Badge className="border-[rgba(24,166,184,0.22)] bg-[rgba(24,166,184,0.08)] text-nirnay-blue">
              Clickable queue
            </Badge>
          </div>

          <div className="mt-6 grid gap-4 md:grid-cols-2">
            {documents.map((document) => (
              <button
                className={`surface-subtle p-5 text-left transition hover:-translate-y-1 ${
                  selectedDocument?.id === document.id
                    ? "border-[rgba(24,166,184,0.28)] bg-[rgba(24,166,184,0.06)]"
                    : ""
                }`}
                key={document.id}
                onClick={() => setSelectedId(document.id)}
                type="button"
              >
                <div className="flex items-center justify-between gap-3">
                  <Badge>{document.documentType}</Badge>
                  <Badge className="border-[rgba(11,63,117,0.1)] bg-[rgba(11,63,117,0.04)] text-nirnay-slate">
                    {document.status}
                  </Badge>
                </div>
                <h3 className="mt-4 text-xl font-semibold tracking-tight text-nirnay-navy">
                  {document.name}
                </h3>
                <p className="mt-3 text-sm leading-7 text-nirnay-slate">{document.summary}</p>
                <div className="mt-5 flex items-center justify-between text-sm text-nirnay-slate">
                  <span>{document.assignedModule}</span>
                  <span>{Math.round(document.confidence * 100)}%</span>
                </div>
              </button>
            ))}
          </div>
        </div>

        <div className="surface p-6">
          {selectedDocument ? (
            <div className="space-y-5">
              <div className="flex items-start justify-between gap-3">
                <div>
                  <p className="eyebrow">Selected packet</p>
                  <h2 className="mt-3 text-2xl font-semibold tracking-tight text-nirnay-navy">
                    {selectedDocument.name}
                  </h2>
                </div>
                <Button onClick={() => setDrawerId(selectedDocument.id)} variant="secondary">
                  <FileSearch className="h-4 w-4" />
                  Detail
                </Button>
              </div>

              <div className="grid gap-3">
                {Object.entries(selectedDocument.metadata).map(([key, value]) => (
                  <div className="rounded-2xl border border-[rgba(11,63,117,0.08)] p-4" key={key}>
                    <p className="eyebrow">{key}</p>
                    <p className="mt-2 text-sm font-semibold text-nirnay-navy">{value}</p>
                  </div>
                ))}
              </div>

              <div className="rounded-2xl border border-[rgba(11,63,117,0.08)] bg-[rgba(11,63,117,0.03)] p-4">
                <p className="eyebrow">Detected routing</p>
                <div className="mt-3 flex flex-wrap items-center gap-2">
                  <Badge>{selectedDocument.documentType}</Badge>
                  <Badge className="border-[rgba(24,166,184,0.22)] bg-[rgba(24,166,184,0.08)] text-nirnay-blue">
                    {Math.round(selectedDocument.confidence * 100)}% confidence
                  </Badge>
                </div>
                <p className="mt-3 text-sm leading-7 text-nirnay-slate">{selectedDocument.preview}</p>
              </div>

              <div className="flex flex-wrap gap-3">
                <Button
                  disabled={classificationState.phase === "classifying"}
                  onClick={() => runClassification(selectedDocument.id)}
                >
                  {classificationState.phase === "classifying" ? (
                    <>
                      <LoaderCircle className="h-4 w-4 animate-spin" />
                      Classifying
                    </>
                  ) : (
                    <>
                      <FilePlus2 className="h-4 w-4" />
                      Run classification
                    </>
                  )}
                </Button>
                <Button
                  disabled={
                    classificationState.phase !== "complete" &&
                    selectedDocument.status !== "Ready for Review"
                  }
                  onClick={handleSendToAnonymisation}
                  variant="secondary"
                >
                  Send to Anonymisation
                  <ArrowRight className="h-4 w-4" />
                </Button>
              </div>
            </div>
          ) : null}
        </div>
      </section>

      <Drawer
        description={drawerDocument?.summary}
        onClose={() => setDrawerId(null)}
        open={Boolean(drawerDocument)}
        title={drawerDocument?.name ?? "Document detail"}
      >
        {drawerDocument ? (
          <div className="space-y-5">
            <div className="grid gap-4 md:grid-cols-2">
              {Object.entries(drawerDocument.metadata).map(([key, value]) => (
                <div className="surface-subtle p-4" key={key}>
                  <p className="eyebrow">{key}</p>
                  <p className="mt-3 text-sm font-semibold text-nirnay-navy">{value}</p>
                </div>
              ))}
            </div>
            <div className="surface-subtle p-4">
              <p className="eyebrow">Preview</p>
              <p className="mt-3 text-sm leading-7 text-nirnay-slate">{drawerDocument.preview}</p>
            </div>
            <div className="flex flex-wrap gap-3">
              <Button
                onClick={() => {
                  setSelectedId(drawerDocument.id);
                  setDrawerId(null);
                }}
              >
                Focus packet
              </Button>
              <Button
                onClick={() => {
                  setSelectedId(drawerDocument.id);
                  runClassification(drawerDocument.id);
                  setDrawerId(null);
                }}
                variant="secondary"
              >
                Run from drawer
              </Button>
            </div>
          </div>
        ) : null}
      </Drawer>
    </div>
  );
}
