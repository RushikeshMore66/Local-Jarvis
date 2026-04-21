"""
Emergency stop — registers Ctrl+Shift+X as a kill switch.
When triggered, sets a global stop flag and speaks a warning.
"""

import threading
import keyboard

# Global stop flag accessible by all modules
_stop_event = threading.Event()


def is_stopped() -> bool:
    """Check if emergency stop has been triggered."""
    return _stop_event.is_set()


def clear_stop():
    """Clear the emergency stop flag to resume normal operation."""
    _stop_event.clear()


def _trigger_stop():
    _stop_event.set()
    print("\n\n⛔  EMERGENCY STOP ACTIVATED — All actions halted.\n")
    try:
        from voice.voice import speak
        speak("Emergency stop activated. All actions halted.")
        # Auto-clear after speaking so Jarvis can resume
        _stop_event.clear()
    except Exception:
        pass


class EmergencyStop:
    """Register and manage the emergency stop hotkey."""

    def __init__(self, hotkey: str = "ctrl+shift+x"):
        self.hotkey = hotkey
        self._registered = False

    def start(self):
        """Start listening for the emergency stop hotkey in a background thread."""
        if self._registered:
            return
        try:
            keyboard.add_hotkey(self.hotkey, _trigger_stop, suppress=False)
            self._registered = True
            print(f"[🔒 Emergency Stop]: Hotkey '{self.hotkey.upper()}' registered.")
        except Exception as e:
            print(f"[Emergency Stop]: Could not register hotkey — {e}")

    def stop(self):
        """Unregister the hotkey."""
        if self._registered:
            keyboard.remove_hotkey(self.hotkey)
            self._registered = False
