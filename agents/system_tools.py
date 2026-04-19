from langchain.tools import tool
import pyautogui
import time
import os


"""Only use when explicitly asked by user"""
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 1

def open_app(app_name:str):
    """Open desktop application like notepad, chrome, etc."""
    try:
        os.system(f"start{app_name}")
        return f"{app_name} opened successfully"
    except Exception as e:
        return f"Error opening: {e}"

@tool
def type_text(text:str):
    """Type the given text using keyboard."""
    pyautogui.write(text, interval=0.05)
    return f"Typed: {text}"

@tool
def press_key(key:str):
    """Press a keyboard key like enter, tab, escape, ctrl, etc."""
    pyautogui.press(key)
    return f"Pressed: {key}"

@tool
def move_mouse(x:int, y:int):
    """Move mouse to (x, y) coordinates."""
    pyautogui.moveTo(x, y, duration=1)
    return f"Mouse moved to ({x}, {y})"

@tool
def click_mouse():
    """Click the mouse."""
    pyautogui.click()
    return "Mouse clicked"


