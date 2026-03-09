"""
SevaSetu — Lightweight Vector Store for Scheme Discovery
Builds a semantic search index using TF-IDF and cosine similarity to fit in 512MB RAM.
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from schemes_data import get_scheme_descriptions, get_scheme_by_id

# Singleton instances
_vectorizer = None
_tfidf_matrix = None
_scheme_ids = []


def build_index():
    """Build the TF-IDF index from scheme descriptions."""
    global _vectorizer, _tfidf_matrix, _scheme_ids

    pairs = get_scheme_descriptions()
    _scheme_ids = [sid for sid, _ in pairs]
    texts = [text for _, text in pairs]

    _vectorizer = TfidfVectorizer(stop_words='english')
    _tfidf_matrix = _vectorizer.fit_transform(texts)

    print(f"[VectorStore] Built TF-IDF index with {len(_scheme_ids)} schemes")
    return _tfidf_matrix


def search(query: str, top_k: int = 5):
    """Search for schemes matching the query text."""
    global _vectorizer, _tfidf_matrix, _scheme_ids

    if _vectorizer is None or _tfidf_matrix is None:
        build_index()
        
    if not query.strip():
        return []

    query_vec = _vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, _tfidf_matrix).flatten()
    
    # Get top_k matching indices descending
    top_indices = similarities.argsort()[::-1][:top_k]

    results = []
    for idx in top_indices:
        score = similarities[idx]
        if score > 0.01:
            scheme = get_scheme_by_id(_scheme_ids[idx])
            if scheme:
                results.append({
                    "scheme": scheme,
                    "score": float(score),
                })

    return results
