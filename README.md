# Sales Analysis

This project involves analyzing sales data to extract insights and trends using Data Science Algorithms implemented with Machine learning. The analysis includes data cleaning, visualization, statistical modeling, and machine learning to understand sales performance over time.

## Features

- 🚀 **Fast Development**: Uses UV for lightning-fast package management
- 📊 **Comprehensive Analysis**: EDA, preprocessing, and modeling workflows
- 🔧 **Modern Python**: Type hints, proper project structure, and best practices
- 🧪 **Testing**: Comprehensive test suite with pytest
- 📝 **Documentation**: Well-documented code and API
- 🎯 **CLI Interface**: Easy-to-use command-line interface

## Quick Start

### Prerequisites

- Python 3.9 or higher
- [UV](https://github.com/astral-sh/uv) (recommended) or pip

### Installation with UV (Recommended)

1. **Install UV** (if not already installed):
   ```bash
   # On Windows (PowerShell)
   powershell -c "irm https://astral-sh.github.io/uv/install.ps1 | iex"
   
   # On macOS/Linux
   curl -LsSf https://astral-sh.github.io/uv/install.sh | sh
   ```

2. **Clone and setup the project**:
   ```bash
   git clone https://github.com/samdansk2/sales-analysis.git
   cd sales-analysis
   
   # Run the setup script
   # On Windows:
   .\scripts\setup-dev.ps1
   
   # On macOS/Linux:
   ./scripts/setup-dev.sh
   ```

3. **Activate the virtual environment**:
   ```bash
   # UV automatically manages the virtual environment
   # Commands will be run with: uv run <command>
   ```

### Installation with pip (Alternative)

```bash
git clone https://github.com/samdansk2/sales-analysis.git
cd sales-analysis

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the project
pip install -e ".[dev]"
```

## Usage

### Command Line Interface

```bash
# Run exploratory data analysis
uv run sales-analyze --analysis-type eda

# Run data preprocessing
uv run sales-analyze --analysis-type preprocessing --data-path data/raw/ecommerce_sales.csv

# Run modeling
uv run sales-analyze --analysis-type modeling --output-dir results/
```

### Jupyter Notebooks

```bash
# Start Jupyter Lab
uv run jupyter lab

# The notebooks/ directory contains:
# - EDA.ipynb: Exploratory Data Analysis
# - data_preprocessing.ipynb: Data cleaning and preparation
# - data_analysis.ipynb: Advanced analysis and modeling
```

## Development

### UV Best Practices Implemented

This project follows UV best practices for modern Python development:

1. **pyproject.toml**: Modern project configuration with proper dependencies
2. **Lock file management**: Reproducible installations with `uv.lock`
3. **Virtual environment**: Automatic virtual environment management
4. **Development dependencies**: Separated dev, ML, and NLP dependencies
5. **Scripts and tasks**: Defined common development tasks
6. **Fast installs**: Lightning-fast dependency resolution and installation

### Development Commands

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest

# Code formatting
uv run black src/ tests/

# Import sorting
uv run isort src/ tests/

# Linting
uv run flake8 src/ tests/

# Type checking
uv run mypy src/

# Run all checks
uv run pre-commit run --all-files

# Install pre-commit hooks
uv run pre-commit install
```

### Dependency Management

```bash
# Add a new dependency
uv add pandas numpy

# Add a development dependency
uv add --dev pytest black

# Add optional dependencies
uv add --optional ml xgboost lightgbm

# Update dependencies
uv sync --upgrade

# Generate requirements.txt (if needed)
uv pip freeze > requirements.txt
```

## Project Structure

```
sales-analysis/
├── pyproject.toml          # Modern Python project configuration
├── uv.toml                 # UV workspace configuration
├── uv.lock                 # Lock file for reproducible builds
├── README.md               # This file
├── .gitignore              # Git ignore patterns
├── .pre-commit-config.yaml # Pre-commit hooks
├── data/
│   ├── raw/                # Raw data files
│   └── processed/          # Processed data files
├── notebooks/              # Jupyter notebooks
│   ├── EDA.ipynb
│   ├── data_preprocessing.ipynb
│   └── data_analysis.ipynb
├── src/                    # Source code
│   ├── __init__.py
│   ├── main.py            # CLI entry point
│   └── utils.py           # Utility functions
├── tests/                 # Test files
│   ├── conftest.py
│   ├── test_main.py
│   └── test_utils.py
└── scripts/               # Development scripts
    ├── setup-dev.ps1      # Windows setup script
    └── setup-dev.sh       # Unix setup script
```

## Optional Dependencies

Install additional dependencies based on your needs:

```bash
# Machine Learning dependencies
uv sync --extra ml

# NLP dependencies  
uv sync --extra nlp

# Documentation dependencies
uv sync --extra docs

# All optional dependencies
uv sync --all-extras
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting (`uv run pytest`, `uv run pre-commit run --all-files`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [UV](https://github.com/astral-sh/uv) for fast Python package management
- Uses modern Python packaging standards with pyproject.toml
- Implements best practices for data science project structure