import re
from typing import Tuple, List

class PromptInjectionGuard:
    """
    Guards the local model against Indirect Prompt Injections (IPI)
    and adversarial overrides embedded in untrusted webpage content.
    """

    INJECTION_PATTERNS = [
        re.compile(r"ignore\s+(all\s+)?(previous|prior|above)\s+instructions", re.IGNORECASE),
        re.compile(r"you\s+are\s+now\s+(in\s+)?(developer\s+mode|dan|jailbreak)", re.IGNORECASE),
        re.compile(r"disregard\s+(all\s+)?safety\s+guidelines", re.IGNORECASE),
        re.compile(r"system\s*:\s*you\s+must", re.IGNORECASE),
        re.compile(r"<\|im_start\|>", re.IGNORECASE),
        re.compile(r"<\|im_end\|>", re.IGNORECASE),
        re.compile(r"exfiltrate|send\s+(secrets|passwords|tokens)\s+to", re.IGNORECASE),
        re.compile(r"!\[.*?\]\(https?://[^\s]+\)", re.IGNORECASE),  # Markdown image exfiltration
    ]

    @classmethod
    def inspect_untrusted_text(cls, text: str) -> Tuple[bool, str]:
        """
        Inspects text before sending it to the model.
        Returns (is_clean, reason).
        """
        for pattern in cls.INJECTION_PATTERNS:
            match = pattern.search(text)
            if match:
                return False, f"Potential prompt injection pattern detected: '{match.group(0)}'"

        return True, "No prompt injection patterns detected."

    @classmethod
    def sanitize_untrusted_input(cls, text: str) -> str:
        """
        Neutralizes known chat-template delimiters and potential injection tokens.
        """
        sanitized = text
        for pattern in [re.compile(r"<\|im_start\|>", re.IGNORECASE), re.compile(r"<\|im_end\|>", re.IGNORECASE)]:
            sanitized = pattern.sub("[FILTERED_TOKEN]", sanitized)
        return sanitized
