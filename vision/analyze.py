from vision.screen import capture_screen
from brain.cloud_llm import ask_cloud
from vision.screen import read_text

def analyze_screen():
    capture_screen()

def get_screen_text():
    text = read_text()

    return f"""
    screen content:
    {text[:1000]}
    """

    prompt="""
You are seeing a screenshot of a computer screen.

Based on visible UI elements, describe:
- what app is open
- what user can do next

Be concise.
    """
    return ask_cloud(prompt)