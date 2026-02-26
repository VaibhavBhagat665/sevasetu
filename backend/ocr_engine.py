"""
SevaSetu — OCR Engine (Simulated)
Accepts document uploads and returns simulated but realistic extracted data.
Architecture is pluggable for real Tesseract/PaddleOCR integration.
"""

import uuid
import os
from datetime import datetime

# In-memory document store (for MVP — no persistent storage)
_documents = {}

# Upload directory
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


# Simulated OCR outputs per document type
MOCK_EXTRACTIONS = {
    "AADHAAR": {
        "name": "Raj Kumar Sharma",
        "name_hindi": "राज कुमार शर्मा",
        "dob": "1985-06-15",
        "gender": "Male",
        "aadhaar_number": "XXXX-XXXX-4521",
        "address": {
            "line1": "H.No. 45, Ward No. 3",
            "line2": "Village Khedla",
            "district": "Bhopal",
            "state": "Madhya Pradesh",
            "pincode": "462001"
        },
    },
    "BANK_PASSBOOK": {
        "account_holder_name": "Raj Kumar Sharma",
        "bank_name": "State Bank of India",
        "branch": "Bhopal Main Branch",
        "account_number": "XXXXX67890",
        "ifsc_code": "SBIN0001234",
        "address": {
            "line1": "H.No. 45, Ward 3",
            "district": "Bhopal",
            "state": "Madhya Pradesh",
            "pincode": "462001"
        },
    },
    "INCOME_CERTIFICATE": {
        "name": "Raj Kumar Sharma",
        "father_name": "Shri Harish Sharma",
        "annual_income": 180000,
        "income_source": "Agriculture",
        "issuing_authority": "Tehsildar, Bhopal",
        "certificate_number": "IC/2024/MP/78543",
        "valid_until": "2025-03-31",
    },
    "LAND_RECORD": {
        "owner_name": "Raj Kumar Sharma",
        "father_name": "Harish Sharma",
        "survey_number": "234/A",
        "area_hectares": 1.5,
        "land_type": "Agricultural",
        "village": "Khedla",
        "tehsil": "Huzur",
        "district": "Bhopal",
        "state": "Madhya Pradesh",
    },
    "RATION_CARD": {
        "head_of_family": "Raj Kumar Sharma",
        "card_type": "BPL",
        "card_number": "MP/BPL/2023/45678",
        "family_members": 4,
        "address": {
            "village": "Khedla",
            "district": "Bhopal",
            "state": "Madhya Pradesh",
            "pincode": "462001"
        },
    },
    "CASTE_CERTIFICATE": {
        "name": "Raj Kumar Sharma",
        "father_name": "Harish Sharma",
        "caste": "General",
        "category": "General",
        "issuing_authority": "SDM, Bhopal",
        "certificate_number": "CC/2024/MP/12345",
    },
    "BPL_CERTIFICATE": {
        "name": "Raj Kumar Sharma",
        "family_income": 120000,
        "bpl_number": "BPL/MP/2023/6789",
        "category": "BPL",
        "valid_until": "2025-12-31",
    },
}


async def upload_document(file, document_type: str, user_id: str = None) -> dict:
    """Save uploaded document and return document ID."""
    doc_id = str(uuid.uuid4())

    # Save file
    file_ext = os.path.splitext(file.filename)[1] if file.filename else ".jpg"
    file_path = os.path.join(UPLOAD_DIR, f"{doc_id}{file_ext}")

    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    # Store metadata
    _documents[doc_id] = {
        "document_id": doc_id,
        "user_id": user_id or "demo-user",
        "document_type": document_type.upper(),
        "file_path": file_path,
        "file_name": file.filename,
        "uploaded_at": datetime.now().isoformat(),
        "status": "uploaded",
        "extracted_data": None,
    }

    return {
        "document_id": doc_id,
        "status": "uploaded",
        "message": f"Document '{file.filename}' uploaded successfully. Ready for OCR extraction.",
    }


async def extract_data(document_id: str) -> dict:
    """Extract data from uploaded document using simulated OCR."""
    doc = _documents.get(document_id)
    if not doc:
        return {"error": f"Document '{document_id}' not found"}

    doc_type = doc["document_type"]

    # Get simulated extraction
    extracted = MOCK_EXTRACTIONS.get(doc_type, {
        "name": "Unknown",
        "raw_text": "OCR extraction completed but document type not recognized."
    })

    # Update stored document
    doc["extracted_data"] = extracted
    doc["status"] = "extracted"

    return {
        "document_id": document_id,
        "document_type": doc_type,
        "extracted_data": extracted,
        "confidence": 0.94,
        "status": "extracted",
        "message": f"Successfully extracted data from {doc_type} document.",
    }


def get_document(document_id: str) -> dict:
    """Get document by ID."""
    return _documents.get(document_id)


def get_all_documents_for_user(user_id: str = "demo-user") -> list:
    """Get all documents for a user."""
    return [d for d in _documents.values() if d["user_id"] == user_id]
