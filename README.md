# Speaky

A fast, cross-platform command-line text-to-speech application powered by OpenAI's TTS API with intelligent caching for optimal performance.

## Features

- **High-Quality Voice Synthesis**: Uses OpenAI's `gpt-4o-mini-tts` model with natural-sounding voices
- **Intelligent Caching**: Automatically caches generated audio files to avoid redundant API calls
- **Cross-Platform**: Works on Windows, macOS, and Linux with platform-appropriate cache directories
- **Simple CLI**: Easy-to-use command-line interface with minimal setup
- **Fast Playback**: Uses VLC for reliable audio playback across all platforms

## Quick Start

### Prerequisites

- **Python 3.10+**: Modern Python installation
- **VLC Media Player**: Required for audio playback
  - **Windows**: Download from [videolan.org](https://www.videolan.org/vlc/)
  - **macOS**: `brew install vlc` or download from website
  - **Linux**: `sudo apt install vlc` (Ubuntu/Debian) or equivalent
- **OpenAI API Key**: Get one from [platform.openai.com](https://platform.openai.com/api-keys)

### Installation

#### Option 1: Install as Global Tool (Recommended)
```bash
# Clone the repository
git clone https://github.com/your-username/speaky.git
cd speaky

# Install globally with UV
uv tool install .

# Or install with pipx
pipx install .
```

#### Option 2: Development Installation
```bash
# Clone and install in development mode
git clone https://github.com/your-username/speaky.git
cd speaky
uv pip install -e .

# Or with pip
pip install -e .
```

### Configuration

1. **Set up your OpenAI API key** (choose one method):

   **Environment variable:**
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

   **Or create a `.env` file:**
   ```bash
   cp example.env .env
   # Edit .env and add your API key
   ```

2. **Verify installation:**
   ```bash
   speaky "Hello, world!"
   ```

## Usage

### Basic Usage

```bash
# Speak some text
speaky "Hello, this is a test of the text-to-speech system."

# Multiple words (automatically joined)
speaky Hello world, this is speaky!

# Longer text
speaky "The quick brown fox jumps over the lazy dog. This sentence contains every letter of the alphabet."
```

### Command Options

```bash
# Clear the audio cache
speaky --clear-cache

# Get help
speaky --help
```
## How It Works

1. **Input Processing**: Takes your text input from command line arguments
2. **Cache Check**: Generates MD5 hash of text + voice + instructions to check for cached audio
3. **Audio Generation**: If not cached, calls OpenAI's TTS API to generate high-quality audio
4. **Caching**: Saves the generated audio file to platform-appropriate cache directory
5. **Playback**: Uses VLC to play the audio with proper state management

### Cache Locations

Speaky automatically stores cached audio files in platform-appropriate locations:

- **Linux**: `~/.cache/speaky/`
- **macOS**: `~/Library/Caches/speaky/`
- **Windows**: `%LOCALAPPDATA%\speaky\cache\`

## Voice Configuration

Currently configured with:
- **Voice**: Nova (cheerful, professional tone)
- **Model**: gpt-4o-mini-tts
- **Format**: MP3
- **Instructions**: "Speak in a cheerful, positive yet professional tone"

## Development

### Project Structure

```
speaky/
  speaky/              # Main package
      __init__.py     # Package initialization
      main.py         # CLI entry point
      config.py       # Configuration management
      cache.py        # Cache system
      tts.py          # OpenAI TTS integration
      audio.py        # VLC audio playback
   tests/              # Test suite
   pyproject.toml      # Project configuration
   pytest.ini         # Test configuration
   README.md          # This file
```

### Setting up Development Environment

```bash
# Clone the repository
git clone https://github.com/your-username/speaky.git
cd speaky

# Install development dependencies
uv sync --extra test

# Run tests
uv run pytest

# Install in development mode
uv pip install -e .
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=speaky

# Run specific test file
uv run pytest tests/test_config.py -v

# Run tests with detailed output
uv run pytest -v --tb=long
```

### Code Quality

```bash
# Run linting (if configured)
uv run ruff check

# Run type checking (if configured)
uv run mypy speaky/
```

## API Usage Costs

Speaky uses OpenAI's TTS API, which charges per character:
- Current pricing: ~$0.015 per 1K characters
- Example: 100 words (~500 characters) H $0.0075
- **Caching minimizes costs** by reusing generated audio for identical text

## Troubleshooting

### Common Issues

**"speaky: command not found"**
- Ensure you've installed with `uv tool install .` or `pipx install .`
- Check that your PATH includes the installation directory

**"OPENAI_API_KEY not found"**
- Set environment variable: `export OPENAI_API_KEY="your-key"`
- Or create `.env` file with your API key

**"VLC not found" or audio playback issues**
- Install VLC Media Player on your system
- Ensure VLC is in your system PATH

**Permission errors on cache directory**
- Check write permissions for cache directory
- Clear cache with `speaky --clear-cache`

**API rate limit errors**
- OpenAI has rate limits; wait a moment and try again
- Caching helps reduce API calls for repeated text

### Getting Help

1. **Check the logs**: Speaky provides helpful error messages
2. **Clear cache**: `speaky --clear-cache` resolves many cache-related issues
3. **Verify dependencies**: Ensure VLC and Python are properly installed
4. **Test API key**: Try a simple request to verify your OpenAI API access

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Your mum

## Changelog

### v0.1.0
- Initial release
- OpenAI TTS integration
- Cross-platform caching
- VLC audio playback
- CLI interface
- Comprehensive test suite