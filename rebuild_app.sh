#!/bin/bash
# Quick rebuild script for MCOS development

echo "🔧 Rebuilding MCOS.app..."

# Activate virtual environment
source .venv/bin/activate

# Clean previous build
echo "📦 Cleaning previous build..."
rm -rf build/ dist/

# Rebuild the app
echo "🏗️  Building new app bundle..."
pyinstaller mcos.spec --clean

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    echo "📱 MCOS.app is ready at: dist/MCOS.app"
    
    # Ask if user wants to install to Applications
    read -p "🚀 Install to Applications folder? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "/Applications/MCOS.app"
        cp -r "dist/MCOS.app" "/Applications/"
        echo "📲 Installed to /Applications/MCOS.app"
    fi
    
    # Ask if user wants to test launch
    read -p "🧪 Test launch the app? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🚀 Launching MCOS..."
        open "dist/MCOS.app"
    fi
else
    echo "❌ Build failed!"
    exit 1
fi
