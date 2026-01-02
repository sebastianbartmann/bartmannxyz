.DEFAULT_GOAL := help

.PHONY: help run sync clean

help:
	@printf "Targets:\n"
	@printf "  run   - start the dev server (uvicorn)\n"
	@printf "  sync  - sync python dependencies with uv\n"
	@printf "  clean - remove local venv + uv.lock\n"
	@printf "  help  - show this message\n"

run:
	cd app && uv run uvicorn main:app --host 127.0.0.1 --port 2000 --reload

sync:
	cd app && uv sync

clean:
	cd app && rm -rf .venv
	cd app && rm -f uv.lock
