import re
from typing import Dict, Any, List
from backend.schemas.task import PageTaskExtraction, TaskType, TargetRegion

class PageUnderstandingEngine:
    """
    Parses unstructured visible page text and starter code into structured
    tasks, identifying whether the editor is empty, has a TODO, or has an incomplete method.
    """

    @staticmethod
    def extract_task(
        visible_text: str,
        starter_code: str = "",
        language_hint: str = "python"
    ) -> PageTaskExtraction:
        lines = visible_text.splitlines()
        clean_text = "\n".join([line.strip() for line in lines if line.strip()])

        # 1. Determine Task Type
        starter = starter_code.strip()
        task_type = TaskType.EMPTY_EDITOR
        target = TargetRegion(kind="entire_file")

        if not starter:
            task_type = TaskType.EMPTY_EDITOR
        elif "TODO" in starter or "FIXME" in starter or "pass" in starter or "..." in starter:
            task_type = TaskType.STARTER_CODE_TODO
            target = TargetRegion(kind="function_body", name="placeholder_region")
        elif "def " in starter or "public " in starter or "function " in starter:
            task_type = TaskType.INCOMPLETE_METHOD
            target = TargetRegion(kind="function_body")
        else:
            task_type = TaskType.EXISTING_CODE_ERROR

        # 2. Extract Constraints & Examples if present in visible text
        constraints: List[str] = []
        for line in lines:
            if re.search(r"(constraint|note|time limit|memory limit)", line, re.IGNORECASE):
                constraints.append(line.strip())

        # 3. Detect Language
        detected_language = language_hint
        if "def " in starter:
            detected_language = "python"
        elif "public class " in starter or "System.out" in starter:
            detected_language = "java"
        elif "function " in starter or "console.log" in starter:
            detected_language = "javascript"
        elif "#include" in starter:
            detected_language = "cpp"

        return PageTaskExtraction(
            task_type=task_type,
            language=detected_language,
            problem_statement=clean_text[:1000],  # bounded to prevent overflow
            constraints=constraints[:5],
            starter_code=starter,
            target=target,
            analysis_confidence=0.92
        )
