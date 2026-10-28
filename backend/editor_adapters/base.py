from typing import Protocol, Dict, Any, Optional

class EditorAdapter(Protocol):
    """
    Common protocol interface for all supported browser code editors.
    (Textarea, Monaco, CodeMirror, Ace).
    """
    def detect(self, element_metadata: Dict[str, Any]) -> bool:
        """Determines if this adapter handles the target element."""
        ...

    def read_content(self, element_id: str) -> str:
        """Reads current content from the editor."""
        ...

    def prepare_edit(self, current: str, proposal: str) -> Dict[str, Any]:
        """Prepares a unified diff or targeted patch."""
        ...

    def apply_approved_edit(self, edit_payload: Dict[str, Any]) -> bool:
        """Applies the approved change to the editor state."""
        ...

    def verify_edit(self, expected_content: str, element_id: str) -> bool:
        """Verifies that the editor's actual state matches the expectation."""
        ...
