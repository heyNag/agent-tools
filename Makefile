.PHONY: test syntax install install-dry-run groq-test mcp-build ci-local

AUDIO ?=
PYTHON ?= $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)

test:
	$(PYTHON) -m pytest

syntax:
	$(PYTHON) -m py_compile packages/watch-video/scripts/*.py

install:
	./scripts/install-all.sh

install-dry-run:
	DRY_RUN=1 ./scripts/install-all.sh

groq-test:
	@if [ -z "$(AUDIO)" ]; then \
		echo "usage: make groq-test AUDIO=path/to/audio.mp3"; \
		exit 2; \
	fi
	./scripts/test-groq.sh "$(AUDIO)"

mcp-build:
	npm --prefix mcp/watch-video ci
	npm --prefix mcp/watch-video run build

ci-local: test syntax mcp-build install-dry-run
