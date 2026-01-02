#!/bin/bash
# Script to create a macOS desktop app shortcut for the DaVinci Resolve MCP Server Launcher

# Get the absolute path to the project directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_DIR="$( cd "$SCRIPT_DIR/.." &> /dev/null && pwd )"
LAUNCHER_SCRIPT="$SCRIPT_DIR/launch.sh"
APP_NAME="DaVinci Resolve MCP Server.app"
APP_DIR="$HOME/Desktop/$APP_NAME"

# Make sure the launcher script is executable
chmod +x "$LAUNCHER_SCRIPT"

# Create the app structure
echo "Creating app structure at $APP_DIR..."
mkdir -p "$APP_DIR/Contents/MacOS"
mkdir -p "$APP_DIR/Contents/Resources"

# Create the Info.plist
cat > "$APP_DIR/Contents/Info.plist" << EOL
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>app</string>
    <key>CFBundleIconFile</key>
    <string>AppIcon</string>
    <key>CFBundleIdentifier</key>
    <string>com.davinciresolve.mcpserver</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>DaVinci Resolve MCP Server</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundleVersion</key>
    <string>1</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.13</string>
    <key>NSHumanReadableCopyright</key>
    <string>Copyright © 2023. All rights reserved.</string>
</dict>
</plist>
EOL

# Create the wrapper script
cat > "$APP_DIR/Contents/MacOS/app" << EOL
#!/bin/bash
cd "$PROJECT_DIR"
osascript -e 'tell application "Terminal" to do script "\"$LAUNCHER_SCRIPT\""'
EOL

# Make the wrapper script executable
chmod +x "$APP_DIR/Contents/MacOS/app"

# Copy a default icon if available, or create a placeholder
if [ -f "$PROJECT_DIR/assets/icon.icns" ]; then
    cp "$PROJECT_DIR/assets/icon.icns" "$APP_DIR/Contents/Resources/AppIcon.icns"
fi

echo "App shortcut created at $APP_DIR"
echo "Double-click to launch the DaVinci Resolve MCP Server" 