.PHONY: check lint format-check typecheck test

check: lint format-check typecheck test

lint:
	uv run ruff check .

format-check:
	uv run ruff format --check .

typecheck:
	uv run mypy

test:
	uv run pytest
