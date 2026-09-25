---
title: Testing
scope: component
relates-to: [architecture.md, cli.md, cache-system.md, tts-integration.md, audio-playback.md, configuration.md]
last-verified: 2026-03-11
---

## Overview

The test suite covers all five modules using `pytest` with `pytest-asyncio` for async tests. All external I/O (OpenAI API, VLC, filesystem via `get_cache_dir`) is mocked; no real API calls or audio output occur during tests.

## Test Structure

| Test file | Module under test | Key concerns |
| --- | --- | --- |
| `tests/test_main.py` | `speaky.main` | Argument parsing, orchestration flow, error exit codes, KeyboardInterrupt |
| `tests/test_cache.py` | `speaky.cache` | MD5 key determinism, file path construction, cache clearing |
| `tests/test_config.py` | `speaky.config` | Directory creation, API key validation, config dict contents |
| `tests/test_tts.py` | `speaky.tts` | Cache hit short-circuit, streaming write, API error propagation |
| `tests/test_audio.py` | `speaky.audio` | VLC lifecycle (play/poll/stop/release), state transitions, error handling |

## Configuration

`pytest.ini` sets:

- `testpaths = tests`
- `asyncio_mode = auto` — all `async def` test functions run under `pytest-asyncio` without explicit decorators
- `addopts = -v --tb=short`

The optional test dependencies (`pytest >= 7.0.0`, `pytest-asyncio >= 0.21.0`) are declared under `[project.optional-dependencies] test` in `pyproject.toml` and installed with `uv sync --extra test`.

## Mocking Patterns

**VLC**: `@patch('speaky.audio.vlc')` replaces the entire `vlc` module. `mock_vlc.MediaPlayer.return_value` is a `MagicMock` that exposes `play`, `get_state`, `stop`, and `release`. State sequence is controlled via `side_effect`.

**OpenAI client**: `@patch('speaky.tts.AsyncOpenAI')` replaces the client class. The streaming context manager is simulated with `@asynccontextmanager` returning a mock response whose `iter_bytes` is an async generator.

**Filesystem**: `@patch('speaky.cache.get_cache_dir')` redirects cache operations to a `tempfile.TemporaryDirectory`, so no files are written to the real cache.

**Environment variables**: `@patch.dict(os.environ, {'OPENAI_API_KEY': 'test-api-key'})` injects values without affecting the host environment.

## CI Execution

The GitHub Actions workflow (`build.yml`) runs tests on every push to `main` or `develop`:

1. Checks out the repository
2. Sets up Python using the version in `.python-version` (3.10)
3. Installs system dependencies: `vlc`, `libasound2-dev`, `portaudio19-dev`
4. Installs `uv` 0.7.20
5. Runs `uv sync --extra test` to install application and test dependencies
6. Runs `uv run pytest --tb=short`

The `OPENAI_API_KEY` secret is injected from the repository environment (`prd` for `main`, `dev` for `develop`). Tests mock the API, so the key is present in the environment but not actually used during test execution.
