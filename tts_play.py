# tts_play.py
import os
import io
import threading
import time
import sounddevice as sd
import soundfile as sf
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

def speak_text(text: str):
    """Convert text to speech using Deepgram and play it"""
    if not text or not text.strip():
        return
    
    if not DEEPGRAM_API_KEY:
        print("DEEPGRAM_API_KEY not set, skipping speech")
        return
    
    try:
        print(f"Converting to speech: {text[:50]}...")
        
        # Use Deepgram REST API directly
        url = "https://api.deepgram.com/v1/speak?model=aura-asteria-en&encoding=linear16&sample_rate=24000"
        
        headers = {
            "Authorization": f"Token {DEEPGRAM_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "text": text
        }
        
        # Make API request
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        # Get audio data
        audio_data = response.content
        
        # Convert to numpy array and play
        audio_array, sample_rate = sf.read(io.BytesIO(audio_data))
        print(f"Playing audio: {len(audio_array)} samples at {sample_rate}Hz")
        
        # Play audio and wait for completion (blocking)
        sd.play(audio_array, sample_rate)
        sd.wait()  # This blocks until playback is completely finished
        print("Audio playback completed")
        
    except Exception as e:
        print(f"Deepgram TTS error: {e}")
