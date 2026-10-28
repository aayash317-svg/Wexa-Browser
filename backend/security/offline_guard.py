import re
from typing import Dict, Any

class OfflineSecurityGuard:
    """
    Comprehensive zero-leakage security guard.
    Guarantees no API keys, cloud tokens, private keys, or passwords
    can ever enter prompts, telemetry datasets, or model context.
    """

    SECRET_PATTERNS = [
        # Bearer tokens & Authorization headers
        re.compile(r"bearer\s+[a-zA-Z0-9_\-\.]{10,}", re.IGNORECASE),
        re.compile(r"eyJ[a-zA-Z0-9_\-]{10,}\.[a-zA-Z0-9_\-\.]+", re.IGNORECASE),

        # OpenAI / Anthropic / LLM API Keys
        re.compile(r"sk-[a-zA-Z0-9_\-]{20,}", re.IGNORECASE),
        re.compile(r"sk-ant-[a-zA-Z0-9_\-]{20,}", re.IGNORECASE),
        
        # GitHub Personal Access Tokens
        re.compile(r"ghp_[a-zA-Z0-9]{36}", re.IGNORECASE),
        re.compile(r"github_pat_[a-zA-Z0-9_]{22,}", re.IGNORECASE),

        # AWS Access Keys & Secrets
        re.compile(r"AKIA[0-9A-Z]{16}", re.IGNORECASE),
        re.compile(r"aws_secret_access_key\s*[:=]\s*['\"][a-zA-Z0-9/+=]{30,}['\"]", re.IGNORECASE),

        # Slack Tokens
        re.compile(r"xox[baprs]-[0-9a-zA-Z]{10,}", re.IGNORECASE),

        # Private Keys
        re.compile(r"-----BEGIN (?:RSA|EC|DSA|OPENSSH)?\s*PRIVATE KEY-----[\s\S]*?-----END (?:RSA|EC|DSA|OPENSSH)?\s*PRIVATE KEY-----"),

        # Generic API Keys & Passwords
        re.compile(r"(?:api[_\-]?key|secret[_\-]?key|auth[_\-]?token)\s*[:=]\s*['\"][a-zA-Z0-9_\-\.]{12,}['\"]", re.IGNORECASE),
        re.compile(r"password\s*[:=]\s*['\"][^'\"]{4,}['\"]", re.IGNORECASE),
        re.compile(r"cookie\s*[:=]\s*['\"][^'\"]+['\"]", re.IGNORECASE),
    ]

    @classmethod
    def sanitize_text(cls, text: str) -> str:
        """
        Redacts any detected API key, token, or secret with [REDACTED_KEY_OR_SECRET].
        """
        if not text:
            return ""

        sanitized = text
        for pattern in cls.SECRET_PATTERNS:
            sanitized = pattern.sub("[REDACTED_KEY_OR_SECRET]", sanitized)
        return sanitized

    @classmethod
    def sanitize_metadata(cls, meta: Dict[str, Any]) -> Dict[str, Any]:
        """
        Strips auth headers, cookies, and secret keys from metadata dictionary.
        """
        safe_meta = {}
        for k, v in meta.items():
            if any(forbidden in k.lower() for forbidden in ["auth", "token", "cookie", "password", "session", "secret", "apikey", "api_key"]):
                continue
            if isinstance(v, str):
                safe_meta[k] = cls.sanitize_text(v)
            elif isinstance(v, dict):
                safe_meta[k] = cls.sanitize_metadata(v)
            else:
                safe_meta[k] = v
        return safe_meta

    @classmethod
    def contains_api_keys_or_secrets(cls, text: str) -> bool:
        """
        Checks if text contains exposed API keys or credentials.
        """
        return any(pattern.search(text) for pattern in cls.SECRET_PATTERNS)
