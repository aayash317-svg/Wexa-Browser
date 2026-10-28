import re
from typing import Dict, Any

class OfflineSecurityGuard:
    """
    Guarantees privacy-preserving offline operation.
    Sanitizes data to prevent saving tokens, cookies, or secrets into local telemetry.
    """
    
    SECRET_PATTERNS = [
        re.compile(r"bearer\s+[a-zA-Z0-9_\-\.]{15,}", re.IGNORECASE),
        re.compile(r"api[_\-]?key\s*[:=]\s*['\"][a-zA-Z0-9_\-]{16,}['\"]", re.IGNORECASE),
        re.compile(r"password\s*[:=]\s*['\"][^'\"]+['\"]", re.IGNORECASE),
        re.compile(r"cookie\s*[:=]\s*['\"][^'\"]+['\"]", re.IGNORECASE),
    ]

    @classmethod
    def sanitize_text(cls, text: str) -> str:
        """
        Redacts any accidental auth tokens, passwords, or cookies from task text.
        """
        sanitized = text
        for pattern in cls.SECRET_PATTERNS:
            sanitized = pattern.sub("[REDACTED_SECRET]", sanitized)
        return sanitized

    @classmethod
    def sanitize_metadata(cls, meta: Dict[str, Any]) -> Dict[str, Any]:
        """
        Strips cookie or auth headers from metadata before logging.
        """
        safe_meta = {}
        for k, v in meta.items():
            if any(forbidden in k.lower() for forbidden in ["auth", "token", "cookie", "password", "session"]):
                continue
            if isinstance(v, str):
                safe_meta[k] = cls.sanitize_text(v)
            else:
                safe_meta[k] = v
        return safe_meta
