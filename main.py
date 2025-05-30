#!/usr/bin/env python3
"""
Claude Desktop Real-time Audio MCP Server (Python Implementation)

A FastMCP-based server that provides real-time microphone input capabilities
for Claude Desktop on Windows using WASAPI audio capture and multiple
speech-to-text engines.

Author: Joel Fuller
License: MIT
"""

import asyncio
import argparse
import logging
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List

# Core MCP and FastMCP imports
from mcp.server.fastmcp import FastMCP, Context
from mcp.server.fastmcp.resources import Resource

# Local imports
from src.audio.capture import AudioCapture, AudioDevice
from src.audio.vad import VoiceActivityDetector
from src.stt.engine_manager import STTEngineManager
from src.config.manager import ConfigManager
from src.utils.logger import setup_logger
from src.utils.exceptions import AudioCaptureError, STTError

# Initialize FastMCP server
mcp = FastMCP(
    name="claude-audio-mcp",
    description="Real-time microphone input MCP server for Claude Desktop",
    version="1.0.0"
)

# Global components
config_manager: Optional[ConfigManager] = None
audio_capture: Optional[AudioCapture] = None
vad: Optional[VoiceActivityDetector] = None
stt_manager: Optional[STTEngineManager] = None
logger: Optional[logging.Logger] = None

# Recording state
is_recording = False
recording_task: Optional[asyncio.Task] = None


async def initialize_components():
    """Initialize all components with proper error handling."""
    global config_manager, audio_capture, vad, stt_manager, logger
    
    try:
        # Initialize configuration manager
        config_manager = ConfigManager()
        await config_manager.load_config()
        
        # Setup logger
        logger = setup_logger(
            name="claude-audio-mcp",
            level=config_manager.get("logging.level", "INFO"),
            log_file=config_manager.get("logging.file")
        )
        
        logger.info("Initializing Claude Desktop Audio MCP Server...")
        
        # Initialize audio capture
        audio_config = config_manager.get("audio", {})
        audio_capture = AudioCapture(
            sample_rate=audio_config.get("sample_rate", 16000),
            channels=audio_config.get("channels", 1),
            chunk_size=audio_config.get("chunk_size", 1024),
            device_id=audio_config.get("device_id"),
            low_latency=audio_config.get("low_latency", True)
        )
        
        # Initialize voice activity detection
        vad_config = config_manager.get("vad", {})
        vad = VoiceActivityDetector(
            mode=vad_config.get("mode", "hybrid"),
            aggressiveness=vad_config.get("webrtc_aggressiveness", 2),
            energy_threshold=vad_config.get("energy_threshold", 0.01)
        )
        
        # Initialize STT engine manager
        stt_config = config_manager.get("stt", {})
        stt_manager = STTEngineManager(stt_config)
        await stt_manager.initialize()
        
        logger.info("All components initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize components: {e}")
        raise


@mcp.tool()
async def start_recording() -> str:
    """Start real-time audio capture and speech recognition."""
    global is_recording, recording_task
    
    if is_recording:
        return "Recording is already active"
    
    try:
        logger.info("Starting audio recording...")
        is_recording = True
        recording_task = asyncio.create_task(recording_loop())
        return "Audio recording started successfully"
    except Exception as e:
        is_recording = False
        logger.error(f"Failed to start recording: {e}")
        return f"Failed to start recording: {str(e)}"


@mcp.tool()
async def stop_recording() -> str:
    """Stop audio capture and speech recognition."""
    global is_recording, recording_task
    
    if not is_recording:
        return "Recording is not active"
    
    try:
        logger.info("Stopping audio recording...")
        is_recording = False
        
        if recording_task:
            recording_task.cancel()
            try:
                await recording_task
            except asyncio.CancelledError:
                pass
            recording_task = None
        
        audio_capture.stop()
        return "Audio recording stopped successfully"
    except Exception as e:
        logger.error(f"Failed to stop recording: {e}")
        return f"Failed to stop recording: {str(e)}"


@mcp.tool()
async def get_recording_status() -> Dict[str, Any]:
    """Get current recording status and configuration."""
    status = {
        "is_recording": is_recording,
        "audio_config": {
            "sample_rate": audio_capture.sample_rate if audio_capture else None,
            "channels": audio_capture.channels if audio_capture else None,
            "chunk_size": audio_capture.chunk_size if audio_capture else None,
            "device_id": audio_capture.device_id if audio_capture else None,
        },
        "stt_engine": stt_manager.current_engine if stt_manager else None,
        "available_engines": list(stt_manager.available_engines.keys()) if stt_manager else [],
    }
    return status


@mcp.tool()
async def list_audio_devices() -> List[Dict[str, Any]]:
    """List all available audio input devices."""
    try:
        devices = audio_capture.list_devices()
        return [
            {
                "id": device.id,
                "name": device.name,
                "channels": device.max_input_channels,
                "sample_rate": device.default_sample_rate,
                "is_default": device.is_default
            }
            for device in devices
            if device.max_input_channels > 0  # Only input devices
        ]
    except Exception as e:
        logger.error(f"Failed to list audio devices: {e}")
        return []


