#!/usr/bin/env bash
pip install mypy black pytest
black . --check
mypy .
pytest .