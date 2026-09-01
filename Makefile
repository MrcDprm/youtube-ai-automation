# Zero-cost local video production pipeline.
# Works on POSIX and on Windows (Git Bash / MSYS / nmake-free GNU make).

ifeq ($(OS),Windows_NT)
	PY := .venv/Scripts/python.exe
	SYSPY := python
else
	PY := .venv/bin/python
	SYSPY := python3
endif

SCENARIO ?= senaryo.json

.DEFAULT_GOAL := help
.PHONY: help venv install dev font doctor generate validate run dry daily schedule test lint format typecheck check clean

help: ## Show this help.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

venv: ## Create the virtualenv.
	$(SYSPY) -m venv .venv

install: venv ## Install runtime dependencies.
	$(PY) -m pip install --upgrade pip
	$(PY) -m pip install -r requirements.txt

dev: venv ## Install runtime + development dependencies.
	$(PY) -m pip install --upgrade pip
	$(PY) -m pip install -r requirements-dev.txt

font: ## Download the default subtitle/thumbnail font into assets/fonts/.
	$(PY) main.py doctor --fix

doctor: ## Run all preflight checks.
	$(PY) main.py doctor

generate: ## Draft a scenario with a local Ollama model. Usage: make generate TOPIC="konu"
	$(PY) main.py generate "$(TOPIC)" --out $(SCENARIO) --overwrite

validate: ## Validate the scenario file.
	$(PY) main.py validate --scenario $(SCENARIO)

run: ## Render the video (upload obeys the scenario's upload_enabled flag).
	$(PY) main.py run --scenario $(SCENARIO)

dry: ## Print the resolved plan without touching the network.
	$(PY) main.py run --scenario $(SCENARIO) --dry-run

daily: ## Produce at most one video today (inbox first, else next topic).
	$(PY) main.py daily --yes

schedule: ## Register the Windows daily task (09:00, StartWhenAvailable).
	$(PY) main.py schedule

test: ## Run the offline test suite.
	$(PY) -m pytest -q

lint: ## Lint with ruff.
	$(PY) -m ruff check .

format: ## Auto-format with ruff.
	$(PY) -m ruff format .
	$(PY) -m ruff check . --fix

typecheck: ## Type-check with mypy.
	$(PY) -m mypy .

check: lint typecheck test ## Lint, type-check and test.

clean: ## Remove generated output and caches.
	$(PY) main.py clean --all
