from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from backend.schemas.restrictions import RestrictionEvaluation


class TaskType(str, Enum):
    EMPTY_EDITOR = "empty_editor"
    STARTER_CODE_TODO = "starter_code_todo"
    INCOMPLETE_METHOD = "incomplete_method"
    EXISTING_CODE_ERROR = "existing_code_error"
    AMBIGUOUS = "ambiguous"
    UNSUPPORTED = "unsupported"


class TargetRegion(BaseModel):
    kind: str = Field(..., description="e.g. function_body, class_body, entire_file")
    name: Optional[str] = Field(None, description="Identifier of method or block")
    start_line: Optional[int] = None
    end_line: Optional[int] = None


class PageAnalysisRequest(BaseModel):
    page_title: str
    origin: str
    visible_text: str
    starter_code: Optional[str] = ""
    language: Optional[str] = "python"
    editor_type: Optional[str] = "textarea"
    dom_metadata: Dict[str, Any] = Field(default_factory=dict)


class PageTaskExtraction(BaseModel):
    task_type: TaskType
    language: str
    problem_statement: str
    constraints: List[str] = Field(default_factory=list)
    examples: List[Dict[str, Any]] = Field(default_factory=list)
    starter_code: str = ""
    target: Optional[TargetRegion] = None
    editable_region_hint: Optional[str] = None
    analysis_confidence: float = 0.95
    restriction_evaluation: Optional[RestrictionEvaluation] = None



class ProposedSolution(BaseModel):
    language: str
    task_type: TaskType
    target: Optional[TargetRegion] = None
    proposed_code: str
    explanation: str
    diff_patch: Optional[str] = None
    requires_review: bool = True
