---
title: Logging — Project Implementation
topic: logging
last-verified: 2026-03-11
status: recommended
---

## Stack

No logging library is currently used. The codebase uses bare `print()` statements with emoji indicators for user-facing output and error messages. The recommended library is Python's built-in `logging` module, which requires no additional dependencies and fits the project's minimal dependency approach.

## Configuration

Logging should be configured in `speaky/config.py` alongside existing environment variable handling. A single `logging.basicConfig()` call at module level should set the default level from a `SPEAKY_LOG_LEVEL` environment variable (defaulting to `WARNING`). User-facing output (cache hits, playback status) should remain as `print()` statements since they are intentional CLI output, not log messages. Diagnostic and error information should use the logging module.

## Patterns

Replace internal diagnostic `print()` calls in `audio.py` and `cache.py` with `logger.error()` or `logger.info()` calls. Each module should create its own logger with `logging.getLogger(__name__)`. User-facing status messages in `main.py` (cache cleared confirmation, error summaries) should remain as `print()` since they are part of the CLI interface.

## File Locations

- `speaky/config.py` — logging configuration and initialization
- `speaky/audio.py` — error logging for VLC playback failures (lines 33-34)
- `speaky/cache.py` — status logging for cache operations (line 26)
- `speaky/main.py` — CLI output remains as print statements (lines 57-73)
