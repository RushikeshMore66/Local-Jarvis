"""
Memory — short-term conversation buffer + long-term FAISS vector store.
"""

from .store import MemoryStore
from .filter import is_important
from .processor import process_memory
from collections import deque

# Long-term memory (FAISS)
_long_term = MemoryStore()

# Short-term memory — last 10 conversation turns
_short_term: deque = deque(maxlen=10)


def save_memory(user: str, response: str):
    """Save a conversation turn to short-term and (if important) long-term memory."""
    # Always save to short-term
    _short_term.append({"user": user, "assistant": response})

    # Only save important info to long-term FAISS
    if is_important(user):
        processed = process_memory(user, response)
        if processed:
            _long_term.add(processed)


def get_context(query: str) -> str:
    """Retrieve relevant context from both memory tiers."""
    parts = []

    # Short-term: recent conversation buffer
    if _short_term:
        recent = "\n".join(
            f"User: {t['user']}\nJARVIS: {t['assistant']}"
            for t in list(_short_term)[-3:]  # last 3 turns
        )
        parts.append(f"Recent conversation:\n{recent}")

    # Long-term: FAISS semantic search
    memories = _long_term.search(query, k=3)
    if memories:
        parts.append("Known facts about the user:\n" + "\n".join(memories))

    if not parts:
        return ""

    return "\n\n".join(parts) + "\n\n"


def get_short_term_history() -> list:
    """Return the short-term history as a list of dicts for cloud LLM."""
    return list(_short_term)


def memory_count() -> int:
    """Total memories in long-term store."""
    return len(_long_term.texts)