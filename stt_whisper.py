# stt_whisper.py
import os
import tempfile
import sounddevice as sd
import soundfile as sf
import numpy as np
import speech_recognition as sr
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize speech recognizer
_recognizer = sr.Recognizer()

print("Initializing speech recognition...")
print("Speech recognition ready (using sounddevice for recording)")

def record_audio_chunk(duration_s=4, samplerate=16000, channels=1):
    """Record duration_s seconds of audio and return path to temp WAV file"""
    try:
        print(f"Recording audio for {duration_s}s ...")
        audio = sd.rec(int(duration_s * samplerate), samplerate=samplerate, channels=channels, dtype='int16')
        sd.wait()
        audio = np.squeeze(audio)  # (N,) or (N, channels)
        tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        sf.write(tmpfile.name, audio, samplerate)
        return tmpfile.name
    except Exception as e:
        print(f"Audio recording error: {e}")
        # Create a silent audio file as fallback
        silent_audio = np.zeros(int(duration_s * samplerate), dtype='int16')
        tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        sf.write(tmpfile.name, silent_audio, samplerate)
        return tmpfile.name

def transcribe_file(wav_path: str):
    """Transcribe audio file using speech_recognition library"""
    try:
        print("Transcribing with speech recognition:", wav_path)
        with sr.AudioFile(wav_path) as source:
            audio = _recognizer.record(source)
        
        # Try Google Speech Recognition (free)
        try:
            text = _recognizer.recognize_google(audio)
            return text.strip()
        except sr.UnknownValueError:
            return ""  # No speech detected
        except sr.RequestError:
            # Fallback to Windows Speech Recognition
            try:
                text = _recognizer.recognize_sphinx(audio)
                return text.strip()
            except:
                return ""
    except Exception as e:
        print(f"STT error: {e}")
        return ""

def record_and_transcribe(duration_s=4):
    """Record audio using sounddevice and transcribe with speech_recognition"""
    # Use the existing sounddevice recording that was working
    wav_path = record_audio_chunk(duration_s=duration_s)
    text = transcribe_file(wav_path)
    
    # Clean up temp file
    try:
        os.unlink(wav_path)
    except Exception:
        pass
    
    return text
