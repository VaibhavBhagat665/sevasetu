import './SchemeCard.css';

/**
 * Displays a single government scheme result card.
 */
export default function SchemeCard({ scheme, onSelect, onCheckEligibility, selected }) {
    const scorePercent = Math.round((scheme.score || 0) * 100);

    return (
        <div className={`scheme-card glass-card ${selected ? 'selected' : ''}`}>
            <div className="scheme-header">
                <div className="scheme-meta">
                    <span className="badge badge-accent">{scheme.category}</span>
                    <span className="scheme-score">{scorePercent}% match</span>
                </div>
                <h3 className="scheme-name">{scheme.name}</h3>
                <p className="scheme-short">{scheme.short_name}</p>
            </div>

            <p className="scheme-desc">{scheme.description}</p>

            <div className="scheme-benefits">
                <span className="benefits-icon">💰</span>
                <span>{scheme.benefits}</span>
            </div>

            {scheme.required_documents && (
                <div className="scheme-docs">
                    <span className="docs-label">Documents needed:</span>
                    <div className="docs-list">
                        {scheme.required_documents.map((doc) => (
                            <span key={doc} className="chip">{doc.replace(/_/g, ' ')}</span>
                        ))}
                    </div>
                </div>
            )}

            <div className="scheme-actions">
                <button className="btn btn-primary btn-sm" onClick={() => onCheckEligibility?.(scheme)}>
                    Check Eligibility
                </button>
                {scheme.official_website && (
                    <a href={scheme.official_website} target="_blank" rel="noopener noreferrer" className="btn btn-ghost btn-sm">
                        Official Site ↗
                    </a>
                )}
            </div>
        </div>
    );
}
