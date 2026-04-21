"""
Wake word detection — checks if "jarvis" or "hey jarvis" is in the transcript.
"""

WAKE_WORDS = ["jarvis", "hey jarvis", "ok jarvis", "yo jarvis"]


def has_wake_word(text: str) -> bool:
    """Return True if a wake phrase was found in the transcript."""
    normalized = text.lower().strip()
    return any(w in normalized for w in WAKE_WORDS)


def strip_wake_word(text: str) -> str:
    """Remove the wake phrase from the beginning of the query."""
    normalized = text.lower().strip()
    for w in sorted(WAKE_WORDS, key=len, reverse=True):
        if normalized.startswith(w):
            return text[len(w):].strip(" ,.")
    return text
