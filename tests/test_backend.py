import pytest
from backend.agent.state_machine import PermissionStateMachine, ApprovalContext, AgentState
from backend.page_parser.extractor import PageUnderstandingEngine
from backend.schemas.task import TaskType
from backend.execution.runner import IsolatedTestRunner
from backend.data.telemetry_logger import AutomatedDatasetLogger
from pathlib import Path
import tempfile


def test_permission_state_machine():
    sm = PermissionStateMachine()
    assert sm.current_state == AgentState.IDLE

    sm.begin_analysis()
    assert sm.current_state == AgentState.ANALYSING

    ctx = ApprovalContext(
        proposal_id="prop-123",
        origin="https://practice.example",
        target_editor="textarea",
        expected_original_hash="abc",
        proposed_code="return a + b"
    )
    sm.set_proposal_ready(ctx)
    assert sm.current_state == AgentState.WAITING_FOR_APPROVAL

    # Invalidate if origin doesn't match
    assert not sm.user_approved("prop-123", "https://different-site.example")
    assert sm.current_state == AgentState.ERROR

    # Valid approval flow
    sm.set_proposal_ready(ctx)
    assert sm.user_approved("prop-123", "https://practice.example")
    assert sm.current_state == AgentState.APPROVED


def test_page_understanding_extractor():
    visible_text = "Problem Statement: Write a function that returns the square of n.\nConstraints: n >= 0"
    starter = "def square(n):\n    # TODO: write code\n    pass"

    task = PageUnderstandingEngine.extract_task(visible_text, starter, "python")
    assert task.task_type == TaskType.STARTER_CODE_TODO
    assert task.language == "python"
    assert "square" in task.problem_statement


def test_isolated_test_runner():
    good_code = "def add(a, b): return a + b\nassert add(2, 3) == 5"
    res = IsolatedTestRunner.run_python_code(good_code)
    assert res["status"] == "PASS"

    bad_code = "assert 1 == 2"
    res_bad = IsolatedTestRunner.run_python_code(bad_code)
    assert res_bad["status"] == "FAIL"


def test_automated_dataset_logger():
    with tempfile.TemporaryDirectory() as tmp_dir:
        log_file = Path(tmp_dir) / "test_interactions.jsonl"
        logger = AutomatedDatasetLogger(log_path=log_file)

        logger.log_interaction(
            origin="https://practice.test",
            language="python",
            problem_statement="Return doubled number",
            starter_code="def double(x): pass",
            model_proposed_code="def double(x): return x * 2",
            user_final_code="def double(x): return x * 2",
            test_result_status="PASS"
        )

        stats = logger.get_statistics()
        assert stats["total_records"] == 1
        assert stats["verified_passing"] == 1

        export_file = Path(tmp_dir) / "export_train.jsonl"
        count = logger.export_to_training_jsonl(export_file, min_status="PASS")
        assert count == 1
