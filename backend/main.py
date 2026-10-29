from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
from pathlib import Path

from backend.config import settings
from backend.schemas.task import PageAnalysisRequest
from backend.agent.orchestrator import WexaAgentOrchestrator
from backend.page_parser.page_resolver import PageResolver
from backend.agent.action_loop import UniversalActionLoop
from backend.schemas.universal_action import ProposedAction, PageObservation

app = FastAPI(
    title=settings.APP_NAME,
    description="Local-first page-aware AI coding orchestrator with embedded inference and automated training telemetry.",
    version="0.1.0"
)

# Allow local Electron / webview requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = WexaAgentOrchestrator()
action_loop = UniversalActionLoop()


class ApprovalRequest(BaseModel):
    proposal_id: str
    origin: str
    user_approved: bool


class VerifyTestRequest(BaseModel):
    actual_editor_content: str
    test_harness_code: Optional[str] = None


class ResolvePageRequest(BaseModel):
    url: str


class NextStepAnalysisRequest(BaseModel):
    url: str
    visible_text: Optional[str] = ""
    user_goal: Optional[str] = None


class ActionLoopInspectRequest(BaseModel):
    url: str
    title: Optional[str] = ""
    visible_text: Optional[str] = ""
    dom_elements: Optional[list] = None
    starter_code: Optional[str] = None


class ActionLoopPlanRequest(BaseModel):
    url: str
    title: Optional[str] = ""
    visible_text: Optional[str] = ""
    dom_elements: Optional[list] = None
    starter_code: Optional[str] = None
    user_goal: Optional[str] = None


class ActionLoopExecuteRequest(BaseModel):
    action: Dict[str, Any]
    observation: Dict[str, Any]
    user_approved: bool = False


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "engine_ready": orchestrator.engine.is_ready,
        "model_file": str(orchestrator.engine.model_path),
        "agent_state": orchestrator.state_machine.current_state.value
    }


@app.post("/api/action-loop/inspect")
def action_loop_inspect(payload: ActionLoopInspectRequest):
    """
    Step 2: Inspect page and return comprehensive DOM & element observation.
    """
    return action_loop.step_inspect(
        url=payload.url,
        title=payload.title or "",
        visible_text=payload.visible_text or "",
        dom_elements=payload.dom_elements,
        starter_code=payload.starter_code
    )


@app.post("/api/action-loop/plan")
def action_loop_plan(payload: ActionLoopPlanRequest):
    """
    Step 3: Wexa's own model reasons on the page observation and proposes the next action.
    """
    action_loop.step_inspect(
        url=payload.url,
        title=payload.title or "",
        visible_text=payload.visible_text or "",
        dom_elements=payload.dom_elements,
        starter_code=payload.starter_code
    )
    return action_loop.step_reason_and_plan(user_goal=payload.user_goal)


@app.post("/api/action-loop/execute")
def action_loop_execute(payload: ActionLoopExecuteRequest):
    """
    Step 5: Execute proposed action and verify updated state.
    """
    act = ProposedAction(**payload.action)
    obs = PageObservation(**payload.observation)
    action_loop.current_observation = obs
    action_loop.active_proposal = act
    return action_loop.step_execute_and_verify(user_approved=payload.user_approved)


@app.post("/api/resolve-page")
def resolve_page(payload: ResolvePageRequest):
    """
    Dynamically resolves any URL into a structured practice problem page.
    """
    return PageResolver.resolve_url(payload.url)


@app.get("/api/random-page")
def get_random_page(exclude_id: Optional[str] = None):
    """
    Selects a random web practice page and automatically sets up progression.
    """
    return PageResolver.get_random_page(exclude_slug=exclude_id)


@app.post("/api/analyze-page-next-step")
def analyze_page_next_step(payload: NextStepAnalysisRequest):
    """
    Analyzes current page state, identifies page type and next-step actions,
    and returns next action reasoning and progression URLs.
    """
    resolved = PageResolver.resolve_url(payload.url)
    return {
        "url": payload.url,
        "page_type": resolved.get("page_type", "general_web"),
        "title": resolved.get("title", ""),
        "next_step": resolved.get("nextAction", {}),
        "next_url": resolved.get("nextUrl", ""),
        "user_goal": payload.user_goal or "Complete primary page workflow"
    }


@app.post("/api/analyze-page")
def analyze_page(request: PageAnalysisRequest):
    """
    Called by the browser side-panel when the user clicks 'Analyse Page'.
    """
    try:
        result = orchestrator.analyze_page(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/approve")
def handle_approval(payload: ApprovalRequest):
    """
    Submits user approval or cancellation for the active proposal.
    """
    result = orchestrator.handle_approval(
        proposal_id=payload.proposal_id,
        origin=payload.origin,
        user_approved=payload.user_approved
    )
    return result


@app.post("/api/verify-and-test")
def verify_and_test(payload: VerifyTestRequest):
    """
    Verifies actual editor state, runs isolated unit tests,
    and automatically records the sample for model training.
    """
    result = orchestrator.verify_and_test(
        actual_inserted_code=payload.actual_editor_content,
        test_harness_code=payload.test_harness_code
    )
    return result


@app.get("/api/datasets/stats")
def get_dataset_statistics():
    """
    Returns counts of automatically collected training samples.
    """
    return orchestrator.dataset_logger.get_statistics()


@app.get("/api/datasets/manifest")
def get_datasets_manifest():
    """
    Returns the manifest for all 10 installed training and benchmark datasets.
    """
    manifest_path = settings.DATASETS_DIR / "manifest.json"
    if manifest_path.exists():
        import json
        with open(manifest_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"total_datasets": 0, "datasets": []}


@app.post("/api/datasets/export")
def export_dataset(min_status: str = "PASS"):
    """
    Exports collected passing telemetry into an instruction-tuning JSONL file.
    """
    export_path = settings.DATASETS_DIR / "wexa_coder_finetune.jsonl"
    count = orchestrator.dataset_logger.export_to_training_jsonl(
        output_path=export_path,
        min_status=min_status
    )
    return {
        "exported_records": count,
        "export_path": str(export_path)
    }


from fastapi.staticfiles import StaticFiles

# Mount static frontend for browser UI
frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
if frontend_dir.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host=settings.HOST, port=settings.PORT, reload=True)
