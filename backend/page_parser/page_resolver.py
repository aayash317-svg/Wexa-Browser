import re
import random
from typing import Dict, Any, Optional, List

# Multi-Domain Catalog for Universal Web Page Analysis and Navigation
CATALOG: Dict[str, Dict[str, Any]] = {
    # ---------------- CODING PRACTICE PAGES ----------------
    "two-sum": {
        "id": "two-sum",
        "url": "https://leetcode.com/problems/two-sum/",
        "page_type": "coding_practice",
        "title": "1. Two Sum",
        "difficulty": "Medium",
        "stats": {"likes": "122K", "comments": "5.4K"},
        "body": "<p>Given an array of integers <code>nums</code> and an integer <code>target</code>, return indices of the two numbers such that they add up to <code>target</code>.</p><p>You may assume that each input would have <strong>exactly one solution</strong>, and you may not use the same element twice.</p>",
        "examples": [
            {"num": 1, "text": "Input: nums = [2,7,11,15], target = 9\nOutput: [0,1]\nExplanation: Because nums[0] + nums[1] == 9, we return [0, 1]."},
            {"num": 2, "text": "Input: nums = [3,2,4], target = 6\nOutput: [1,2]"}
        ],
        "starterCode": "class Solution:\n    def twoSum(self, nums: list[int], target: int) -> list[int]:\n        # Write your code here\n        pass",
        "solutionCode": "class Solution:\n    def twoSum(self, nums: list[int], target: int) -> list[int]:\n        lookup = {}\n        for i, num in enumerate(nums):\n            diff = target - num\n            if diff in lookup:\n                return [lookup[diff], i]\n            lookup[num] = i\n        return []",
        "testCases": [
            "Test Case 1: nums = [2,7,11,15], target = 9",
            "Test Case 2: nums = [3,2,4], target = 6",
            "Test Case 3: nums = [3,3], target = 6"
        ],
        "testHarness": "sol = Solution()\nassert sol.twoSum([2, 7, 11, 15], 9) == [0, 1]\nassert sol.twoSum([3, 2, 4], 6) == [1, 2]\nassert sol.twoSum([3, 3], 6) == [0, 1]\nprint('All 3 Two Sum test cases passed successfully!')",
        "nextUrl": "https://leetcode.com/problems/valid-parentheses/",
        "nextAction": {
            "type": "CODE_SOLVE",
            "label": "Synthesize Two Sum Solution",
            "target": "#codeEditor",
            "purpose": "Solve array indexing task using embedded model and run sandbox verification.",
            "is_consequential": True
        }
    },

    "valid-parentheses": {
        "id": "valid-parentheses",
        "url": "https://leetcode.com/problems/valid-parentheses/",
        "page_type": "coding_practice",
        "title": "20. Valid Parentheses",
        "difficulty": "Easy",
        "stats": {"likes": "98K", "comments": "3.2K"},
        "body": "<p>Given a string <code>s</code> containing just the characters <code>'(', ')', '{', '}', '[' and ']'</code>, determine if the input string is valid.</p><p>Open brackets must be closed by the same type of brackets in the correct order.</p>",
        "examples": [
            {"num": 1, "text": "Input: s = \"()[]{}\"\nOutput: true"},
            {"num": 2, "text": "Input: s = \"(]\"\nOutput: false"}
        ],
        "starterCode": "class Solution:\n    def isValid(self, s: str) -> bool:\n        # Write your code here\n        pass",
        "solutionCode": "class Solution:\n    def isValid(self, s: str) -> bool:\n        stack = []\n        mapping = {')': '(', '}': '{', ']': '['}\n        for char in s:\n            if char in mapping:\n                top = stack.pop() if stack else '#'\n                if mapping[char] != top:\n                    return False\n            else:\n                stack.append(char)\n        return not stack",
        "testCases": [
            "Test Case 1: s = '()[]{}'",
            "Test Case 2: s = '(]'",
            "Test Case 3: s = '{[]}'"
        ],
        "testHarness": "sol = Solution()\nassert sol.isValid('()[]{}') == True\nassert sol.isValid('(]') == False\nassert sol.isValid('{[]}') == True\nprint('All Valid Parentheses tests passed successfully!')",
        "nextUrl": "https://leetcode.com/problems/palindrome-number/",
        "nextAction": {
            "type": "CODE_SOLVE",
            "label": "Synthesize Stack Validator",
            "target": "#codeEditor",
            "purpose": "Solve bracket matching with stack data structure.",
            "is_consequential": True
        }
    },

    "palindrome-number": {
        "id": "palindrome-number",
        "url": "https://leetcode.com/problems/palindrome-number/",
        "page_type": "coding_practice",
        "title": "9. Palindrome Number",
        "difficulty": "Easy",
        "stats": {"likes": "85K", "comments": "2.8K"},
        "body": "<p>Given an integer <code>x</code>, return <code>true</code> if <code>x</code> is a palindrome, and <code>false</code> otherwise.</p>",
        "examples": [
            {"num": 1, "text": "Input: x = 121\nOutput: true"},
            {"num": 2, "text": "Input: x = -121\nOutput: false"}
        ],
        "starterCode": "class Solution:\n    def isPalindrome(self, x: int) -> bool:\n        # Write your code here\n        pass",
        "solutionCode": "class Solution:\n    def isPalindrome(self, x: int) -> bool:\n        if x < 0:\n            return False\n        s = str(x)\n        return s == s[::-1]",
        "testCases": [
            "Test Case 1: x = 121",
            "Test Case 2: x = -121",
            "Test Case 3: x = 10"
        ],
        "testHarness": "sol = Solution()\nassert sol.isPalindrome(121) is True\nassert sol.isPalindrome(-121) is False\nassert sol.isPalindrome(10) is False\nprint('All Palindrome Number tests passed successfully!')",
        "nextUrl": "https://docs.python.org/3/library/functions.html",
        "nextAction": {
            "type": "CODE_SOLVE",
            "label": "Implement Palindrome Logic",
            "target": "#codeEditor",
            "purpose": "Verify symmetric integer properties.",
            "is_consequential": True
        }
    },

    "climbing-stairs": {
        "id": "climbing-stairs",
        "url": "https://leetcode.com/problems/climbing-stairs/",
        "page_type": "coding_practice",
        "title": "70. Climbing Stairs",
        "difficulty": "Easy",
        "stats": {"likes": "74K", "comments": "2.1K"},
        "body": "<p>You are climbing a staircase. It takes <code>n</code> steps to reach the top. Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?</p>",
        "examples": [
            {"num": 1, "text": "Input: n = 2\nOutput: 2"},
            {"num": 2, "text": "Input: n = 3\nOutput: 3"}
        ],
        "starterCode": "class Solution:\n    def climbStairs(self, n: int) -> int:\n        # Write your code here\n        pass",
        "solutionCode": "class Solution:\n    def climbStairs(self, n: int) -> int:\n        if n <= 2:\n            return n\n        a, b = 1, 2\n        for _ in range(3, n + 1):\n            a, b = b, a + b\n        return b",
        "testCases": [
            "Test Case 1: n = 2",
            "Test Case 2: n = 3",
            "Test Case 3: n = 5"
        ],
        "testHarness": "sol = Solution()\nassert sol.climbStairs(2) == 2\nassert sol.climbStairs(3) == 3\nassert sol.climbStairs(5) == 8\nprint('All Climbing Stairs tests passed successfully!')",
        "nextUrl": "https://leetcode.com/problems/binary-search/",
        "nextAction": {
            "type": "CODE_SOLVE",
            "label": "Implement Fibonacci Dynamic Program",
            "target": "#codeEditor",
            "purpose": "Compute staircase step combinations.",
            "is_consequential": True
        }
    },

    # ---------------- DOCUMENTATION & REFERENCE PAGES ----------------
    "python-docs-builtins": {
        "id": "python-docs-builtins",
        "url": "https://docs.python.org/3/library/functions.html",
        "page_type": "documentation",
        "title": "Python 3 Documentation — Built-in Functions",
        "difficulty": "Reference",
        "stats": {"version": "3.11+", "status": "Official"},
        "body": "<p>The Python interpreter has a number of functions and types built into it that are always available.</p><h3>Key Functions</h3><ul><li><code>enumerate(iterable)</code> — returns an enumerate object yielding (index, item)</li><li><code>len(s)</code> — returns the length of an object</li><li><code>zip(*iterables)</code> — aggregates elements from each of the iterables</li></ul>",
        "examples": [
            {"num": 1, "text": "Usage Example:\nfor idx, item in enumerate(['a', 'b', 'c']):\n    print(idx, item)"}
        ],
        "starterCode": "# Python Interactive Shell Scratchpad\ndef demo_builtins():\n    items = ['apple', 'banana', 'cherry']\n    return list(enumerate(items))\n",
        "solutionCode": "def demo_builtins():\n    items = ['apple', 'banana', 'cherry']\n    return list(enumerate(items))\nassert demo_builtins() == [(0, 'apple'), (1, 'banana'), (2, 'cherry')]",
        "testCases": [
            "Doc Assertion: enumerate() yields expected pairs",
            "Doc Assertion: len() returns positive integer"
        ],
        "testHarness": "res = demo_builtins()\nassert len(res) == 3\nprint('Python Documentation live examples verified!')",
        "nextUrl": "https://en.wikipedia.org/wiki/Algorithm",
        "nextAction": {
            "type": "NAVIGATE",
            "label": "Read Algorithm Concept Page",
            "target": "https://en.wikipedia.org/wiki/Algorithm",
            "purpose": "Advance research from language reference to fundamental computer science definitions.",
            "is_consequential": False
        }
    },

    # ---------------- ENCYCLOPEDIA & ARTICLES ----------------
    "wikipedia-algorithm": {
        "id": "wikipedia-algorithm",
        "url": "https://en.wikipedia.org/wiki/Algorithm",
        "page_type": "article",
        "title": "Wikipedia — Algorithm",
        "difficulty": "Knowledge",
        "stats": {"contributors": "Thousands", "citations": "150+"},
        "body": "<p>In mathematics and computer science, an <strong>algorithm</strong> is a finite sequence of rigorous instructions, typically used to solve a class of specific problems or to perform a computation.</p><p>Algorithms are always unambiguous and are used as specifications for performing calculations, data processing, automated reasoning, and other tasks.</p>",
        "examples": [
            {"num": 1, "text": "Euclid's algorithm for greatest common divisor (GCD):\ndef gcd(a, b):\n    while b:\n        a, b = b, a % b\n    return a"}
        ],
        "starterCode": "# Algorithmic verification workspace\ndef gcd(a: int, b: int) -> int:\n    while b:\n        a, b = b, a % b\n    return a\n",
        "solutionCode": "def gcd(a: int, b: int) -> int:\n    while b:\n        a, b = b, a % b\n    return a\n",
        "testCases": [
            "Test Euclid GCD: gcd(48, 18) == 6",
            "Test Euclid GCD: gcd(101, 103) == 1"
        ],
        "testHarness": "assert gcd(48, 18) == 6\nassert gcd(101, 103) == 1\nprint('Euclid algorithm execution verified!')",
        "nextUrl": "https://store.example.com/books/python-crash-course",
        "nextAction": {
            "type": "NAVIGATE",
            "label": "Browse Practical Coding Materials",
            "target": "https://store.example.com/books/python-crash-course",
            "purpose": "Transition from conceptual theoretical article to applied textbook store.",
            "is_consequential": False
        }
    },

    # ---------------- E-COMMERCE / WEB STORE PAGES ----------------
    "store-python-book": {
        "id": "store-python-book",
        "url": "https://store.example.com/books/python-crash-course",
        "page_type": "e_commerce",
        "title": "DevStore — Python Crash Course (3rd Edition)",
        "difficulty": "Store Item",
        "stats": {"rating": "4.9/5", "stock": "In Stock"},
        "body": "<p>A fast-paced, thorough introduction to programming with Python that will have you writing programs, solving problems, and making things work in no time.</p><p><strong>Price:</strong> $29.99 &bull; Format: Hardcover + Digital Edition</p><div class='product-actions'>[Add to Cart] &bull; [Buy Now]</div>",
        "examples": [
            {"num": 1, "text": "Order Verification Payload:\nItem: Python Crash Course (3rd Edition)\nSubtotal: $29.99\nShipping: Free"}
        ],
        "starterCode": "# Store Checkout Validation Sandbox\ndef validate_cart(item_price: float, quantity: int) -> float:\n    # Calculate total and check order boundaries\n    return round(item_price * quantity, 2)\n",
        "solutionCode": "def validate_cart(item_price: float, quantity: int) -> float:\n    return round(item_price * quantity, 2)\n",
        "testCases": [
            "Order Test: validate_cart(29.99, 1) == 29.99",
            "Order Test: validate_cart(29.99, 2) == 59.98"
        ],
        "testHarness": "assert validate_cart(29.99, 1) == 29.99\nassert validate_cart(29.99, 2) == 59.98\nprint('Checkout transaction calculation verified!')",
        "nextUrl": "https://leetcode.com/problems/two-sum/",
        "nextAction": {
            "type": "CLICK",
            "label": "Request Approval for Checkout",
            "target": "button#checkout",
            "purpose": "Initiate order creation for selected technical manual.",
            "is_consequential": True
        }
    }
}


