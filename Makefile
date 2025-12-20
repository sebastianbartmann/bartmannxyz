.PHONY: run sync clean

run:
	cd app && uv run uvicorn main:app --host 127.0.0.1 --port 2000 --reload

sync:
	cd app && uv sync

clean:
	cd app && rm -rf .venv
	cd app && rm -f uv.lock
