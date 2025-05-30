# Claude Desktop Real-time Audio MCP Server (Python Implementation)

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)

A Python-based Model Context Protocol (MCP) server that enables **real-time microphone input** for Claude Desktop on Windows. This implementation leverages Python's superior audio processing ecosystem to provide robust voice-driven conversations with Claude through WASAPI audio capture and multiple speech recognition engines.

## 🚀 Key Advantages of Python Implementation

- **🐍 Mature Audio Ecosystem**: Leverages `sounddevice`, `webrtcvad`, and specialized Windows audio libraries
- **🧠 Multiple STT Engines**: OpenAI Whisper (local/API), Azure Speech, Google Speech-to-Text
- **⚡ FastMCP Framework**: High-level Pythonic interface for rapid MCP development
- **🔧 Easy Configuration**: JSON/YAML configuration with environment variable support
- **📊 Better Debugging**: Comprehensive logging and performance monitoring
- **🔄 Async Architecture**: Non-blocking operations with asyncio

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Claude        │    │   FastMCP Server │    │  Audio Capture  │
│   Desktop       │◄──►│   (Python)       │◄──►│  (sounddevice)  │
│                 │    │                  │    │  + WASAPI       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │  STT Engines     │    │  Voice Activity │
                       │  • Whisper       │    │  Detection      │
                       │  • Azure Speech  │    │  (webrtcvad)    │
                       │  • Google Speech │    │                 │
                       └──────────────────┘    └─────────────────┘
```

## 📋 Prerequisites

- **Windows 10/11** (Windows 7+ with WASAPI support)
- **Python 3.8+**
- **Claude Desktop** (latest version)

## 🚦 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/joelfuller2016/claude-desktop-realtime-audio-mcp-python.git
cd claude-desktop-realtime-audio-mcp-python

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Install with GPU support (optional)
pip install -r requirements.txt[gpu]
```

### 2. Configuration

Create a configuration file or use environment variables:

```bash
# Set OpenAI API key (for Whisper API)
set OPENAI_API_KEY=your_api_key_here

# Set Azure Speech key (optional)
set AZURE_SPEECH_KEY=your_azure_key
set AZURE_SPEECH_REGION=eastus

# Set Google credentials (optional)
set GOOGLE_CREDENTIALS_PATH=path/to/credentials.json
```

### 3. Test Audio Setup

```bash
# Test your microphone and audio devices
python -m audio.test_setup
```

### 4. Run the MCP Server

```bash
# Start the server
python main.py

# Or with debug logging
python main.py --debug
```

### 5. Configure Claude Desktop

