#!/bin/bash

cd /home/developer/projects/speaky/
uv run --script /home/developer/projects/speaky/main.py "$@"
cd -
