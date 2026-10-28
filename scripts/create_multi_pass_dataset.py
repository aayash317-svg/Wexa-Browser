"""
Wexa Browser — Multi-Pass Dataset Generator
Generates:
1. Pass 1: Core Function Infilling & Algorithm Synthesis
2. Pass 2: Compiler Error Recovery & Precision Edge Case Hardening
"""
import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "datasets"
DATA_DIR.mkdir(parents=True, exist_ok=True)

PASS1_DATA = [
    {
        "instruction": "Complete the missing implementation for Two Sum in Python. Return indices of the two numbers that add up to target.",
        "input": "class Solution:\n    def twoSum(self, nums: list[int], target: int) -> list[int]:\n        pass",
        "output": "class Solution:\n    def twoSum(self, nums: list[int], target: int) -> list[int]:\n        seen = {}\n        for i, n in enumerate(nums):\n            diff = target - n\n            if diff in seen:\n                return [seen[diff], i]\n            seen[n] = i\n        return []",
        "category": "algorithm"
    },
    {
        "instruction": "Implement Valid Parentheses in Python. Verify brackets match and close properly.",
        "input": "class Solution:\n    def isValid(self, s: str) -> bool:\n        pass",
        "output": "class Solution:\n    def isValid(self, s: str) -> bool:\n        stack = []\n        mapping = {')': '(', '}': '{', ']': '['}\n        for char in s:\n            if char in mapping:\n                top = stack.pop() if stack else '#'\n                if mapping[char] != top:\n                    return False\n            else:\n                stack.append(char)\n        return not stack",
        "category": "algorithm"
    },
    {
        "instruction": "Reverse a singly linked list in Python.",
        "input": "class Solution:\n    def reverseList(self, head):\n        pass",
        "output": "class Solution:\n    def reverseList(self, head):\n        prev = None\n        curr = head\n        while curr:\n            nxt = curr.next\n            curr.next = prev\n            prev = curr\n            curr = nxt\n        return prev",
        "category": "algorithm"
    },
    {
        "instruction": "Find maximum profit buying and selling stock once.",
        "input": "class Solution:\n    def maxProfit(self, prices: list[int]) -> int:\n        pass",
        "output": "class Solution:\n    def maxProfit(self, prices: list[int]) -> int:\n        min_price = float('inf')\n        max_profit = 0\n        for price in prices:\n            if price < min_price:\n                min_price = price\n            elif price - min_price > max_profit:\n                max_profit = price - min_price\n        return max_profit",
        "category": "algorithm"
    }
]

PASS2_ERROR_CORRECTION_DATA = [
    {
        "instruction": "Fix the IndexError in this Python twoSum implementation.",
        "input": "Broken Code:\nfor i in range(len(nums)):\n    if nums[i] + nums[i+1] == target: return [i, i+1]\nError: IndexError: list index out of range",
        "output": "Fix:\nseen = {}\nfor i, n in enumerate(nums):\n    diff = target - n\n    if diff in seen:\n        return [seen[diff], i]\n    seen[n] = i\nreturn []",
        "category": "error_recovery"
    },
    {
        "instruction": "Fix the empty stack error (IndexError: pop from empty list) in this bracket validator.",
        "input": "Broken Code:\nfor c in s:\n    if c in mapping:\n        if stack.pop() != mapping[c]: return False\nError: IndexError: pop from empty list on input ')'",
        "output": "Fix:\nfor c in s:\n    if c in mapping:\n        top = stack.pop() if stack else '#'\n        if mapping[c] != top: return False\n    else:\n        stack.append(c)\nreturn not stack",
        "category": "error_recovery"
    },
    {
        "instruction": "Fix NoneType attribute error in linked list traversal.",
        "input": "Broken Code:\nwhile curr.next:\n    curr = curr.next\nError: AttributeError: 'NoneType' object has no attribute 'next' on empty list",
        "output": "Fix:\nwhile curr:\n    nxt = curr.next\n    curr.next = prev\n    prev = curr\n    curr = nxt",
        "category": "error_recovery"
    }
]

def generate_multi_pass_datasets():
    pass1_path = DATA_DIR / "pass1_foundation_train.jsonl"
    pass2_path = DATA_DIR / "pass2_error_recovery_train.jsonl"

    with open(pass1_path, "w", encoding="utf-8") as f:
        for item in PASS1_DATA:
            f.write(json.dumps(item) + "\n")
    print(f"Generated Pass 1 dataset ({len(PASS1_DATA)} samples): {pass1_path}")

    with open(pass2_path, "w", encoding="utf-8") as f:
        # Pass 2 combines foundation + error recovery pairs for resilient retention
        for item in PASS1_DATA + PASS2_ERROR_CORRECTION_DATA:
            f.write(json.dumps(item) + "\n")
    print(f"Generated Pass 2 dataset ({len(PASS1_DATA) + len(PASS2_ERROR_CORRECTION_DATA)} samples): {pass2_path}")

if __name__ == "__main__":
    generate_multi_pass_datasets()
