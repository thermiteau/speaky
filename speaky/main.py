"""Main entry point for Speaky CLI."""

import asyncio
import argparse
import sys
from .config import load_config
from .tts import generate_and_cache_audio
from .audio import play_audio_file
from .cache import clear_cache


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Text-to-speech using OpenAI TTS API",
        prog="speaky"
    )
    parser.add_argument(
        "text",
        nargs="*",
        help="Text to convert to speech"
    )
    parser.add_argument(
        "--clear-cache",
        action="store_true",
        help="Clear the audio cache and exit"
    )
    return parser.parse_args()


async def main():
    """Main async function."""
    args = parse_arguments()
    
    # Handle cache clearing
    if args.clear_cache:
        clear_cache()
        return
    
    # Get text input
    if args.text:
        text = " ".join(args.text)
    else:
        text = "What would you like me to say?"
    
    try:
        # Load configuration
        config = load_config()
        
        # Generate and cache audio
        cache_file = await generate_and_cache_audio(text, config)
        
        # Play audio
        play_audio_file(cache_file)
        
    except ValueError as e:
        print(f"Configuration Error: {e}")
        sys.exit(1)
    except ImportError:
        print("Error: Required package not installed")
        print("Make sure all dependencies are installed.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


def cli_main():
    """Entry point for console script."""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit(1)


if __name__ == "__main__":
    cli_main()