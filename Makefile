.PHONY: run eval test

run:
	uv run python -m ant_harness

eval:
	uv run python -m pytest tests/ -v --tb=short

test:
	uv run python -m pytest tests/ -v
