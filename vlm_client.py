import os
import base64
import json
import requests
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def call_vlm_with_image_and_text(image_bytes: bytes, user_text: str, provider="gemini"):
    """
    Sends image (bytes) + user_text to Gemini and returns the text response.
    """
    
    if provider != "gemini":
        raise NotImplementedError("Only 'gemini' provider is implemented.")

    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY not set in environment.")

    try:
        # Initialize Gemini model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Convert bytes to PIL Image for Gemini
        from PIL import Image
        import io
        image = Image.open(io.BytesIO(image_bytes))
        
        # Create prompt
        prompt = f"""You are a multimodal assistant that can analyze screenshots and spoken text.

User speech transcript: "{user_text}"

Please analyze the screenshot and the speech transcript, then provide a concise, helpful response that addresses what the user is asking about or commenting on."""

        # Generate response with image and text
        response = model.generate_content([prompt, image])
        
        return response.text.strip()
        
    except Exception as e:
        print(f"Gemini API error: {e}")
        return f"Sorry, I encountered an error processing your request: {str(e)}"
