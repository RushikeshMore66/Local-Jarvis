def is_important(text: str) -> bool:
    """Return True if the user's message contains info worth storing long-term."""
    text = text.lower().strip()

    keywords = [
        # Identity
        "my name is", "i am", "i'm", "call me",
        # Preferences
        "i like", "i love", "i hate", "i prefer", "i enjoy",
        "my favorite", "i always", "i usually", "i never",
        # Goals
        "my goal", "my dream", "i want to", "i'm trying to",
        "i plan to", "my target",
        # Projects & work
        "my project", "my startup", "my company", "my business",
        "i work at", "i work on", "my job", "i'm working on",
        # Explicit memory
        "remember this", "remember that", "don't forget",
        "important", "note this", "save this",
        # Personal facts
        "i live in", "i'm from", "my city", "my country",
        "my age", "i was born", "my birthday",
    ]

    return any(k in text for k in keywords)