"""
Input sanitization middleware for prompt injection protection and HTML stripping.
"""

import re
import html
from typing import Tuple
import logging

logger = logging.getLogger(__name__)

# Prompt injection patterns to detect
INJECTION_PATTERNS = [
    r"(?i)(ignore|disregard|forget)\s+(your|the)\s+(system\s+)?prompt",
    r"(?i)(system\s+)?prompt\s+(injection|override|jailbreak)",
    r"(?i)(as\s+)?an\s+ai|as\s+an\s+assistant.*?you\s+(are|should)",
    r"(?i)instructions?:\s*ignore|forget|override",
    r"(?i)(do\s+not|don't)\s+(follow|adhere)\s+to",
    r"(?i)pretend\s+(you\s+)?are\s+not",
    r"(?i)act\s+as\s+if.*?no\s+(safety|restrictions)",
    r"(?i)DAN\s*:|Do\s+Anything\s+Now",
    r"(?i)jailbreak|bypass.*?filter",
    r"(?i)admin\s+mode|debug\s+mode|god\s+mode",
    r"(?i)role\s+play\s+as.*?without.*?restriction",
    r"\{\{.*?\}\}",  # Template injection attempts
    r"<%.*?%>",      # Server-side template injection
    r"\$\{.*?\}",    # Expression injection
]

# HTML tags pattern
HTML_TAG_PATTERN = re.compile(r'<[^>]+>', re.IGNORECASE)

class SanitizationError(Exception):
    """Raised when input fails sanitization checks."""
    pass


def strip_html(text: str) -> str:
    """
    Strip HTML tags and decode HTML entities from text.
    
    Args:
        text: Input text that may contain HTML
        
    Returns:
        Text with HTML tags removed and entities decoded
    """
    # Remove HTML tags
    text = HTML_TAG_PATTERN.sub('', text)
    # Decode HTML entities
    text = html.unescape(text)
    return text


def detect_prompt_injection(text: str) -> Tuple[bool, str]:
    """
    Detect potential prompt injection attempts.
    
    Args:
        text: Input text to analyze
        
    Returns:
        Tuple of (is_injection_detected, detected_pattern)
    """
    for pattern in INJECTION_PATTERNS:
        match = re.search(pattern, text)
        if match:
            logger.warning(f"Prompt injection detected: {match.group()}")
            return True, match.group()
    return False, ""


def sanitize_input(text: str, check_injection: bool = True) -> str:
    """
    Sanitize user input by stripping HTML and detecting injection attempts.
    
    Args:
        text: Input text to sanitize
        check_injection: Whether to check for prompt injection patterns
        
    Returns:
        Sanitized text
        
    Raises:
        SanitizationError: If input contains malicious patterns
    """
    if not isinstance(text, str):
        raise SanitizationError("Input must be a string")
    
    if len(text) == 0:
        raise SanitizationError("Input cannot be empty")
    
    if len(text) > 10000:
        raise SanitizationError("Input exceeds maximum length of 10000 characters")
    
    # Check for prompt injection
    if check_injection:
        is_injection, pattern = detect_prompt_injection(text)
        if is_injection:
            raise SanitizationError(f"Suspicious pattern detected: {pattern}")
    
    # Strip HTML tags
    sanitized = strip_html(text)
    
    # Remove excessive whitespace
    sanitized = re.sub(r'\s+', ' ', sanitized).strip()
    
    logger.info("Input sanitized successfully")
    return sanitized


def sanitize_dict(data: dict, keys_to_sanitize: list = None, check_injection: bool = True) -> dict:
    """
    Sanitize specific keys in a dictionary.
    
    Args:
        data: Dictionary to sanitize
        keys_to_sanitize: List of keys to sanitize (if None, sanitizes all string values)
        check_injection: Whether to check for prompt injection patterns
        
    Returns:
        Dictionary with sanitized values
        
    Raises:
        SanitizationError: If any sanitization fails
    """
    sanitized = {}
    
    for key, value in data.items():
        if isinstance(value, str):
            if keys_to_sanitize is None or key in keys_to_sanitize:
                try:
                    sanitized[key] = sanitize_input(value, check_injection)
                except SanitizationError as e:
                    raise SanitizationError(f"Failed to sanitize '{key}': {str(e)}")
            else:
                sanitized[key] = value
        else:
            sanitized[key] = value
    
    return sanitized
