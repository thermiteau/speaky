---
title: Unit Testing — Project Implementation
topic: unit-testing
last-verified: 2026-03-11
---

## Stack

pytest 7.0+ with pytest-asyncio 0.21+ for async test support. Mocking is handled by the standard library's `unittest.mock` module. Both testing dependencies are declared as optional extras under the `[test]` group in `pyproject.toml`.

## Configuration

pytest is configured via `pytest.ini` at the project root. Test discovery uses the `testpaths = tests` directive with `python_files = test_*.py` pattern. Output is set to verbose (`-v`) with short tracebacks (`--tb=short`). The asyncio mode is set to `auto` via `asyncio_mode = auto` enabling automatic detection of async test functions without explicit markers on every test.

## Patterns

Tests are organized by module — each source file in `speaky/` has a corresponding `test_<module>.py` file in `tests/`. Test classes use the `Test*` naming convention to group related tests. External dependencies (OpenAI API, VLC player, filesystem, environment variables) are mocked using `@patch` decorators and `MagicMock`/`AsyncMock` objects. Async functions are tested with `@pytest.mark.asyncio` and `AsyncMock` for coroutine mocking. Integration tests exist within `test_main.py` as a `TestIntegration` class that tests the full workflow from argument parsing through audio generation to playback.

## File Locations

- `pytest.ini` — pytest configuration
- `pyproject.toml` — test dependencies under `[project.optional-dependencies.test]`
- `tests/test_main.py` — CLI entry point and integration tests
- `tests/test_config.py` — configuration module tests
- `tests/test_tts.py` — TTS API integration tests
- `tests/test_cache.py` — cache system tests
- `tests/test_audio.py` — audio playback tests
