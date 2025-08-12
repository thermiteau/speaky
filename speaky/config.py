"""Configuration management for Speaky."""

import os
from pathlib import Path
from dotenv import load_dotenv
import platformdirs


def get_cache_dir() -> Path:
    """Get platform-appropriate cache directory."""
    cache_dir = Path(platformdirs.user_cache_dir("speaky"))
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


def load_config():
    """Load configuration from environment variables."""
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY not found in environment variables. "
            "Please add your OpenAI API key to .env file or environment variables."
        )
    
    return {
        "api_key": api_key,
        "model": "gpt-4o-mini-tts",
        "voice": "nova",
        "instructions": "Speak in a cheerful, positive yet professional tone.",
        "response_format": "mp3"
    }