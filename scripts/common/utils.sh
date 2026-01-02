#!/bin/bash
# Utility functions for DaVinci Resolve MCP Server scripts

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Print a section header
print_header() {
    local text="$1"
    echo ""
    echo -e "${WHITE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${WHITE}  $text${NC}"
    echo -e "${WHITE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

# Print a status message
print_status() {
    local status="$1"
    local message="$2"
    
    case "$status" in
        "success")
            echo -e "${GREEN}✓ $message${NC}"
            ;;
        "warning")
            echo -e "${YELLOW}⚠ $message${NC}"
            ;;
        "error")
            echo -e "${RED}✗ $message${NC}"
            ;;
        "info")
            echo -e "${BLUE}ℹ $message${NC}"
            ;;
        *)
            echo -e "${NC}$message${NC}"
            ;;
    esac
}

# Check if a command exists
command_exists() {
    command -v "$1" &>/dev/null
}

# Check if a port is in use
is_port_in_use() {
    local port="$1"
    lsof -i ":$port" &>/dev/null
}

# Kill processes using a port
kill_port_process() {
    local port="$1"
    local pids=$(lsof -t -i ":$port")
    
    if [ -n "$pids" ]; then
        print_status "info" "Stopping processes using port $port (PIDs: $pids)..."
        kill $pids 2>/dev/null
        sleep 1
        
        # Check if they're still running and force kill if needed
        pids=$(lsof -t -i ":$port")
        if [ -n "$pids" ]; then
            print_status "warning" "Forcing termination of processes using port $port..."
            kill -9 $pids 2>/dev/null
        fi
    fi
}

# Check if DaVinci Resolve is running
is_resolve_running() {
    # Try multiple patterns to detect DaVinci Resolve on macOS
    if pgrep -i "DaVinci Resolve" &>/dev/null || \
       pgrep -i "Resolve" &>/dev/null || \
       ps -ef | grep -i "[D]aVinci Resolve" &>/dev/null || \
       ps -ef | grep -i "Resolve.app" &>/dev/null; then
        return 0
    fi
    
    # Check for Resolve process using the application path
    if [ -d "/Applications/DaVinci Resolve" ] && \
       ps -ef | grep -i "/Applications/DaVinci Resolve" | grep -v grep &>/dev/null; then
        return 0
    fi
    
    return 1
}

# Function to compare version numbers
version_compare() {
    if [[ "$1" == "$2" ]]; then
        return 0
    fi
    
    local IFS=.
    local i ver1=($1) ver2=($2)
    
    # Fill empty fields with zeros
    for ((i=${#ver1[@]}; i<${#ver2[@]}; i++)); do
        ver1[i]=0
    done
    for ((i=${#ver2[@]}; i<${#ver1[@]}; i++)); do
        ver2[i]=0
    done
    
    # Compare version numbers field by field
    for ((i=0; i<${#ver1[@]}; i++)); do
        if [[ ${ver1[i]} -gt ${ver2[i]} ]]; then
            return 1 # ver1 > ver2
        fi
        if [[ ${ver1[i]} -lt ${ver2[i]} ]]; then
            return 2 # ver1 < ver2
        fi
    done
    
    return 0 # ver1 == ver2
}

# Check for Python and pip
check_python() {
    if ! command_exists python3; then
        print_status "error" "Python 3 is required but not installed. Please install Python 3 and try again."
        return 1
    fi
    
    # Check version (need 3.6+)
    python_version=$(python3 --version | awk '{print $2}')
    required_version="3.6"
    
    version_compare "$python_version" "$required_version"
    result=$?
    
    if [[ $result -eq 2 ]]; then
        # Version is less than required
        print_status "error" "Python 3.6+ is required. Your version: $python_version"
        return 1
    else
        # Version is equal to or greater than required
        return 0
    fi
}

# Check for required environment variables
check_resolve_env() {
    local all_set=true
    local missing=""
    
    if [ -z "$RESOLVE_SCRIPT_API" ]; then
        all_set=false
        missing="$missing RESOLVE_SCRIPT_API"
    fi
    
    if [ -z "$RESOLVE_SCRIPT_LIB" ]; then
        all_set=false
        missing="$missing RESOLVE_SCRIPT_LIB"
    fi
    
    if [ "$all_set" = false ]; then
        return 1
    fi
    
    return 0
}

# Set Resolve environment variables
set_resolve_env() {
    export RESOLVE_SCRIPT_API="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
    export RESOLVE_SCRIPT_LIB="/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
    export PYTHONPATH="$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/"
}

# Check if a virtual environment exists
check_venv() {
    local venv_dir="$1"
    
    if [ ! -d "$venv_dir" ]; then
        return 1
    fi
    
    if [ ! -f "$venv_dir/bin/python" ]; then
        return 1
    fi
    
    return 0
}

# Check if a package is installed in the virtual environment
is_package_installed() {
    local venv_dir="$1"
    local package="$2"
    
    "$venv_dir/bin/pip" list | grep -q "^$package "
}

# Install a package in the virtual environment
install_package() {
    local venv_dir="$1"
    local package="$2"
    
    "$venv_dir/bin/pip" install "$package"
} 