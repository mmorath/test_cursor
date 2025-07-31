#!/bin/bash
# Frontend Virtual Environment Setup Script

set -e

echo "🔧 Setting up frontend virtual environment..."

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install pip-tools
echo "🔧 Installing pip-tools..."
pip install pip-tools

# Compile requirements
echo "📋 Compiling requirements..."
pip-compile requirements.in

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "✅ Frontend virtual environment setup complete!"
echo "💡 To activate: source .venv/bin/activate" 