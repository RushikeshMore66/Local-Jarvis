"""
Intelligent router — classifies user intent to decide: local, web, or cloud.
"""

WEB_KEYWORDS = [
    "search", "google", "find online", "look up", "news", "weather",
    "latest", "current", "today", "trending", "what is happening",
    "stock", "price", "score", "headline", "update", "recent",
    "who is", "who was", "where is", "when did", "how much",
    "wikipedia", "definition of", "meaning of",
]

SYSTEM_KEYWORDS = [
    "open", "close", "start", "launch", "type", "click", "press",
    "screenshot", "volume", "brightness", "battery", "process",
    "file", "folder", "directory", "copy", "paste", "clipboard",
    "run", "execute", "command", "task manager", "delete", "move",
    "install", "uninstall", "download",
]

CLOUD_KEYWORDS = [
    "explain", "analyze", "summarize", "write", "create", "generate",
    "plan", "strategy", "help me", "how to", "steps to", "guide",
    "code", "program", "debug", "fix", "review", "compare", "essay",
    "translate", "difference between", "pros and cons", "what are",
]


def classify_intent(query: str) -> str:
    """Returns 'web', 'system', 'cloud', or 'local'."""
    q = query.lower().strip()

    if any(k in q for k in WEB_KEYWORDS):
        return "web"
    if any(k in q for k in SYSTEM_KEYWORDS):
        return "system"
    if len(q) > 80 or any(k in q for k in CLOUD_KEYWORDS):
        return "cloud"
    return "local"


def is_complex(query: str) -> bool:
    """Return True if the query should go to the cloud LLM."""
    intent = classify_intent(query)
    return intent == "cloud"