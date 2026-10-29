"""
Comprehensive Test Suite for Universal URL Support across Wexa Browser.
Verifies that ANY type of URL (Articles, Shopping, Docs, Coding, General Web, Naked Domains)
works end-to-end without errors.
"""

import os
import pytest
os.environ["WEXA_OFFLINE_MODE"] = "1"

from backend.page_parser.page_resolver import PageResolver
from backend.page_parser.universal_inspector import UniversalPageInspector
from backend.agent.action_planner import WexaActionPlanner
from backend.agent.action_executor import WexaActionExecutor
from backend.agent.action_loop import UniversalActionLoop
from backend.schemas.universal_action import PageType, ActionType, LoopPhase


def test_any_coding_practice_url():
    """Verify coding platforms and challenges."""
    urls = [
        "https://leetcode.com/problems/two-sum/",
        "https://leetcode.com/problems/climbing-stairs/",
        "https://www.hackerrank.com/challenges/arrays-ds/problem",
        "https://custom-coder.net/problems/sample-challenge",
        "https://custom-practice.org/challenges/fast-matrix-multiply"
    ]
    loop = UniversalActionLoop()
    for u in urls:
        res = PageResolver.resolve_url(u)
        assert res["id"] is not None
        assert res["url"] == u
        assert res["page_type"] == "coding_practice"
        assert "class Solution" in res["starterCode"]
        assert res["nextUrl"].startswith("http")

        obs = loop.step_inspect(url=res["url"], title=res["title"], visible_text=res["body"], starter_code=res["starterCode"])
        assert obs.page_type == PageType.CODING_PRACTICE
        assert obs.has_code_editor is True

        plan = loop.step_reason_and_plan()
        assert plan.action_type == ActionType.SOLVE_CODE
        assert plan.is_consequential is True


def test_any_documentation_url():
    """Verify technical documentation URLs."""
    urls = [
        "https://docs.python.org/3/library/json.html",
        "https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API",
        "https://fastapi.tiangolo.com/tutorial/",
        "https://react.dev/reference/react"
    ]
    loop = UniversalActionLoop()
    for u in urls:
        res = PageResolver.resolve_url(u)
        assert res["id"] is not None
        assert res["page_type"] == "documentation"
        assert "Doc" in res["title"]

        obs = loop.step_inspect(url=res["url"], title=res["title"], visible_text=res["body"], starter_code=res.get("starterCode"))
        assert obs.page_type == PageType.DOCUMENTATION

        plan = loop.step_reason_and_plan()
        assert plan.action_type in [ActionType.NAVIGATE, ActionType.TYPE]
        assert plan.is_consequential is False


def test_any_ecommerce_shopping_url():
    """Verify shopping & checkout safety guards."""
    urls = [
        "https://amazon.com/dp/B08N5WRWNW",
        "https://store.example.com/books/python-crash-course",
        "https://shop.merchandise.org/products/wexa-hoodie"
    ]
    loop = UniversalActionLoop()
    for u in urls:
        res = PageResolver.resolve_url(u)
        assert res["id"] is not None
        assert res["page_type"] == "e_commerce"

        obs = loop.step_inspect(url=res["url"], title=res["title"], visible_text=res["body"], starter_code=res.get("starterCode"))
        assert obs.page_type == PageType.E_COMMERCE

        # Default action: Add to cart
        plan_cart = loop.step_reason_and_plan()
        assert plan_cart.action_type == ActionType.CLICK

        # Consequential action: Checkout requires explicit user approval
        plan_checkout = loop.step_reason_and_plan(user_goal="checkout and place order")
        assert plan_checkout.action_type == ActionType.CLICK
        assert plan_checkout.is_consequential is True
        assert plan_checkout.requires_approval is True


def test_any_article_and_publication_url():
    """Verify news, blogs, Wikipedia, and knowledge publications."""
    urls = [
        "https://techcrunch.com/2026/01/15/ai-browser-agents",
        "https://news.ycombinator.com",
        "https://en.wikipedia.org/wiki/Binary_search_algorithm",
        "https://medium.com/@researcher/browser-agents"
    ]
    loop = UniversalActionLoop()
    for u in urls:
        res = PageResolver.resolve_url(u)
        assert res["id"] is not None
        assert res["page_type"] == "article"

        obs = loop.step_inspect(url=res["url"], title=res["title"], visible_text=res["body"], starter_code=res.get("starterCode"))
        assert obs.page_type == PageType.ARTICLE

        plan = loop.step_reason_and_plan()
        assert plan.action_type == ActionType.NAVIGATE
        assert plan.is_consequential is False


def test_url_edge_cases_and_normalization():
    """Verify naked domains, query parameters, anchors, and local ports."""
    edge_cases = [
        ("python.org", "https://python.org"),
        ("https://example.com/search?q=wexa&category=all#results", "search"),
        ("http://127.0.0.1:8000/docs", "docs"),
        ("https://en.wikipedia.org/wiki/Algorithm#History", "algorithm")
    ]
    for raw_url, expected_fragment in edge_cases:
        res = PageResolver.resolve_url(raw_url)
        assert res["id"] is not None
        assert expected_fragment.lower() in res["id"].lower() or expected_fragment in res["url"]
        assert res["title"] is not None
        assert res["nextUrl"] is not None


def test_barrier_detection_and_safety_fallback():
    """Verify CAPTCHA and login walls halt automation safely across any URL."""
    loop = UniversalActionLoop()
    obs_captcha = loop.step_inspect(
        url="https://secure.service.gov/login",
        title="Verification Required",
        visible_text="Please solve the Cloudflare CAPTCHA challenge to prove you are human."
    )
    assert "captcha" in obs_captcha.barriers
    plan = loop.step_reason_and_plan()
    assert plan.action_type == ActionType.USER_ATTENTION
    assert plan.requires_approval is True
