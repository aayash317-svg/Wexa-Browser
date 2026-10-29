import pytest
from backend.page_parser.page_resolver import PageResolver
from backend.agent.orchestrator import WexaAgentOrchestrator
from backend.schemas.task import PageAnalysisRequest


def test_dynamic_url_resolution_and_progression():
    """Verify that different URLs can be resolved dynamically with nextUrl progression."""
    urls = [
        "https://leetcode.com/problems/palindrome-number/",
        "https://leetcode.com/problems/climbing-stairs/",
        "https://leetcode.com/problems/binary-search/",
        "https://leetcode.com/problems/maximum-subarray/",
        "https://custom-coder.net/problems/sample-challenge"
    ]

    for url in urls:
        page = PageResolver.resolve_url(url)
        assert page["id"] is not None
        assert page["title"] is not None
        assert "class Solution" in page["starterCode"]
        assert len(page["testCases"]) >= 2
        assert page["nextUrl"] is not None
        assert page["nextUrl"].startswith("http")


def test_random_page_flow():
    """Verify random page generation returns diverse problems."""
    p1 = PageResolver.get_random_page()
    assert p1["id"] is not None
    assert p1["nextUrl"] is not None

    p2 = PageResolver.get_random_page(exclude_slug=p1["id"])
    assert p2["id"] != p1["id"]
    assert p2["nextUrl"] is not None


def test_different_pages_model_and_test_execution():
    """Verify end-to-end model analysis, execution, and progression on a different URL."""
    orc = WexaAgentOrchestrator()
    page = PageResolver.resolve_url("https://leetcode.com/problems/palindrome-number/")

    req = PageAnalysisRequest(
        origin=page["url"],
        page_title=page["title"],
        visible_text=page["body"],
        starter_code=page["starterCode"],
        language="python",
        editor_type="textarea"
    )

    analysis = orc.analyze_page(req)
    assert analysis["proposal_id"] is not None
    assert "isPalindrome" in analysis["proposed_code"]

    approval = orc.handle_approval(proposal_id=analysis["proposal_id"], origin=page["url"], user_approved=True)
    assert approval["status"] == "APPROVED"

    verif = orc.verify_and_test(actual_inserted_code=analysis["proposed_code"], test_harness_code=page["testHarness"])
    assert verif["editor_verified"] is True
    assert verif["test_result"]["status"] == "PASS"

    # Progression: advance to next page
    next_url = page["nextUrl"]
    assert next_url is not None
    next_page = PageResolver.resolve_url(next_url)
    assert next_page["id"] is not None
    assert next_page["id"] != page["id"]
