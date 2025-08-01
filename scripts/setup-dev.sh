#!/bin/bash
# UV Development Scripts for Unix-like systems
# Common commands for development workflow

set -e

echo "Setting up development environment with UV..."

# Create virtual environment
uv venv

# Install dependencies
echo "Installing project dependencies..."
uv pip install -e .

# Install development dependencies
echo "Installing development dependencies..."
uv pip install -e ".[dev]"

# Install machine learning dependencies (optional)
echo "Installing ML dependencies (optional)..."
# uv pip install -e ".[ml]"

# Install NLP dependencies (optional)
echo "Installing NLP dependencies (optional)..."
# uv pip install -e ".[nlp]"

echo "Development environment setup complete!"
echo ""
echo "Available commands:"
echo "  uv run pytest                    # Run tests"
echo "  uv run black src/ tests/         # Format code"
echo "  uv run isort src/ tests/         # Sort imports"
echo "  uv run flake8 src/ tests/        # Lint code"
echo "  uv run mypy src/                 # Type checking"
echo "  uv run jupyter lab               # Start Jupyter Lab"
echo "  uv run dsa-analyze --help        # Run main CLI"
