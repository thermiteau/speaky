---
title: Linting — Project Implementation
topic: linting
last-verified: 2026-03-11
status: recommended
---

## Stack

No linter or formatter is currently configured. The recommended tool is Ruff, which provides both linting and formatting in a single fast binary. It supports Python 3.10 (the project's target version) and requires only a `[tool.ruff]` section in the existing `pyproject.toml` — no additional config files needed.

## Configuration

Add a `[tool.ruff]` section to `pyproject.toml` with `target-version = "py310"` and a sensible rule set (at minimum: `E`, `F`, `W`, `I` for import sorting). Add `ruff` to the `[project.optional-dependencies]` test group alongside pytest. No separate `.ruff.toml` file is needed for a project of this size.

## Patterns

Run `ruff check` for linting and `ruff format` for formatting. Both commands should be added to the GitHub Actions CI workflow in `.github/workflows/build.yml` as steps before the pytest run. Developers should run `ruff check --fix` locally before committing to auto-fix import ordering and simple lint issues.

## File Locations

- `pyproject.toml` — add `[tool.ruff]` configuration section
- `.github/workflows/build.yml` — add linting step to CI pipeline
