"""
Integration and Unit Tests for Wexa Browser Architecture & Playwright Manager.
Verifies:
- Active-tab detection and multi-tab lifecycle
- DOM element extraction with unique bids (data-wexa-bid)
- Page classification across Coding, E-commerce, Docs, Articles, General Web
- Consequential action approval guards
- Verification and recovery loops
- Barrier detection (CAPTCHA, Login walls)
"""

import pytest
from backend.browser.playwright_manager import PlaywrightBrowserManager, BrowserTabInfo
from backend.agent.action_planner import WexaActionPlanner
from backend.agent.action_loop import UniversalActionLoop
from backend.schemas.universal_action import (
    PageType,
    ActionType,
    LoopPhase,
    ProposedAction,
    InteractiveElement,
    PageObservation
)


@pytest.fixture
def browser_manager():
    return PlaywrightBrowserManager()


@pytest.fixture
def action_planner():
    return WexaActionPlanner()


def test_browser_initialization(browser_manager):
    """Verifies browser manager singleton and tab listing."""
    assert browser_manager is not None
    tabs = browser_manager.list_tabs()
    assert isinstance(tabs, list)
    assert len(tabs) >= 1
    assert any(t.is_active for t in tabs)


def test_multi_tab_lifecycle(browser_manager):
    """Tests creating, switching, and closing tabs."""
    initial_tabs = len(browser_manager.list_tabs())
    new_tid = browser_manager.new_tab("https://example.com")
    assert new_tid is not None

    tabs_after = browser_manager.list_tabs()
    assert len(tabs_after) == initial_tabs + 1

    # Switch tab
    switch_res = browser_manager.switch_tab(new_tid)
    assert switch_res is True

    # Close tab
    browser_manager.close_tab(new_tid)
    tabs_final = browser_manager.list_tabs()
    assert not any(t.tab_id == new_tid for t in tabs_final)


def test_page_observation_structure(browser_manager):
    """Verifies that observing a page produces structured PageObservation with interactive elements."""
    obs = browser_manager.observe_active_page("https://example.com")
    assert isinstance(obs, PageObservation)
    assert obs.url is not None
    assert obs.title is not None
    assert isinstance(obs.interactive_elements, list)
    assert obs.confidence > 0.0


def test_page_classification_universal(browser_manager):
    """Tests automatic domain-agnostic classification across categories."""
    assert browser_manager._classify_page_type("https://leetcode.com/problems/two-sum", "leetcode.com", "Given an array of integers", None) == PageType.CODING_PRACTICE
    assert browser_manager._classify_page_type("https://store.amazon.com/item/123", "amazon.com", "Add to cart Free shipping", None) == PageType.E_COMMERCE
    assert browser_manager._classify_page_type("https://docs.python.org/3/library/os.html", "docs.python.org", "Standard Library OS", None) == PageType.DOCUMENTATION
    assert browser_manager._classify_page_type("https://medium.com/engineering/microservices", "medium.com", "A deep dive into microservices", None) == PageType.ARTICLE
    assert browser_manager._classify_page_type("https://example.com", "example.com", "Example domain", None) == PageType.GENERAL_WEB


def test_consequential_action_approval_guard(browser_manager):
    """Verifies that consequential actions are blocked without explicit user approval."""
    consequential_action = ProposedAction(
        action_id="act-test-submit",
        action_type=ActionType.CLICK,
        target_element_id="b-submit",
        target_selector="button.submit",
        parameters={},
        explanation="Submit final payment or exam answer.",
        is_consequential=True,
        requires_approval=True
    )

    # 1. Without approval -> MUST be blocked
    result_denied = browser_manager.execute_browser_action(consequential_action, user_approved=False)
    assert result_denied.success is False
    assert result_denied.verification_passed is False
    assert result_denied.next_recommended_phase == LoopPhase.AWAIT_APPROVAL
    assert "requires explicit user permission" in result_denied.message

    # 2. With approval -> permitted
    result_approved = browser_manager.execute_browser_action(consequential_action, user_approved=True)
    assert result_approved.success is True
    assert result_approved.verification_passed is True


def test_barrier_detection(action_planner):
    """Verifies that CAPTCHAs and login barriers pause the agent and request user attention."""
    # CAPTCHA barrier
    obs_captcha = PageObservation(
        url="https://protected.example.com",
        title="Security Check",
        page_type=PageType.GENERAL_WEB,
        domain="protected.example.com",
        headings=["Please verify you are human"],
        interactive_elements=[],
        barriers=["captcha"]
    )
    plan_captcha = action_planner.plan_next_action(obs_captcha)
    assert plan_captcha.action_type == ActionType.USER_ATTENTION
    assert "CAPTCHA" in plan_captcha.explanation

    # Login barrier
    obs_login = PageObservation(
        url="https://portal.example.com/dashboard",
        title="Sign In",
        page_type=PageType.GENERAL_WEB,
        domain="portal.example.com",
        headings=["Login Required"],
        interactive_elements=[],
        barriers=["login_required"]
    )
    plan_login = action_planner.plan_next_action(obs_login)
    assert plan_login.action_type == ActionType.USER_ATTENTION
    assert "sign in" in plan_login.explanation.lower()


def test_action_loop_full_cycle():
    """Tests the full 5-step loop (Observe -> Plan -> Approval Check -> Act -> Verify)."""
    loop = UniversalActionLoop()

    # Step 1 & 2: Inspect
    obs = loop.step_inspect(
        url="https://leetcode.com/problems/valid-parentheses/",
        title="20. Valid Parentheses",
        visible_text="Given a string s containing just '(', ')', determine if valid.",
        starter_code="class Solution:\n    def isValid(self, s: str) -> bool:\n        pass"
    )
    assert obs.page_type == PageType.CODING_PRACTICE
    assert obs.has_code_editor is True

    # Step 3: Plan
    proposal = loop.step_reason_and_plan(user_goal="Solve problem")
    assert proposal.action_type == ActionType.SOLVE_CODE
    assert proposal.is_consequential is True

    # Step 4 & 5: Execute with approval & verify
    exec_result = loop.step_execute_and_verify(user_approved=True)
    assert exec_result.success is True
    assert exec_result.verification_passed is True
    assert exec_result.next_recommended_phase == LoopPhase.COMPLETED

