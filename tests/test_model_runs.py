import pytest
from backend.agent.orchestrator import WexaAgentOrchestrator
from backend.schemas.task import PageAnalysisRequest


def test_model_run_1_two_sum():
    """Test 1: Model analysis, code synthesis, and verification for Two Sum."""
    orc = WexaAgentOrchestrator()
    req = PageAnalysisRequest(
        origin="https://leetcode.com/problems/two-sum/",
        page_title="Two Sum - LeetCode",
        visible_text="Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
        starter_code="class Solution:\n    def twoSum(self, nums: list[int], target: int) -> list[int]:\n        pass",
        language="python",
        editor_type="textarea"
    )
    analysis = orc.analyze_page(req)
    assert analysis["proposal_id"] is not None
    assert "twoSum" in analysis["proposed_code"]
    assert "diff_unified" in analysis

    approval = orc.handle_approval(proposal_id=analysis["proposal_id"], origin=req.origin, user_approved=True)
    assert approval["status"] == "APPROVED"

    test_harness = """sol = Solution()
assert sol.twoSum([2, 7, 11, 15], 9) == [0, 1]
assert sol.twoSum([3, 2, 4], 6) == [1, 2]
"""
    verif = orc.verify_and_test(actual_inserted_code=analysis["proposed_code"], test_harness_code=test_harness)
    assert verif["editor_verified"] is True
    assert verif["test_result"]["status"] == "PASS"
    assert verif["agent_state"] == "COMPLETED"


def test_model_run_2_valid_parentheses():
    """Test 2: Model analysis, code synthesis, and verification for Valid Parentheses."""
    orc = WexaAgentOrchestrator()
    req = PageAnalysisRequest(
        origin="https://leetcode.com/problems/valid-parentheses/",
        page_title="Valid Parentheses - LeetCode",
        visible_text="Given a string s containing just characters ()[]{}, determine if input string is valid.",
        starter_code="class Solution:\n    def isValid(self, s: str) -> bool:\n        pass",
        language="python",
        editor_type="textarea"
    )
    analysis = orc.analyze_page(req)
    assert analysis["proposal_id"] is not None
    assert "isValid" in analysis["proposed_code"]

    approval = orc.handle_approval(proposal_id=analysis["proposal_id"], origin=req.origin, user_approved=True)
    assert approval["status"] == "APPROVED"

    test_harness = """sol = Solution()
assert sol.isValid('()[]{}') is True
assert sol.isValid('(]') is False
"""
    verif = orc.verify_and_test(actual_inserted_code=analysis["proposed_code"], test_harness_code=test_harness)
    assert verif["editor_verified"] is True
    assert verif["test_result"]["status"] == "PASS"
    assert verif["agent_state"] == "COMPLETED"
