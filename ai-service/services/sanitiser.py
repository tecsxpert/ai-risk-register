# I am the input sanitisation module. All text input to AI endpoints passes through me
# before reaching the Groq API. I strip HTML and block prompt injection attempts.
import re
import logging
import bleach

logger = logging.getLogger(__name__)

# These patterns indicate prompt injection attempts
INJECTION_PATTERNS = [
    re.compile(r'ignore\s+(all\s+)?(previous|prior|above)\s+instructions', re.IGNORECASE),
    re.compile(r'you\s+are\s+now\s+a\s+(different|new|other)', re.IGNORECASE),
    re.compile(r'reveal\s+(your\s+)?(system\s+prompt|instructions|training)', re.IGNORECASE),
    re.compile(r'disregard\s+(all\s+)?(previous|prior)\s+(instructions|context)', re.IGNORECASE),
    re.compile(r'act\s+as\s+(if\s+you\s+are|a\s+different)', re.IGNORECASE),
    re.compile(r'pretend\s+(you\s+are|to\s+be)\s+(a\s+)?(?!risk)', re.IGNORECASE),
    re.compile(r'from\s+now\s+on\s+(you\s+are|act)', re.IGNORECASE),
    re.compile(r'new\s+instruction[s]?:', re.IGNORECASE),
    re.compile(r'system\s*:\s*(you\s+are|your\s+new)', re.IGNORECASE),
    re.compile(r'\[INST\]|\[\/INST\]|<\|im_start\|>|<\|im_end\|>', re.IGNORECASE),
]

# HTML tags and attributes that bleach will allow — none for risk text fields
ALLOWED_TAGS = []
ALLOWED_ATTRIBUTES = {}

def sanitise_text(text: str) -> tuple[str, bool]:
    """
    Sanitise a text string: strip HTML, detect prompt injection.
    
    Returns:
        tuple: (cleaned_text: str, is_injection: bool)
    """
    if not isinstance(text, str):
        return "", False

    # Step 1: Strip all HTML tags using bleach
    cleaned = bleach.clean(text, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, strip=True)

    # Step 2: Detect prompt injection patterns in the cleaned text
    for pattern in INJECTION_PATTERNS:
        if pattern.search(cleaned):
            logger.warning(f"Prompt injection pattern detected: '{pattern.pattern}'.")
            return cleaned, True

    return cleaned, False
