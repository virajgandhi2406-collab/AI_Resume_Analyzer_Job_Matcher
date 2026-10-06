# ⚡ ResumePulse AI: Intelligent ATS Resume Analyzer & Job Matcher Platform

[![Live Demo](https://img.shields.io/badge/Live_Demo-GitHub_Pages-22c55e.svg?style=for-the-badge&logo=github)](https://virajgandhi2406-collab.github.io/AI_Resume_Analyzer_Job_Matcher/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB.svg?style=flat&logo=python)](https://www.python.org)
[![SQLAlchemy](https://img.shields.io/badge/ORM-SQLAlchemy%202.0-D71F00.svg?style=flat)](https://www.sqlalchemy.org)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

> 🌐 **Live Web App:** [https://virajgandhi2406-collab.github.io/AI_Resume_Analyzer_Job_Matcher/](https://virajgandhi2406-collab.github.io/AI_Resume_Analyzer_Job_Matcher/)

An enterprise-grade, full-stack AI career platform that empowers job seekers to optimize resumes for Applicant Tracking Systems (ATS), match profiles against real-time job openings using Cosine & Semantic Similarity, and generate customized career assets (Cover Letters, Bullet Optimizations, Interview Prep, Upskilling Roadmaps) with state-of-the-art Multi-Provider AI.

---

## 🌟 Core Feature Matrix

| Module | Features & Capabilities |
| :--- | :--- |
| 📊 **Interactive Analytics Dashboard** | Real-time overview of candidate ATS scores, application pipeline funnel, and in-demand market skill trends. |
| 📄 **ATS Resume Analyzer** | Multi-format parser (`PDF`, `DOCX`, `TXT`), 4-dimensional ATS scoring (Keywords, Layout, Impact Metrics, Length), skill taxonomy extraction, strengths/weaknesses identification, and PDF Scorecard export. |
| 💼 **Smart Job Match Engine** | Semantic Cosine Similarity matching against job vacancies, detailed Skill Gap Matrix (Matched, Critical Missing, Nice-to-Have), and batch matching. |
| ✉️ **Tailored Cover Letter Generator** | Multi-tone AI generator (Professional, High-Energy, Startup, Executive) that tailors letters directly to resume achievements and job requirements. |
| ⚡ **STAR Bullet Point Optimizer** | Converts weak duty descriptions into high-impact Google XYZ formula metrics (*Accomplished [X], as measured by [Y], by doing [Z]*). |
| 🎯 **AI Interview Coach** | Generates predictive role-specific behavioral (STAR method) and technical architectural interview questions with model answers and talking points. |
| 🗺️ **Career Upskilling Roadmap** | Multi-phase structured milestone roadmap with recommended portfolio projects and curated resources. |
| 📌 **Application Kanban Tracker** | Visual drag-and-drop workflow tracking (`Wishlist` → `Applied` → `Interviewing` → `Offer` → `Archived`). |

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10+
- Modern Web Browser (Chrome, Edge, Firefox, Safari)

### 2. Backend Installation & Startup
```bash
# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Run the FastAPI server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
- Interactive Swagger API Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)
- Interactive Redoc Documentation: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### 3. Frontend Web Application
The frontend is built with vanilla modern HTML5, cyber-glassmorphic CSS3, and responsive JavaScript.

Simply open `frontend/index.html` in your browser or serve it with any local static web server:
```bash
# Serve frontend via Python simple server
python -m http.server 3000 --directory frontend
```
Then visit: [http://localhost:3000](http://localhost:3000)

---

## 🤖 Multi-Provider AI Architecture

ResumePulse AI seamlessly supports multi-provider switching:
1. **Google Gemini 1.5 Flash** (via `GEMINI_API_KEY`)
2. **OpenAI GPT-4o / GPT-4o-mini** (via `OPENAI_API_KEY`)
3. **Groq LLaMA-3.1 70B** (via `GROQ_API_KEY`)
4. **Local NLP & Heuristic Engine** (Zero external API key needed — operates 100% offline with built-in taxonomy and TF-IDF semantic algorithms)

---

## 🏗️ Architecture & Project Structure

```
AI_Resume_Analyzer_Job_Matcher/
├── backend/
│   ├── app/
│   │   ├── config.py              # Application settings & environment configuration
│   │   ├── database.py            # SQLAlchemy database engine & session dependency
│   │   ├── main.py                # FastAPI entrypoint, lifespan seeding, & routes
│   │   ├── models/                # SQLAlchemy database models (User, Resume, Job, Match, Application)
│   │   ├── schemas/               # Pydantic v2 schemas for request validation & response formatting
│   │   ├── services/              # Business logic (LLM Engine, NLP Tokenizer, ATS Analyzer, Matcher)
│   │   ├── utils/                 # PDF Generator, Skill Taxonomy, Action Verbs, Security
│   │   └── routers/               # Modular FastAPI endpoints (Resumes, Jobs, Match, AI Tools, Tracker)
│   ├── uploads/                   # Uploaded resume storage directory
│   └── requirements.txt           # Python dependency specifications
│
├── frontend/
│   ├── index.html                 # Semantic single-page application structure & modals
│   ├── css/
│   │   └── styles.css             # Cyber-glassmorphism design system & score gauges
│   └── js/
│       ├── api.js                 # Centralized API service client
│       └── app.js                 # UI controller, state manager, sample loaders, Kanban
│
├── .env.example                   # Sample environment configuration
└── README.md                      # Comprehensive project documentation
```

---

## 📄 License
Released under the [MIT License](LICENSE).
