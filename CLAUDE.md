# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Speaky is a Python command-line text-to-speech application that uses OpenAI's TTS API. It's structured as a proper Python package with modular components and cross-platform compatibility.

## Development Setup

This project uses UV for Python package management and execution, but can also be installed via standard pip.

### Required Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key (see `example.env` for template)

### Key Commands

**Install in development mode:**
```bash
# Using UV
uv pip install -e .

# Using pip
pip install -e .
```

**Run the application:**
```bash
# After installation, use the console script
speaky "your text here"

# Development mode with UV
uv run speaky "your text here"

# Clear cache
speaky --clear-cache
```

**Install dependencies:**
```bash
uv sync
```

## Architecture

### Package Structure
```
speaky/
├── speaky/
│   ├── __init__.py      # Package initialization
│   ├── main.py          # CLI entry point and argument parsing
│   ├── config.py        # Configuration and environment management
│   ├── cache.py         # Cross-platform cache management
│   ├── tts.py           # OpenAI TTS integration
│   └── audio.py         # VLC audio playback
└── main_old.py          # Original single-file version (backup)
```

### Core Components

- **config.py**: Handles environment variables, platform-specific cache directories using `platformdirs`
- **cache.py**: MD5-based cache key generation and cross-platform cache directory management
- **tts.py**: OpenAI TTS API integration with streaming response handling
- **audio.py**: VLC-based audio playback with error handling
- **main.py**: Command-line interface with argparse, console script entry point

### Key Functions

- `get_cache_dir()`: Returns platform-appropriate cache directory (~/.cache/speaky on Linux/macOS)
- `generate_and_cache_audio()`: Handles TTS generation and file caching
- `play_audio_file()`: VLC audio playback with proper state management
- `cli_main()`: Console script entry point for package installation

### Cache System

- Cross-platform cache directory using `platformdirs`
- Cache keys are MD5 hashes of: `{text}::{voice}::{instructions}`
- Cache clearing functionality via `--clear-cache` option
- Uses `.mp3` format for cached audio files

### Dependencies

- `openai[voice-helpers]`: TTS API and audio streaming
- `platformdirs`: Cross-platform cache directory handling
- `python-vlc`: Audio playback
- `pyaudio`: Audio system interface
- `pyttsx3`: Text-to-speech fallback
- `load-dotenv`: Environment variable management

## Installation and Distribution

The package includes a console script entry point (`speaky = "speaky.main:cli_main"`) for proper CLI installation. Users can install with `pip install .` or `uv pip install .` and then use `speaky` command globally.

## Voice Configuration

Currently configured to use:
- Voice: "nova"
- Model: "gpt-4o-mini-tts" 
- Instructions: "Speak in a cheerful, positive yet professional tone."
- Format: MP3