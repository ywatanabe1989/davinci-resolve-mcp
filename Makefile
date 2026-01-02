# DaVinci Resolve MCP - Makefile
# Run from WSL. For Windows, see 'make help'.

.PHONY: help setup status test clean

help:
	@echo "=============================================="
	@echo "  DaVinci Resolve MCP"
	@echo "=============================================="
	@echo ""
	@echo "WINDOWS SETUP (run in Admin PowerShell):"
	@echo "  cd 'C:\Program Files (x86)\ywatanabe\davinci-resolve-mcp'"
	@echo "  .\scripts\setup\windows_setup.ps1"
	@echo ""
	@echo "WSL COMMANDS:"
	@echo "  make status  - Check system status"
	@echo "  make test    - Run tests"
	@echo "  make clean   - Clear cache"
	@echo ""
	@echo "START MCP SERVER (from WSL):"
	@echo "  python3 mcp-entry --verbose"
	@echo ""

setup:
	@echo "=== Windows Setup Instructions ==="
	@echo ""
	@echo "1. Open Admin PowerShell on Windows"
	@echo "2. Run these commands:"
	@echo ""
	@echo "   cd 'C:\Program Files (x86)\ywatanabe\davinci-resolve-mcp'"
	@echo "   .\scripts\setup\windows_setup.ps1"
	@echo ""
	@echo "3. After setup, reconnect MCP in Claude Code"
	@echo ""

status:
	@./scripts/status.sh 2>/dev/null || echo "Run: make setup"

test:
	@./scripts/run_tests.sh 2>/dev/null || python3 -m pytest tests/ -v

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -name "*.pyc" -delete 2>/dev/null || true
	@echo "Cache cleared"
