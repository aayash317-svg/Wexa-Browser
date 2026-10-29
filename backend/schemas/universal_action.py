from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class PageType(str, Enum):
    CODING_PRACTICE = "coding_practice"
    DOCUMENTATION = "documentation"
    ARTICLE = "article"
    E_COMMERCE = "e_commerce"
    FORM_WORKFLOW = "form_workflow"
    GENERAL_WEB = "general_web"


class ActionType(str, Enum):
    NAVIGATE = "navigate"
    CLICK = "click"
    TYPE = "type"
    SUBMIT = "submit"
    SOLVE_CODE = "solve_code"
    USER_ATTENTION = "user_attention"


class LoopPhase(str, Enum):
    OBSERVE = "observe"
    PLAN = "plan"
    AWAIT_APPROVAL = "await_approval"
    ACT = "act"
    VERIFY = "verify"
    RECOVERY = "recovery"
    COMPLETED = "completed"


class InteractiveElement(BaseModel):
    element_id: str
    tag: str
    role: Optional[str] = None
    text: str = ""
    name: Optional[str] = None
    selector: str
    input_type: Optional[str] = None
    value: Optional[str] = None
    is_interactive: bool = True
    is_consequential: bool = False


class PageObservation(BaseModel):
    url: str
    title: str
    page_type: PageType
    domain: str
    headings: List[str] = Field(default_factory=list)
    interactive_elements: List[InteractiveElement] = Field(default_factory=list)
    has_code_editor: bool = False
    starter_code: Optional[str] = None
    barriers: List[str] = Field(default_factory=list)  # captcha, login_required, rate_limit
    visible_summary: str = ""
    confidence: float = 0.95


class ProposedAction(BaseModel):
    action_id: str
    action_type: ActionType
    target_element_id: Optional[str] = None
    target_selector: Optional[str] = None
    parameters: Dict[str, Any] = Field(default_factory=dict)  # text to type, destination url, etc.
    explanation: str
    is_consequential: bool = False
    requires_approval: bool = False
    confidence: float = 0.90


class ActionResult(BaseModel):
    success: bool
    action_id: str
    action_type: ActionType
    new_url: Optional[str] = None
    message: str
    state_changed: bool = True
    barrier_detected: Optional[str] = None
    verification_passed: bool = True
    next_recommended_phase: LoopPhase = LoopPhase.OBSERVE
