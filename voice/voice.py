import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
import pyttsx3
import threading

# ── Whisper Singleton (load once, reuse) ─────────────────────────────────────
_whisper_model = None
_whisper_lock = threading.Lock()

def _get_whisper():
    global _whisper_model
    with _whisper_lock:
        if _whisper_model is None:
            _whisper_model = WhisperModel("base", compute_type="int8")
    return _whisper_model

# ── TTS Engine Singleton ──────────────────────────────────────────────────────
_engine = None
_engine_lock = threading.Lock()

def _get_engine():
    global _engine
    with _engine_lock:
        if _engine is None:
            _engine = pyttsx3.init()
            voices = _engine.getProperty("voices")
            # Prefer a male voice for Jarvis feel
            for v in voices:
                if "david" in v.name.lower() or "male" in v.name.lower() or "en" in v.id.lower():
                    _engine.setProperty("voice", v.id)
                    break
            _engine.setProperty("rate", 185)   # slightly faster than default
            _engine.setProperty("volume", 1.0)
    return _engine

# ── Listen ────────────────────────────────────────────────────────────────────
def listen(duration: int = 5) -> str:
    """Record audio and transcribe it with Whisper."""
    print("\n[  Listening...]")
    fs = 16000
    try:
        recording = sd.rec(
            int(duration * fs),
            samplerate=fs,
            channels=1,
            dtype="int16"
        )
        sd.wait()
        write("input.wav", fs, recording)

        model = _get_whisper()
        segments, _ = model.transcribe("input.wav", language="en")

        text = " ".join(seg.text for seg in segments).strip()
        if text:
            print(f"[You]: {text}")
        return text
    except Exception as e:
        print(f"[Listen error]: {e}")
        return ""

# ── Speak ─────────────────────────────────────────────────────────────────────
def speak(text: str):
    """Speak text aloud with Jarvis-style voice."""
    if not text:
        return
    print(f"[JARVIS]: {text}")
    try:
        engine = _get_engine()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"[Speak error]: {e}")