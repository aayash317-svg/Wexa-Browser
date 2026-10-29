"""
FastAPI Router for Real Browser Control and Persistent Side Panel Integration.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

from backend.browser.playwright_manager import PlaywrightBrowserManager
from backend.agent.action_planner import WexaActionPlanner
from backend.schemas.universal_action import (
    PageObservation,
    ProposedAction,
    ActionResult
)

router = APIRouter(prefix="/api/browser", tags=["Browser Integration"])
browser_manager = PlaywrightBrowserManager()
action_planner = WexaActionPlanner()


class NavigateRequest(BaseModel):
    url: str
    tab_id: Optional[str] = None


class PlanActionRequest(BaseModel):
    user_goal: Optional[str] = None


class ExecuteActionRequest(BaseModel):
    action: ProposedAction
    user_approved: bool = False


class TabSwitchRequest(BaseModel):
    tab_id: str


@router.get("/status")
def get_browser_status():
    """Returns active browser state, open tabs, and current active tab."""
    tabs = browser_manager.list_tabs()
    active_tab = next((t for t in tabs if t.is_active), tabs[0] if tabs else None)
    return {
        "is_ready": browser_manager.is_ready,
        "active_tab_id": browser_manager.active_tab_id,
        "active_tab": active_tab,
        "tabs": tabs
    }


@router.post("/navigate")
def navigate_to_url(payload: NavigateRequest):
    """
    Navigates active tab to given URL, waits for network/DOM readiness,
    and returns full page observation.
    """
    observation = browser_manager.navigate(url=payload.url, tab_id=payload.tab_id)
    tabs = browser_manager.list_tabs()
    return {
        "status": "success",
        "observation": observation,
        "tabs": tabs
    }


@router.get("/observe")
def observe_active_tab():
    """Inspects the currently active tab and returns accessibility tree + elements."""
    observation = browser_manager.observe_active_page()
    screenshot = browser_manager.capture_screenshot()
    return {
        "observation": observation,
        "screenshot": screenshot
    }


@router.get("/screenshot")
def capture_screenshot():
    """Captures a live viewport screenshot of the active browser tab."""
    screenshot = browser_manager.capture_screenshot()
    if not screenshot:
        raise HTTPException(status_code=404, detail="Screenshot capture not available.")
    return {"screenshot": screenshot}


@router.post("/plan")
def plan_next_action(payload: PlanActionRequest):
    """
    Wexa's own model reasons over the current page observation and user goal
    to propose the next structured action plan.
    """
    obs = browser_manager.observe_active_page()
    proposed = action_planner.plan_next_action(observation=obs, user_goal=payload.user_goal)
    return {
        "observation": obs,
        "proposed_action": proposed
    }


@router.post("/action")
def execute_browser_action(payload: ExecuteActionRequest):
    """
    Executes a controlled browser action (navigate, click, type) and verifies post-state.
    Enforces user approval for consequential actions.
    """
    result = browser_manager.execute_browser_action(
        action=payload.action,
        user_approved=payload.user_approved
    )
    updated_obs = browser_manager.observe_active_page()
    return {
        "result": result,
        "updated_observation": updated_obs
    }


@router.post("/tabs/new")
def open_new_tab(payload: Optional[NavigateRequest] = None):
    """Opens a new browser tab."""
    target_url = payload.url if payload else "about:blank"
    tab_id = browser_manager.new_tab(url=target_url)
    return {
        "tab_id": tab_id,
        "tabs": browser_manager.list_tabs()
    }


@router.post("/tabs/switch")
def switch_active_tab(payload: TabSwitchRequest):
    """Switches the active browser tab."""
    success = browser_manager.switch_tab(payload.tab_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tab ID not found.")
    return {
        "status": "success",
        "active_tab_id": payload.tab_id,
        "observation": browser_manager.observe_active_page()
    }


@router.post("/tabs/close")
def close_tab(payload: TabSwitchRequest):
    """Closes a specific tab."""
    browser_manager.close_tab(payload.tab_id)
    return {
        "status": "success",
        "tabs": browser_manager.list_tabs()
    }

