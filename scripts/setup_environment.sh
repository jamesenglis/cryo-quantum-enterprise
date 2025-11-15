#!/bin/bash
echo "🚀 Setting up Enterprise Quantum Development Environment"

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv .venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies in batches
echo "📚 Installing core dependencies..."
pip install -r requirements.txt

echo "🔧 Installing development dependencies..."
pip install -r requirements-dev.txt

# Set up pre-commit
echo "✅ Setting up pre-commit hooks..."
pre-commit install

# Verify installation
echo "🔍 Verifying installation..."
python verify_installation.py

echo ""
echo "🎉 Setup complete! Your enterprise quantum environment is ready."
echo "   To activate in the future, run: source .venv/bin/activate"
