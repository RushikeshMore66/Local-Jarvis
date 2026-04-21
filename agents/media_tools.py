"""
Media & system info tools — screenshot, battery, CPU, RAM, volume control.
"""

from langchain.tools import tool
import os
import datetime


@tool
def take_screenshot(filename: str = "") -> str:
    """Take a screenshot of the current screen and save it.
    Input is optional filename (default: saves to Desktop with timestamp)."""
    try:
        import pyautogui
        if not filename:
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            filename = os.path.join(desktop, f"screenshot_{ts}.png")
        filename = os.path.expanduser(filename)
        img = pyautogui.screenshot()
        img.save(filename)
        return f"Screenshot saved to: {filename}"
    except Exception as e:
        return f"Screenshot error: {e}"


@tool
def get_system_info(query: str = "") -> str:
    """Get current system resource usage: CPU, RAM, disk space, uptime.
    No input required."""
    try:
        import psutil
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        boot = datetime.datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.datetime.now() - boot

        return (
            f"🖥️  System Info:\n"
            f"  CPU Usage    : {cpu}%\n"
            f"  RAM Used     : {ram.used // (1024**2):,} MB / {ram.total // (1024**2):,} MB ({ram.percent}%)\n"
            f"  Disk (C:)    : {disk.used // (1024**3):.1f} GB / {disk.total // (1024**3):.1f} GB ({disk.percent}%)\n"
            f"  Uptime       : {str(uptime).split('.')[0]}"
        )
    except Exception as e:
        return f"System info error: {e}"


@tool
def get_battery_info(query: str = "") -> str:
    """Get laptop battery status, percentage, and charging state.
    No input required."""
    try:
        import psutil
        batt = psutil.sensors_battery()
        if batt is None:
            return "No battery detected (desktop PC or battery info unavailable)."
        status = "Charging ⚡" if batt.power_plugged else "Discharging 🔋"
        secs = batt.secsleft
        time_left = ""
        if secs > 0 and not batt.power_plugged:
            h, m = divmod(secs // 60, 60)
            time_left = f"  Time Left    : {h}h {m}m\n"
        return (
            f"🔋 Battery: {batt.percent:.0f}% — {status}\n"
            f"{time_left}"
        )
    except Exception as e:
        return f"Battery info error: {e}"


@tool
def list_processes(query: str = "") -> str:
    """List the top 15 running processes sorted by CPU usage.
    No input required."""
    try:
        import psutil
        procs = []
        for p in psutil.process_iter(["pid", "name", "cpu_percent", "memory_info"]):
            try:
                procs.append(p.info)
            except psutil.NoSuchProcess:
                pass
        procs.sort(key=lambda x: x.get("cpu_percent", 0), reverse=True)
        lines = ["PID    NAME                     CPU%   MEM(MB)"]
        for p in procs[:15]:
            mem = p["memory_info"].rss // (1024 * 1024) if p.get("memory_info") else 0
            lines.append(f"{p['pid']:<6} {p['name']:<25} {p.get('cpu_percent', 0):<6.1f} {mem}")
        return "\n".join(lines)
    except Exception as e:
        return f"Process list error: {e}"


@tool
def kill_process_by_name(name: str) -> str:
    """Kill/terminate a running process by name. Only use when user asks.
    Input is the process name, e.g. 'notepad.exe'"""
    try:
        import psutil
        killed = []
        for p in psutil.process_iter(["pid", "name"]):
            if name.lower() in p.info["name"].lower():
                p.kill()
                killed.append(f"{p.info['name']} (PID {p.info['pid']})")
        if killed:
            return f"Killed: {', '.join(killed)}"
        return f"No process found with name: {name}"
    except Exception as e:
        return f"Error killing process: {e}"


@tool
def get_clipboard(query: str = "") -> str:
    """Get the current content of the clipboard. No input required."""
    try:
        import pyperclip
        content = pyperclip.paste()
        return f"Clipboard contents:\n{content}" if content else "Clipboard is empty."
    except Exception as e:
        return f"Clipboard read error: {e}"


@tool
def set_clipboard(text: str) -> str:
    """Copy text to the clipboard. Input is the text to copy."""
    try:
        import pyperclip
        pyperclip.copy(text)
        return f"Copied to clipboard: {text[:100]}{'...' if len(text) > 100 else ''}"
    except Exception as e:
        return f"Clipboard write error: {e}"
