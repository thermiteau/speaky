"""Configuration management for Speaky."""

import json
import os
from pathlib import Path
from dotenv import load_dotenv
import platformdirs

USER_CONFIG_PATH = Path.home() / ".speaky.json"

DEFAULT_CONFIG = {
    "model": "gpt-4o-mini-tts",
    "voice": "nova",
    "instructions": "Speak in a cheerful, positive yet professional tone.",
    "response_format": "mp3",
}


def get_cache_dir() -> Path:
    """Get platform-appropriate cache directory."""
    cache_dir = Path(platformdirs.user_cache_dir("speaky"))
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


def install_default_config():
    """Copy default config to user's home directory if it doesn't exist."""
    if not USER_CONFIG_PATH.exists():
        USER_CONFIG_PATH.write_text(json.dumps(DEFAULT_CONFIG, indent=2) + "\n")


def load_config():
    """Load configuration from ~/.speaky.json with defaults, plus env vars."""
    api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key:
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY not found in environment variables. "
            "Please add your OpenAI API key to .env file or environment variables."
        )

    config = dict(DEFAULT_CONFIG)

    if USER_CONFIG_PATH.exists():
        user_config = json.loads(USER_CONFIG_PATH.read_text())
        config.update(user_config)

    config["api_key"] = api_key
    return config
