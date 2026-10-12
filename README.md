# ResuMatch AI - Intelligent Resume Analyzer & ATS Optimizer

A polished, modern web application that analyzes resumes against target job descriptions, providing instant match scoring, keyword matrix audits, ATS formatting checks, and tailored bullet-point rewrites.

![ResuMatch AI](https://img.shields.io/badge/Privacy-100%25%20In--Memory-emerald?style=flat-square)
![Stack](https://img.shields.io/badge/Stack-Python%20%7C%20Flask%20%7C%20Vanilla%20JS%20%7C%20CSS3-indigo?style=flat-square)
![Status](https://img.shields.io/badge/Status-Production%20Ready-blue?style=flat-square)

---

## 🌟 Key Features

1. **Dual Resume Ingestion**:
   - **File Upload**: Native in-memory parsing for **PDF** (`pdfplumber` with `pdfminer.six` fallback), **DOCX** (`python-docx`), and **TXT**.
   - **Direct Text Paste**: Clean textarea fallback with live word and character counters.
   - **100% Privacy Guarantee**: Resumes are parsed strictly in-memory using `BytesIO` streams and are never persisted to disk or shared.

2. **Dual Intelligence Analysis Engine**:
   - **Smart Local ATS & Semantic Engine (Default, Free, 100% Private)**:
     - Powered by spaCy NLP and scikit-learn TF-IDF cosine similarity.
     - 500+ categorized skill taxonomy (Languages, Frontend, Backend, Databases, Cloud & DevOps, AI/Data, Testing, Product Management, Architecture, Leadership).
     - Identifies matched skills, critical missing requirements, and bonus resume skills.
     - Evaluates quantifiable metrics (percentages, dollar amounts, velocity boosts).
     - Detects executive action verbs (*"Architected"*, *"Spearheaded"*, *"Optimized"*).
     - Audits ATS contact info (email, phone, LinkedIn) and standard document sections.
   - **Optional Google Gemini Live AI Mode**:
     - Optional user-configured API key stored securely in `localStorage`.
     - Structured JSON schema generation with deep qualitative resume rewrites.
     - Explicit transparency badge clearly displaying which engine performed the evaluation.

3. **Rich, Modern User Interface**:
   - **Step-by-Step Stepper**: Upload Resume → Target Job Description → Run Analysis → Actionable Results.
   - **1-Click Sample Profiles**: Try instant pre-configured scenarios without uploading a file:
     - *Senior Full Stack Engineer* (High match)
     - *Technical Product Manager* (SaaS PM)
     - *Junior Data Analyst → ML Role* (Demonstrates clear gap warnings & transition guidance).
   - **Animated Circular Score Gauge (0–100)**: Color-coded grading (*Strong Match*, *Competitive Match*, *Needs Optimization*).
   - **4 Core Sub-Scores**: Skill Overlap, Semantic Relevance, Experience & Impact, and ATS Readability.
   - **Interactive Skills Matrix**: Filter between *All*, *Matched*, *Missing (High Priority & Recommended)*, and *Resume Extras*.
   - **Specific Actionable Suggestions**: Categorized recommendations featuring before-and-after bullet rewrites using Google's XYZ formula.
   - **Dark / Light Theme Toggle**: Seamless theme switching with persistent user preference.

4. **Multi-Format Export & Sharing**:
   - **Print / PDF Export**: Styled with custom print stylesheet (`print.css`) for high-contrast, professional A4/Letter PDF reports.
   - **Export .MD**: One-click download of a structured Markdown audit report.
   - **Copy Summary**: Formatted clipboard copy with toast feedback.

5. **Ethical AI Disclaimer**:
   - Prominent disclaimer clarifying that the score is an automated ATS & semantic estimate to help candidates tailor their resume, not an official employer hiring decision.

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10+ (Tested on Python 3.12)
- Dependencies installed: `flask`, `pdfplumber`, `python-docx`, `scikit-learn`, `spacy`

### 2. Start the Application
Run from the project directory:
```bash
python app.py
```

The application will start on:
```
http://127.0.0.1:5000
```

Open your browser to [http://127.0.0.1:5000](http://127.0.0.1:5000) and begin optimizing resumes!

---

## 🧪 Automated Testing

An automated end-to-end verification suite is included:
```bash
python verify_app.py
```

Tests run:
- [x] Health check (`/api/health`) and privacy assertion
- [x] Sample data loading (`/api/samples`)
- [x] In-memory DOCX parsing and text extraction (`/api/extract`)
- [x] Local NLP scoring and suggestion synthesis (`/api/analyze`)
- [x] Input validation, empty checks, and unsupported file handling

---

## 📁 Project Architecture

```
AI Resume Analyzer/
├── app.py                 # Flask server with RESTful API routes & error handling
├── verify_app.py          # Automated end-to-end verification test suite
├── README.md              # Project documentation
├── analyzer/
│   ├── __init__.py        # Package exports
│   ├── extractor.py       # In-memory PDF, DOCX, and TXT parsing
│   ├── nlp_engine.py      # spaCy & TF-IDF semantic engine, taxonomy, ATS scoring
│   ├── gemini_engine.py   # Optional Google Gemini live model integration
│   └── samples.py         # Pre-loaded realistic resumes & job descriptions
├── static/
│   ├── css/
│   │   ├── style.css      # Design system, glassmorphism, responsive grid, animations
│   │   └── print.css      # Print & PDF export stylesheet
│   └── js/
│       └── app.js         # Reactive UI, drag-and-drop, gauge animation, export handlers
└── templates/
    └── index.html         # Accessible, semantic single-page dashboard
```
