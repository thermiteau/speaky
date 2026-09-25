---
title: Configuration
scope: component
relates-to: [architecture.md, cache-system.md, tts-integration.md]
last-verified: 2026-03-11
---

## Overview

`config.py` has two responsibilities: resolving the platform-appropriate cache directory and assembling the configuration dict that the TTS module consumes. All TTS parameters except the API key are hard-coded constants in `load_config`.

## Environment Variables

| Variable | Required | Description |
| --- | --- | --- |
| `OPENAI_API_KEY` | Yes | OpenAI API key used to authenticate TTS requests |

No other environment variables are read. `load_dotenv()` is called at the start of `load_config()`, which loads a `.env` file from the current working directory (or any parent directory) into `os.environ` before `os.getenv` is called.

If `OPENAI_API_KEY` is absent or an empty string, `load_config` raises `ValueError` with the message:

```
OPENAI_API_KEY not found in environment variables. Please add your OpenAI API key to .env file or environment variables.
```

## Configuration Dict

`load_config()` returns a plain dict. All values except `api_key` are static strings:

| Key | Value | Description |
| --- | --- | --- |
| `api_key` | from `OPENAI_API_KEY` | OpenAI authentication |
| `model` | `"gpt-4o-mini-tts"` | TTS model |
| `voice` | `"nova"` | OpenAI voice name |
| `instructions` | `"Speak in a cheerful, positive yet professional tone."` | Delivery style prompt |
| `response_format` | `"mp3"` | Audio format for API response |

## Cache Directory Resolution

`get_cache_dir()` uses `platformdirs.user_cache_dir("speaky")` to resolve the OS-appropriate cache path, then creates it if it does not exist.

```mermaid
flowchart LR
    A["get_cache_dir()"] --> B["platformdirs.user_cache_dir('speaky')"]
    B --> C["Path(result)"]
    C --> D["mkdir(parents=True, exist_ok=True)"]
    D --> E["return Path"]
```

`get_cache_dir` is called by `cache.py`'s `get_cache_file` and `clear_cache`. It is not called by `load_config`; the two functions in `config.py` are independent.

## .env File

The project includes `example.env` as a template:

```
OPENAI_API_KEY=your key
```

Copy to `.env` in the project root and replace the placeholder value. The `.env` file is listed in `.gitignore` and is not committed.

## Design Decisions

- **Static TTS parameters**: Voice, model, and instructions are not configurable via CLI flags or environment variables. They are constants in `load_config`. This simplifies the interface for the primary use case (scripted notifications) but requires a code change to alter voice behaviour.
- **`load_dotenv` on every call**: `load_config` calls `load_dotenv()` each time it is invoked. For a CLI that runs once per invocation this has no practical cost. It ensures the `.env` file is always loaded even when the module is imported in test contexts without prior setup.
- **`platformdirs` over hard-coded paths**: Avoids per-OS conditional logic in the application. `platformdirs` correctly handles XDG_CACHE_HOME overrides on Linux when set.
