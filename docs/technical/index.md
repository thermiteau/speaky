---
title: Technical Documentation Index
scope: architecture
relates-to: []
last-verified: 2026-03-11
---

## Overview

Technical documentation for Speaky, a Python CLI text-to-speech application backed by the OpenAI TTS API.

## Documents

| Document | Description |
| --- | --- |
| [architecture.md](architecture.md) | System architecture overview, component map, request lifecycle, and technology choices |
| [cli.md](cli.md) | CLI argument surface, execution flow, error handling, and entry point registration |
| [configuration.md](configuration.md) | Environment variables, config dict structure, and cache directory resolution |
| [cache-system.md](cache-system.md) | MD5-based cache key generation, file naming, cache lookup flow, and clearing |
| [tts-integration.md](tts-integration.md) | OpenAI TTS API call details, streaming write pattern, and client instantiation |
| [audio-playback.md](audio-playback.md) | VLC player lifecycle, state polling, error handling, and system dependencies |
| [testing.md](testing.md) | Test structure, mocking patterns, pytest configuration, and CI execution |
| [usage-examples.md](usage-examples.md) | CLI, Makefile, and Claude Code hook integration patterns |
