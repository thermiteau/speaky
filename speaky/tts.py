"""OpenAI TTS integration."""

from openai import AsyncOpenAI
from .cache import get_cache_file


async def generate_and_cache_audio(text: str, config: dict):
    """Generate audio using OpenAI TTS and save to cache."""
    cache_file = get_cache_file(text, config["voice"], config["instructions"])
    
    # Return cached file if exists
    if cache_file.exists():
        return cache_file
    
    # Generate new audio
    openai = AsyncOpenAI(api_key=config["api_key"])
    
    async with openai.audio.speech.with_streaming_response.create(
        model=config["model"],
        voice=config["voice"],
        input=text,
        instructions=config["instructions"],
        response_format=config["response_format"],
    ) as response:
        # Save to cache file
        with open(cache_file, "wb") as f:
            async for chunk in response.iter_bytes():
                f.write(chunk)
    
    return cache_file