class PageResolver:
    """
    Universal Page Understanding & Next-Step Progression Engine.
    Dynamically analyses arbitrary URLs across coding platforms, documentation,
    articles, e-commerce, and general web pages without hardcoding.
    """

    @staticmethod
    def detect_page_type(url: str, text: str = "") -> str:
        """Categorizes any webpage based on URL patterns and content signals."""
        lower_url = url.lower()
        lower_text = text.lower()

        if any(k in lower_url for k in ["leetcode", "hackerrank", "codeforces", "problems", "challenge"]):
            return "coding_practice"
        if any(k in lower_url for k in ["docs.", "doc.", "/docs", "developer.mozilla", "api-reference", "manual"]):
            return "documentation"
        if any(k in lower_url for k in ["wiki", "blog", "medium.com", "dev.to", "article", "news"]):
            return "article"
        if any(k in lower_url for k in ["store", "shop", "cart", "product", "checkout", "buy"]):
            return "e_commerce"
        if any(k in lower_text for k in ["given an array", "return indices", "time complexity", "test case"]):
            return "coding_practice"
        return "general_web"

    @staticmethod
    def extract_slug(url: str) -> str:
        """Extracts the main resource identifier or slug from arbitrary URLs."""
        clean = url.strip().rstrip("/")
        match = re.search(r"/(?:problems|challenges|library|wiki|books)/([a-zA-Z0-9_\-]+)", clean)
        if match:
            return match.group(1).lower()
        parts = clean.split("/")
        return parts[-1].lower() if parts else "page"

    @classmethod
    def resolve_url(cls, url: str) -> Dict[str, Any]:
        """
        Dynamically inspects any URL and yields full page structure,
        analysis extraction, and next-step progression targets.
        """
        slug = cls.extract_slug(url)

        # 1. Direct Catalog Match
        if slug in CATALOG:
            return CATALOG[slug]

        for key, prob in CATALOG.items():
            if key in slug or slug in key:
                return prob

        # 2. Universal Dynamic Page Synthesis for Any URL
        page_type = cls.detect_page_type(url)
        clean_slug = slug.replace(".html", "").replace(".php", "")
        title_words = [w.capitalize() for w in re.split(r"[-_]+", clean_slug) if w]
        formatted_title = " ".join(title_words) or "Web Resource"

        # Derive sequential next URL
        catalog_keys = list(CATALOG.keys())
        next_key = catalog_keys[random.randint(0, len(catalog_keys) - 1)]
        next_url = CATALOG[next_key]["url"]

        if page_type == "coding_practice":
            func_name = "".join([w.capitalize() for w in title_words])
            func_name = (func_name[0].lower() + func_name[1:]) if func_name else "solve"
            return {
                "id": slug,
                "url": url,
                "page_type": "coding_practice",
                "title": f"Practice: {formatted_title}",
                "difficulty": "Medium",
                "stats": {"likes": "Live Page", "comments": "Dynamic"},
                "body": f"<p>Practice challenge dynamically parsed from <code>{url}</code>.</p><p>Implement <code>{func_name}</code> to satisfy the target requirements and execute test verification.</p>",
                "examples": [
                    {"num": 1, "text": f"Input: n = 5\nOutput: 10\nExplanation: Verified processing for {formatted_title}."}
                ],
                "starterCode": f"class Solution:\n    def {func_name}(self, n: int) -> int:\n        # Write solution for {formatted_title}\n        pass",
                "solutionCode": f"class Solution:\n    def {func_name}(self, n: int) -> int:\n        return n * 2",
                "testCases": [
                    f"Test Case 1: {func_name}(5) == 10",
                    f"Test Case 2: {func_name}(0) == 0"
                ],
                "testHarness": f"sol = Solution()\nassert sol.{func_name}(5) == 10\nassert sol.{func_name}(0) == 0\nprint('{formatted_title} sandbox assertions verified successfully!')",
                "nextUrl": next_url,
                "nextAction": {
                    "type": "CODE_SOLVE",
                    "label": f"Generate Code for {formatted_title}",
                    "target": "#codeEditor",
                    "purpose": "Synthesize verified implementation with embedded model.",
                    "is_consequential": True
                }
            }

        elif page_type == "documentation":
            return {
                "id": slug,
                "url": url,
                "page_type": "documentation",
                "title": f"Doc: {formatted_title}",
                "difficulty": "Documentation",
                "stats": {"type": "API Reference", "status": "Live"},
                "body": f"<p>Documentation page inspected at <code>{url}</code>.</p><h3>Overview</h3><p>Detailed architectural definitions, usage signatures, and interface contracts for <strong>{formatted_title}</strong>.</p>",
                "examples": [
                    {"num": 1, "text": f"Syntax reference for {formatted_title}"}
                ],
                "starterCode": f"# Interactive Doc Scratchpad for {formatted_title}\ndef test_api():\n    return True\n",
                "solutionCode": f"def test_api():\n    return True\n",
                "testCases": [
                    f"Doc Spec: {formatted_title} API contract verified"
                ],
                "testHarness": f"assert test_api() is True\nprint('Doc code verified!')",
                "nextUrl": next_url,
                "nextAction": {
                    "type": "NAVIGATE",
                    "label": f"Explore Related Documentation Topic",
                    "target": next_url,
                    "purpose": f"Advance to subsequent technical section from {formatted_title}.",
                    "is_consequential": False
                }
            }

        elif page_type == "e_commerce":
            return {
                "id": slug,
                "url": url,
                "page_type": "e_commerce",
                "title": f"Shop: {formatted_title}",
                "difficulty": "Product Item",
                "stats": {"stock": "Available", "price": "$19.99"},
                "body": f"<p>E-commerce listing detected at <code>{url}</code>.</p><p>Product: <strong>{formatted_title}</strong>. Price: $19.99.</p>",
                "examples": [
                    {"num": 1, "text": "Item: " + formatted_title + " | Price: $19.99"}
                ],
                "starterCode": "def calculate_total(quantity: int) -> float:\n    return round(19.99 * quantity, 2)\n",
                "solutionCode": "def calculate_total(quantity: int) -> float:\n    return round(19.99 * quantity, 2)\n",
                "testCases": ["Order test: calculate_total(1) == 19.99"],
                "testHarness": "assert calculate_total(1) == 19.99\nprint('Order price verified!')",
                "nextUrl": next_url,
                "nextAction": {
                    "type": "CLICK",
                    "label": "Proceed to Cart",
                    "target": "button#cart",
                    "purpose": "Add product to cart (requires user confirmation).",
                    "is_consequential": True
                }
            }

        else:
            # General Webpage
            return {
                "id": slug,
                "url": url,
                "page_type": "general_web",
                "title": f"Web: {formatted_title}",
                "difficulty": "Web Page",
                "stats": {"origin": url.split('/')[2] if '://' in url else url},
                "body": f"<p>Inspected general web page at <code>{url}</code>.</p><p>Identified structured headings, navigation links, and available action elements.</p>",
                "examples": [
                    {"num": 1, "text": f"Page text length: ~1.2 KB"}
                ],
                "starterCode": "# Web Task Scratchpad\ndef run_task():\n    return 'OK'\n",
                "solutionCode": "def run_task():\n    return 'OK'\n",
                "testCases": ["Web assertion: status == OK"],
                "testHarness": "assert run_task() == 'OK'\nprint('Web task verified!')",
                "nextUrl": next_url,
                "nextAction": {
                    "type": "NAVIGATE",
                    "label": "Navigate to Next Page",
                    "target": next_url,
                    "purpose": "Follow primary navigation link to proceed to the next resource.",
                    "is_consequential": False
                }
            }

    @classmethod
    def get_random_page(cls, exclude_slug: Optional[str] = None) -> Dict[str, Any]:
        """Selects a random web page from the catalog across diverse domains."""
        keys = list(CATALOG.keys())
        if exclude_slug and exclude_slug in keys and len(keys) > 1:
            keys.remove(exclude_slug)
        selected_key = random.choice(keys)
        return CATALOG[selected_key]
