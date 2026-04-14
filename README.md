# Nirnay Portal

**Nirnay Portal** is a polished MVP reviewer workbench built for the **CDSCO-IndiaAI Health Innovation Hackathon**. It is designed as a **human-in-the-loop regulatory operations console**, not a chatbot.

The Stage 1 prototype demonstrates:

- document intake and routing
- data anonymisation
- SAE review and severity classification
- completeness checks for regulatory forms
- protocol version comparison
- inspection report generation from rough notes
- full audit trail visibility

## Product Positioning

Nirnay Portal is intended for CDSCO reviewers handling safety, compliance, and inspection workflows. The system is explicitly:

- reviewer-controlled
- privacy-aware
- traceable and auditable
- modular enough to integrate later with **SUGAM** and **MD Online**

Every AI output is exposed with confidence, rationale, and a reviewer action path such as accept, edit, or override.

## Stack

- Next.js App Router
- React
- TypeScript
- Custom CSS design system
- Mock workflow engine and seed data only

No paid APIs are used in this MVP.

## Run Locally

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

To verify a production build:

```bash
npm run build
```

## Folder Structure

```text
app/
  globals.css
  layout.tsx
  page.tsx
components/
  portal-workbench.tsx
  sidebar.tsx
  modules/
    dashboard-overview.tsx
    document-intake-module.tsx
    anonymisation-module.tsx
    sae-review-module.tsx
    completeness-check-module.tsx
    version-compare-module.tsx
    inspection-report-module.tsx
    audit-trail-module.tsx
  ui/
    badge.tsx
    confidence-meter.tsx
    section-card.tsx
lib/
  mock-data.ts
  mock-engine.ts
  types.ts
```

`app.py` remains in the repo as an older Streamlit prototype reference. The current MVP app surface is the Next.js implementation above.

## Architecture

### 1. Reviewer Workbench Shell

The app uses a single dashboard shell with a left-side navigation for:

- Dashboard
- Document Intake
- Anonymisation
- SAE Review
- Completeness Check
- Version Compare
- Inspection Report
- Audit Trail

### 2. Mock Workflow Engine

`lib/mock-engine.ts` contains pure functions for demo logic:

- `classifyDocument()`
- `generateAnonymisationResult()`
- `parseSaeNarrative()`
- `runCompletenessCheck()`
- `compareProtocolVersions()`
- `generateInspectionReport()`
- `createAuditEntry()`

These functions are intentionally isolated so real OCR, LLM, classification, or rule-engine services can replace them later without rewriting the UI.

### 3. Seed Data

`lib/mock-data.ts` contains sample documents, synthetic PHI/PII text, SAE narrative content, regulatory form data, protocol snippets, inspection notes, and audit entries. This keeps the app deterministic and presentation-ready.

### 4. Integration Boundaries

Comments are included where real services would be attached, including:

- OCR or handwriting extraction for PDFs/images
- document parsing for DOCX/PDF
- hosted or on-prem LLM summarisation/extraction
- case sync to SUGAM or MD Online
- audit persistence and reviewer identity linkage

## Module-by-Module Demo Flow

### Dashboard

Shows operational metrics, seeded review packets, product principles, and future integration attach points.

### Document Intake

- accepts PDF, DOCX, TXT, and image placeholder uploads
- classifies incoming documents into:
  - SUGAM Application
  - SAE Narrative
  - Meeting Transcript
  - Inspection Notes
  - Protocol Amendment
- shows confidence and routing rationale

### Anonymisation

- detects sample PII/PHI such as patient name, age, initials, phone, address, hospital ID, investigator name, site name, and sponsor name
- displays original and redacted text side by side
- shows entity labels and confidence scores
- exports anonymised JSON

### SAE Review

- parses a synthetic SAE narrative
- extracts patient profile, event, seriousness criteria, severity, causality, action taken, outcome, and missing info
- supports reviewer accept, edit, and override actions
- exposes severity classes:
  - Death
  - Life-threatening
  - Hospitalisation
  - Disability
  - Medically significant
  - Non-serious

### Completeness Check

- checks a sample regulatory form object
- flags missing mandatory fields
- categorises them as Critical, Major, or Minor
- shows explicit reviewer follow-up actions

### Version Compare

- compares two protocol snippets
- highlights substantive changes
- explains likely regulatory impact
- covers:
  - eligibility criteria change
  - endpoint change
  - consent wording change

### Inspection Report

- takes rough unstructured inspection notes
- generates a formal report with:
  - site details
  - observations
  - critical/major/minor findings
  - evidence summary
  - recommended action

### Audit Trail

- logs AI outputs
- records confidence
- stores reviewer actions
- ties everything to source references and timestamps
- reinforces that AI is assistive only

## Mapping to CDSCO Hackathon Requirements

This MVP covers the requested Stage 1 scope directly:

- **data anonymisation**: implemented with redaction workflow and JSON export
- **document summarisation foundation**: intake routing and structured extraction architecture are in place
- **missing-field checks**: implemented in the completeness module
- **SAE severity classification**: implemented with reviewer override controls
- **duplicate/version comparison**: implemented via protocol amendment comparison
- **inspection report generation**: implemented from rough note input

It also keeps the correct governance posture:

- human reviewer remains in control
- privacy is visible, not hidden
- outputs are traceable
- confidence and rationale are exposed

## Future Integration with SUGAM and MD Online

The MVP is deliberately modular so production integrations can be added in a controlled way:

### SUGAM

- pull incoming submission packets and metadata into the intake queue
- push reviewer-approved completeness outputs back to submission records
- link version comparison summaries to amendment records

### MD Online

- sync device or safety review cases
- attach SAE extraction outputs and inspection findings
- persist reviewer overrides and case status transitions

### Additional Production Enhancements

- OCR and handwriting recognition
- policy/rule configuration by form type
- role-based access control
- persistent audit logging
- reviewer identity and e-signature capture
- document store integration
- queue management and SLA views

## Demo Notes

- All data is synthetic and mock-driven.
- The app is presentation-ready but intentionally backend-light.
- The UI is designed to look like a premium government/regulatory operations console rather than a startup chatbot.
