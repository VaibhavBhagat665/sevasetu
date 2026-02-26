# SevaSetu — AI-Powered Welfare Scheme Assistant

An Agentic AI platform that helps Indian citizens and CSC/VLE operators successfully apply for government welfare schemes by preventing application errors and automating documentation workflows.

## 🚀 Quick Start

### Prerequisites
- Python 3.9+ 
- Node.js 18+
- npm

### 1. Backend Setup

```bash
cd backend
pip install -r requirements.txt
python main.py
```

The backend starts at **http://localhost:8000**. Visit http://localhost:8000/docs for Swagger API docs.

> **Optional**: Set `GEMINI_API_KEY` in `backend/.env` for LLM-powered intent extraction. Without it, keyword-based fallback is used.

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend starts at **http://localhost:5173**.

## 🏗️ Architecture

```
sevasetu/
├── backend/                    # Python FastAPI server
│   ├── main.py                 # API entry point (8 endpoints)
│   ├── schemes_data.py         # 10 government schemes knowledge base
│   ├── vector_store.py         # FAISS semantic search index
│   ├── intent_engine.py        # Gemini LLM + keyword fallback
│   ├── scheme_matcher.py       # Vector search for scheme discovery
│   ├── eligibility_engine.py   # Rule-based eligibility checker
│   ├── ocr_engine.py           # Simulated OCR document extraction
│   ├── document_validator.py   # Cross-document mismatch detection
│   ├── form_generator.py       # PDF application form auto-fill
│   ├── grievance_generator.py  # Grievance letter PDF generation
│   └── agent_workflow.py       # State machine orchestrator
│
├── frontend/                   # React + Vite PWA
│   └── src/
│       ├── App.jsx             # Root with navigation
│       ├── pages/
│       │   ├── Home.jsx        # Landing page
│       │   └── Assistant.jsx   # 5-step guided workflow
│       ├── components/
│       │   ├── VoiceInput.jsx  # Web Speech API microphone
│       │   ├── SchemeCard.jsx  # Scheme result card
│       │   ├── StepIndicator.jsx # Progress tracker
│       │   └── DocumentUpload.jsx # Upload + OCR display
│       └── services/
│           └── api.js          # Backend API client
```

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/intent` | Extract structured intent from text |
| POST | `/scheme-match` | Semantic search for matching schemes |
| POST | `/validate-eligibility` | Rule-based eligibility check |
| POST | `/upload-documents` | Upload document for OCR |
| POST | `/extract-ocr/{id}` | Extract data from uploaded document |
| POST | `/validate-documents` | Cross-validate document consistency |
| POST | `/generate-form` | Generate auto-filled PDF application |
| POST | `/generate-grievance` | Generate grievance letter PDF |

## 🔄 User Workflow

1. **Voice/Text Input** → Describe needs in natural language
2. **Scheme Discovery** → AI finds matching government schemes via FAISS vector search
3. **Eligibility Check** → Rule engine validates against scheme criteria with explanations
4. **Document Upload** → Upload Aadhaar, bank passbook, etc. for OCR extraction
5. **Mismatch Detection** → Cross-validate name, address, pincode across documents
6. **Form Generation** → Download auto-filled PDF application form
7. **Grievance** → Generate formal grievance letter if needed

## 🛠️ Key Technologies

- **Backend**: FastAPI, FAISS, sentence-transformers, fpdf2, fuzzywuzzy
- **Frontend**: React, Vite, Web Speech API
- **AI**: Google Gemini (optional), semantic embeddings, rule engine
- **PDF**: fpdf2 for form and grievance generation
