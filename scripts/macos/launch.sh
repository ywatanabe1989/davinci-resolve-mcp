#!/bin/bash
# DaVinci Resolve MCP Server Launch Script for macOS
# Easy launcher that handles environment setup, checking and starting the server

# Get the absolute path to the project directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_DIR="$( cd "$SCRIPT_DIR/.." &> /dev/null && pwd )"
VENV_DIR="$PROJECT_DIR/venv"
MCP_PORT=8080

# Load utility functions
source "$SCRIPT_DIR/utils.sh"

# Main menu function
show_main_menu() {
    clear
    print_header "DaVinci Resolve MCP Server Launcher"
    
    echo -e "${CYAN}What would you like to do?${NC}"
    echo ""
    echo -e "${WHITE}1${NC}. Start MCP Server"
    echo -e "${WHITE}2${NC}. Stop MCP Server(s)"
    echo -e "${WHITE}3${NC}. Check Environment"
    echo -e "${WHITE}4${NC}. Setup Environment"
    echo -e "${WHITE}5${NC}. View Readme"
    echo -e "${WHITE}0${NC}. Exit"
    echo ""
    
    read -p "Enter your choice [1-5 or 0]: " choice
    
    case "$choice" in
        1) start_server ;;
        2) stop_servers ;;
        3) check_environment ;;
        4) setup_environment ;;
        5) view_readme ;;
        0) exit 0 ;;
        *) 
            echo -e "${YELLOW}Invalid choice. Please try again.${NC}"
            sleep 1
            show_main_menu
            ;;
    esac
}

# Function to start the server
start_server() {
    print_header "Starting DaVinci Resolve MCP Server"
    
    # Check if Python is available
    if ! check_python; then
        print_status "error" "Cannot start the server without Python."
        read -p "Press Enter to return to the main menu..." dummy
        show_main_menu
        return
    fi
    
    # Check if the virtual environment exists
    if ! check_venv "$VENV_DIR"; then
        print_status "warning" "Virtual environment not found. Setting up now..."
        setup_virtual_environment
    fi
    
    # Check for required packages
    if ! is_package_installed "$VENV_DIR" "mcp"; then
        print_status "warning" "MCP package not installed. Installing now..."
        install_package "$VENV_DIR" "mcp[cli]"
    fi
    
    # Check if Resolve environment variables are set
    if ! check_resolve_env; then
        print_status "warning" "Resolve environment variables not set. Setting defaults..."
        set_resolve_env
    fi
    
    # Check if DaVinci Resolve is running
    if ! is_resolve_running; then
        print_status "warning" "DaVinci Resolve is not running. The server will start but won't be able to connect to Resolve."
        print_status "info" "Please start DaVinci Resolve and then restart the server."
    else
        print_status "success" "DaVinci Resolve is running."
    fi
    
    # Check if the port is in use
    if is_port_in_use "$MCP_PORT"; then
        print_status "warning" "Port $MCP_PORT is already in use."
        read -p "Do you want to stop the process using this port? (y/n): " stop_process
        if [[ "$stop_process" =~ ^[Yy]$ ]]; then
            kill_port_process "$MCP_PORT"
        else
            print_status "error" "Cannot start the server on port $MCP_PORT as it's already in use."
            read -p "Press Enter to return to the main menu..." dummy
            show_main_menu
            return
        fi
    fi
    
    # Run the server in development mode
    print_status "info" "Starting the MCP server in development mode..."
    
    # Navigate to the project directory and start the server
    cd "$PROJECT_DIR"
    
    # Run the server in background or foreground?
    read -p "Run server in background? (y/n): " bg_choice
    if [[ "$bg_choice" =~ ^[Yy]$ ]]; then
        print_status "info" "Starting server in background mode..."
        nohup "$VENV_DIR/bin/mcp" dev "$PROJECT_DIR/src/src/__main__.py" > "$PROJECT_DIR/mcp_server.log" 2>&1 &
        print_status "success" "Server is running in the background."
        print_status "info" "Logs are being written to: $PROJECT_DIR/mcp_server.log"
        print_status "info" "To stop the server, use option 2 from the main menu."
    else
        print_status "info" "Starting server in foreground mode..."
        print_status "info" "Press Ctrl+C to stop the server"
        print_status "info" "Server is starting..."
        sleep 1
        "$VENV_DIR/bin/mcp" dev "$PROJECT_DIR/src/src/__main__.py"
    fi
    
    read -p "Press Enter to return to the main menu..." dummy
    show_main_menu
}

