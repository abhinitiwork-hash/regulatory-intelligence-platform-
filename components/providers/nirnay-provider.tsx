"use client";

import {
  createContext,
  ReactNode,
  useContext,
  useMemo,
  useState
} from "react";
import {
  AUDIT_EVENTS,
  PRIORITY_ITEMS,
  REVIEWERS,
  SAMPLE_DOCUMENTS
} from "@/lib/demo-data";
import {
  DemoAuditEvent,
  DemoDocument,
  DemoStage,
  DemoStatus,
  RiskLevel,
  ToastItem
} from "@/lib/demo-types";
import { formatTimestamp } from "@/lib/utils";

interface NirnayContextValue {
  reviewerName: string;
  documents: DemoDocument[];
  auditEvents: DemoAuditEvent[];
  priorityItems: typeof PRIORITY_ITEMS;
  toasts: ToastItem[];
  addToast: (toast: Omit<ToastItem, "id">) => void;
  dismissToast: (id: string) => void;
  updateDocument: (id: string, patch: Partial<DemoDocument>) => void;
  uploadDocument: (file: File) => DemoDocument;
  addAuditEvent: (event: Omit<DemoAuditEvent, "id" | "timestamp">) => void;
  updatePriority: (id: string, patch: Partial<(typeof PRIORITY_ITEMS)[number]>) => void;
}

const NirnayContext = createContext<NirnayContextValue | null>(null);

function classifyByFilename(name: string): DemoDocument["documentType"] {
  const lower = name.toLowerCase();

  if (lower.includes("sae") || lower.includes("narrative")) {
    return "SAE Narrative";
  }

  if (lower.includes("inspection") || lower.includes("site") || /\.(png|jpg|jpeg)$/i.test(lower)) {
    return "Inspection Notes";
  }

  if (lower.includes("minutes") || lower.includes("transcript")) {
    return "Meeting Transcript";
  }

  if (lower.includes("protocol") || lower.includes("amendment")) {
    return "Protocol Amendment";
  }

  return "SUGAM Application";
}

function moduleForType(type: DemoDocument["documentType"]) {
  if (type === "SAE Narrative") {
    return "SAE Review";
  }

  if (type === "Protocol Amendment") {
    return "Version Compare";
  }

  if (type === "Inspection Notes") {
    return "Inspection Report";
  }

  if (type === "Meeting Transcript") {
    return "Summarisation";
  }

  return "Completeness Check";
}

function stageForType(type: DemoDocument["documentType"]): DemoStage {
  if (type === "SAE Narrative") {
    return "Human Review";
  }

  if (type === "Protocol Amendment" || type === "Meeting Transcript") {
    return "Intelligence";
  }

  return "Document Intake";
}

function formatFromFilename(name: string): DemoDocument["format"] {
  if (/\.(png|jpg|jpeg)$/i.test(name)) {
    return "IMG";
  }

  if (/\.docx$/i.test(name)) {
    return "DOCX";
  }

  if (/\.txt$/i.test(name)) {
    return "TXT";
  }

  return "PDF";
}

function riskForType(type: DemoDocument["documentType"]): RiskLevel {
  if (type === "SAE Narrative") {
    return "Critical";
  }

  if (type === "Protocol Amendment" || type === "Inspection Notes") {
    return "High";
  }

  return "Medium";
}

export function NirnayProvider({ children }: { children: ReactNode }) {
  const [documents, setDocuments] = useState<DemoDocument[]>(SAMPLE_DOCUMENTS);
  const [auditEvents, setAuditEvents] = useState<DemoAuditEvent[]>(AUDIT_EVENTS);
  const [priorityItems, setPriorityItems] = useState(PRIORITY_ITEMS);
  const [toasts, setToasts] = useState<ToastItem[]>([]);

  function addToast(toast: Omit<ToastItem, "id">) {
    const id = `toast-${Date.now()}-${Math.round(Math.random() * 1000)}`;

    setToasts((current) => [...current, { id, ...toast }]);

    window.setTimeout(() => {
      setToasts((current) => current.filter((item) => item.id !== id));
    }, 3800);
  }

  function dismissToast(id: string) {
    setToasts((current) => current.filter((item) => item.id !== id));
  }

  function updateDocument(id: string, patch: Partial<DemoDocument>) {
    setDocuments((current) =>
      current.map((document) =>
        document.id === id
          ? {
              ...document,
              ...patch,
              updatedAt: formatTimestamp()
            }
          : document
      )
    );
  }

  function uploadDocument(file: File) {
    const documentType = classifyByFilename(file.name);
    const uploaded: DemoDocument = {
      id: `upload-${Date.now()}`,
      name: file.name,
      format: formatFromFilename(file.name),
      documentType,
      source: "Local upload",
      stage: stageForType(documentType),
      status: "Classifying",
      riskLevel: riskForType(documentType),
      confidence: 0.88,
      updatedAt: formatTimestamp(),
      assignedModule: moduleForType(documentType),
      reviewer: REVIEWERS[1].name,
      summary: "User-uploaded document staged for local demo processing.",
      preview: "Local upload accepted. Classification and metadata extraction started.",
      metadata: {
        filename: file.name,
        size: `${Math.max(1, Math.round(file.size / 1024))} KB`,
        origin: "Live demo upload"
      },
      tags: ["Uploaded", "Local demo", documentType]
    };

    setDocuments((current) => [uploaded, ...current]);

    return uploaded;
  }

  function addAuditEvent(event: Omit<DemoAuditEvent, "id" | "timestamp">) {
    setAuditEvents((current) => [
      {
        id: `audit-${Date.now()}`,
        timestamp: formatTimestamp(),
        ...event
      },
      ...current
    ]);
  }

  function updatePriority(id: string, patch: Partial<(typeof PRIORITY_ITEMS)[number]>) {
    setPriorityItems((current) =>
      current.map((item) => (item.id === id ? { ...item, ...patch } : item))
    );
  }

  const value = useMemo<NirnayContextValue>(
    () => ({
      reviewerName: REVIEWERS[0].name,
      documents,
      auditEvents,
      priorityItems,
      toasts,
      addToast,
      dismissToast,
      updateDocument,
      uploadDocument,
      addAuditEvent,
      updatePriority
    }),
    [documents, auditEvents, priorityItems, toasts]
  );

  return <NirnayContext.Provider value={value}>{children}</NirnayContext.Provider>;
}

export function useNirnay() {
  const context = useContext(NirnayContext);

  if (!context) {
    throw new Error("useNirnay must be used within NirnayProvider");
  }

  return context;
}
