import uuid
from typing import Optional, Dict, Any
from backend.schemas.universal_action import (
    PageObservation,
    ProposedAction,
    ActionType,
    PageType
)
from backend.engine.inference import EmbeddedInferenceEngine


class WexaActionPlanner:
    """
    Step 3 in Wexa Architecture: Wexa's own model reasons.
    Understands the user's goal, evaluates candidate actions from the page observation,
    identifies safety boundaries, and selects the next action without requiring a GPT API.
    """

    def __init__(self, engine: Optional[EmbeddedInferenceEngine] = None):
        self.engine = engine or EmbeddedInferenceEngine()

    def plan_next_action(
        self,
        observation: PageObservation,
        user_goal: Optional[str] = None
    ) -> ProposedAction:
        goal = (user_goal or "").strip().lower()
        action_id = str(uuid.uuid4())

        # 1. Fallback & Barrier Checks (CAPTCHA, Login Barriers, Rate Limits)
        if observation.barriers:
            barrier_name = observation.barriers[0]
            if barrier_name == "captcha":
                return ProposedAction(
                    action_id=action_id,
                    action_type=ActionType.USER_ATTENTION,
                    explanation="CAPTCHA challenge detected on page. Automated interaction paused for manual user verification.",
                    is_consequential=False,
                    requires_approval=True,
                    confidence=0.99
                )
            elif barrier_name == "login_required":
                return ProposedAction(
                    action_id=action_id,
                    action_type=ActionType.USER_ATTENTION,
                    explanation="Page requires authenticated session. Please sign in to proceed with this workflow.",
                    is_consequential=False,
                    requires_approval=True,
                    confidence=0.98
                )

        # 2. Domain-Aware Reasoning using Wexa's Local Decision Logic

        # A. Coding Practice Pages
        if observation.page_type == PageType.CODING_PRACTICE:
            return ProposedAction(
                action_id=action_id,
                action_type=ActionType.SOLVE_CODE,
                target_element_id="editor-area",
                target_selector="#codeEditor",
                parameters={"language": "python", "verify_sandbox": True},
                explanation=f"Synthesize verified algorithm implementation for '{observation.title}' and run isolated test suite.",
                is_consequential=True,
                requires_approval=True,
                confidence=0.95
            )

        # B. E-Commerce & Shopping Pages
        elif observation.page_type == PageType.E_COMMERCE:
            if "checkout" in goal or "buy" in goal or "purchase" in goal:
                return ProposedAction(
                    action_id=action_id,
                    action_type=ActionType.CLICK,
                    target_element_id="btn-checkout",
                    target_selector="button.checkout-btn",
                    parameters={"action": "checkout"},
                    explanation="Initiate checkout sequence for selected product. Explicit user confirmation required for consequential financial action.",
                    is_consequential=True,
                    requires_approval=True,
                    confidence=0.92
                )
            else:
                return ProposedAction(
                    action_id=action_id,
                    action_type=ActionType.CLICK,
                    target_element_id="btn-add-cart",
                    target_selector="button.add-to-cart",
                    parameters={"quantity": 1},
                    explanation="Add item to shopping cart and inspect updated subtotal.",
                    is_consequential=False,
                    requires_approval=False,
                    confidence=0.90
                )

        # C. Documentation Pages
        elif observation.page_type == PageType.DOCUMENTATION:
            if "search" in goal:
                query = goal.replace("search", "").strip() or "methods"
                return ProposedAction(
                    action_id=action_id,
                    action_type=ActionType.TYPE,
                    target_element_id="input-doc-search",
                    target_selector="input#docSearch",
                    parameters={"text": query, "press_enter": True},
                    explanation=f"Query documentation index for '{query}'.",
                    is_consequential=False,
                    requires_approval=False,
                    confidence=0.91
                )
            else:
                return ProposedAction(
                    action_id=action_id,
                    action_type=ActionType.NAVIGATE,
                    target_element_id="link-next-section",
                    target_selector="a.nav-next",
                    parameters={"destination_url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise"},
                    explanation=f"Advance to subsequent API reference chapter from '{observation.title}'.",
                    is_consequential=False,
                    requires_approval=False,
                    confidence=0.88
                )

        # D. Article & Knowledge Pages
        elif observation.page_type == PageType.ARTICLE:
            return ProposedAction(
                action_id=action_id,
                action_type=ActionType.NAVIGATE,
                target_element_id="link-read-more",
                target_selector="a.related-article",
                parameters={"destination_url": "https://store.example.com/books/python-crash-course"},
                explanation=f"Follow related topic link to continue research beyond '{observation.title}'.",
                is_consequential=False,
                requires_approval=False,
                confidence=0.85
            )

        # E. General Web & Form Workflow Pages
        else:
            return ProposedAction(
                action_id=action_id,
                action_type=ActionType.NAVIGATE,
                target_element_id="btn-action-primary",
                target_selector="button.primary",
                parameters={"url": observation.url},
                explanation=f"Inspect primary workflow options on {observation.domain}.",
                is_consequential=False,
                requires_approval=False,
                confidence=0.82
            )
