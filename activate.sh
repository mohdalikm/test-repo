#!/bin/bash
# Activation script for the performance issues Python application
# Usage: source activate.sh

echo "🐍 Activating Python virtual environment..."

# Check if venv directory exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run 'python3 -m venv venv' first."
    return 1
fi

# Activate the virtual environment
source venv/bin/activate

# Verify activation
if [ "$VIRTUAL_ENV" != "" ]; then
    echo "✅ Virtual environment activated successfully!"
    echo "📍 Virtual environment path: $VIRTUAL_ENV"
    echo "🐍 Python version: $(python --version)"
    echo "📦 Pip version: $(pip --version)"
    echo ""
    echo "🎯 Available commands:"
    echo "  python main.py                    # Run the main application with performance issues"
    echo "  python generate_test_data.py     # Generate sample data files"
    echo "  python utils.py                  # Test utility functions"
    echo "  python -m cProfile main.py       # Profile the application"
    echo "  deactivate                       # Exit the virtual environment"
    echo ""
    echo "🔧 Development tools available:"
    echo "  black *.py                       # Format code"
    echo "  flake8 *.py                      # Lint code"
    echo "  mypy *.py                        # Type checking"
    echo "  pytest                           # Run tests"
    echo ""
else
    echo "❌ Failed to activate virtual environment"
    return 1
fi