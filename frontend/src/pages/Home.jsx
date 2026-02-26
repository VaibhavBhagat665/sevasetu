import './Home.css';

const WORKFLOW_STEPS = [
    { icon: '🎤', title: 'Describe Your Needs', desc: 'Tell us about your situation using voice or text — in Hindi or English' },
    { icon: '🔍', title: 'Discover Schemes', desc: 'AI finds the best government schemes matching your profile instantly' },
    { icon: '✅', title: 'Check Eligibility', desc: 'Rule-based verification tells you exactly if you qualify, and why' },
    { icon: '📄', title: 'Upload Documents', desc: 'Snap photos of Aadhaar, bank passbook, certificates — OCR extracts data' },
    { icon: '📋', title: 'Auto-Fill Application', desc: 'Download a perfectly filled PDF application form, ready to submit' },
];

const FEATURES = [
    { icon: '🧠', title: 'AI-Powered', desc: 'Semantic search and intelligent intent understanding' },
    { icon: '🔒', title: 'Privacy-First', desc: 'No permanent storage of sensitive documents' },
    { icon: '📱', title: 'Offline-Ready', desc: 'Works even in low-connectivity rural areas' },
    { icon: '🗣️', title: 'Voice Input', desc: 'Speak naturally in Hindi or English' },
    { icon: '⚡', title: 'Instant Results', desc: 'Get scheme matches in seconds' },
    { icon: '📊', title: 'Explainable', desc: 'Every decision is transparent and auditable' },
];

/**
 * Landing page with hero, workflow steps, and features.
 */
export default function Home({ onGetStarted }) {
    return (
        <div className="home">
            {/* Hero */}
            <section className="hero">
                <div className="hero-content animate-slideUp">
                    <div className="hero-badge">
                        <span className="badge badge-primary">🇮🇳 For Every Indian Citizen</span>
                    </div>
                    <h1 className="hero-title">
                        <span className="gradient-text">SevaSetu</span>
                    </h1>
                    <p className="hero-subtitle">
                        AI-powered bridge to government welfare schemes.
                        Discover schemes, verify eligibility, and auto-fill applications — all in one place.
                    </p>
                    <div className="hero-actions">
                        <button className="btn btn-primary btn-lg" onClick={onGetStarted}>
                            Get Started →
                        </button>
                        <a href="#how-it-works" className="btn btn-outline btn-lg">
                            How It Works
                        </a>
                    </div>
                    <div className="hero-stats">
                        <div className="stat">
                            <span className="stat-value">10+</span>
                            <span className="stat-label">Schemes</span>
                        </div>
                        <div className="stat-divider" />
                        <div className="stat">
                            <span className="stat-value">OCR</span>
                            <span className="stat-label">Document Scan</span>
                        </div>
                        <div className="stat-divider" />
                        <div className="stat">
                            <span className="stat-value">PDF</span>
                            <span className="stat-label">Auto-Fill</span>
                        </div>
                    </div>
                </div>

                {/* Abstract background shapes */}
                <div className="hero-shapes">
                    <div className="shape shape-1" />
                    <div className="shape shape-2" />
                    <div className="shape shape-3" />
                </div>
            </section>

            {/* Workflow */}
            <section id="how-it-works" className="workflow-section">
                <h2 className="section-title">How It Works</h2>
                <p className="section-desc">Five simple steps from need to application</p>
                <div className="workflow-grid stagger">
                    {WORKFLOW_STEPS.map((step, i) => (
                        <div key={i} className="workflow-card glass-card">
                            <div className="workflow-number">{i + 1}</div>
                            <span className="workflow-icon">{step.icon}</span>
                            <h3>{step.title}</h3>
                            <p>{step.desc}</p>
                        </div>
                    ))}
                </div>
            </section>

            {/* Features */}
            <section className="features-section">
                <h2 className="section-title">Why SevaSetu?</h2>
                <div className="features-grid stagger">
                    {FEATURES.map((f, i) => (
                        <div key={i} className="feature-card glass-card">
                            <span className="feature-icon">{f.icon}</span>
                            <h3>{f.title}</h3>
                            <p>{f.desc}</p>
                        </div>
                    ))}
                </div>
            </section>

            {/* CTA */}
            <section className="cta-section">
                <div className="cta-content glass-card">
                    <h2>Ready to find your eligible schemes?</h2>
                    <p>Start the AI-guided application process now.</p>
                    <button className="btn btn-primary btn-lg" onClick={onGetStarted}>
                        Start Application →
                    </button>
                </div>
            </section>
        </div>
    );
}
