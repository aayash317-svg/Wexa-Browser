from enum import Enum
from typing import Optional
from pydantic import BaseModel


class AgentState(str, Enum):
    IDLE = "IDLE"
    ANALYSING = "ANALYSING"
    PROPOSAL_READY = "PROPOSAL_READY"
    WAITING_FOR_APPROVAL = "WAITING_FOR_APPROVAL"
    APPROVED = "APPROVED"
    APPLYING_EDIT = "APPLYING_EDIT"
    VERIFYING_EDIT = "VERIFYING_EDIT"
    TESTING = "TESTING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    ERROR = "ERROR"


class ApprovalContext(BaseModel):
    proposal_id: str
    origin: str
    target_editor: str
    expected_original_hash: str
    proposed_code: str
    is_valid: bool = True


class PermissionStateMachine:
    """
    Enforces the single-action, non-bypassable approval lifecycle
    specified in Section 9 of the Wexa Specification.
    """
    def __init__(self):
        self.current_state: AgentState = AgentState.IDLE
        self.active_context: Optional[ApprovalContext] = None

    def begin_analysis(self):
        self.current_state = AgentState.ANALYSING
        self.active_context = None

    def set_proposal_ready(self, context: ApprovalContext):
        self.active_context = context
        self.current_state = AgentState.WAITING_FOR_APPROVAL

    def user_approved(self, proposal_id: str, current_page_origin: str) -> bool:
        if self.current_state != AgentState.WAITING_FOR_APPROVAL:
            return False
        
        if not self.active_context or self.active_context.proposal_id != proposal_id:
            return False

        # Invalidate if page origin changed
        if self.active_context.origin != current_page_origin:
            self.current_state = AgentState.ERROR
            return False

        self.current_state = AgentState.APPROVED
        return True

    def user_cancelled(self):
        self.current_state = AgentState.CANCELLED
        self.active_context = None

    def mark_applied(self):
        self.current_state = AgentState.VERIFYING_EDIT

    def mark_verified(self):
        self.current_state = AgentState.TESTING

    def mark_completed(self):
        self.current_state = AgentState.COMPLETED
        self.active_context = None

    def mark_error(self):
        self.current_state = AgentState.ERROR
