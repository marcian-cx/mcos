#!/bin/bash
# MCOS Daily Use Setup Script

echo "Setting up MCOS for daily use..."

# Create vault in home directory if it doesn't exist
VAULT_DIR="$HOME/mcos_vault"
if [ ! -d "$VAULT_DIR" ]; then
    echo "Creating MCOS vault at $VAULT_DIR"
    mkdir -p "$VAULT_DIR"/{Inbox,Projects,Goals,Reviews,Calendar,Notes}
    
    # Copy demo content as starter
    if [ -d "demo_vault" ]; then
        cp -r demo_vault/* "$VAULT_DIR/"
        echo "Copied demo content to your vault"
    fi
fi

# Copy app to Applications folder (optional)
read -p "Install MCOS.app to /Applications? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ -d "dist/MCOS.app" ]; then
        cp -r "dist/MCOS.app" "/Applications/"
        echo "MCOS.app installed to Applications folder"
        echo "You can now launch MCOS from Spotlight (Cmd+Space, type 'MCOS')"
    else
        echo "MCOS.app not found. Run 'pyinstaller mcos.spec' first."
    fi
fi

# Create desktop launcher script
LAUNCHER_SCRIPT="$HOME/Desktop/Launch MCOS.command"
cat > "$LAUNCHER_SCRIPT" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
if [ -d "/Applications/MCOS.app" ]; then
    open "/Applications/MCOS.app"
else
    # Fallback to local copy
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    MCOS_DIR="$(dirname "$SCRIPT_DIR")/Documents/Craft/marcian.cx/Art/code/mcos"
    if [ -d "$MCOS_DIR/dist/MCOS.app" ]; then
        open "$MCOS_DIR/dist/MCOS.app"
    else
        echo "MCOS.app not found!"
        read -p "Press enter to close..."
    fi
fi
EOF

chmod +x "$LAUNCHER_SCRIPT"
echo "Created desktop launcher: $LAUNCHER_SCRIPT"

echo ""
echo "MCOS Setup Complete!"
echo "====================="
echo "Vault location: $VAULT_DIR"
echo "App location: /Applications/MCOS.app (if installed)"
echo "Desktop launcher: $LAUNCHER_SCRIPT"
echo ""
echo "To launch MCOS:"
echo "1. Double-click the desktop launcher"
echo "2. Use Spotlight: Cmd+Space, type 'MCOS'"
echo "3. Open from Applications folder"
echo ""
echo "For daily test driving, use the desktop launcher for quickest access!"
