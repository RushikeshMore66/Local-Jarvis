def process_memory(user, response):
    user = user.lower().strip()
    
    if "my name is" in user:
        name = user.replace("my name is", "").strip()
        return f"Remember: My name is {name}"
    
    if "i am" in user:
        age = user.replace("i am", "").strip()
        return f"Remember: I am {age} years old"
    
    if "i like" in user:
        hobby = user.replace("i like", "").strip()
        return f"Remember: I like {hobby}"
    
    if "i prefer" in user:
        preference = user.replace("i prefer", "").strip()
        return f"Remember: I prefer {preference}"
    
    if "my goal" in user:
        goal = user.replace("my goal", "").strip()
        return f"Remember: My goal is {goal}"
    
    if "remember this" in user:
        memory = user.replace("remember this", "").strip()
        return f"Remember: {memory}"
    
    if "important" in user:
        important = user.replace("important", "").strip()
        return f"Remember: {important}"
    
    if "my project" in user:
        project = user.replace("my project", "").strip()
        return f"Remember: My project is {project}"
    
    if "remember that" in user:
        return f"User important info: {user}"
    
    if "my startup" in user:
        startup = user.replace("my startup", "").strip()
        return f"Remember: My startup is {startup}"
    
    return None