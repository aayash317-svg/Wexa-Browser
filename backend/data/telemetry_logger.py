import json
import uuid
from pathlib import Path
from typing import Optional, Dict, Any, List
from backend.config import settings
from backend.schemas.feedback import InteractionFeedbackRecord

class AutomatedDatasetLogger:
    """
    Automatically captures user interactions, corrections, and test verification
    outcomes to compile high-quality fine-tuning datasets for Wexa Coder.
    """
    def __init__(self, log_path: Optional[Path] = None):
        self.log_path = log_path or settings.TELEMETRY_LOG_FILE
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def log_interaction(
        self,
        origin: str,
        language: str,
        problem_statement: str,
        starter_code: str,
        model_proposed_code: str,
        user_final_code: str,
        test_result_status: str,
        target_region: Optional[str] = None,
        test_stdout: Optional[str] = None,
        test_stderr: Optional[str] = None,
        compiler_error_corrected: bool = False,
        metadata: Optional[Dict[str, Any]] = None
    ) -> InteractionFeedbackRecord:
        """
        Appends an interaction record as a single JSON line.
        """
        record = InteractionFeedbackRecord(
            record_id=str(uuid.uuid4()),
            origin=origin,
            language=language,
            problem_statement=problem_statement,
            starter_code=starter_code,
            target_region=target_region,
            model_proposed_code=model_proposed_code,
            user_final_code=user_final_code,
            user_accepted_without_changes=(model_proposed_code.strip() == user_final_code.strip()),
            test_result_status=test_result_status,
            test_stdout=test_stdout,
            test_stderr=test_stderr,
            compiler_error_corrected=compiler_error_corrected,
            metadata=metadata or {}
        )

        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(record.model_dump_json() + "\n")

        return record

    def export_to_training_jsonl(self, output_path: Path, min_status: str = "PASS") -> int:
        """
        Filters verified passing solutions and converts them into
        standard instruction-tuning pairs for LoRA training.
        """
        if not self.log_path.exists():
            return 0

        exported_count = 0
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.log_path, "r", encoding="utf-8") as src, open(output_path, "w", encoding="utf-8") as dst:
            for line in src:
                if not line.strip():
                    continue
                data = json.loads(line)
                
                # Only train on verified code (or user approved code)
                if min_status == "PASS" and data.get("test_result_status") != "PASS":
                    continue

                train_sample = {
                    "instruction": (
                        f"Solve the following coding task in {data['language']}.\n"
                        f"Problem: {data['problem_statement']}\n\n"
                        f"Starter Code:\n{data['starter_code']}"
                    ),
                    "input": "",
                    "output": data["user_final_code"]
                }
                dst.write(json.dumps(train_sample) + "\n")
                exported_count += 1

        return exported_count

    def get_statistics(self) -> Dict[str, Any]:
        """Returns statistics on collected automated training data."""
        if not self.log_path.exists():
            return {"total_records": 0, "verified_passing": 0}

        total = 0
        passing = 0
        languages = {}

        with open(self.log_path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                total += 1
                item = json.loads(line)
                if item.get("test_result_status") == "PASS":
                    passing += 1
                lang = item.get("language", "unknown")
                languages[lang] = languages.get(lang, 0) + 1

        return {
            "total_records": total,
            "verified_passing": passing,
            "languages": languages
        }
