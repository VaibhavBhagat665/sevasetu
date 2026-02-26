"""
SevaSetu — Scheme Matcher
Takes extracted intent and performs vector search + optional filtering.
"""

from vector_store import search as vector_search
from schemes_data import get_all_schemes


async def match_schemes(query: str, attributes: dict = None, top_k: int = 5) -> dict:
    """
    Find matching schemes using semantic search and optional attribute filtering.

    Args:
        query: search query text
        attributes: optional user attributes for filtering
        top_k: number of results to return

    Returns:
        dict with matched schemes and metadata
    """
    # Perform vector search
    results = vector_search(query, top_k=top_k)

    matched = []
    for r in results:
        scheme = r["scheme"]
        score = r["score"]

        # Compute a simple attribute-based boost
        boost = 0.0
        if attributes:
            occupation = attributes.get("occupation")
            if occupation:
                for rule in scheme["eligibility_rules"]["rules"]:
                    if rule["field"] == "occupation":
                        if rule["operator"] == "eq" and rule["value"] == occupation:
                            boost = 0.15
                        elif rule["operator"] == "in" and occupation in rule["value"]:
                            boost = 0.15

        final_score = min(score + boost, 1.0)

        matched.append({
            "scheme_id": scheme["scheme_id"],
            "name": scheme["name"],
            "short_name": scheme["short_name"],
            "category": scheme["category"],
            "description": scheme["description"],
            "benefits": scheme["benefits"],
            "required_documents": scheme["required_documents"],
            "score": round(final_score, 3),
            "official_website": scheme["official_website"],
        })

    # Sort by final score descending
    matched.sort(key=lambda x: x["score"], reverse=True)

    return {
        "query": query,
        "total_results": len(matched),
        "schemes": matched[:top_k],
    }
