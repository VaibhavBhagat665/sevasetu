"""
SevaSetu — Main FastAPI Application
Central API server orchestrating all services.
"""

import os
import uuid
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

# Import service modules
from intent_engine import extract_intent
from scheme_matcher import match_schemes
from eligibility_engine import check_eligibility
from ocr_engine import upload_document, extract_data
from document_validator import validate_documents
from form_generator import generate_form
from grievance_generator import generate_grievance
from agent_workflow import get_or_create_session, process_step
import vector_store

# Initialize FastAPI
app = FastAPI(
    title="SevaSetu API",
    description="Agentic AI platform helping Indian citizens apply for government welfare schemes",
    version="1.0.0-mvp",
)

# CORS — allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Pydantic Models ───

class IntentRequest(BaseModel):
    text: str = Field(..., description="User input text (voice transcribed or typed)")
    session_id: Optional[str] = None

class SchemeMatchRequest(BaseModel):
    query: str
    attributes: Optional[Dict[str, Any]] = None
    top_k: Optional[int] = 5

class EligibilityRequest(BaseModel):
    scheme_id: str
    user_profile: Dict[str, Any]

class DocumentValidationRequest(BaseModel):
    user_id: Optional[str] = "demo-user"
    documents: Optional[List[Dict[str, Any]]] = None

class FormRequest(BaseModel):
    scheme_name: str
    applicant: Dict[str, Any]
    documents: Optional[Dict[str, Any]] = {}
    scheme_specific: Optional[Dict[str, Any]] = {}
    required_documents: Optional[List[str]] = None

class GrievanceRequest(BaseModel):
    applicant_name: str
    scheme_name: str
    rejection_reason: str
    application_reference: Optional[str] = "N/A"
    details: Optional[str] = ""
    address: Optional[str] = ""
    phone: Optional[str] = ""

class WorkflowStepRequest(BaseModel):
    session_id: str
    step: str
    data: Optional[Dict[str, Any]] = {}


# ─── Health Check ───

@app.get("/")
async def root():
    return {
        "service": "SevaSetu API",
        "version": "1.0.0-mvp",
        "status": "operational",
        "endpoints": [
            "POST /intent",
            "POST /scheme-match",
            "POST /validate-eligibility",
            "POST /upload-documents",
            "POST /extract-ocr/{document_id}",
            "POST /validate-documents",
            "POST /generate-form",
            "POST /generate-grievance",
            "POST /workflow/step",
            "GET /workflow/status/{session_id}",
        ]
    }


# ─── Intent Extraction ───

@app.post("/intent")
async def api_intent(req: IntentRequest):
    """Extract structured intent from user text input."""
    try:
        result = await extract_intent(req.text)
        session_id = req.session_id or str(uuid.uuid4())
        session = get_or_create_session(session_id)
        session.update_data("user_input", req.text)
        session.update_data("intent", result)
        return {
            "session_id": session_id,
            "input": req.text,
            "extracted_intent": result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─── Scheme Matching ───

@app.post("/scheme-match")
async def api_scheme_match(req: SchemeMatchRequest):
    """Find matching government schemes using semantic search."""
    try:
        result = await match_schemes(req.query, req.attributes, req.top_k)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─── Eligibility Validation ───

@app.post("/validate-eligibility")
async def api_validate_eligibility(req: EligibilityRequest):
    """Check user eligibility for a specific scheme using rule-based logic."""
    try:
        result = await check_eligibility(req.scheme_id, req.user_profile)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─── Document Upload ───

@app.post("/upload-documents")
async def api_upload_documents(
    file: UploadFile = File(...),
    document_type: str = Form(...),
    user_id: str = Form(default="demo-user"),
):
    """Upload a document for OCR processing."""
    try:
        result = await upload_document(file, document_type, user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─── OCR Extraction ───

@app.post("/extract-ocr/{document_id}")
async def api_extract_ocr(document_id: str):
    """Extract structured data from an uploaded document using OCR."""
    try:
        result = await extract_data(document_id)
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─── Document Validation ───

@app.post("/validate-documents")
async def api_validate_documents(req: DocumentValidationRequest):
    """Cross-validate multiple documents for consistency."""
    try:
        result = await validate_documents(req.user_id, req.documents)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─── Form Generation ───

@app.post("/generate-form")
async def api_generate_form(req: FormRequest):
    """Generate an auto-filled PDF application form."""
    try:
        result = await generate_form(req.model_dump())
        if result["status"] == "success":
            # Return JSON with download URL
            return {
                **result,
                "download_url": f"/download/form/{result['file_name']}",
            }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─── Grievance Generation ───

@app.post("/generate-grievance")
async def api_generate_grievance(req: GrievanceRequest):
    """Generate a formal grievance letter PDF."""
    try:
        result = await generate_grievance(req.model_dump())
        if result["status"] == "success":
            return {
                **result,
                "download_url": f"/download/form/{result['file_name']}",
            }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─── File Download ───

@app.get("/download/form/{file_name}")
async def download_form(file_name: str):
    """Download a generated PDF form."""
    file_path = os.path.join(os.path.dirname(__file__), "generated_forms", file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, media_type="application/pdf", filename=file_name)


# ─── Workflow Orchestrator ───

@app.post("/workflow/step")
async def api_workflow_step(req: WorkflowStepRequest):
    """Process a workflow step through the agent orchestrator."""
    try:
        result = await process_step(req.session_id, req.step, req.data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/workflow/status/{session_id}")
async def api_workflow_status(session_id: str):
    """Get current workflow status for a session."""
    session = get_or_create_session(session_id)
    return session.get_status()


# ─── Startup ───

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    print("[SevaSetu] Starting up...")
    vector_store.build_index()
    print("[SevaSetu] API ready at http://localhost:8000")
    print("[SevaSetu] Docs at http://localhost:8000/docs")


# ─── Run ───

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
