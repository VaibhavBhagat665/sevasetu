import './StepIndicator.css';

const STEPS = [
    { key: 'input', label: 'Describe Need', icon: '🎤' },
    { key: 'schemes', label: 'Find Schemes', icon: '🔍' },
    { key: 'eligibility', label: 'Eligibility', icon: '✅' },
    { key: 'documents', label: 'Documents', icon: '📄' },
    { key: 'form', label: 'Application', icon: '📋' },
];

/**
 * Workflow progress indicator showing current step.
 */
export default function StepIndicator({ currentStep }) {
    const currentIndex = STEPS.findIndex(s => s.key === currentStep);

    return (
        <div className="step-indicator">
            {STEPS.map((step, i) => {
                let status = 'pending';
                if (i < currentIndex) status = 'completed';
                if (i === currentIndex) status = 'active';

                return (
                    <div key={step.key} className={`step ${status}`}>
                        <div className="step-icon">
                            {status === 'completed' ? '✓' : step.icon}
                        </div>
                        <span className="step-label">{step.label}</span>
                        {i < STEPS.length - 1 && <div className="step-connector" />}
                    </div>
                );
            })}
        </div>
    );
}