@mcp.tool()
async def set_audio_device(device_id: int) -> str:
    """Set the audio input device."""
    try:
        audio_capture.set_device(device_id)
        config_manager.set("audio.device_id", device_id)
        await config_manager.save_config()
        return f"Audio device set to device ID {device_id}"
    except Exception as e:
        logger.error(f"Failed to set audio device: {e}")
        return f"Failed to set audio device: {str(e)}"


@mcp.tool()
async def set_stt_engine(engine: str) -> str:
    """Set the speech-to-text engine (whisper, azure, google)."""
    try:
        await stt_manager.set_engine(engine)
        config_manager.set("stt.default_engine", engine)
        await config_manager.save_config()
        return f"STT engine set to {engine}"
    except Exception as e:
        logger.error(f"Failed to set STT engine: {e}")
        return f"Failed to set STT engine: {str(e)}"


@mcp.tool()
async def test_audio_capture(duration: float = 3.0) -> str:
    """Test audio capture for a specified duration."""
    try:
        logger.info(f"Testing audio capture for {duration} seconds...")
        test_data = audio_capture.test_capture(duration)
        
        # Basic audio analysis
        import numpy as np
        peak_level = np.max(np.abs(test_data))
        rms_level = np.sqrt(np.mean(test_data**2))
        
        return f"Audio test completed. Peak: {peak_level:.3f}, RMS: {rms_level:.3f}"
    except Exception as e:
        logger.error(f"Audio test failed: {e}")
        return f"Audio test failed: {str(e)}"


@mcp.resource("audio://devices")
async def get_audio_devices() -> Resource:
    """Resource providing available audio devices."""
    devices = await list_audio_devices()
    return Resource(
        uri="audio://devices",
        name="Available Audio Devices",
        description="List of available audio input devices",
        mimeType="application/json",
        text=str(devices)
    )


@mcp.resource("audio://config")
async def get_audio_config() -> Resource:
    """Resource providing current audio configuration."""
    config = config_manager.get("audio", {}) if config_manager else {}
    return Resource(
        uri="audio://config",
        name="Audio Configuration",
        description="Current audio capture configuration",
        mimeType="application/json",
        text=str(config)
    )


@mcp.resource("stt://engines")
async def get_stt_engines() -> Resource:
    """Resource providing STT engines status."""
    if not stt_manager:
        engines_info = {"error": "STT manager not initialized"}
    else:
        engines_info = {
            "current_engine": stt_manager.current_engine,
            "available_engines": list(stt_manager.available_engines.keys()),
            "engine_status": await stt_manager.get_engines_status()
        }
    
    return Resource(
        uri="stt://engines",
        name="STT Engines Status",
        description="Status of speech-to-text engines",
        mimeType="application/json",
        text=str(engines_info)
    )


async def recording_loop():
    """Main recording loop that captures audio and processes speech."""
    logger.info("Starting recording loop...")
    
    try:
        audio_stream = audio_capture.start_stream()
        
        async for audio_chunk in audio_stream:
            if not is_recording:
                break
            
            # Voice activity detection
            has_speech = vad.detect_speech(audio_chunk)
            
            if has_speech:
                logger.debug("Speech detected, processing...")
                
                # Speech-to-text processing
                try:
                    text = await stt_manager.transcribe(audio_chunk)
                    if text.strip():
                        logger.info(f"Transcribed: {text}")
                        # Here you would send the text to Claude Desktop
                        # This is handled by the MCP protocol automatically
                        
                except STTError as e:
                    logger.error(f"STT processing failed: {e}")
                    
    except AudioCaptureError as e:
        logger.error(f"Audio capture error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error in recording loop: {e}")
    finally:
        logger.info("Recording loop stopped")


async def shutdown():
    """Cleanup function called on server shutdown."""
    global is_recording
    
    logger.info("Shutting down server...")
    
    # Stop recording if active
    if is_recording:
        await stop_recording()
    
    # Cleanup components
    if audio_capture:
        audio_capture.cleanup()
    
    if stt_manager:
        await stt_manager.cleanup()
    
    logger.info("Server shutdown complete")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Claude Desktop Real-time Audio MCP Server"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )
    parser.add_argument(
        "--config",
        type=str,
        help="Path to configuration file"
    )
    
    args = parser.parse_args()
    
    # Setup basic logging before component initialization
    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Initialize components
    try:
        asyncio.run(initialize_components())
    except Exception as e:
        logging.error(f"Failed to initialize server: {e}")
        sys.exit(1)
    
    # Register shutdown handler
    import signal
    
    def signal_handler(sig, frame):
        asyncio.create_task(shutdown())
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Run the MCP server
    try:
        mcp.run()
    except KeyboardInterrupt:
        asyncio.run(shutdown())
    except Exception as e:
        logging.error(f"Server error: {e}")
        asyncio.run(shutdown())
        sys.exit(1)


if __name__ == "__main__":
    main()