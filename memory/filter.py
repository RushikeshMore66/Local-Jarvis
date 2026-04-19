def is_important(text:str):
    text = text.lower().strip()
    
    keywords = [
        "my name is",
        "i am",
        "i like",
        "i prefer",
        "my goal",
        "remember this",
        "important",
        "my project",
        "my startup"
    ]

    return any(k in text for k in keywords)