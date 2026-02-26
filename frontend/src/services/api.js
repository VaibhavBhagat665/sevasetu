/**
 * SevaSetu — API Service
 * Client for communicating with the FastAPI backend.
 */

const API_BASE = 'http://localhost:8000';

async function request(endpoint, options = {}) {
    try {
        const res = await fetch(`${API_BASE}${endpoint}`, {
            headers: { 'Content-Type': 'application/json' },
            ...options,
        });
        if (!res.ok) {
            const err = await res.json().catch(() => ({ detail: res.statusText }));
            throw new Error(err.detail || `API error: ${res.status}`);
        }
        return await res.json();
    } catch (error) {
        if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
            throw new Error('Cannot connect to backend. Ensure the server is running at ' + API_BASE);
        }
        throw error;
    }
}

/** POST /intent — extract intent from text */
export async function extractIntent(text, sessionId = null) {
    return request('/intent', {
        method: 'POST',
        body: JSON.stringify({ text, session_id: sessionId }),
    });
}

/** POST /scheme-match — semantic search for schemes */
export async function matchSchemes(query, attributes = null, topK = 5) {
    return request('/scheme-match', {
        method: 'POST',
        body: JSON.stringify({ query, attributes, top_k: topK }),
    });
}

/** POST /validate-eligibility — check eligibility */
export async function validateEligibility(schemeId, userProfile) {
    return request('/validate-eligibility', {
        method: 'POST',
        body: JSON.stringify({ scheme_id: schemeId, user_profile: userProfile }),
    });
}

/** POST /upload-documents — upload a document */
export async function uploadDocument(file, documentType, userId = 'demo-user') {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('document_type', documentType);
    formData.append('user_id', userId);

    const res = await fetch(`${API_BASE}/upload-documents`, {
        method: 'POST',
        body: formData,
    });
    if (!res.ok) throw new Error('Upload failed');
    return res.json();
}

/** POST /extract-ocr/{id} — extract data from document */
export async function extractOCR(documentId) {
    return request(`/extract-ocr/${documentId}`, { method: 'POST' });
}

/** POST /validate-documents — cross-validate documents */
export async function validateDocuments(documents, userId = 'demo-user') {
    return request('/validate-documents', {
        method: 'POST',
        body: JSON.stringify({ user_id: userId, documents }),
    });
}

/** POST /generate-form — generate PDF form */
export async function generateForm(formData) {
    return request('/generate-form', {
        method: 'POST',
        body: JSON.stringify(formData),
    });
}

/** POST /generate-grievance — generate grievance letter */
export async function generateGrievance(data) {
    return request('/generate-grievance', {
        method: 'POST',
        body: JSON.stringify(data),
    });
}

/** Download a generated PDF */
export function getDownloadUrl(fileName) {
    return `${API_BASE}/download/form/${fileName}`;
}
