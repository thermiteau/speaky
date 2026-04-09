---
title: CI/CD — Project Implementation
topic: cicd
last-verified: 2026-03-11
---

## Stack

GitHub Actions is used as the CI/CD platform. A single workflow file handles build and test for both the main and develop branches.

## Configuration

The workflow is triggered on pushes to `main` and `develop` branches, plus manual dispatch via `workflow_dispatch`. It uses GitHub Environments — `prd` for the main branch and `dev` for the develop branch — to manage secrets and deployment contexts. The `OPENAI_API_KEY` secret is referenced from the environment. Python version is read from the `.python-version` file (currently 3.10). UV version is pinned to 0.7.20 via the `astral-sh/setup-uv@v6` action.

## Patterns

The pipeline runs on `ubuntu-latest` and follows a linear sequence: checkout, Python setup, system dependency installation (VLC, libasound2-dev, portaudio19-dev for audio support), UV setup, dependency installation with test extras (`uv sync --extra test`), and pytest execution (`uv run pytest --tb=short`). System-level audio dependencies are installed via `apt-get` because the project depends on VLC for playback and PortAudio for PyAudio. There is no separate deploy stage — the workflow is build-and-test only.

## File Locations

- `.github/workflows/build.yml` — single CI workflow definition
- `.python-version` — Python version constraint consumed by CI
- `pyproject.toml` — dependency and test extra definitions consumed by `uv sync`
