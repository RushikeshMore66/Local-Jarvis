from .store import MemoryStore
from .filter import is_important
from .processor import process_memory

Memory_Store = MemoryStore()

def save_memory(user , response):
    if not is_important(user):
        return
    
    processed = process_memory(user, response)
    
    if processed:
        Memory_Store.add(processed)

def get_context(query):
    memories = Memory_Store.search(query)
    
    if not memories:
        return ""
    
    context = "\n".join(memories)

    return f"""
    Use this memory about the user:
    {context}
    """