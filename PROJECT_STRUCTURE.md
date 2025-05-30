# Project Structure

This document outlines the complete project structure for the Claude Desktop Real-time Audio MCP Server.

```
claude-desktop-realtime-audio-mcp-python/
│
├── README.md                   # Project documentation
├── LICENSE                     # MIT License
├── requirements.txt            # Python dependencies
├── config.template.yaml        # Configuration template
├── main.py                     # Main MCP server entry point
│
├── src/                        # Source code directory
│   ├── __init__.py
│   │
│   ├── audio/                  # Audio processing modules
│   │   ├── __init__.py
│   │   ├── capture.py          # Audio capture using sounddevice/WASAPI
│   │   ├── vad.py              # Voice Activity Detection
│   │   ├── preprocessing.py    # Audio preprocessing and filtering
│   │   └── test_setup.py       # Audio setup testing utilities
│   │
│   ├── stt/                    # Speech-to-Text engines
│   │   ├── __init__.py
│   │   ├── engine_manager.py   # STT engine management
│   │   ├── whisper_engine.py   # OpenAI Whisper implementation
│   │   ├── azure_engine.py     # Azure Speech Services
│   │   ├── google_engine.py    # Google Speech-to-Text
│   │   └── benchmark.py        # STT engine benchmarking
│   │
│   ├── config/                 # Configuration management
│   │   ├── __init__.py
│   │   ├── manager.py          # Configuration manager
│   │   └── defaults.py         # Default configuration values
│   │
│   └── utils/                  # Utility modules
│       ├── __init__.py
│       ├── logger.py           # Logging configuration
│       ├── exceptions.py       # Custom exceptions
│       ├── performance.py      # Performance monitoring
│       └── audio_utils.py      # Audio utility functions
│
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── test_audio_capture.py   # Audio capture tests
│   ├── test_vad.py             # Voice activity detection tests
│   ├── test_stt_engines.py     # STT engine tests
│   ├── test_config.py          # Configuration tests
│   └── test_integration.py     # Integration tests
│
├── docs/                       # Documentation
│   ├── installation.md         # Installation guide
│   ├── configuration.md        # Configuration guide
│   ├── troubleshooting.md      # Troubleshooting guide
│   ├── development.md          # Development guide
│   └── api.md                  # API documentation
│
├── examples/                   # Example scripts and configurations
│   ├── basic_usage.py          # Basic usage example
│   ├── advanced_config.yaml    # Advanced configuration example
│   └── claude_desktop_config.json  # Claude Desktop configuration
│
└── scripts/                    # Utility scripts
    ├── setup_dev.py            # Development environment setup
    ├── test_audio.py           # Audio testing script
    └── benchmark_performance.py # Performance benchmarking
```

## Module Descriptions

### Core Modules

- **main.py**: FastMCP server entry point with all MCP tools and resources
- **src/audio/capture.py**: Real-time audio capture using sounddevice and WASAPI
- **src/audio/vad.py**: Voice activity detection using webrtcvad and energy-based methods
- **src/stt/engine_manager.py**: Manages multiple STT engines and handles switching

### Audio Processing

- **src/audio/preprocessing.py**: Audio preprocessing including noise reduction and normalization
- **src/utils/audio_utils.py**: Common audio processing utilities and format conversions

### STT Engines

- **src/stt/whisper_engine.py**: OpenAI Whisper implementation (local and API)
- **src/stt/azure_engine.py**: Azure Speech Services integration
- **src/stt/google_engine.py**: Google Speech-to-Text integration

### Configuration

- **src/config/manager.py**: Configuration management with YAML/JSON support and environment variables
- **config.template.yaml**: Template configuration file with all available options

### Utilities

- **src/utils/logger.py**: Structured logging with performance monitoring
- **src/utils/exceptions.py**: Custom exception classes for different error types
- **src/utils/performance.py**: Performance monitoring and metrics collection

## Development Status

✅ **Completed**:
- Project structure planning
- Main FastMCP server implementation
- Requirements and dependencies
- Configuration template
- Documentation framework

🚧 **In Progress**:
- Audio capture module implementation
- Voice activity detection
- STT engine integrations
- Configuration management

📋 **Planned**:
- Comprehensive testing suite
- Performance optimization
- Cross-platform support
- Advanced audio preprocessing
- Documentation completion

## Getting Started

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `config.template.yaml` to `config.yaml` and customize
4. Run the server: `python main.py`
5. Configure Claude Desktop with the MCP server

For detailed instructions, see the [README.md](README.md) file.