from typing import Dict, Any, Optional
from backend.schemas.universal_action import (
    PageObservation,
    ProposedAction,
    ActionResult,
    LoopPhase
)
from backend.page_parser.universal_inspector import UniversalPageInspector
from backend.agent.action_planner import WexaActionPlanner
from backend.agent.action_executor import WexaActionExecutor


class UniversalActionLoop:
    """
    Coordinates the 5-step universal agent workflow:
    1. Enter any URL
    2. Inspect page (text, links, buttons, forms, editor)
    3. Wexa's own model reasons (understand goal, choose next action)
    4. Show proposed action (explain next step, ask permission if consequential)
    5. Execute & verify (navigate, click, type, re-inspect page, error recovery)
    """

    def __init__(self):
        self.planner = WexaActionPlanner()
        self.executor = WexaActionExecutor()
        self.current_observation: Optional[PageObservation] = None
        self.active_proposal: Optional[ProposedAction] = None
        self.phase: LoopPhase = LoopPhase.OBSERVE

    def step_inspect(
        self,
        url: str,
        title: str = "",
        visible_text: str = "",
        dom_elements: Optional[list] = None,
        starter_code: Optional[str] = None
    ) -> PageObservation:
        self.phase = LoopPhase.OBSERVE
        obs = UniversalPageInspector.inspect(
            url=url,
            title=title,
            visible_text=visible_text,
            dom_elements=dom_elements,
            starter_code=starter_code
        )
        self.current_observation = obs
        self.phase = LoopPhase.PLAN
        return obs

    def step_reason_and_plan(self, user_goal: Optional[str] = None) -> ProposedAction:
        if not self.current_observation:
            raise ValueError("Cannot plan without prior page inspection. Call step_inspect first.")
        
        proposal = self.planner.plan_next_action(
            observation=self.current_observation,
            user_goal=user_goal
        )
        self.active_proposal = proposal
        self.phase = LoopPhase.AWAIT_APPROVAL if proposal.requires_approval else LoopPhase.ACT
        return proposal

    def step_execute_and_verify(self, user_approved: bool = False) -> ActionResult:
        if not self.active_proposal or not self.current_observation:
            raise ValueError("No active action proposal to execute.")

        result = self.executor.execute_and_verify(
            action=self.active_proposal,
            current_observation=self.current_observation,
            user_approved=user_approved
        )
        self.phase = result.next_recommended_phase
        return result
