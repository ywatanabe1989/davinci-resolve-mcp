# DaVinci Resolve MCP Server - Makefile
# Usage: make [target]

.PHONY: all install run test status clean help

# Default target
all: install

# Install dependencies and setup
install:
	@echo "=== DaVinci Resolve MCP Server Setup ==="
	@if [ -f install.sh ]; then \
		./install.sh; \
	elif [ -f install.bat ]; then \
		echo "Run: install.bat (Windows)"; \
	else \
		echo "Creating virtual environment..."; \
		python3 -m venv venv && \
		. venv/bin/activate && \
		pip install -r requirements.txt; \
	fi
	@echo "=== Setup Complete ==="

# Run the MCP server
run:
	@echo "Starting DaVinci Resolve MCP Server..."
	@if [ -f venv/bin/python ]; then \
		venv/bin/python src/main.py; \
	else \
		python3 src/main.py; \
	fi

# Run tests
test:
	@echo "Running tests..."
	@if [ -f venv/bin/pytest ]; then \
		venv/bin/pytest tests/ -v; \
	else \
		pytest tests/ -v; \
	fi

# Show status
status:
	@echo "=== DaVinci Resolve MCP Status ==="
	@echo "Python: $$(python3 --version 2>/dev/null || echo 'Not found')"
	@echo "Venv: $$([ -d venv ] && echo 'OK' || echo 'Not created - run: make install')"
	@echo "DaVinci Resolve: Check if running on Windows host"
	@echo ""
	@echo "Configuration files:"
	@echo "  - .env: $$([ -f .env ] && echo 'OK' || echo 'Missing - copy from .env.example')"
	@echo ""
	@echo "For Claude Code (WSL), add to ~/.claude.json:"
	@echo '  "davinci-resolve": {"command": "'$$(pwd)'/scripts/wsl-launcher.sh"}'

# Clean build artifacts
clean:
	@echo "Cleaning..."
	@rm -rf __pycache__ .pytest_cache *.pyc
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@echo "Done"

# Show help
help:
	@echo "DaVinci Resolve MCP Server"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  install  - Install dependencies (default)"
	@echo "  run      - Start the MCP server"
	@echo "  test     - Run tests"
	@echo "  status   - Show current status and configuration"
	@echo "  clean    - Remove build artifacts"
	@echo "  help     - Show this help"