# Function to stop all running servers
stop_servers() {
    print_header "Stopping DaVinci Resolve MCP Server(s)"
    
    # Check if any MCP servers are running
    local pids=$(pgrep -f "mcp dev")
    
    if [ -z "$pids" ]; then
        print_status "info" "No MCP servers are currently running."
    else
        print_status "info" "Found MCP server processes: $pids"
        print_status "info" "Stopping servers..."
        
        kill $pids 2>/dev/null
        sleep 1
        
        # Check if they're still running and force kill if needed
        pids=$(pgrep -f "mcp dev")
        if [ -n "$pids" ]; then
            print_status "warning" "Forcing termination of server processes..."
            kill -9 $pids 2>/dev/null
        fi
        
        print_status "success" "All MCP servers have been stopped."
    fi
    
    # Also check for any processes using the MCP port
    if is_port_in_use "$MCP_PORT"; then
        print_status "warning" "Port $MCP_PORT is still in use."
        read -p "Do you want to stop processes using this port? (y/n): " stop_port
        if [[ "$stop_port" =~ ^[Yy]$ ]]; then
            kill_port_process "$MCP_PORT"
            print_status "success" "Freed port $MCP_PORT."
        fi
    else
        print_status "success" "Port $MCP_PORT is free."
    fi
    
    read -p "Press Enter to return to the main menu..." dummy
    show_main_menu
}

# Function to check the environment
check_environment() {
    print_header "Checking Environment"
    
    # Check Python
    if check_python; then
        python_version=$(python3 --version)
        print_status "success" "Python is available: $python_version"
    else
        print_status "error" "Python check failed."
    fi
    
    # Check virtual environment
    if check_venv "$VENV_DIR"; then
        print_status "success" "Virtual environment exists at $VENV_DIR"
        
        # Check for MCP package
        if is_package_installed "$VENV_DIR" "mcp"; then
            mcp_version=$("$VENV_DIR/bin/pip" show mcp | grep Version | awk '{print $2}')
            print_status "success" "MCP package is installed (version $mcp_version)"
        else
            print_status "error" "MCP package is not installed"
        fi
    else
        print_status "error" "Virtual environment not found or incomplete"
    fi
    
    # Check Resolve environment variables
    if check_resolve_env; then
        print_status "success" "Resolve environment variables are set"
        echo -e "${BLUE}RESOLVE_SCRIPT_API${NC} = $RESOLVE_SCRIPT_API"
        echo -e "${BLUE}RESOLVE_SCRIPT_LIB${NC} = $RESOLVE_SCRIPT_LIB"
    else
        print_status "error" "Missing Resolve environment variables"
    fi
    
    # Check if DaVinci Resolve is running
    if is_resolve_running; then
        print_status "success" "DaVinci Resolve is running"
    else
        print_status "error" "DaVinci Resolve is not running"
    fi
    
    # Check if port is in use
    if is_port_in_use "$MCP_PORT"; then
        process_info=$(lsof -i ":$MCP_PORT" | tail -n +2 | head -1)
        print_status "warning" "Port $MCP_PORT is in use: $process_info"
    else
        print_status "success" "Port $MCP_PORT is free"
    fi
    
    read -p "Press Enter to return to the main menu..." dummy
    show_main_menu
}

