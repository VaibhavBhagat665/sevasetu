import { useState, useRef } from 'react';
import { uploadDocument, extractOCR } from '../services/api';
import './DocumentUpload.css';

const DOC_TYPES = [
    { value: 'AADHAAR', label: 'Aadhaar Card', icon: '🪪' },
    { value: 'BANK_PASSBOOK', label: 'Bank Passbook', icon: '🏦' },
    { value: 'INCOME_CERTIFICATE', label: 'Income Certificate', icon: '💵' },
    { value: 'LAND_RECORD', label: 'Land Record', icon: '🌾' },
    { value: 'RATION_CARD', label: 'Ration Card', icon: '🃏' },
    { value: 'CASTE_CERTIFICATE', label: 'Caste Certificate', icon: '📜' },
    { value: 'BPL_CERTIFICATE', label: 'BPL Certificate', icon: '📋' },
];

/**
 * Document upload component with drag-and-drop and OCR extraction.
 */
export default function DocumentUpload({ requiredDocs, onDocumentsProcessed }) {
    const [uploads, setUploads] = useState([]);
    const [processing, setProcessing] = useState(false);
    const fileRef = useRef(null);
    const [selectedType, setSelectedType] = useState('');

    const filteredTypes = requiredDocs
        ? DOC_TYPES.filter(d => requiredDocs.includes(d.value))
        : DOC_TYPES;

    const handleFileSelect = async (e) => {
        const file = e.target.files[0];
        if (!file || !selectedType) return;

        setProcessing(true);
        try {
            // Upload
            const uploadResult = await uploadDocument(file, selectedType);
            const docId = uploadResult.document_id;

            // Extract OCR
            const ocrResult = await extractOCR(docId);

            const newUpload = {
                id: docId,
                type: selectedType,
                fileName: file.name,
                extracted: ocrResult.extracted_data,
                confidence: ocrResult.confidence,
                status: 'extracted',
            };

            const updated = [...uploads, newUpload];
            setUploads(updated);
            onDocumentsProcessed?.(updated);
        } catch (err) {
            const newUpload = {
                id: Date.now().toString(),
                type: selectedType,
                fileName: file.name,
                extracted: null,
                status: 'error',
                error: err.message,
            };
            setUploads([...uploads, newUpload]);
        } finally {
            setProcessing(false);
            setSelectedType('');
            if (fileRef.current) fileRef.current.value = '';
        }
    };

    return (
        <div className="doc-upload">
            <div className="upload-controls">
                <select
                    className="input doc-type-select"
                    value={selectedType}
                    onChange={(e) => setSelectedType(e.target.value)}
                    disabled={processing}
                >
                    <option value="">Select document type...</option>
                    {filteredTypes.map(dt => (
                        <option key={dt.value} value={dt.value}>
                            {dt.icon} {dt.label}
                        </option>
                    ))}
                </select>

                <input
                    ref={fileRef}
                    type="file"
                    accept="image/*,.pdf"
                    onChange={handleFileSelect}
                    disabled={!selectedType || processing}
                    style={{ display: 'none' }}
                    id="doc-file-input"
                />
                <button
                    className="btn btn-accent"
                    onClick={() => fileRef.current?.click()}
                    disabled={!selectedType || processing}
                >
                    {processing ? (
                        <><span className="loader loader-sm" /> Processing...</>
                    ) : (
                        <>📷 Upload / Capture</>
                    )}
                </button>
            </div>

            {uploads.length > 0 && (
                <div className="uploaded-docs stagger">
                    {uploads.map(doc => (
                        <div key={doc.id} className={`doc-card glass-card ${doc.status}`}>
                            <div className="doc-card-header">
                                <span className="doc-icon">
                                    {DOC_TYPES.find(d => d.value === doc.type)?.icon || '📄'}
                                </span>
                                <div>
                                    <h4>{DOC_TYPES.find(d => d.value === doc.type)?.label || doc.type}</h4>
                                    <span className="doc-filename">{doc.fileName}</span>
                                </div>
                                <span className={`badge ${doc.status === 'extracted' ? 'badge-success' : 'badge-danger'}`}>
                                    {doc.status === 'extracted' ? 'Extracted' : 'Error'}
                                </span>
                            </div>

                            {doc.extracted && (
                                <div className="doc-extracted">
                                    <table className="doc-data-table">
                                        <tbody>
                                            {Object.entries(doc.extracted).map(([key, val]) => {
                                                if (typeof val === 'object' && val !== null) {
                                                    return (
                                                        <tr key={key}>
                                                            <td className="field-name">{key.replace(/_/g, ' ')}</td>
                                                            <td className="field-value">
                                                                {Object.entries(val).map(([k, v]) => (
                                                                    <div key={k}><span className="sub-key">{k}:</span> {String(v)}</div>
                                                                ))}
                                                            </td>
                                                        </tr>
                                                    );
                                                }
                                                return (
                                                    <tr key={key}>
                                                        <td className="field-name">{key.replace(/_/g, ' ')}</td>
                                                        <td className="field-value">{String(val)}</td>
                                                    </tr>
                                                );
                                            })}
                                        </tbody>
                                    </table>

                                    {doc.confidence && (
                                        <div className="ocr-confidence">
                                            <span>OCR Confidence:</span>
                                            <div className="confidence-bar">
                                                <div className="confidence-fill" style={{ width: `${doc.confidence * 100}%` }} />
                                            </div>
                                            <span>{Math.round(doc.confidence * 100)}%</span>
                                        </div>
                                    )}
                                </div>
                            )}

                            {doc.error && (
                                <p className="doc-error">Error: {doc.error}</p>
                            )}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
