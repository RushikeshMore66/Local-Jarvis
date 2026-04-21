"""
System tools — open apps, type text, press keys, mouse control,
run commands, kill processes, clipboard.
"""

from langchain.tools import tool
import pyautogui
import subprocess
import os
import datetime

pyautogui.FAILSAFE = True  # Move mouse to top-left corner to abort


@tool
def open_app(app_name: str) -> str:
    """Open a desktop application by name.
    Examples: 'notepad', 'chrome', 'spotify', 'calculator', 'explorer'.
    Input is the application name as a string."""
    try:
        # Use subprocess for better compatibility
        subprocess.Popen(f"start {app_name}", shell=True)
        return f"Opened: {app_name}"
    except Exception as e:
        return f"Error opening {app_name}: {e}"


@tool
def type_text(text: str) -> str:
    """Type the given text using the keyboard at the current cursor position.
    Input is the text string to type."""
    try:
        import time
        time.sleep(0.3)
        pyautogui.write(text, interval=0.04)
        return f"Typed: {text}"
    except Exception as e:
        return f"Error typing text: {e}"


@tool
def press_key(key: str) -> str:
    """Press a keyboard key or hotkey combination.
    Examples: 'enter', 'tab', 'escape', 'ctrl+c', 'ctrl+v', 'win+d', 'alt+f4'.
    Input is the key or key combination string."""
    try:
        if "+" in key:
            keys = [k.strip() for k in key.split("+")]
            pyautogui.hotkey(*keys)
        else:
            pyautogui.press(key)
        return f"Pressed: {key}"
    except Exception as e:
        return f"Error pressing key: {e}"


@tool
def move_mouse(coords: str) -> str:
    """Move the mouse cursor to screen coordinates.
    Input format: 'x,y' — for example '960,540' for center of 1920x1080."""
    try:
        x, y = [int(c.strip()) for c in coords.split(",")]
        pyautogui.moveTo(x, y, duration=0.5)
        return f"Mouse moved to ({x}, {y})"
    except Exception as e:
        return f"Error moving mouse: {e}"


@tool
def click_mouse(location: str = "") -> str:
    """Click the mouse at current position, or at 'x,y' coordinates.
    Input is optional 'x,y' coordinates, or leave empty to click current position."""
    try:
        if location and "," in location:
            x, y = [int(c.strip()) for c in location.split(",")]
            pyautogui.click(x, y)
            return f"Clicked at ({x}, {y})"
        else:
            pyautogui.click()
            return "Mouse clicked at current position"
    except Exception as e:
        return f"Error clicking mouse: {e}"


@tool
def run_shell_command(command: str) -> str:
    """Run a Windows shell command and return its output.
    Only use for safe, read-only commands like 'ipconfig', 'dir', 'systeminfo', 'ping'.
    Input is the command string."""
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True,
            text=True, timeout=15, encoding="utf-8", errors="ignore"
        )
        output = result.stdout or result.stderr
        return output[:2000] if output else "Command executed with no output."
    except subprocess.TimeoutExpired:
        return "Command timed out after 15 seconds."
    except Exception as e:
        return f"Shell command error: {e}"


@tool
def get_time(query: str = "") -> str:
    """Return the current system date and time. No input required."""
    now = datetime.datetime.now()
    return (
        f"📅 {now.strftime('%A, %B %d, %Y')}\n"
        f"🕐 {now.strftime('%I:%M:%S %p')}"
    )
