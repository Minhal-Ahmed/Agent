# AI Multimodal Assistant

A real-time AI-powered assistant that combines **screen capture**, **speech recognition**, and **computer vision** to provide intelligent responses based on what you say and what's on your screen.

## ✨ Features

- 🎤 **Real-time Speech Recognition** - Continuous audio recording and transcription
- 📸 **Screen Capture** - Automatic screenshot capture at 5 FPS for visual context
- 🧠 **AI Vision Analysis** - Uses Google Gemini 1.5 Flash for multimodal understanding
- 🔊 **Text-to-Speech** - Natural voice responses using Deepgram's Aura TTS
- 🖥️ **Live Preview** - Real-time screen preview window
- ⚡ **Multithreaded** - Efficient parallel processing of audio and visual streams

## 🏗️ Architecture

The project consists of four main components:

- **`recorder.py`** - Main orchestrator that coordinates all components
- **`stt_whisper.py`** - Speech-to-text using Google Speech Recognition with fallback
- **`vlm_client.py`** - Vision-language model client (Google Gemini)
- **`tts_play.py`** - Text-to-speech using Deepgram API

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Windows OS (optimized for Windows audio/video capture)
- Microphone and speakers/headphones
- Internet connection for API calls

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd "Agent"
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   # API Keys (Required)
   GEMINI_API_KEY=your_gemini_api_key_here
   DEEPGRAM_API_KEY=your_deepgram_api_key_here
   
   # Audio/Video Settings (Optional)
   AUDIO_CHUNK_SECONDS=10
   SCREEN_SCALE=0.6
   ```

### Getting API Keys

- **Gemini API Key**: Get it from [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Deepgram API Key**: Sign up at [Deepgram Console](https://console.deepgram.com/)

### Usage

1. **Activate virtual environment**
   ```bash
   venv\Scripts\activate
   ```

2. **Run the assistant**
   ```bash
   python recorder.py
   ```

3. **Interact with the assistant**
   - Speak naturally - the assistant listens continuously
   - It will analyze your screen and provide contextual responses
   - Press `q` in the preview window or `Ctrl+C` to stop

## ⚙️ Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GEMINI_API_KEY` | - | **Required** - Google Gemini API key |
| `DEEPGRAM_API_KEY` | - | **Required** - Deepgram TTS API key |
| `AUDIO_CHUNK_SECONDS` | 10 | Duration of audio recording chunks |
| `SCREEN_SCALE` | 0.6 | Screen capture scale factor (0.1-1.0) |

### Performance Tuning

- **Reduce `SCREEN_SCALE`** for better performance on slower systems
- **Increase `AUDIO_CHUNK_SECONDS`** for longer conversation context
- **Close unnecessary applications** to improve screen capture performance

## 🔧 Technical Details

### Audio Processing
- Records 4-10 second audio chunks using `sounddevice`
- Uses Google Speech Recognition API with Windows Speech Recognition fallback
- Supports 16kHz mono audio for optimal speech recognition

### Screen Capture
- Captures primary monitor at 5 FPS using `mss` library
- Scales images for efficient processing while maintaining quality
- Converts to PNG format for AI model compatibility

### AI Integration
- **Vision Model**: Google Gemini 1.5 Flash for multimodal understanding
- **TTS**: Deepgram Aura Asteria voice model
- **Fallback**: Robust error handling with graceful degradation

## 🛠️ Troubleshooting

### Common Issues

**Audio not working:**
- Ensure microphone permissions are granted
- Check default audio input device in Windows settings
- Try running as administrator

**Screen capture black/blank:**
- Check display scaling settings
- Ensure no fullscreen applications are blocking capture
- Try adjusting `SCREEN_SCALE` value

**API errors:**
- Verify API keys are correctly set in `.env` file
- Check internet connection
- Ensure API quotas haven't been exceeded

### Dependencies Issues

If you encounter package installation issues:
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

## 📁 Project Structure

```
Also Agent/
├── recorder.py          # Main application entry point
├── stt_whisper.py       # Speech recognition module
├── vlm_client.py        # Vision-language model client
├── tts_play.py          # Text-to-speech module
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (create this)
├── README.md           # This file
└── venv/               # Virtual environment (created during setup)
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **Google Gemini** for multimodal AI capabilities
- **Deepgram** for high-quality text-to-speech
- **OpenAI Whisper** community for speech recognition insights
- **MSS** library for efficient screen capture