# Function to set up the environment
setup_environment() {
    print_header "Setting Up Environment"
    
    # Check Python first
    if ! check_python; then
        print_status "error" "Cannot set up the environment without Python."
        read -p "Press Enter to return to the main menu..." dummy
        show_main_menu
        return
    fi
    
    # Set up virtual environment
    setup_virtual_environment
    
    # Set up Resolve environment variables
    print_status "info" "Setting up Resolve environment variables..."
    set_resolve_env
    
    # Add environment variables to shell profile if needed
    shell_profile=""
    if [ -f "$HOME/.zshrc" ]; then
        shell_profile="$HOME/.zshrc"
    elif [ -f "$HOME/.bash_profile" ]; then
        shell_profile="$HOME/.bash_profile"
    elif [ -f "$HOME/.bashrc" ]; then
        shell_profile="$HOME/.bashrc"
    fi
    
    if [ -n "$shell_profile" ]; then
        print_status "info" "Checking for environment variables in $shell_profile..."
        
        if grep -q "RESOLVE_SCRIPT_API" "$shell_profile"; then
            print_status "success" "Environment variables already exist in $shell_profile"
        else
            print_status "info" "Adding environment variables to $shell_profile..."
            echo "" >> "$shell_profile"
            echo "# DaVinci Resolve MCP Server environment variables" >> "$shell_profile"
            echo "export RESOLVE_SCRIPT_API=\"$RESOLVE_SCRIPT_API\"" >> "$shell_profile"
            echo "export RESOLVE_SCRIPT_LIB=\"$RESOLVE_SCRIPT_LIB\"" >> "$shell_profile"
            echo "export PYTHONPATH=\"\$PYTHONPATH:\$RESOLVE_SCRIPT_API/Modules/\"" >> "$shell_profile"
            print_status "success" "Environment variables added to $shell_profile"
        fi
    else
        print_status "warning" "No shell profile found for setting persistent environment variables"
        print_status "info" "You'll need to set these variables manually in your shell profile:"
        echo "export RESOLVE_SCRIPT_API=\"$RESOLVE_SCRIPT_API\""
        echo "export RESOLVE_SCRIPT_LIB=\"$RESOLVE_SCRIPT_LIB\""
        echo "export PYTHONPATH=\"\$PYTHONPATH:\$RESOLVE_SCRIPT_API/Modules/\""
    fi
    
    print_status "success" "Environment setup complete!"
    read -p "Press Enter to return to the main menu..." dummy
    show_main_menu
}

# Function to set up virtual environment
setup_virtual_environment() {
    print_status "info" "Setting up Python virtual environment..."
    
    if check_venv "$VENV_DIR"; then
        print_status "info" "Virtual environment already exists at $VENV_DIR"
    else
        print_status "info" "Creating virtual environment at $VENV_DIR"
        python3 -m venv "$VENV_DIR"
        
        if ! check_venv "$VENV_DIR"; then
            print_status "error" "Failed to create virtual environment"
            return 1
        fi
    fi
    
    # Install or upgrade pip
    print_status "info" "Updating pip in virtual environment..."
    "$VENV_DIR/bin/pip" install --upgrade pip
    
    # Install MCP with CLI support
    print_status "info" "Installing MCP SDK with CLI support..."
    "$VENV_DIR/bin/pip" install "mcp[cli]"
    
    print_status "success" "Virtual environment is ready"
    return 0
}

# Function to view README
view_readme() {
    print_header "DaVinci Resolve MCP Server Documentation"
    
    # Check if less is available
    if command_exists less; then
        less "$PROJECT_DIR/README.md"
    else
        cat "$PROJECT_DIR/README.md"
    fi
    
    read -p "Press Enter to return to the main menu..." dummy
    show_main_menu
}

# Make all scripts executable
chmod +x "$SCRIPT_DIR"/*.sh
chmod +x "$PROJECT_DIR/src/src/__main__.py"

# Start the main menu
show_main_menu 