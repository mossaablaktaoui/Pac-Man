install:
	uv sync
	UV_SKIP_WHEEL_FILENAME_CHECK=1 uv pip install mazegenerator-00001-py3-none-any.whl

run:
	uv run python pac-man.py config.json

debug:
	python -m pdb pac-man.py config.json

test:
	uv run python -m unittest discover -s tests -v

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

package:
	@echo "==> Building standalone executable..."
	uv run pyinstaller --clean pac-man.spec
	@echo "==> Generating run.sh on the fly..."
	@echo '#!/bin/bash' > dist/run.sh
	@echo 'DIR="$$(cd "$$(dirname "$$0")" && pwd)"' >> dist/run.sh
	@echo 'chmod +x "$$DIR/pac-man"' >> dist/run.sh
	@echo 'exec "$$DIR/pac-man" "$$DIR/config.json" "$$@"' >> dist/run.sh
	@echo "==> Copying config and instructions..."
	cp config.json dist/
	cp INSTRUCTIONS.txt dist/
	chmod +x dist/pac-man dist/run.sh
	@echo "==> Creating release zip..."
	cd dist && zip -q -r pac-man-release.zip pac-man run.sh config.json instruction.txt
	@echo "==> Package ready: dist/pac-man-release.zip"

.PHONY: install run debug test clean lint lint-strict