Add to your Claude Desktop configuration file (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "claude-audio": {
      "command": "python",
      "args": [
        "C:\\full\\path\\to\\main.py"
      ],
      "env": {
        "OPENAI_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## 🛠️ MCP Tools Available

### Audio Control
- `start_recording()` - Start real-time audio capture
- `stop_recording()` - Stop audio capture
- `get_recording_status()` - Get current status and config
- `test_audio_capture(duration=3.0)` - Test microphone

### Device Management
- `list_audio_devices()` - List all audio input devices
- `set_audio_device(device_id)` - Set audio input device
- `configure_audio_settings()` - Adjust sample rate, channels, etc.

### Speech Recognition
- `set_stt_engine(engine)` - Switch between whisper/azure/google
- View available engines and status

### Resources
- `audio://devices` - Available audio devices
- `audio://config` - Current audio configuration
- `stt://engines` - STT engines status

## ⚙️ Configuration

### Audio Settings
```json
{
  "audio": {
    "sample_rate": 16000,
    "channels": 1,
    "chunk_size": 1024,
    "device_id": null,
    "use_wasapi_exclusive": false,
    "low_latency": true
  }
}
```

### Voice Activity Detection
```json
{
  "vad": {
    "mode": "hybrid",
    "webrtc_aggressiveness": 2,
    "energy_threshold": 0.01,
    "min_speech_duration": 0.1,
    "min_silence_duration": 0.3
  }
}
```

### Speech-to-Text Engines
```json
{
  "stt": {
    "default_engine": "whisper",
    "whisper": {
      "model_size": "base",
      "use_api": false,
      "language": null
    },
    "azure": {
      "enabled": false,
      "api_key": null,
      "region": "eastus"
    },
    "google": {
      "enabled": false,
      "credentials_path": null
    }
  }
}
```

## 🔧 Advanced Usage

### Using Local Whisper Models
```python
# Different model sizes (tiny, base, small, medium, large)
config.stt.whisper.model_size = "small"  # Faster
config.stt.whisper.model_size = "large"  # More accurate
```

### Optimizing for Real-time Performance
```python
# Low-latency settings
config.audio.chunk_size = 512
config.audio.sample_rate = 16000
config.vad.min_speech_duration = 0.1
```

### Using Cloud STT Services
```bash
# Azure Speech
export AZURE_SPEECH_KEY="your_key"
export AZURE_SPEECH_REGION="eastus"

# Google Speech
export GOOGLE_CREDENTIALS_PATH="/path/to/credentials.json"
```

## 🧪 Testing

### Test Audio Devices
```bash
python -c "from audio.capture import list_audio_devices; print(list_audio_devices())"
```

### Test Voice Activity Detection
```bash
python -c "from audio.vad import create_vad; vad = create_vad('hybrid')"
```

### Benchmark STT Engines
```bash
python -m stt.benchmark --audio test_audio.wav
```

## 📊 Performance Monitoring

The server includes comprehensive logging and performance monitoring:

- **Audio Processing**: Chunk processing times, dropouts, queue status
- **VAD Performance**: Speech detection accuracy, false positives
- **STT Metrics**: Transcription latency, confidence scores, accuracy
- **System Resources**: Memory usage, CPU utilization

Enable debug logging for detailed metrics:

```bash
python main.py --debug
```

## 🔍 Troubleshooting

### Common Issues

**1. No audio devices detected**
```bash
# Check if sounddevice can see your devices
python -c "import sounddevice as sd; print(sd.query_devices())"
```

**2. High latency**
```python
# Reduce chunk size and enable low latency
config.audio.chunk_size = 512
config.audio.low_latency = True
```

**3. Whisper model loading errors**
```bash
# Clear Whisper cache and redownload
pip uninstall openai-whisper
pip install openai-whisper
```

**4. WASAPI permissions on Windows**
- Check microphone privacy settings
- Run as administrator if needed
- Ensure Claude Desktop has microphone permissions

### Debug Mode
```bash
# Enable comprehensive logging
python main.py --debug

# Or set environment variable
set LOG_LEVEL=DEBUG
python main.py
```

## 🔐 Security Considerations

- API keys are stored in environment variables or secure config files
- Audio data is processed locally by default (Whisper local models)
- Cloud STT services can be disabled for maximum privacy
- No audio data is permanently stored

## 🚀 Performance Optimization

### For Low Latency (<200ms)
```json
{
  "audio": {
    "chunk_size": 512,
    "sample_rate": 16000
  },
  "stt": {
    "whisper": {
      "model_size": "tiny",
      "fp16": true
    }
  }
}
```

### For High Accuracy
```json
{
  "audio": {
    "chunk_size": 2048
  },
  "stt": {
    "whisper": {
      "model_size": "large",
      "beam_size": 10
    }
  }
}
```

## 🤝 Contributing

We welcome contributions! Areas where help is needed:

- 🎯 **Additional STT engines** (AssemblyAI, Rev.ai, etc.)
- 🔧 **Audio preprocessing** (noise reduction, normalization)
- 📱 **Cross-platform support** (macOS, Linux)
- 🧪 **Testing frameworks** (automated audio testing)
- 📚 **Documentation** (tutorials, examples)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Anthropic** for Claude and the Model Context Protocol
- **OpenAI** for Whisper speech recognition
- **Python Audio Community** for excellent libraries
- **FastMCP** for the high-level MCP framework

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/joelfuller2016/claude-desktop-realtime-audio-mcp-python/issues)
- **Discussions**: [GitHub Discussions](https://github.com/joelfuller2016/claude-desktop-realtime-audio-mcp-python/discussions)
- **Documentation**: [Wiki](https://github.com/joelfuller2016/claude-desktop-realtime-audio-mcp-python/wiki)

---

**⭐ Star this repository if you find it useful!**

*This Python implementation provides a more maintainable and feature-rich alternative to the original TypeScript version, with better audio processing capabilities and easier extensibility.*