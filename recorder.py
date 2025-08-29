# recorder.py
import os
import time
import io
import threading
from PIL import Image
import numpy as np
import mss
import cv2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from stt_whisper import record_and_transcribe
from vlm_client import call_vlm_with_image_and_text
from tts_play import speak_text

AUDIO_CHUNK_SECONDS = int(os.getenv("AUDIO_CHUNK_SECONDS", "4"))
SCREEN_SCALE = float(os.getenv("SCREEN_SCALE", "0.6"))
FPS = 5.0
FRAME_INTERVAL = 1.0 / FPS

def capture_screen_pil(scale=1.0):
    try:
        with mss.mss() as sct:
            monitor = sct.monitors[1]  # primary monitor
            sct_img = sct.grab(monitor)
            arr = np.array(sct_img)  # BGRA
            img = cv2.cvtColor(arr, cv2.COLOR_BGRA2RGB)
            pil = Image.fromarray(img)
            if scale != 1.0:
                w, h = pil.size
                pil = pil.resize((int(w*scale), int(h*scale)), Image.LANCZOS)
            return pil
    except Exception as e:
        print(f"Screen capture error: {e}")
        # Return a blank image as fallback
        return Image.new('RGB', (640, 480), color='black')

def pil_to_png_bytes(pil_img: Image.Image) -> bytes:
    buf = io.BytesIO()
    pil_img.save(buf, format="PNG")
    return buf.getvalue()

def main_loop():
    print("Starting main loop. Press Ctrl+C to stop.")
    last_frame = None

    # run a background thread that continually records audio chunks and processes them
    def audio_worker():
        while True:
            try:
                transcript = record_and_transcribe(AUDIO_CHUNK_SECONDS)
            except Exception as e:
                print("STT error:", e)
                transcript = ""
            if not transcript:
                print("(No speech detected in the last chunk.)")
                continue
            print("TRANSCRIPT:", transcript)

            # take a recent screenshot for VLM context
            try:
                pil = capture_screen_pil(scale=SCREEN_SCALE)
                img_bytes = pil_to_png_bytes(pil)
            except Exception as e:
                print("Screenshot error:", e)
                img_bytes = b""

            # call VLM (Gemini)
            try:
                print("Calling Gemini...")
                response = call_vlm_with_image_and_text(img_bytes, transcript, provider="gemini")
                print("Gemini response:", response)
            except Exception as e:
                response = f"(VLM call failed: {e})"
                print(response)
            # speak the response (blocking to ensure complete playback)
            try:
                print("Speaking response...")
                speak_text(response)
                print("Finished speaking response")
            except Exception as e:
                print("TTS error:", e)

    th = threading.Thread(target=audio_worker, daemon=True)
    th.start()

    # visual loop: capture & optionally display frames at FPS (for local preview)
    try:
        while True:
            start = time.time()
            pil = capture_screen_pil(scale=SCREEN_SCALE)
            last_frame = pil
            # show quick preview window (optional)
            cv_img = cv2.cvtColor(np.array(pil), cv2.COLOR_RGB2BGR)
            cv2.imshow("Live preview (press q to quit)", cv_img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            elapsed = time.time() - start
            to_wait = FRAME_INTERVAL - elapsed
            if to_wait > 0:
                time.sleep(to_wait)
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main_loop()
