"""Cache management for audio files."""

import hashlib
from pathlib import Path
from .config import get_cache_dir


def generate_cache_key(text: str, voice: str, instructions: str) -> str:
    """Generate MD5 hash for cache key."""
    cache_string = f"{text}::{voice}::{instructions}"
    return hashlib.md5(cache_string.encode()).hexdigest()


def get_cache_file(text: str, voice: str, instructions: str) -> Path:
    """Get cache file path for given parameters."""
    cache_key = generate_cache_key(text, voice, instructions)
    cache_dir = get_cache_dir()
    return cache_dir / f"{cache_key}.mp3"


def clear_cache():
    """Clear all cached audio files."""
    cache_dir = get_cache_dir()
    for cache_file in cache_dir.glob("*.mp3"):
        cache_file.unlink()
    print(f"✅ Cleared cache directory: {cache_dir}")