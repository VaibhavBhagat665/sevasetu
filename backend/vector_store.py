"""
SevaSetu — FAISS Vector Store for Scheme Discovery
Builds a semantic search index from scheme descriptions using sentence-transformers.
"""

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from schemes_data import get_scheme_descriptions, get_scheme_by_id

# Singleton instances
_model = None
_index = None
_scheme_ids = []


def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def build_index():
    """Build the FAISS index from scheme descriptions."""
    global _index, _scheme_ids

    model = _get_model()
    pairs = get_scheme_descriptions()
    _scheme_ids = [sid for sid, _ in pairs]
    texts = [text for _, text in pairs]

    embeddings = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
    dimension = embeddings.shape[1]

    _index = faiss.IndexFlatIP(dimension)  # Inner product (cosine sim with normalized vecs)
    _index.add(embeddings.astype(np.float32))

    print(f"[VectorStore] Built index with {len(_scheme_ids)} schemes, dim={dimension}")
    return _index


def search(query: str, top_k: int = 5):
    """Search for schemes matching the query text."""
    global _index, _scheme_ids

    if _index is None:
        build_index()

    model = _get_model()
    query_vec = model.encode([query], convert_to_numpy=True, normalize_embeddings=True)

    scores, indices = _index.search(query_vec.astype(np.float32), min(top_k, len(_scheme_ids)))

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx < 0:
            continue
        scheme = get_scheme_by_id(_scheme_ids[idx])
        if scheme:
            results.append({
                "scheme": scheme,
                "score": float(score),
            })

    return results
