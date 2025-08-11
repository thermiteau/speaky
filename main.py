#!/usr/bin/env -S uv run --script

import asyncio
import hashlib
import os
import sys
import pathlib
import vlc 
from dotenv import load_dotenv
import time

cache_dir = pathlib.Path(__file__).parent.resolve() / "cache"
cache_dir.mkdir(parents=True, exist_ok=True)
        

def play_audio_file(file_path):
    """Play audio file using VLC."""
    player = vlc.MediaPlayer(str(file_path))
    player.play()
    
    # Wait for playback to start
    time.sleep(0.5)
    
    # Wait for playback to finish
    while player.get_state() in [vlc.State.Playing, vlc.State.Opening, vlc.State.Buffering]:
        time.sleep(0.1)
    
    player.stop()
    player.release()
    

async def main():
    # Load environment variables
    load_dotenv()

    # Get API key from environment
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        print("Please add your OpenAI API key to .env file:")
        print("OPENAI_API_KEY=your_api_key_here")
        sys.exit(1)

    try:
        from openai import AsyncOpenAI
        from openai.helpers import LocalAudioPlayer

        # Initialize OpenAI client
        openai = AsyncOpenAI(api_key=api_key)


        # Get text from command line argument or use default
        if len(sys.argv) > 1:
            text = " ".join(sys.argv[1:])  # Join all arguments as text
        else:
            text = "You didnt add any text"
        # Generate hash for the text + voice + instructions combination
        cache_key = hashlib.md5(
            f"{text}::nova::Speak in a cheerful, positive yet professional tone.".encode()
        ).hexdigest()
        cache_file = cache_dir / f"{cache_key}.mp3"

        # Check if cached file exists
        if cache_file.exists():            
            play_audio_file(cache_file)
        else:
            try:
                # Generate audio using OpenAI TTS and save to cache
                async with openai.audio.speech.with_streaming_response.create(
                    model="gpt-4o-mini-tts",
                    voice="nova",
                    input=text,
                    instructions="Speak in a cheerful, positive yet professional tone.",
                    response_format="mp3",
                ) as response:
                    # Save to cache file
                    with open(cache_file, "wb") as f:
                        async for chunk in response.iter_bytes():
                            f.write(chunk)
                    play_audio_file(cache_file)
            except Exception as e:
                print(f"❌ Error: {e}")
    except ImportError:
        print("❌ Error: Required package not installed")
        print("This script uses UV to auto-install dependencies.")
        print("Make sure UV is installed: https://docs.astral.sh/uv/")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

