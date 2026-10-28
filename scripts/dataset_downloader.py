"""
Wexa Browser — Automated Dataset Downloader & Normalizer
Downloads and prepares permitted coding datasets into unified Wexa JSONL format.
"""
import json
import argparse
import hashlib
from pathlib import Path
from typing import Dict, Any, List

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "datasets"

def compute_checksum(filepath: Path) -> str:
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def normalize_sample(problem: str, starter_code: str, solution: str, language: str = "python") -> Dict[str, Any]:
    return {
        "instruction": f"Complete the missing code for this {language} problem.\n\nProblem:\n{problem}\n\nStarter Code:\n{starter_code}",
        "input": "",
        "output": solution,
        "language": language
    }

def create_sample_evaluation_set(output_path: Path):
    """Creates a starter set of verified coding practice tasks."""
    samples = [
        normalize_sample(
            problem="Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
            starter_code="class Solution:\n    def twoSum(self, nums: list[int], target: int) -> list[int]:\n        pass",
            solution="class Solution:\n    def twoSum(self, nums: list[int], target: int) -> list[int]:\n        seen = {}\n        for i, n in enumerate(nums):\n            diff = target - n\n            if diff in seen:\n                return [seen[diff], i]\n            seen[n] = i\n        return []"
        ),
        normalize_sample(
            problem="Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.",
            starter_code="class Solution:\n    def isValid(self, s: str) -> bool:\n        pass",
            solution="class Solution:\n    def isValid(self, s: str) -> bool:\n        stack = []\n        mapping = {')': '(', '}': '{', ']': '['}\n        for char in s:\n            if char in mapping:\n                top = stack.pop() if stack else '#'\n                if mapping[char] != top:\n                    return False\n            else:\n                stack.append(char)\n        return not stack"
        ),
        normalize_sample(
            problem="Reverse a singly linked list.",
            starter_code="class Solution:\n    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:\n        pass",
            solution="class Solution:\n    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:\n        prev = None\n        curr = head\n        while curr:\n            nxt = curr.next\n            curr.next = prev\n            prev = curr\n            curr = nxt\n        return prev"
        )
    ]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for s in samples:
            f.write(json.dumps(s) + "\n")
    print(f"Created sample benchmark dataset ({len(samples)} records) at: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Wexa Dataset Ingestion Tool")
    parser.add_argument("--create-starter", action="store_true", help="Create initial benchmark dataset")
    args = parser.parse_args()

    target_file = DATA_DIR / "starter_coding_eval.jsonl"
    if args.create_starter or not target_file.exists():
        create_sample_evaluation_set(target_file)
