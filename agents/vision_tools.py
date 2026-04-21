from langchain.tools import tool
from vision.screen import read_text
from vision.analyze import get_screen_text

@tool
def read_screen(dummy: str = ""):
    """Read visible text from the screen"""
    text = read_text()
    return text[:1000] # limit size

@tool
def analyze_screen(dummy: str = ""):
    """Analyze current screen and describe what is visible on it"""
    return get_screen_text()
    