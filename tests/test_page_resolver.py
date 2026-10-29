import pytest
from backend.page_parser.page_resolver import PageResolver, CATALOG


def test_resolve_known_url():
    prob = PageResolver.resolve_url("https://leetcode.com/problems/palindrome-number/")
    assert prob["id"] == "palindrome-number"
    assert "Palindrome" in prob["title"]
    assert "isPalindrome" in prob["starterCode"]
    assert "nextUrl" in prob


def test_resolve_different_url():
    prob = PageResolver.resolve_url("https://leetcode.com/problems/climbing-stairs/")
    assert prob["id"] == "climbing-stairs"
    assert "climbStairs" in prob["starterCode"]
    assert prob["nextUrl"] == "https://leetcode.com/problems/binary-search/"


def test_resolve_arbitrary_custom_url():
    prob = PageResolver.resolve_url("https://custom-practice.org/challenges/fast-matrix-multiply")
    assert "fast-matrix-multiply" in prob["id"]
    assert "Fast Matrix Multiply" in prob["title"]
    assert "class Solution" in prob["starterCode"]
    assert len(prob["testCases"]) >= 2
    assert "nextUrl" in prob


def test_get_random_page():
    p1 = PageResolver.get_random_page()
    assert p1["id"] in CATALOG
    assert "nextUrl" in p1

    p2 = PageResolver.get_random_page(exclude_slug=p1["id"])
    assert p2["id"] != p1["id"]
