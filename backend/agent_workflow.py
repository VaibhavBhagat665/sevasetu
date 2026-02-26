"""
SevaSetu — Agent Workflow Orchestrator
State machine managing the end-to-end application flow with fallback handling.
"""

from enum import Enum
from datetime import datetime


class WorkflowState(str, Enum):
    INTAKE = "intake"
    SCHEME_DISCOVERY = "scheme_discovery"
    ELIGIBILITY_CHECK = "eligibility_check"
    DOCUMENT_UPLOAD = "document_upload"
    DOCUMENT_VALIDATION = "document_validation"
    FORM_GENERATION = "form_generation"
    COMPLETE = "complete"
    GRIEVANCE = "grievance"
    ERROR = "error"


# State transitions: current -> list of valid next states
VALID_TRANSITIONS = {
    WorkflowState.INTAKE: [WorkflowState.SCHEME_DISCOVERY, WorkflowState.ERROR],
    WorkflowState.SCHEME_DISCOVERY: [WorkflowState.ELIGIBILITY_CHECK, WorkflowState.INTAKE, WorkflowState.ERROR],
    WorkflowState.ELIGIBILITY_CHECK: [WorkflowState.DOCUMENT_UPLOAD, WorkflowState.GRIEVANCE, WorkflowState.SCHEME_DISCOVERY, WorkflowState.ERROR],
    WorkflowState.DOCUMENT_UPLOAD: [WorkflowState.DOCUMENT_VALIDATION, WorkflowState.ERROR],
    WorkflowState.DOCUMENT_VALIDATION: [WorkflowState.FORM_GENERATION, WorkflowState.DOCUMENT_UPLOAD, WorkflowState.ERROR],
    WorkflowState.FORM_GENERATION: [WorkflowState.COMPLETE, WorkflowState.ERROR],
    WorkflowState.COMPLETE: [WorkflowState.GRIEVANCE, WorkflowState.INTAKE],
    WorkflowState.GRIEVANCE: [WorkflowState.COMPLETE, WorkflowState.INTAKE],
    WorkflowState.ERROR: [WorkflowState.INTAKE],
}

# Human-readable step descriptions
STATE_DESCRIPTIONS = {
    WorkflowState.INTAKE: "Tell us about yourself and what you need",
    WorkflowState.SCHEME_DISCOVERY: "Finding matching government schemes",
    WorkflowState.ELIGIBILITY_CHECK: "Checking your eligibility",
    WorkflowState.DOCUMENT_UPLOAD: "Upload your documents",
    WorkflowState.DOCUMENT_VALIDATION: "Verifying your documents",
    WorkflowState.FORM_GENERATION: "Generating your application form",
    WorkflowState.COMPLETE: "Application ready!",
    WorkflowState.GRIEVANCE: "Generating grievance letter",
    WorkflowState.ERROR: "Something went wrong",
}

# In-memory session store
_sessions = {}


