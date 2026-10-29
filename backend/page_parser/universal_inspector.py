import re
import urllib.parse
from typing import Dict, Any, List, Optional
from backend.schemas.universal_action import PageType, InteractiveElement, PageObservation


class UniversalPageInspector:
    """
    Step 2 in Wexa Architecture: Inspect the page.
    Reads visible text, headings, links, buttons, forms, and editor context
    across any website (documentation, shopping, articles, coding practice).
    """

    @classmethod
    def inspect(
        cls,
        url: str,
        title: str = "",
        visible_text: str = "",
        dom_elements: Optional[List[Dict[str, Any]]] = None,
        starter_code: Optional[str] = None
    ) -> PageObservation:
        parsed_url = urllib.parse.urlparse(url)
        domain = parsed_url.netloc or "local-environment"
        clean_text = visible_text.strip()
        lines = [line.strip() for line in clean_text.splitlines() if line.strip()]

        # 1. Extract Headings
        headings: List[str] = []
        for line in lines[:25]:
            if len(line) < 90 and (line.startswith("#") or re.match(r"^[0-9A-Z][A-Za-z0-9\s—:\-]{3,60}$", line)):
                headings.append(line.lstrip("# ").strip())
        if not headings and title:
            headings.append(title)

        # 2. Detect Page Type
        page_type = cls._classify_page_type(url, domain, clean_text, starter_code)

        # 3. Detect Barriers (CAPTCHA, Login, Paywall, Anti-Automation)
        barriers = cls._detect_barriers(clean_text)

        # 4. Extract or Generate Interactive Elements
        interactive_elements = cls._extract_interactive_elements(
            dom_elements=dom_elements,
            page_type=page_type,
            clean_text=clean_text,
            url=url
        )

        # 5. Check for Code Editor Presence
        has_editor = bool(starter_code or page_type == PageType.CODING_PRACTICE)

        # 6. Generate Summary
        summary = f"Page '{title or headings[0] if headings else domain}' on {domain}. Type: {page_type.value.upper()}. Found {len(interactive_elements)} interactive elements."
        if barriers:
            summary += f" Barriers detected: {', '.join(barriers)}."

        return PageObservation(
            url=url,
            title=title or (headings[0] if headings else domain),
            page_type=page_type,
            domain=domain,
            headings=headings[:6],
            interactive_elements=interactive_elements,
            has_code_editor=has_editor,
            starter_code=starter_code,
            barriers=barriers,
            visible_summary=summary,
            confidence=0.96 if dom_elements else 0.90
        )

    @classmethod
    def _classify_page_type(cls, url: str, domain: str, text: str, starter_code: Optional[str]) -> PageType:
        lower_url = url.lower()
        lower_text = text.lower()

        if starter_code or any(k in lower_url for k in ["leetcode", "hackerrank", "codeforces", "/problems/", "/challenges/"]):
            return PageType.CODING_PRACTICE
        if any(k in lower_text for k in ["given an array", "return indices", "time complexity", "class solution:"]):
            return PageType.CODING_PRACTICE

        if any(k in lower_url for k in ["docs.", "doc.", "/docs", "developer.mozilla", "api-reference", "manual"]):
            return PageType.DOCUMENTATION
        if any(k in lower_text for k in ["parameters:", "returns:", "api reference", "usage example", "installation"]):
            return PageType.DOCUMENTATION

        if any(k in lower_url for k in ["store", "shop", "cart", "product", "checkout", "amazon", "ebay", "item"]):
            return PageType.E_COMMERCE
        if any(k in lower_text for k in ["add to cart", "buy now", "in stock", "price:", "$", "shipping"]):
            return PageType.E_COMMERCE

        if any(k in lower_url for k in ["login", "signup", "register", "checkout/step", "form", "survey"]):
            return PageType.FORM_WORKFLOW

        if any(k in lower_url for k in ["wiki", "blog", "medium.com", "dev.to", "article", "news"]):
            return PageType.ARTICLE

        return PageType.GENERAL_WEB

    @classmethod
    def _detect_barriers(cls, text: str) -> List[str]:
        barriers = []
        lower = text.lower()
        if "captcha" in lower or "verify you are human" in lower or "cloudflare" in lower:
            barriers.append("captcha")
        if "please sign in" in lower or "login to continue" in lower or "account required" in lower:
            barriers.append("login_required")
        if "too many requests" in lower or "rate limit exceeded" in lower:
            barriers.append("rate_limit")
        return barriers

    @classmethod
    def _extract_interactive_elements(
        cls,
        dom_elements: Optional[List[Dict[str, Any]]],
        page_type: PageType,
        clean_text: str,
        url: str
    ) -> List[InteractiveElement]:
        results: List[InteractiveElement] = []

        if dom_elements:
            for idx, el in enumerate(dom_elements):
                tag = el.get("tag", "button").lower()
                text = el.get("text", "").strip()
                selector = el.get("selector", f"#{el.get('id', f'el-{idx}')}")
                is_conseq = bool(
                    el.get("is_consequential") or 
                    any(c in text.lower() for c in ["buy", "pay", "order", "submit", "delete", "remove", "checkout"])
                )
                results.append(InteractiveElement(
                    element_id=el.get("id", f"elem-{idx+1}"),
                    tag=tag,
                    role=el.get("role", tag),
                    text=text,
                    name=el.get("name"),
                    selector=selector,
                    input_type=el.get("type"),
                    value=el.get("value"),
                    is_consequential=is_conseq
                ))
            return results

        # Synthetic extraction based on observed page type when raw DOM is unavailable
        if page_type == PageType.CODING_PRACTICE:
            results.append(InteractiveElement(
                element_id="btn-run",
                tag="button",
                role="button",
                text="Run Tests",
                selector="#editorRunBtn",
                is_consequential=False
            ))
            results.append(InteractiveElement(
                element_id="editor-area",
                tag="textarea",
                role="textbox",
                text="Code Editor",
                selector="#codeEditor",
                is_consequential=True
            ))

        elif page_type == PageType.E_COMMERCE:
            results.append(InteractiveElement(
                element_id="btn-add-cart",
                tag="button",
                role="button",
                text="Add to Cart",
                selector="button.add-to-cart",
                is_consequential=False
            ))
            results.append(InteractiveElement(
                element_id="btn-checkout",
                tag="button",
                role="button",
                text="Proceed to Checkout",
                selector="button.checkout-btn",
                is_consequential=True
            ))
            results.append(InteractiveElement(
                element_id="input-qty",
                tag="input",
                role="spinbutton",
                text="Quantity",
                selector="input#quantity",
                input_type="number",
                value="1"
            ))

        elif page_type == PageType.DOCUMENTATION:
            results.append(InteractiveElement(
                element_id="link-next-section",
                tag="a",
                role="link",
                text="Next Chapter",
                selector="a.nav-next",
                is_consequential=False
            ))
            results.append(InteractiveElement(
                element_id="input-doc-search",
                tag="input",
                role="searchbox",
                text="Search Docs",
                selector="input#docSearch",
                input_type="text"
            ))

        elif page_type == PageType.ARTICLE:
            results.append(InteractiveElement(
                element_id="link-read-more",
                tag="a",
                role="link",
                text="Explore Related Topic",
                selector="a.related-article",
                is_consequential=False
            ))

        else:
            results.append(InteractiveElement(
                element_id="btn-action-primary",
                tag="button",
                role="button",
                text="Continue",
                selector="button.primary",
                is_consequential=False
            ))

        return results
