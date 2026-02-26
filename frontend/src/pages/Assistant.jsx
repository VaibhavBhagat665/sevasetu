import { useState, useRef } from 'react';
import StepIndicator from '../components/StepIndicator';
import VoiceInput from '../components/VoiceInput';
import SchemeCard from '../components/SchemeCard';
import DocumentUpload from '../components/DocumentUpload';
import {
    extractIntent, matchSchemes, validateEligibility,
    validateDocuments, generateForm, generateGrievance,
    getDownloadUrl,
} from '../services/api';
import './Assistant.css';

const STEP_KEYS = ['input', 'schemes', 'eligibility', 'documents', 'form'];

/**
 * Main workflow page — guides user through the end-to-end application process.
 */
export default function Assistant({ onBack }) {
    const [step, setStep] = useState('input');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [inputText, setInputText] = useState('');

    // Data
    const [intentResult, setIntentResult] = useState(null);
    const [schemes, setSchemes] = useState([]);
    const [selectedScheme, setSelectedScheme] = useState(null);
    const [eligibility, setEligibility] = useState(null);
    const [userProfile, setUserProfile] = useState({
        age: '', occupation: '', income: '', category: 'General',
        gender: '', state: '', residence: '', land_holding: '',
    });
    const [documents, setDocuments] = useState([]);
    const [validation, setValidation] = useState(null);
    const [formResult, setFormResult] = useState(null);
    const [grievanceResult, setGrievanceResult] = useState(null);

    const messagesEndRef = useRef(null);

    /* ─── Step 1: Input → Intent + Scheme discovery ─── */
    const handleSubmitInput = async (text) => {
        const finalText = text || inputText;
        if (!finalText.trim()) return;
        setInputText(finalText);
        setLoading(true);
        setError('');

        try {
            const intentRes = await extractIntent(finalText);
            setIntentResult(intentRes.extracted_intent);

            const query = intentRes.extracted_intent.summary || finalText;
            const attrs = intentRes.extracted_intent.key_attributes || {};
            const schemeRes = await matchSchemes(query, attrs);
            setSchemes(schemeRes.schemes || []);

            // Pre-fill profile from extracted attributes
            const ka = intentRes.extracted_intent.key_attributes || {};
            setUserProfile(prev => ({
                ...prev,
                ...(ka.age && { age: ka.age }),
                ...(ka.occupation && { occupation: ka.occupation }),
                ...(ka.income && { income: ka.income }),
                ...(ka.category && { category: ka.category }),
                ...(ka.gender && { gender: ka.gender }),
                ...(ka.state && { state: ka.state }),
                ...(ka.residence && { residence: ka.residence }),
                ...(ka.land_holding && { land_holding: ka.land_holding }),
            }));

            setStep('schemes');
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    /* ─── Step 2: Check eligibility ─── */
    const handleCheckEligibility = async (scheme) => {
        setSelectedScheme(scheme);
        setStep('eligibility');
    };

    const handleSubmitEligibility = async () => {
        if (!selectedScheme) return;
        setLoading(true);
        setError('');

        try {
            const profile = {};
            Object.entries(userProfile).forEach(([k, v]) => {
                if (v !== '' && v !== null && v !== undefined) {
                    profile[k] = isNaN(v) ? v : Number(v);
                }
            });

            const result = await validateEligibility(selectedScheme.scheme_id, profile);
            setEligibility(result);

            if (result.is_eligible) {
                setStep('documents');
            }
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    /* ─── Step 3: Documents ─── */
    const handleDocumentsProcessed = (docs) => {
        setDocuments(docs);
    };

    const handleValidateAndGenerate = async () => {
        setLoading(true);
        setError('');
        try {
            // Cross-validate docs
            const docsForValidation = documents
                .filter(d => d.status === 'extracted')
                .map(d => ({
                    document_type: d.type,
                    extracted_data: d.extracted,
                }));

            if (docsForValidation.length >= 2) {
                const valResult = await validateDocuments(docsForValidation);
                setValidation(valResult);
            }

            // Generate form
            const aadhaar = documents.find(d => d.type === 'AADHAAR')?.extracted || {};
            const bank = documents.find(d => d.type === 'BANK_PASSBOOK')?.extracted || {};

            const formData = {
                scheme_name: selectedScheme?.name || 'Government Scheme',
                applicant: {
                    name: aadhaar.name || userProfile.name || 'Applicant Name',
                    father_name: aadhaar.father_name || '',
                    dob: aadhaar.dob || '',
                    gender: aadhaar.gender || userProfile.gender || '',
                    age: userProfile.age || '',
                    category: userProfile.category || '',
                    phone: userProfile.phone || '',
                    aadhaar_number: aadhaar.aadhaar_number || '',
                    address: aadhaar.address || {},
                    occupation: userProfile.occupation || '',
                    income: userProfile.income || '',
                    land_holding: userProfile.land_holding || '',
                },
                documents: { bank },
                required_documents: selectedScheme?.required_documents?.map(
                    d => d.replace(/_/g, ' ')
                ) || [],
            };

            const result = await generateForm(formData);
            setFormResult(result);
            setStep('form');
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    /* ─── Grievance ─── */
    const handleGenerateGrievance = async () => {
        setLoading(true);
        setError('');
        try {
            const result = await generateGrievance({
                applicant_name: userProfile.name || 'Applicant',
                scheme_name: selectedScheme?.name || 'Government Scheme',
                rejection_reason: eligibility?.explanation || 'Application not approved',
                address: userProfile.state || '',
            });
            setGrievanceResult(result);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    /* ─── Render ─── */
    return (
        <div className="assistant">
            {/* Header */}
            <div className="assistant-header">
                <button className="btn btn-ghost btn-sm" onClick={onBack}>← Back</button>
                <h2>SevaSetu Assistant</h2>
                <div style={{ width: 70 }} />
            </div>

            {/* Step Indicator */}
            <StepIndicator currentStep={step} />

            {/* Error */}
            {error && (
                <div className="error-banner">
                    <span>⚠️ {error}</span>
                    <button onClick={() => setError('')}>✕</button>
                </div>
            )}

            {/* Content */}
            <div className="assistant-content">

                {/* ═══ STEP: INPUT ═══ */}
                {step === 'input' && (
                    <div className="step-panel animate-fadeInUp">
                        <div className="step-header">
                            <h3>🎤 Tell us what you need</h3>
                            <p>Describe your situation, and we'll find the best government schemes for you.</p>
                        </div>
                        <div className="input-area">
                            <div className="input-row">
                                <textarea
                                    className="input chat-input"
                                    placeholder="E.g., I am a farmer with 1.5 hectares of land in Madhya Pradesh. My income is ₹1,50,000 per year. I need financial help..."
                                    value={inputText}
                                    onChange={(e) => setInputText(e.target.value)}
                                    rows={4}
                                    disabled={loading}
                                />
                                <VoiceInput
                                    onResult={(text) => {
                                        setInputText(text);
                                        handleSubmitInput(text);
                                    }}
                                    disabled={loading}
                                />
                            </div>
                            <button
                                className="btn btn-primary btn-lg w-full"
                                onClick={() => handleSubmitInput()}
                                disabled={loading || !inputText.trim()}
                            >
                                {loading ? <><span className="loader loader-sm" /> Finding schemes...</> : 'Find Schemes →'}
                            </button>
                        </div>

                        {/* Example prompts */}
                        <div className="example-prompts">
                            <span className="examples-label">Try these:</span>
                            <div className="examples-list">
                                {[
                                    'I am a farmer with 1.5 hectares in MP, income ₹1.5 lakh',
                                    'I need a house in rural Bihar, BPL family',
                                    'I am a woman, need LPG gas connection, BPL',
                                    'I want a scholarship, SC student, income ₹2 lakh',
                                ].map((ex, i) => (
                                    <button
                                        key={i}
                                        className="btn btn-outline btn-sm example-btn"
                                        onClick={() => { setInputText(ex); handleSubmitInput(ex); }}
                                        disabled={loading}
                                    >
                                        {ex}
                                    </button>
                                ))}
                            </div>
                        </div>
                    </div>
                )}

                {/* ═══ STEP: SCHEMES ═══ */}
                {step === 'schemes' && (
                    <div className="step-panel animate-fadeInUp">
                        <div className="step-header">
                            <h3>🔍 Matching Schemes Found</h3>
                            <p>Based on your input, here are the best matching government schemes.</p>
                        </div>

                        {intentResult && (
                            <div className="intent-summary glass-card">
                                <h4>What we understood:</h4>
                                <p>{intentResult.summary}</p>
                                <div className="intent-tags">
                                    {intentResult.scheme_type && <span className="badge badge-accent">{intentResult.scheme_type}</span>}
                                    {intentResult.intent && <span className="badge badge-primary">{intentResult.intent}</span>}
                                </div>
                            </div>
                        )}

                        <div className="schemes-list stagger">
                            {schemes.map((scheme) => (
                                <SchemeCard
                                    key={scheme.scheme_id}
                                    scheme={scheme}
                                    onCheckEligibility={handleCheckEligibility}
                                    selected={selectedScheme?.scheme_id === scheme.scheme_id}
                                />
                            ))}
                        </div>

                        {schemes.length === 0 && !loading && (
                            <div className="empty-state glass-card">
                                <p>No schemes found. Try describing your situation differently.</p>
                                <button className="btn btn-outline" onClick={() => setStep('input')}>← Try Again</button>
                            </div>
                        )}
                    </div>
                )}

                {/* ═══ STEP: ELIGIBILITY ═══ */}
                {step === 'eligibility' && (
                    <div className="step-panel animate-fadeInUp">
                        <div className="step-header">
                            <h3>✅ Eligibility Check — {selectedScheme?.short_name || selectedScheme?.name}</h3>
                            <p>Provide your details to verify eligibility.</p>
                        </div>

                        <div className="profile-form glass-card">
                            <h4>Your Profile</h4>
                            <div className="form-grid">
                                <div className="form-field">
                                    <label>Age</label>
                                    <input className="input" type="number" placeholder="e.g., 35" value={userProfile.age} onChange={e => setUserProfile(p => ({ ...p, age: e.target.value }))} />
                                </div>
                                <div className="form-field">
                                    <label>Occupation</label>
                                    <select className="input" value={userProfile.occupation} onChange={e => setUserProfile(p => ({ ...p, occupation: e.target.value }))}>
                                        <option value="">Select...</option>
                                        <option value="farmer">Farmer</option>
                                        <option value="agricultural_labourer">Agricultural Labourer</option>
                                        <option value="street_vendor">Street Vendor</option>
                                        <option value="self_employed">Self Employed</option>
                                        <option value="student">Student</option>
                                        <option value="labourer">Labourer</option>
                                        <option value="homemaker">Homemaker</option>
                                        <option value="other">Other</option>
                                    </select>
                                </div>
                                <div className="form-field">
                                    <label>Annual Income (₹)</label>
                                    <input className="input" type="number" placeholder="e.g., 150000" value={userProfile.income} onChange={e => setUserProfile(p => ({ ...p, income: e.target.value }))} />
                                </div>
                                <div className="form-field">
                                    <label>Category</label>
                                    <select className="input" value={userProfile.category} onChange={e => setUserProfile(p => ({ ...p, category: e.target.value }))}>
                                        <option value="General">General</option>
                                        <option value="SC">SC</option>
                                        <option value="ST">ST</option>
                                        <option value="OBC">OBC</option>
                                    </select>
                                </div>
                                <div className="form-field">
                                    <label>Gender</label>
                                    <select className="input" value={userProfile.gender} onChange={e => setUserProfile(p => ({ ...p, gender: e.target.value }))}>
                                        <option value="">Select...</option>
                                        <option value="male">Male</option>
                                        <option value="female">Female</option>
                                    </select>
                                </div>
                                <div className="form-field">
                                    <label>State</label>
                                    <input className="input" placeholder="e.g., Madhya Pradesh" value={userProfile.state} onChange={e => setUserProfile(p => ({ ...p, state: e.target.value }))} />
                                </div>
                                <div className="form-field">
                                    <label>Residence</label>
                                    <select className="input" value={userProfile.residence} onChange={e => setUserProfile(p => ({ ...p, residence: e.target.value }))}>
                                        <option value="">Select...</option>
                                        <option value="rural">Rural</option>
                                        <option value="urban">Urban</option>
                                    </select>
                                </div>
                                <div className="form-field">
                                    <label>Land Holding (hectares)</label>
                                    <input className="input" type="number" step="0.1" placeholder="e.g., 1.5" value={userProfile.land_holding} onChange={e => setUserProfile(p => ({ ...p, land_holding: e.target.value }))} />
                                </div>
                            </div>

                            <button
                                className="btn btn-primary btn-lg w-full"
                                onClick={handleSubmitEligibility}
                                disabled={loading}
                                style={{ marginTop: 20 }}
                            >
                                {loading ? <><span className="loader loader-sm" /> Checking...</> : 'Check Eligibility →'}
                            </button>
                        </div>

                        {/* Eligibility Results */}
                        {eligibility && (
                            <div className={`eligibility-result glass-card ${eligibility.is_eligible ? 'eligible' : 'ineligible'}`}>
                                <div className="eligibility-header">
                                    <span className="eligibility-icon">{eligibility.is_eligible ? '🎉' : '⚠️'}</span>
                                    <h4>{eligibility.is_eligible ? 'You are Eligible!' : 'Not Eligible'}</h4>
                                </div>

                                <div className="rules-list">
                                    {eligibility.rule_results?.map((r, i) => (
                                        <div key={i} className={`rule-item ${r.status}`}>
                                            <span className="rule-status">
                                                {r.status === 'pass' ? '✅' : r.status === 'fail' ? '❌' : '❓'}
                                            </span>
                                            <span className="rule-text">{r.rule}</span>
                                            {r.actual_value && (
                                                <span className="rule-actual">Your value: {r.actual_value}</span>
                                            )}
                                        </div>
                                    ))}
                                </div>

                                {eligibility.is_eligible && (
                                    <div className="eligibility-actions">
                                        <p className="success-msg">Great! Now upload your documents to proceed.</p>
                                        <button className="btn btn-success btn-lg" onClick={() => setStep('documents')}>
                                            Upload Documents →
                                        </button>
                                    </div>
                                )}

                                {!eligibility.is_eligible && (
                                    <div className="eligibility-actions">
                                        <button className="btn btn-danger" onClick={handleGenerateGrievance} disabled={loading}>
                                            {loading ? 'Generating...' : '📝 Generate Grievance Letter'}
                                        </button>
                                        <button className="btn btn-outline" onClick={() => setStep('schemes')}>
                                            ← View Other Schemes
                                        </button>
                                    </div>
                                )}

                                {/* Alternatives */}
                                {eligibility.alternatives?.length > 0 && (
                                    <div className="alternatives">
                                        <h4>Alternative Schemes You May Qualify For:</h4>
                                        {eligibility.alternatives.map((alt, i) => (
                                            <div key={i} className="alt-card">
                                                <div className="alt-info">
                                                    <span className="badge badge-accent">{alt.category}</span>
                                                    <strong>{alt.name}</strong>
                                                    <span className="alt-match">{Math.round(alt.match_ratio * 100)}% match</span>
                                                </div>
                                                <p className="alt-benefits">{alt.benefits}</p>
                                            </div>
                                        ))}
                                    </div>
                                )}

                                {/* Grievance result */}
                                {grievanceResult && (
                                    <div className="download-section">
                                        <h4>📝 Grievance Letter Ready</h4>
                                        <p>Reference: {grievanceResult.grievance_reference}</p>
                                        <a
                                            href={getDownloadUrl(grievanceResult.file_name)}
                                            className="btn btn-primary"
                                            download
                                        >
                                            ⬇️ Download Grievance PDF
                                        </a>
                                    </div>
                                )}
                            </div>
                        )}
                    </div>
                )}

                {/* ═══ STEP: DOCUMENTS ═══ */}
                {step === 'documents' && (
                    <div className="step-panel animate-fadeInUp">
                        <div className="step-header">
                            <h3>📄 Upload Documents</h3>
                            <p>Upload your documents for OCR extraction and cross-validation.</p>
                        </div>

                        <DocumentUpload
                            requiredDocs={selectedScheme?.required_documents}
                            onDocumentsProcessed={handleDocumentsProcessed}
                        />

                        {documents.length > 0 && (
                            <div className="doc-actions">
                                <button
                                    className="btn btn-success btn-lg w-full"
                                    onClick={handleValidateAndGenerate}
                                    disabled={loading}
                                >
                                    {loading ? <><span className="loader loader-sm" /> Validating & Generating...</> : 'Validate & Generate Application →'}
                                </button>
                            </div>
                        )}

                        {validation && (
                            <div className={`validation-result glass-card ${validation.is_valid ? 'valid' : 'invalid'}`}>
                                <h4>{validation.message}</h4>
                                {validation.issues?.map((issue, i) => (
                                    <div key={i} className={`validation-issue ${issue.severity}`}>
                                        <span>{issue.severity === 'critical' ? '🔴' : '🟡'}</span>
                                        <div>
                                            <p>{issue.message}</p>
                                            <p className="issue-suggestion">{issue.suggestion}</p>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                )}

                {/* ═══ STEP: FORM ═══ */}
                {step === 'form' && (
                    <div className="step-panel animate-fadeInUp">
                        <div className="step-header">
                            <h3>📋 Application Form Ready!</h3>
                            <p>Your application form has been auto-filled and is ready for download.</p>
                        </div>

                        {formResult && (
                            <div className="form-result glass-card">
                                <div className="form-success-icon">🎉</div>
                                <h3>Application Generated Successfully</h3>
                                <p className="form-ref">Reference: <strong>{formResult.application_reference}</strong></p>
                                <p className="form-msg">{formResult.message}</p>

                                <a
                                    href={getDownloadUrl(formResult.file_name)}
                                    className="btn btn-primary btn-lg download-btn"
                                    download
                                >
                                    ⬇️ Download Application PDF
                                </a>

                                <div className="next-steps">
                                    <h4>Next Steps:</h4>
                                    <ol>
                                        <li>Download and print the filled application form</li>
                                        <li>Attach original documents (Aadhaar, bank passbook, etc.)</li>
                                        <li>Visit your nearest CSC centre or submit online</li>
                                        <li>Keep the application reference for tracking</li>
                                    </ol>
                                </div>

                                <div className="form-actions">
                                    <button className="btn btn-outline" onClick={() => {
                                        setStep('input');
                                        setSchemes([]);
                                        setSelectedScheme(null);
                                        setEligibility(null);
                                        setDocuments([]);
                                        setFormResult(null);
                                        setGrievanceResult(null);
                                        setInputText('');
                                        setIntentResult(null);
                                        setValidation(null);
                                    }}>
                                        🔄 Start New Application
                                    </button>
                                </div>
                            </div>
                        )}
                    </div>
                )}
            </div>

            <div ref={messagesEndRef} />
        </div>
    );
}
