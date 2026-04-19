def is_complex(query: str):
    query = query.lower().strip()
    
    if len(query) < 3:
        return False
    
    keyword = [
        "plan","explain","build","create","stratergy","analyze","how to","steps"
    ]

    if len(query) > 60:
        return True
    
    if any(k in query for k in keyword):
        return True
    
    return False