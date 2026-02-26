"""
SevaSetu — Intent Extraction Engine
Uses Google Gemini (or keyword fallback) to extract structured intent from user text.
"""

import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

# Try to import Gemini
_gemini_available = False
try:
    import google.generativeai as genai
    api_key = os.getenv("GEMINI_API_KEY", "")
    if api_key:
        genai.configure(api_key=api_key)
        _gemini_available = True
        print("[IntentEngine] Gemini API configured successfully")
    else:
        print("[IntentEngine] No GEMINI_API_KEY found, using keyword fallback")
except ImportError:
    print("[IntentEngine] google-generativeai not installed, using keyword fallback")


INTENT_PROMPT = """You are SevaSetu, an AI assistant helping Indian citizens find and apply for government welfare schemes.

Analyze the user's message and extract structured information.

User message: "{user_text}"

Return ONLY a valid JSON object with these fields:
{{
    "intent": "find_scheme" | "check_eligibility" | "apply" | "grievance" | "general_query",
    "scheme_type": "agriculture" | "housing" | "health" | "education" | "livelihood" | "energy" | "employment" | "women_child" | null,
    "key_attributes": {{
        "occupation": string or null,
        "age": number or null,
        "gender": "male" | "female" | null,
        "income": number or null,
        "category": "General" | "SC" | "ST" | "OBC" | null,
        "state": string or null,
        "residence": "rural" | "urban" | null,
        "land_holding": number or null
    }},
    "summary": "brief summary of what the user needs"
}}

Extract what you can from the message. Set unknown fields to null.
"""


def _keyword_fallback(text: str) -> dict:
    """Simple keyword-based intent extraction when LLM is unavailable."""
    text_lower = text.lower()

    # Detect intent
    intent = "find_scheme"
    if any(w in text_lower for w in ["grievance", "complaint", "rejected", "appeal"]):
        intent = "grievance"
    elif any(w in text_lower for w in ["apply", "application", "form", "fill"]):
        intent = "apply"
    elif any(w in text_lower for w in ["eligible", "eligibility", "qualify", "can i get"]):
        intent = "check_eligibility"

    # Detect scheme type
    scheme_type = None
    type_keywords = {
        "agriculture": ["farmer", "kisan", "farming", "agriculture", "crop", "land", "kheti"],
        "housing": ["house", "home", "awas", "housing", "ghar", "construction"],
        "health": ["health", "hospital", "medical", "insurance", "ayushman", "treatment"],
        "education": ["education", "scholarship", "school", "college", "student", "study"],
        "livelihood": ["business", "loan", "vendor", "shop", "mudra", "self-employed"],
        "energy": ["gas", "lpg", "ujjwala", "cooking", "fuel", "cylinder"],
        "employment": ["job", "employment", "work", "mgnrega", "wage", "labour", "nrega"],
        "women_child": ["girl", "daughter", "sukanya", "women", "mahila", "beti"],
    }
    for stype, keywords in type_keywords.items():
        if any(kw in text_lower for kw in keywords):
            scheme_type = stype
            break

    # Extract attributes
    attrs = {
        "occupation": None, "age": None, "gender": None,
        "income": None, "category": None, "state": None,
        "residence": None, "land_holding": None
    }

    # Occupation
    occ_map = {
        "farmer": ["farmer", "kisan", "farming"],
        "street_vendor": ["vendor", "hawker", "street seller"],
        "self_employed": ["self-employed", "business", "shop"],
        "student": ["student", "studying"],
        "labourer": ["labourer", "labour", "worker", "mazdoor"],
    }
    for occ, keywords in occ_map.items():
        if any(kw in text_lower for kw in keywords):
            attrs["occupation"] = occ
            break

    # Age
    age_match = re.search(r'(\d{1,2})\s*(?:years?|yrs?|sal)\s*old|age\s*(?:is)?\s*(\d{1,2})', text_lower)
    if age_match:
        attrs["age"] = int(age_match.group(1) or age_match.group(2))

    # Gender
    if any(w in text_lower for w in ["woman", "female", "mahila", "wife", "mother", "sister"]):
        attrs["gender"] = "female"
    elif any(w in text_lower for w in ["man", "male", "husband", "father", "brother"]):
        attrs["gender"] = "male"

    # Category
    for cat in ["SC", "ST", "OBC"]:
        if cat.lower() in text_lower or cat in text:
            attrs["category"] = cat
            break

    # Residence
    if any(w in text_lower for w in ["village", "rural", "gaon", "gramin"]):
        attrs["residence"] = "rural"
    elif any(w in text_lower for w in ["city", "urban", "town", "shahar"]):
        attrs["residence"] = "urban"

    # Income
    income_match = re.search(r'(?:income|kamai|salary)\s*(?:is)?\s*(?:rs\.?|₹)?\s*([\d,]+)', text_lower)
    if income_match:
        attrs["income"] = int(income_match.group(1).replace(",", ""))

    return {
        "intent": intent,
        "scheme_type": scheme_type,
        "key_attributes": attrs,
        "summary": f"User is looking for {scheme_type or 'government'} scheme assistance."
    }


async def extract_intent(user_text: str) -> dict:
    """Extract structured intent from user text using LLM or fallback."""

    if _gemini_available:
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = INTENT_PROMPT.format(user_text=user_text)
            response = model.generate_content(prompt)
            text = response.text.strip()

            # Extract JSON from response
            json_match = re.search(r'\{[\s\S]*\}', text)
            if json_match:
                result = json.loads(json_match.group())
                return result
        except Exception as e:
            print(f"[IntentEngine] Gemini error, falling back to keywords: {e}")

    # Fallback
    return _keyword_fallback(user_text)
