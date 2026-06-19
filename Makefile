.PHONY: test syntax install install-dry-run groq-test mcp-build build-claude-plugin build-codex-skill build-packages verify-packages ci-local

AUDIO ?=
PYTHON ?= python3

test:
	$(PYTHON) -m unittest discover -s packages/watch-video/tests -p 'test_*.py'

syntax:
	python3 -m py_compile packages/watch-video/scripts/*.py
	bash -n scripts/*.sh

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
	npm --prefix mcp/watch-video run build

build-claude-plugin:
	./scripts/build-claude-plugin.sh

build-codex-skill:
	./scripts/build-codex-skill.sh

build-packages:
	./scripts/build-packages.sh

verify-packages:
	./scripts/verify-packages.sh

ci-local: test syntax mcp-build build-packages verify-packages install-dry-run
