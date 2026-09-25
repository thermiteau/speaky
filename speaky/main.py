"""Main entry point for Speaky CLI."""

import argparse
import asyncio
import sys
from pathlib import Path
from .audio import play_audio_file
from .cache import clear_cache
from .config import load_config
from .tts import generate_and_cache_audio  # type: ignore


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Text-to-speech using OpenAI TTS API", prog="speaky"
    )
    parser.add_argument("text", nargs="*", help="Text to convert to speech")
    parser.add_argument(
        "--f", "--file", dest="file", type=Path, metavar="PATH",
        help="Read text to speak from a UTF-8 text file",
    )
    parser.add_argument(
        "--clear-cache", action="store_true", help="Clear the audio cache and exit"
    )
    parser.add_argument(
        "--s", "--show-output", dest="show_output", action="store_true",
        help="Print the full path to the MP3 file after playback finishes",
    )
    args = parser.parse_args()
    if args.file is not None and args.text:
        parser.error("Use either text arguments or --file, not both")
    return args


async def main():
    """Main async function."""
    args = parse_arguments()

    # Handle cache clearing
    if args.clear_cache:
        clear_cache()
        return

    # Get text input
    if args.file is not None:
        try:
            text = args.file.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as e:
            print(f"Error reading text file '{args.file}': {e}", file=sys.stderr)
            sys.exit(1)
    elif args.text:
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

        if args.show_output:
            print(cache_file.resolve())

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
    install_default_config()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit(1)


if __name__ == "__main__":
    cli_main()
