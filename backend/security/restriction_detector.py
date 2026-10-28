import re
from typing import Dict, Any, List, Optional
from backend.schemas.restrictions import (
    RestrictionType,
    RestrictionEvaluation,
    AlternativeActionType,
    AuthorizedAlternative
)

class WebsiteRestrictionDetector:
    """
    Detects website restrictions, access barriers, and security protections.
    Determines whether automated editing is authorized or must offer safe alternatives.
    """

    @classmethod
    def evaluate_page(
        cls,
        page_origin: str,
        dom_metadata: Dict[str, Any],
        visible_text: str = ""
    ) -> RestrictionEvaluation:
        restrictions: List[RestrictionType] = []

        # 1. CAPTCHA / Human verification challenge
        if cls._detect_captcha(dom_metadata, visible_text):
            restrictions.append(RestrictionType.CAPTCHA_CHALLENGE)

        # 2. Login required / 401 / 403
        if cls._detect_login_required(dom_metadata, visible_text):
            restrictions.append(RestrictionType.LOGIN_REQUIRED)

        # 3. Access Denied / Prohibited automation / Assessment lock
        if cls._detect_automation_prohibited(dom_metadata, visible_text):
            restrictions.append(RestrictionType.AUTOMATION_PROHIBITED)

        # 4. Read-only editor
        if cls._detect_read_only_editor(dom_metadata):
            restrictions.append(RestrictionType.READ_ONLY_EDITOR)

        # 5. Disabled copy/paste
        if cls._detect_copy_paste_disabled(dom_metadata):
            restrictions.append(RestrictionType.COPY_PASTE_DISABLED)

        # Determine Primary Action & Safe Alternative
        if not restrictions:
            return RestrictionEvaluation(
                is_restricted=False,
                primary_restriction=RestrictionType.NONE,
                can_auto_edit=True,
                reason="Page and editor are open for authorized interaction."
            )

        # Priority resolution
        if RestrictionType.CAPTCHA_CHALLENGE in restrictions:
            return RestrictionEvaluation(
                is_restricted=True,
                primary_restriction=RestrictionType.CAPTCHA_CHALLENGE,
                detected_restrictions=restrictions,
                can_auto_edit=False,
                reason="CAPTCHA or verification challenge detected. Automated interaction paused.",
                authorized_alternative=AuthorizedAlternative(
                    action_type=AlternativeActionType.USER_MANUAL_VERIFICATION,
                    title="Manual Verification Required",
                    description="Please solve the verification challenge in the browser to continue."
                )
            )

        if RestrictionType.AUTOMATION_PROHIBITED in restrictions:
            return RestrictionEvaluation(
                is_restricted=True,
                primary_restriction=RestrictionType.AUTOMATION_PROHIBITED,
                detected_restrictions=restrictions,
                can_auto_edit=False,
                reason="This page or assessment explicitly restricts automated editing tools.",
                authorized_alternative=AuthorizedAlternative(
                    action_type=AlternativeActionType.SAVE_LOCAL_FILE,
                    title="Export Solution Locally",
                    description="Automated insertion is disabled by website policy. We can save the solution to your local project disk."
                )
            )

        if RestrictionType.LOGIN_REQUIRED in restrictions:
            return RestrictionEvaluation(
                is_restricted=True,
                primary_restriction=RestrictionType.LOGIN_REQUIRED,
                detected_restrictions=restrictions,
                can_auto_edit=False,
                reason="Authentication required to access full practice features.",
                authorized_alternative=AuthorizedAlternative(
                    action_type=AlternativeActionType.USER_LOGIN_REQUIRED,
                    title="Authentication Required",
                    description="Please log into the service directly using your credentials."
                )
            )

        if RestrictionType.READ_ONLY_EDITOR in restrictions:
            return RestrictionEvaluation(
                is_restricted=True,
                primary_restriction=RestrictionType.READ_ONLY_EDITOR,
                detected_restrictions=restrictions,
                can_auto_edit=False,
                reason="The target editor is currently in read-only mode.",
                authorized_alternative=AuthorizedAlternative(
                    action_type=AlternativeActionType.SAVE_LOCAL_FILE,
                    title="Save Code to Local File",
                    description="Editor cannot be edited directly. The generated code can be saved to your local workspace."
                )
            )

        return RestrictionEvaluation(
            is_restricted=True,
            primary_restriction=restrictions[0],
            detected_restrictions=restrictions,
            can_auto_edit=False,
            reason="Restrictions detected on this page."
        )

    @staticmethod
    def _detect_captcha(dom: Dict[str, Any], text: str) -> bool:
        if dom.get("has_captcha") or "cf-turnstile" in str(dom) or "g-recaptcha" in str(dom):
            return True
        return bool(re.search(r"(verify you are human|security check|recaptcha|hcaptcha)", text, re.IGNORECASE))

    @staticmethod
    def _detect_login_required(dom: Dict[str, Any], text: str) -> bool:
        if dom.get("http_status") in (401, 403):
            return True
        return bool(re.search(r"(please log in to continue|sign in required|session expired)", text, re.IGNORECASE))

    @staticmethod
    def _detect_automation_prohibited(dom: Dict[str, Any], text: str) -> bool:
        meta_policy = dom.get("anti_automation", False)
        if meta_policy:
            return True
        return bool(re.search(r"(automated tools prohibited|proctored assessment|anti-cheating active)", text, re.IGNORECASE))

    @staticmethod
    def _detect_read_only_editor(dom: Dict[str, Any]) -> bool:
        return bool(dom.get("editor_readonly") or dom.get("editor_disabled"))

    @staticmethod
    def _detect_copy_paste_disabled(dom: Dict[str, Any]) -> bool:
        return bool(dom.get("paste_disabled") or dom.get("onpaste_prevented"))
