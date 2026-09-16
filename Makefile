install:
	uv sync
	UV_SKIP_WHEEL_FILENAME_CHECK=1 uv pip install mazegenerator-00001-py3-none-any.whl

run:
	uv run python pac-man.py config.json

debug:
	python -m pdb pac-man.py config.json

clean:
	rm -rf *.pyc __pycache__ .mypy_cache

fclean: clean
	rm -fr build dist .venv highscores.json

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
	@rm -fr build

zip: package
	@echo "==> Creating release zip..."
	@rm -rf zip_package pac-man-release.zip
	@mkdir -p zip_package
	@cp config.json INSTRUCTIONS.txt dist/pac-man zip_package/
	@echo '#!/bin/bash' > zip_package/run.sh
	@echo 'DIR="$$(cd "$$(dirname "$$0")" && pwd)"' >> zip_package/run.sh
	@echo 'chmod +x "$$DIR/pac-man"' >> zip_package/run.sh
	@echo 'exec "$$DIR/pac-man" "$$DIR/config.json" "$$@"' >> zip_package/run.sh
	@chmod +x zip_package/pac-man zip_package/run.sh
	@cd zip_package && zip -q -r ../pac-man-release.zip pac-man run.sh config.json INSTRUCTIONS.txt
	@rm -rf zip_package
	@echo "==> Package ready: pac-man-release.zip"
