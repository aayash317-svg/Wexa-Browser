from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class InteractionFeedbackRecord(BaseModel):
    """
    Structured record captured automatically whenever a user interacts,
    approves, modifies, or tests code. Used directly for training/fine-tuning.
    """
    record_id: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    origin: str
    language: str
    problem_statement: str
    starter_code: str
    target_region: Optional[str] = None
    model_proposed_code: str
    user_final_code: str
    user_accepted_without_changes: bool
    test_result_status: str  # PASS, FAIL, PARTIAL, UNVERIFIED
    test_stdout: Optional[str] = None
    test_stderr: Optional[str] = None
    compiler_error_corrected: bool = False
    metadata: Dict[str, Any] = Field(default_factory=dict)