class WorkflowSession:
    """Manages a single user's workflow session."""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.current_state = WorkflowState.INTAKE
        self.history = []
        self.data = {
            "user_input": None,
            "intent": None,
            "matched_schemes": None,
            "selected_scheme": None,
            "user_profile": None,
            "eligibility_result": None,
            "uploaded_documents": [],
            "extracted_data": {},
            "validation_result": None,
            "form_result": None,
            "grievance_result": None,
        }
        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at
        self._log_transition(None, WorkflowState.INTAKE, "Session created")

    def _log_transition(self, from_state, to_state, reason):
        self.history.append({
            "from": from_state.value if from_state else None,
            "to": to_state.value,
            "reason": reason,
            "timestamp": datetime.now().isoformat(),
        })
        self.updated_at = datetime.now().isoformat()

    def transition(self, next_state: WorkflowState, reason: str = "") -> bool:
        """Attempt a state transition. Returns True if successful."""
        if next_state in VALID_TRANSITIONS.get(self.current_state, []):
            old_state = self.current_state
            self.current_state = next_state
            self._log_transition(old_state, next_state, reason)
            return True
        return False

    def get_status(self) -> dict:
        return {
            "session_id": self.session_id,
            "current_state": self.current_state.value,
            "state_description": STATE_DESCRIPTIONS[self.current_state],
            "next_valid_states": [s.value for s in VALID_TRANSITIONS.get(self.current_state, [])],
            "data_collected": {k: v is not None for k, v in self.data.items()},
            "history": self.history[-5:],  # last 5 transitions
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def update_data(self, key: str, value):
        """Update session data."""
        self.data[key] = value
        self.updated_at = datetime.now().isoformat()


def create_session(session_id: str = None) -> WorkflowSession:
    """Create a new workflow session."""
    import uuid
    sid = session_id or str(uuid.uuid4())
    session = WorkflowSession(sid)
    _sessions[sid] = session
    return session


def get_session(session_id: str) -> WorkflowSession:
    """Get existing session or None."""
    return _sessions.get(session_id)


def get_or_create_session(session_id: str) -> WorkflowSession:
    """Get or create a workflow session."""
    if session_id in _sessions:
        return _sessions[session_id]
    return create_session(session_id)


async def process_step(session_id: str, step: str, data: dict = None) -> dict:
    """
    Process a workflow step and return the result with next actions.

    This is the main orchestrator entry point called by the API.
    """
    session = get_or_create_session(session_id)

    if step == "intake":
        session.update_data("user_input", data.get("text", ""))
        session.transition(WorkflowState.SCHEME_DISCOVERY, "User input received, moving to scheme discovery")
        return {
            "status": "success",
            "current_state": session.current_state.value,
            "message": "Input received. Finding matching schemes...",
            "next_action": "scheme_discovery",
        }

    elif step == "scheme_selected":
        session.update_data("selected_scheme", data.get("scheme_id"))
        session.update_data("user_profile", data.get("user_profile", {}))
        session.transition(WorkflowState.ELIGIBILITY_CHECK, "Scheme selected, checking eligibility")
        return {
            "status": "success",
            "current_state": session.current_state.value,
            "message": "Checking eligibility...",
            "next_action": "eligibility_check",
        }

    elif step == "eligibility_passed":
        session.transition(WorkflowState.DOCUMENT_UPLOAD, "Eligible, requesting documents")
        return {
            "status": "success",
            "current_state": session.current_state.value,
            "message": "You're eligible! Please upload your documents.",
            "next_action": "document_upload",
        }

    elif step == "eligibility_failed":
        session.transition(WorkflowState.GRIEVANCE, "Not eligible, offering grievance option")
        return {
            "status": "success",
            "current_state": session.current_state.value,
            "message": "You may not be eligible. We can help you file a grievance or find alternatives.",
            "next_action": "grievance_or_alternatives",
        }

    elif step == "documents_uploaded":
        session.update_data("uploaded_documents", data.get("document_ids", []))
        session.transition(WorkflowState.DOCUMENT_VALIDATION, "Documents uploaded, validating")
        return {
            "status": "success",
            "current_state": session.current_state.value,
            "message": "Validating your documents...",
            "next_action": "document_validation",
        }

    elif step == "validation_passed":
        session.transition(WorkflowState.FORM_GENERATION, "Validation passed, generating form")
        return {
            "status": "success",
            "current_state": session.current_state.value,
            "message": "Documents validated! Generating your application form...",
            "next_action": "form_generation",
        }

    elif step == "validation_failed":
        session.transition(WorkflowState.DOCUMENT_UPLOAD, "Validation issues, reupload requested")
        return {
            "status": "success",
            "current_state": session.current_state.value,
            "message": "Document issues found. Please correct and re-upload.",
            "next_action": "document_upload",
        }

    elif step == "form_generated":
        session.transition(WorkflowState.COMPLETE, "Form generated successfully")
        return {
            "status": "success",
            "current_state": session.current_state.value,
            "message": "Your application form is ready for download!",
            "next_action": "complete",
        }

    elif step == "generate_grievance":
        if session.current_state != WorkflowState.GRIEVANCE:
            session.transition(WorkflowState.GRIEVANCE, "Grievance requested")
        return {
            "status": "success",
            "current_state": session.current_state.value,
            "message": "Generating grievance letter...",
            "next_action": "grievance",
        }

    else:
        return {
            "status": "error",
            "message": f"Unknown step: {step}",
            "current_state": session.current_state.value,
        }
