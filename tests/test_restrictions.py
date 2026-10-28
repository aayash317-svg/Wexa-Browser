import pytest
from backend.security.restriction_detector import WebsiteRestrictionDetector
from backend.security.offline_guard import OfflineSecurityGuard
from backend.schemas.restrictions import RestrictionType, AlternativeActionType


def test_normal_unrestricted_page():
    eval_res = WebsiteRestrictionDetector.evaluate_page(
        page_origin="https://open-practice.example",
        dom_metadata={"editor_readonly": False},
        visible_text="Write a function to sum numbers."
    )
    assert not eval_res.is_restricted
    assert eval_res.can_auto_edit
    assert eval_res.primary_restriction == RestrictionType.NONE


def test_readonly_editor_offers_local_file_alternative():
    eval_res = WebsiteRestrictionDetector.evaluate_page(
        page_origin="https://practice.example/read-only-problem",
        dom_metadata={"editor_readonly": True},
        visible_text="Problem statement here."
    )
    assert eval_res.is_restricted
    assert eval_res.primary_restriction == RestrictionType.READ_ONLY_EDITOR
    assert not eval_res.can_auto_edit
    assert eval_res.authorized_alternative is not None
    assert eval_res.authorized_alternative.action_type == AlternativeActionType.SAVE_LOCAL_FILE


def test_captcha_challenge_pauses_for_user():
    eval_res = WebsiteRestrictionDetector.evaluate_page(
        page_origin="https://secure.example",
        dom_metadata={"has_captcha": True},
        visible_text="Please verify you are human to proceed."
    )
    assert eval_res.is_restricted
    assert eval_res.primary_restriction == RestrictionType.CAPTCHA_CHALLENGE
    assert not eval_res.can_auto_edit
    assert eval_res.authorized_alternative.action_type == AlternativeActionType.USER_MANUAL_VERIFICATION


def test_automation_prohibited_assessment():
    eval_res = WebsiteRestrictionDetector.evaluate_page(
        page_origin="https://proctored-test.example",
        dom_metadata={"anti_automation": True},
        visible_text="Proctored assessment in progress."
    )
    assert eval_res.is_restricted
    assert eval_res.primary_restriction == RestrictionType.AUTOMATION_PROHIBITED
    assert not eval_res.can_auto_edit
    assert eval_res.authorized_alternative.action_type == AlternativeActionType.SAVE_LOCAL_FILE


def test_offline_guard_sanitizes_credentials():
    dirty_text = "Here is the test session: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xyz and password: 'SecretPassword123'"
    clean_text = OfflineSecurityGuard.sanitize_text(dirty_text)
    assert "SecretPassword123" not in clean_text
    assert "Bearer eyJhb" not in clean_text
    assert "[REDACTED_SECRET]" in clean_text
