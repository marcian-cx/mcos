#!/bin/bash
# MCOS Launch Script - One command to rule them all

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🚀 Launching MCOS..."
echo "📁 Project directory: $SCRIPT_DIR"

# Navigate to project directory
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "💡 Run this first: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Check if dependencies are installed
if ! python -c "import PyQt6" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

# Launch MCOS
echo "✨ Starting MCOS..."
python -m mcos.app --vault ./demo_vault
