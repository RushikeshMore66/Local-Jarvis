from pydantic import DurationError
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
import pyttsx3

# Initialize Whisper model
model = WhisperModel("base", compute_type="int8")
DEVICES_ID =""

# Initialize TTS engine
engine = pyttsx3.init()

# Recording parameters
def listen():
    print("Listening...")
    
    duration = 4
    fs = 16000
    
    recording = sd.rec(
        int(duration * fs), 
        samplerate=fs, 
        channels=1, 
        dtype="int16",
        device=DEVICES_ID
    )
    
    sd.wait()

    from scipy.io.wavfile import write
    write("input.wav", fs, recording)

    from faster_whisper import WhisperModel
    model = WhisperModel("base", compute_type="int8")
    
    segments, _ = model.transcribe("input.wav")
    
    text = " "
    for segment in segments:
        text += segment.text

    print(f"You: {text}")
    return text.strip()

# speak function
def speak(text):
    print(f"JARVIS: {text}")
    engine.say(text)
    engine.runAndWait()


        