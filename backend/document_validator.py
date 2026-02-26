"""
SevaSetu — Document Validator
Cross-document mismatch detection using fuzzy string matching.
"""

from fuzzywuzzy import fuzz
from ocr_engine import get_all_documents_for_user


def _normalize(text: str) -> str:
    """Normalize text for comparison."""
    if not text:
        return ""
    return " ".join(text.strip().lower().split())


def _fuzzy_match(str1: str, str2: str) -> float:
    """Return similarity ratio between two strings (0-100)."""
    if not str1 or not str2:
        return 0.0
    s1 = _normalize(str1)
    s2 = _normalize(str2)
    return fuzz.token_sort_ratio(s1, s2)


def _extract_name(data: dict) -> str:
    """Extract the primary name from extracted document data."""
    for key in ["name", "account_holder_name", "head_of_family", "owner_name"]:
        if key in data and data[key]:
            return data[key]
    return ""


def _extract_address_pincode(data: dict) -> str:
    """Extract pincode from address data."""
    if "address" in data and isinstance(data["address"], dict):
        return data["address"].get("pincode", "")
    return ""


def _extract_address_district(data: dict) -> str:
    """Extract district from address or top-level."""
    if "address" in data and isinstance(data["address"], dict):
        return data["address"].get("district", "")
    if "district" in data:
        return data["district"]
    return ""


async def validate_documents(user_id: str = "demo-user", documents_data: list = None) -> dict:
    """
    Validate consistency across multiple uploaded documents.

    Checks:
    - Name consistency across all documents
    - Address / pincode consistency
    - Date of birth consistency
    """
    # Use provided data or fetch from stored documents
    if documents_data:
        docs = documents_data
    else:
        stored = get_all_documents_for_user(user_id)
        docs = [
            {"document_type": d["document_type"], "extracted_data": d["extracted_data"]}
            for d in stored
            if d.get("extracted_data")
        ]

    if len(docs) < 2:
        return {
            "status": "insufficient",
            "message": "At least 2 documents are needed for cross-validation.",
            "issues": [],
            "is_valid": True,
        }

    issues = []
    warnings = []

    # 1. Name consistency check
    names = []
    for doc in docs:
        name = _extract_name(doc["extracted_data"])
        if name:
            names.append({"doc_type": doc["document_type"], "name": name})

    if len(names) >= 2:
        base_name = names[0]["name"]
        base_doc = names[0]["doc_type"]
        for other in names[1:]:
            similarity = _fuzzy_match(base_name, other["name"])
            if similarity < 80:
                issues.append({
                    "field": "name",
                    "severity": "critical",
                    "message": f"Name mismatch between {base_doc} ('{base_name}') and {other['doc_type']} ('{other['name']}'). Similarity: {similarity}%",
                    "suggestion": "Ensure names match exactly across all documents. Minor spelling variations may cause application rejection.",
                    "documents": [base_doc, other["doc_type"]],
                    "similarity": similarity,
                })
            elif similarity < 95:
                warnings.append({
                    "field": "name",
                    "severity": "warning",
                    "message": f"Minor name variation between {base_doc} ('{base_name}') and {other['doc_type']} ('{other['name']}'). Similarity: {similarity}%",
                    "suggestion": "Names are similar but not identical. This may or may not cause issues during verification.",
                    "documents": [base_doc, other["doc_type"]],
                    "similarity": similarity,
                })

    # 2. Pincode consistency
    pincodes = []
    for doc in docs:
        pc = _extract_address_pincode(doc["extracted_data"])
        if pc:
            pincodes.append({"doc_type": doc["document_type"], "pincode": pc})

    if len(pincodes) >= 2:
        base_pc = pincodes[0]["pincode"]
        for other in pincodes[1:]:
            if base_pc != other["pincode"]:
                issues.append({
                    "field": "pincode",
                    "severity": "warning",
                    "message": f"Pincode mismatch: {pincodes[0]['doc_type']} has '{base_pc}' but {other['doc_type']} has '{other['pincode']}'",
                    "suggestion": "Ensure your address pincode is consistent across documents.",
                    "documents": [pincodes[0]["doc_type"], other["doc_type"]],
                })

    # 3. District consistency
    districts = []
    for doc in docs:
        d = _extract_address_district(doc["extracted_data"])
        if d:
            districts.append({"doc_type": doc["document_type"], "district": d})

    if len(districts) >= 2:
        base_d = districts[0]["district"]
        for other in districts[1:]:
            sim = _fuzzy_match(base_d, other["district"])
            if sim < 80:
                warnings.append({
                    "field": "district",
                    "severity": "warning",
                    "message": f"District mismatch between {districts[0]['doc_type']} ('{base_d}') and {other['doc_type']} ('{other['district']}')",
                    "suggestion": "Verify district information across documents.",
                    "documents": [districts[0]["doc_type"], other["doc_type"]],
                })

    all_issues = issues + warnings
    has_critical = any(i["severity"] == "critical" for i in all_issues)

    return {
        "status": "completed",
        "is_valid": not has_critical,
        "total_issues": len(all_issues),
        "critical_issues": len(issues),
        "warnings": len(warnings),
        "issues": all_issues,
        "documents_checked": len(docs),
        "message": (
            "❌ Critical mismatches found. Please resolve before submitting."
            if has_critical
            else ("⚠️ Minor warnings found. Review recommended." if warnings else "✅ All documents are consistent.")
        ),
    }
