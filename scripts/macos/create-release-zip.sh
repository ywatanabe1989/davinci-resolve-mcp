#!/bin/bash
# create-release-zip.sh
# Script to create a versioned zip file for distribution

# Colors for terminal output
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." &> /dev/null && pwd )"

# Get version from VERSION.md
VERSION=$(grep -m 1 "Current Version:" "$PROJECT_ROOT/docs/VERSION.md" | sed 's/Current Version: //')

if [ -z "$VERSION" ]; then
    echo -e "${RED}Error: Could not determine version from VERSION.md${NC}"
    exit 1
fi

# Create filename with version
ZIP_FILE="davinci-resolve-mcp-v$VERSION.zip"
DIST_DIR="$PROJECT_ROOT/dist"
ZIP_PATH="$DIST_DIR/$ZIP_FILE"

# Ensure dist directory exists
mkdir -p "$DIST_DIR"

echo -e "${BLUE}=================================================${NC}"
echo -e "${BLUE}  Creating Release Zip for DaVinci Resolve MCP   ${NC}"
echo -e "${BLUE}=================================================${NC}"
echo -e "${YELLOW}Version: $VERSION${NC}"
echo -e "${YELLOW}Output file: $ZIP_FILE${NC}"
echo -e "${YELLOW}Output directory: $DIST_DIR${NC}"
echo ""

# Change to project root directory
cd "$PROJECT_ROOT" || exit 1

# Create zip file with tracked files
echo -e "${YELLOW}Adding tracked files to zip...${NC}"
git ls-files | zip -@ "$ZIP_PATH"

# Add untracked files (but exclude ignored files and the .git directory)
echo -e "${YELLOW}Adding untracked files to zip...${NC}"
git ls-files --others --exclude-standard | zip -@ "$ZIP_PATH"

# Check if the zip file was created successfully
if [ -f "$ZIP_PATH" ]; then
    ZIP_SIZE=$(du -h "$ZIP_PATH" | cut -f1)
    echo -e "${GREEN}Successfully created release zip: $ZIP_PATH (Size: $ZIP_SIZE)${NC}"
else
    echo -e "${RED}Failed to create release zip${NC}"
    exit 1
fi

echo -e "${YELLOW}Archive contents:${NC}"
unzip -l "$ZIP_PATH" | head -n 10
echo -e "${YELLOW}... (additional files)${NC}"
echo ""
echo -e "${GREEN}Release zip created successfully!${NC}"

exit 0 