from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class RestrictionType(str, Enum):
    NONE = "none"
    READ_ONLY_EDITOR = "read_only_editor"
    COPY_PASTE_DISABLED = "copy_paste_disabled"
    CAPTCHA_CHALLENGE = "captcha_challenge"
    LOGIN_REQUIRED = "login_required"
    AUTOMATION_PROHIBITED = "automation_prohibited"
    ACCESS_DENIED = "access_denied"
    RATE_LIMITED = "rate_limited"


class AlternativeActionType(str, Enum):
    PROCEED_NORMALLY = "proceed_normally"
    SAVE_LOCAL_FILE = "save_local_file"
    COPY_TO_CLIPBOARD = "copy_to_clipboard"
    USER_MANUAL_VERIFICATION = "user_manual_verification"
    USER_LOGIN_REQUIRED = "user_login_required"
    STOP_AUTOMATION = "stop_automation"


class AuthorizedAlternative(BaseModel):
    action_type: AlternativeActionType
    title: str
    description: str
    suggested_local_path: Optional[str] = None
    data_payload: Optional[Dict[str, Any]] = None


class RestrictionEvaluation(BaseModel):
    is_restricted: bool
    primary_restriction: RestrictionType = RestrictionType.NONE
    detected_restrictions: List[RestrictionType] = Field(default_factory=list)
    can_auto_edit: bool = True
    reason: Optional[str] = None
    authorized_alternative: Optional[AuthorizedAlternative] = None
