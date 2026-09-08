install:
	uv sync

run:
	uv run python pac-man.py config.json

debug:
	python -m pdb pac-man.py config.json

clean:
	rm -rf *.pyc __pycache__ .mypy_cache

lint:
	uv run flake8 .
	uv run mypy . --warn-return-any --warn-unused-ignores \
	--ignore-missing-imports --disallow-untyped-defs \
	--check-untyped-defs

lint-strict:
	uv run flake8 .
	uv run mypy . --strict

.PHONY: install run clean debug lint
