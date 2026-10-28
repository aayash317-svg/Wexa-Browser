import subprocess
import tempfile
import sys
from pathlib import Path
from typing import Dict, Any, Optional
from backend.config import settings
from backend.security.ast_safety import ASTCodeSafetyAnalyzer

class IsolatedTestRunner:
    """
    Executes generated code in an isolated temporary process with strict
    AST safety validation, timeouts, output caps, and explicit status reporting.
    """

    @staticmethod
    def run_python_code(code_string: str, test_code: Optional[str] = None) -> Dict[str, Any]:
        """
        Executes Python code in a safe temporary environment after passing AST checks.
        """
        full_code = code_string
        if test_code:
            full_code = f"{code_string}\n\n# --- Test Execution Harness ---\n{test_code}"

        # 1. Static AST Safety Analysis (Blocks malicious code before execution)
        is_safe, safety_msg = ASTCodeSafetyAnalyzer.analyze_python_code(full_code)
        if not is_safe:
            return {
                "status": "BLOCKED",
                "returncode": -1,
                "stdout": "",
                "stderr": f"Security Violation: {safety_msg}",
                "execution_time_sec": 0
            }

        # 2. Isolated Subprocess Sandbox with strict timeout
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = Path(temp_dir) / "solution_run.py"
            temp_file.write_text(full_code, encoding="utf-8")

            try:
                proc = subprocess.run(
                    [sys.executable, str(temp_file)],
                    capture_output=True,
                    text=True,
                    timeout=settings.EXECUTION_TIMEOUT_SECONDS,
                    cwd=temp_dir
                )

                stdout = proc.stdout[:2000] if proc.stdout else ""
                stderr = proc.stderr[:2000] if proc.stderr else ""

                if proc.returncode == 0:
                    status = "PASS"
                else:
                    status = "FAIL"

                return {
                    "status": status,
                    "returncode": proc.returncode,
                    "stdout": stdout,
                    "stderr": stderr,
                    "execution_time_sec": None
                }

            except subprocess.TimeoutExpired:
                return {
                    "status": "FAIL",
                    "returncode": -1,
                    "stdout": "",
                    "stderr": f"Execution timed out after {settings.EXECUTION_TIMEOUT_SECONDS}s.",
                    "execution_time_sec": settings.EXECUTION_TIMEOUT_SECONDS
                }
            except Exception as e:
                return {
                    "status": "UNVERIFIED",
                    "returncode": -1,
                    "stdout": "",
                    "stderr": f"Sandbox runner error: {str(e)}",
                    "execution_time_sec": None
                }
