# Regulatory Intelligence Platform
**CDSCO AI Hackathon — Stage 1**

## Live Demo
> Deploy to Streamlit Cloud and paste URL here

## Features
1. AI-Powered Data Anonymisation (DPDP Act 2023 compliant)
2. Document Summarisation (SAE | Checklist | Meeting Transcript)
3. Completeness Assessment (Schedule Y — 20 mandatory fields)
4. SAE Classification & Duplicate Detection (ICD-10 based)
5. Document Comparison (Substantive vs Administrative changes)
6. Inspection Report Generation (CDSCO GCP format)

## Public Datasets Used
- FDA FAERS (fis.fda.gov)
- CDSCO Forms CT-04, CT-05, CT-06 (cdsco.gov.in)
- ClinicalTrials.gov — Indian trial records
- CTRI — Clinical Trials Registry India
- Synthetic data mirroring real document structures

## Compliance
- DPDP Act 2023 (India)
- ICMR Biomedical Research Guidelines 2017
- CDSCO Schedule Y
- MeitY AI Ethics Guidelines
- No real patient data used at any stage

## How to Run Locally
```bash
pip install streamlit pandas
streamlit run app.py
```

## Ethical AI Statement
This platform assists regulatory officers. All final decisions must be made by qualified human reviewers. The system is transparent, explainable, and non-discriminatory.
