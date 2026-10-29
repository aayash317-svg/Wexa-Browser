import pytest
from backend.schemas.universal_action import PageType, ActionType, LoopPhase
from backend.page_parser.universal_inspector import UniversalPageInspector
from backend.agent.action_planner import WexaActionPlanner
from backend.agent.action_executor import WexaActionExecutor
from backend.agent.action_loop import UniversalActionLoop


def test_universal_page_inspection_domains():
    """Verify inspection across multiple different types of websites."""
    # 1. Coding
    obs_code = UniversalPageInspector.inspect(
        url="https://leetcode.com/problems/two-sum/",
        title="Two Sum",
        visible_text="Given an array of integers nums and an integer target, return indices...",
        starter_code="class Solution: def twoSum(self, nums, target): pass"
    )
    assert obs_code.page_type == PageType.CODING_PRACTICE
    assert obs_code.has_code_editor is True

    # 2. Documentation
    obs_doc = UniversalPageInspector.inspect(
        url="https://docs.python.org/3/library/functions.html",
        title="Built-in Functions",
        visible_text="The Python interpreter has a number of functions and types built into it. Parameters: iterable."
    )
    assert obs_doc.page_type == PageType.DOCUMENTATION
    assert len(obs_doc.interactive_elements) >= 1

    # 3. E-Commerce
    obs_shop = UniversalPageInspector.inspect(
        url="https://store.example.com/books/python-crash-course",
        title="Python Crash Course Book",
        visible_text="Price: $29.99. In stock. Add to Cart. Proceed to Checkout."
    )
    assert obs_shop.page_type == PageType.E_COMMERCE
    checkout_btn = next((el for el in obs_shop.interactive_elements if "checkout" in el.element_id), None)
    assert checkout_btn is not None
    assert checkout_btn.is_consequential is True

    # 4. Barrier Detection (CAPTCHA)
    obs_captcha = UniversalPageInspector.inspect(
        url="https://protected.example.com/",
        title="Security Check",
        visible_text="Please solve the CAPTCHA to verify you are human."
    )
    assert "captcha" in obs_captcha.barriers


def test_action_planner_safety_and_reasoning():
    """Verify Wexa's own model reasoning and safety boundaries."""
    planner = WexaActionPlanner()

    # E-Commerce Checkout requires approval
    obs_shop = UniversalPageInspector.inspect(
        url="https://store.example.com/books/python-crash-course",
        title="Python Crash Course Book",
        visible_text="Price: $29.99. Add to Cart. Proceed to Checkout."
    )
    plan_checkout = planner.plan_next_action(obs_shop, user_goal="buy the book")
    assert plan_checkout.action_type == ActionType.CLICK
    assert plan_checkout.is_consequential is True
    assert plan_checkout.requires_approval is True

    # CAPTCHA requires user attention
    obs_captcha = UniversalPageInspector.inspect(
        url="https://protected.example.com/",
        visible_text="Please solve the CAPTCHA"
    )
    plan_captcha = planner.plan_next_action(obs_captcha)
    assert plan_captcha.action_type == ActionType.USER_ATTENTION
    assert plan_captcha.requires_approval is True


def test_action_executor_safety_enforcement():
    """Verify consequential actions cannot execute without explicit user approval."""
    executor = WexaActionExecutor()
    planner = WexaActionPlanner()

    obs_shop = UniversalPageInspector.inspect(
        url="https://store.example.com/books/python-crash-course",
        visible_text="Price: $29.99. Proceed to Checkout."
    )
    action = planner.plan_next_action(obs_shop, user_goal="checkout")

    # Attempt execution without approval -> BLOCKED
    res_blocked = executor.execute_and_verify(action, obs_shop, user_approved=False)
    assert res_blocked.success is False
    assert "requires explicit user permission" in res_blocked.message

    # Attempt execution with approval -> ALLOWED
    res_allowed = executor.execute_and_verify(action, obs_shop, user_approved=True)
    assert res_allowed.success is True
    assert res_allowed.verification_passed is True


def test_universal_action_loop_full_cycle():
    """Verify observe -> plan -> act -> verify loop."""
    loop = UniversalActionLoop()

    # 1. Observe
    obs = loop.step_inspect(
        url="https://leetcode.com/problems/valid-parentheses/",
        title="Valid Parentheses",
        visible_text="Given a string s containing '()[]{}', determine if valid.",
        starter_code="class Solution:\n    def isValid(self, s: str) -> bool:\n        pass"
    )
    assert obs.page_type == PageType.CODING_PRACTICE
    assert loop.phase == LoopPhase.PLAN

    # 2. Reason & Plan
    plan = loop.step_reason_and_plan(user_goal="Solve the parentheses problem")
    assert plan.action_type == ActionType.SOLVE_CODE
    assert plan.requires_approval is True
    assert loop.phase == LoopPhase.AWAIT_APPROVAL

    # 3. Act & Verify with Approval
    result = loop.step_execute_and_verify(user_approved=True)
    assert result.success is True
    assert result.verification_passed is True
    assert loop.phase == LoopPhase.COMPLETED
