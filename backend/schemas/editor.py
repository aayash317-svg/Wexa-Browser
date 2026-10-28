from enum import Enum
from typing import Optional
from pydantic import BaseModel


class EditorType(str, Enum):
    TEXTAREA = "textarea"
    MONACO = "monaco"
    CODEMIRROR = "codemirror"
    ACE = "ace"
    CUSTOM = "custom"


class EditProposal(BaseModel):
    proposal_id: str
    target_region: Optional[str] = None
    original_code: str
    replacement_code: str
    diff_unified: str


class ApplyEditResult(BaseModel):
    success: bool
    verified: bool
    message: str
    actual_editor_content: Optional[str] = None
