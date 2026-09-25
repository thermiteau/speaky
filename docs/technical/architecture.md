---
title: Architecture Overview
scope: architecture
relates-to: [cli.md, configuration.md, cache-system.md, tts-integration.md, audio-playback.md]
last-verified: 2026-03-11
---

## Overview

Speaky is a single-repo Python CLI application that accepts text input, generates MP3 audio via the OpenAI TTS API, caches the result on disk, and plays it back through VLC. The package is distributed as a standard Python package with a registered console script entry point.

## Component Map

```mermaid
flowchart TD
    User["User (CLI)"] -->|"text arguments"| Main["main.py\ncli_main / main"]
    Main -->|"load_config()"| Config["config.py\nConfiguration"]
    Main -->|"generate_and_cache_audio()"| TTS["tts.py\nTTS Integration"]
    Main -->|"play_audio_file()"| Audio["audio.py\nAudio Playback"]
    Main -->|"clear_cache()"| Cache["cache.py\nCache Management"]
    Config -->|"get_cache_dir()"| Cache
    TTS -->|"get_cache_file()"| Cache
    Cache -->|"platformdirs"| FS["Filesystem\n~/.cache/speaky/"]
    TTS -->|"AsyncOpenAI"| OpenAI["OpenAI TTS API\ngpt-4o-mini-tts"]
    Audio -->|"vlc.MediaPlayer"| VLC["VLC Media Player\n(system library)"]
```

## Request Lifecycle

```mermaid
sequenceDiagram
    participant User
    participant CLI as main.py
    participant Config as config.py
    participant Cache as cache.py
    participant TTS as tts.py
    participant API as OpenAI API
    participant Audio as audio.py

    User->>CLI: speaky "text"
    CLI->>Config: load_config()
    Config-->>CLI: {api_key, model, voice, instructions, format}
    CLI->>TTS: generate_and_cache_audio(text, config)
    TTS->>Cache: get_cache_file(text, voice, instructions)
    Cache-->>TTS: Path to .mp3 file
    alt Cache hit
        TTS-->>CLI: cached Path
    else Cache miss
        TTS->>API: audio.speech.with_streaming_response.create(...)
        API-->>TTS: streamed MP3 bytes
        TTS->>Cache: write chunks to disk
        TTS-->>CLI: new Path
    end
    CLI->>Audio: play_audio_file(path)
    Audio->>VLC: MediaPlayer(path).play()
    VLC-->>Audio: playback state polling
    Audio-->>User: audio played
```

## Module Responsibilities

| Module | Responsibility |
| --- | --- |
| `main.py` | Argument parsing, orchestration, error handling, async event loop |
| `config.py` | Environment loading, cache directory resolution, static TTS parameters |
| `cache.py` | Cache key generation (MD5), file path construction, cache clearing |
| `tts.py` | OpenAI API calls, streaming response handling, writing audio to cache |
| `audio.py` | VLC player lifecycle: create, play, poll state, stop, release |

## Entry Point

The package declares a console script in `pyproject.toml`:

```
speaky = "speaky.main:cli_main"
```

`cli_main` wraps `asyncio.run(main())` and catches `KeyboardInterrupt`, mapping it to `sys.exit(1)`. All async I/O (the OpenAI streaming call) runs inside the single event loop created by `asyncio.run`.

## Technology Choices

| Choice | Rationale |
| --- | --- |
| Python 3.10+ | Match system Python on CI (`ubuntu-latest`); sufficient for `str \| Path` union type hints |
| `asyncio` + `AsyncOpenAI` | OpenAI's streaming TTS response is natively async; avoids blocking the process during download |
| `python-vlc` | Thin binding to libVLC; handles MP3 decoding and audio device routing without additional codec dependencies |
| `platformdirs` | Resolves the correct per-OS cache path (`~/.cache/speaky` on Linux/macOS) without hard-coding paths |
| MD5 cache keys | Fast, collision-resistant enough for keying on `text::voice::instructions`; not used for security |
| `load-dotenv` | Allows `OPENAI_API_KEY` to be stored in a `.env` file alongside the project without shell export boilerplate |
| `setuptools` + `wheel` | Standard build backend; compatible with both `pip install` and `uv pip install` |

## Getting Started

Prerequisites: Python 3.10+, `uv` (or `pip`), VLC installed on the host system.

```
uv sync
uv pip install -e .
cp example.env .env   # add OPENAI_API_KEY
speaky "Hello world"
```

Test suite:

```
uv sync --extra test
uv run pytest --tb=short
```
