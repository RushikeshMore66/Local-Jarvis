from langchain.tools import tool
import pyautogui

@tool
def click_position(x:int, y:int):
    """Click at the specific screen coordinates."""
    pyautogui.click(x, y)
    return f"Clicked at ({x}, {y})"