import difflib
from typing import Dict, Any, Optional

class TextareaAdapter:
    """
    Standard HTML Textarea adapter for purpose-built practice environments.
    """
    def detect(self, element_metadata: Dict[str, Any]) -> bool:
        tag = element_metadata.get("tag_name", "").lower()
        return tag == "textarea" or element_metadata.get("is_textarea", False)

    def prepare_edit(self, current: str, proposal: str) -> Dict[str, Any]:
        """
        Generates a unified diff between current code and proposed code.
        """
        current_lines = current.splitlines(keepends=True)
        proposal_lines = proposal.splitlines(keepends=True)
        
        diff = difflib.unified_diff(
            current_lines,
            proposal_lines,
            fromfile="current_editor",
            tofile="proposed_solution",
            lineterm="\n"
        )
        unified_diff_str = "".join(diff)

        return {
            "original_code": current,
            "replacement_code": proposal,
            "diff_unified": unified_diff_str,
            "requires_full_replace": not bool(current.strip())
        }

    def verify_edit(self, expected_content: str, actual_content: str) -> bool:
        """
        Verifies that the content actually present in the editor matches expected code.
        """
        return actual_content.strip() == expected_content.strip()
