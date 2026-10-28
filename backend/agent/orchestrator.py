import uuid
import hashlib
from typing import Dict, Any, Optional

from backend.schemas.task import PageAnalysisRequest
from backend.agent.state_machine import PermissionStateMachine, ApprovalContext, AgentState
from backend.page_parser.extractor import PageUnderstandingEngine
from backend.engine.inference import EmbeddedInferenceEngine
from backend.editor_adapters.textarea import TextareaAdapter
from backend.execution.runner import IsolatedTestRunner
from backend.data.telemetry_logger import AutomatedDatasetLogger
from backend.security.restriction_detector import WebsiteRestrictionDetector
from backend.security.offline_guard import OfflineSecurityGuard
from backend.security.injection_guard import PromptInjectionGuard
from backend.security.ast_safety import ASTCodeSafetyAnalyzer

class WexaAgentOrchestrator:
    """
    Central orchestrator coordinating page inspection, offline embedded inference,
    restriction evaluation, zero-leakage secret hiding, AST safety analysis,
    permission lifecycle, code insertion, testing, and telemetry.
    """
    def __init__(self):
        self.state_machine = PermissionStateMachine()
        self.engine = EmbeddedInferenceEngine()
        self.editor_adapter = TextareaAdapter()
        self.dataset_logger = AutomatedDatasetLogger()
        self.last_analysis: Optional[Dict[str, Any]] = None

    def analyze_page(self, request: PageAnalysisRequest) -> Dict[str, Any]:
        """
        Extracts task, verifies website restrictions, sanitizes prompt injections and API keys,
        and generates proposed solution.
        """
        self.state_machine.begin_analysis()
        
        # 1. API Key & Secret Hiding / Redaction (Guarantees zero-leakage)
        sanitized_text = OfflineSecurityGuard.sanitize_text(request.visible_text)
        sanitized_starter = OfflineSecurityGuard.sanitize_text(request.starter_code or "")

        # 2. Anti-Prompt Injection Defense
        is_clean_prompt, injection_msg = PromptInjectionGuard.inspect_untrusted_text(sanitized_text)
        if not is_clean_prompt:
            self.state_machine.mark_error()
            return {
                "error": "Security Alert: Indirect Prompt Injection detected in webpage.",
                "details": injection_msg,
                "state": AgentState.ERROR.value
            }
        sanitized_text = PromptInjectionGuard.sanitize_untrusted_input(sanitized_text)

        # 3. Evaluate Website Restrictions (anti-automation, CAPTCHA, read-only, etc.)
        restriction = WebsiteRestrictionDetector.evaluate_page(
            page_origin=request.origin,
            dom_metadata=request.dom_metadata,
            visible_text=sanitized_text
        )

        # 4. Extract Task Representation
        task = PageUnderstandingEngine.extract_task(
            visible_text=sanitized_text,
            starter_code=sanitized_starter,
            language_hint=request.language or "python"
        )
        task.restriction_evaluation = restriction

        # If automated editing is completely blocked (e.g. CAPTCHA or Anti-Automation policy)
        if not restriction.can_auto_edit and restriction.primary_restriction != "read_only_editor":
            self.last_analysis = {
                "proposal_id": None,
                "origin": request.origin,
                "task": task.model_dump(),
                "proposed_code": None,
                "diff_unified": None,
                "explanation": restriction.reason,
                "restriction": restriction.model_dump(),
                "state": AgentState.IDLE.value
            }
            return self.last_analysis

        # 5. Embedded Local Model Inference (runs offline)
        inference_out = self.engine.generate_code_patch(
            problem=task.problem_statement,
            starter_code=task.starter_code,
            language=task.language
        )
        proposed_code = inference_out["proposed_code"]
        
        # 6. Model Output AST Safety Check (Verify generated code has no harmful calls)
        if task.language.lower() == "python":
            is_code_safe, code_safety_reason = ASTCodeSafetyAnalyzer.analyze_python_code(proposed_code)
            if not is_code_safe:
                self.state_machine.mark_error()
                return {
                    "error": "Model Security Violation: Generated code contained prohibited operations.",
                    "details": code_safety_reason,
                    "state": AgentState.ERROR.value
                }

        # 7. Prepare Diff & Proposal
        edit_patch = self.editor_adapter.prepare_edit(
            current=task.starter_code,
            proposal=proposed_code
        )
        
        proposal_id = str(uuid.uuid4())
        context = ApprovalContext(
            proposal_id=proposal_id,
            origin=request.origin,
            target_editor=request.editor_type or "textarea",
            expected_original_hash=hashlib.sha256(task.starter_code.encode("utf-8")).hexdigest(),
            proposed_code=proposed_code
        )
        
        self.state_machine.set_proposal_ready(context)
        
        self.last_analysis = {
            "proposal_id": proposal_id,
            "origin": request.origin,
            "task": task.model_dump(),
            "proposed_code": proposed_code,
            "diff_unified": edit_patch["diff_unified"],
            "explanation": inference_out["explanation"],
            "restriction": restriction.model_dump(),
            "state": self.state_machine.current_state.value
        }
        
        return self.last_analysis

    def handle_approval(self, proposal_id: str, origin: str, user_approved: bool) -> Dict[str, Any]:
        """
        Validates user approval before any code can be applied.
        """
        if not user_approved:
            self.state_machine.user_cancelled()
            return {"status": "CANCELLED", "message": "User declined the proposed solution."}

        is_valid = self.state_machine.user_approved(proposal_id, current_page_origin=origin)
        if not is_valid:
            return {
                "status": "REJECTED",
                "message": "Approval failed: invalid proposal ID or origin mismatch."
            }

        return {
            "status": "APPROVED",
            "message": "Approval confirmed. Proceed with code insertion."
        }

    def verify_and_test(
        self,
        actual_inserted_code: str,
        test_harness_code: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Verifies actual editor state, runs isolated tests, and logs to the automated dataset.
        """
        if not self.last_analysis:
            return {"error": "No active task context to verify."}

        expected_code = self.last_analysis.get("proposed_code", "")
        verified = self.editor_adapter.verify_edit(
            expected_content=expected_code,
            actual_content=actual_inserted_code
        )
        
        test_result = {"status": "UNVERIFIED", "stdout": "", "stderr": "Tests not executed."}
        if verified:
            self.state_machine.mark_verified()
            # Run in isolated local environment with AST and timeout guards
            test_result = IsolatedTestRunner.run_python_code(
                code_string=actual_inserted_code,
                test_code=test_harness_code
            )
            self.state_machine.mark_completed()
        else:
            self.state_machine.mark_error()

        # AUTOMATED DATASET RECORDING: Log the complete interaction for training (sanitized)
        task_data = self.last_analysis["task"]
        self.dataset_logger.log_interaction(
            origin=self.last_analysis["origin"],
            language=task_data["language"],
            problem_statement=OfflineSecurityGuard.sanitize_text(task_data["problem_statement"]),
            starter_code=task_data["starter_code"],
            model_proposed_code=expected_code,
            user_final_code=actual_inserted_code,
            test_result_status=test_result.get("status", "UNVERIFIED"),
            test_stdout=test_result.get("stdout"),
            test_stderr=test_result.get("stderr"),
            compiler_error_corrected=False
        )

        return {
            "editor_verified": verified,
            "test_result": test_result,
            "agent_state": self.state_machine.current_state.value,
            "automated_dataset_updated": True
        }
