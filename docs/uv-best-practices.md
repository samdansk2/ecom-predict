# UV Python Package Manager Best Practices Documentation

## Overview

This project implements UV best practices for modern Python development. UV is a fast Python package installer and resolver that serves as a drop-in replacement for pip and pip-tools.

## Key Benefits of UV

1. **Speed**: Up to 10-100x faster than pip
2. **Reliability**: Better dependency resolution
3. **Modern**: Built-in support for pyproject.toml
4. **Compatibility**: Drop-in replacement for pip commands

## Best Practices Implemented

### 1. Project Configuration (pyproject.toml)

- **Modern packaging**: Uses `pyproject.toml` instead of `setup.py`
- **Dependency groups**: Separate dev, ML, and NLP dependencies
- **Tool configuration**: Black, isort, mypy, pytest configurations
- **Project metadata**: Proper project description and classifiers

### 2. Virtual Environment Management

```bash
# UV automatically creates and manages virtual environments
uv venv                    # Create virtual environment
uv sync                    # Install dependencies in venv
uv run <command>           # Run commands in venv context
```

### 3. Dependency Management

```bash
# Install dependencies
uv add pandas numpy        # Add runtime dependencies
uv add --dev pytest       # Add development dependencies
uv add --optional ml torch # Add optional dependencies

# Lock file for reproducibility
uv lock                    # Generate uv.lock file
uv sync                    # Install from lock file
```

### 4. Development Workflow

```bash
# Setup development environment
uv sync --all-extras       # Install all dependencies
uv run pre-commit install  # Setup pre-commit hooks

# Development commands
uv run pytest             # Run tests
uv run black src/          # Format code
uv run mypy src/           # Type checking
uv run jupyter lab         # Start Jupyter
```

### 5. Performance Optimizations

- **Parallel installs**: UV installs packages in parallel
- **Caching**: Aggressive caching of downloads and builds
- **Wheel building**: Faster wheel building and installation
- **Network optimization**: Better handling of network requests

### 6. Lock File Benefits

The `uv.lock` file provides:
- **Reproducible builds**: Exact versions for all dependencies
- **Security**: Hash verification for all packages
- **Performance**: Pre-resolved dependency tree
- **Cross-platform**: Works across different operating systems

### 7. CI/CD Integration

```yaml
# GitHub Actions example
- name: Install UV
  uses: astral-sh/setup-uv@v2
  
- name: Install dependencies
  run: uv sync --all-extras

- name: Run tests
  run: uv run pytest
```

### 8. Migration from pip

If migrating from pip:

```bash
# Convert requirements.txt to pyproject.toml
uv init                    # Initialize UV project
uv add $(cat requirements.txt)  # Add existing requirements

# Or use existing pyproject.toml
uv sync                    # Install from pyproject.toml
```

## Commands Reference

### Basic Commands

```bash
uv --help                 # Show help
uv init                   # Initialize new project
uv add <package>          # Add dependency
uv remove <package>       # Remove dependency
uv sync                   # Install dependencies
uv lock                   # Generate lock file
uv run <command>          # Run command in venv
```

### Advanced Commands

```bash
uv tree                   # Show dependency tree
uv outdated               # Show outdated packages
uv upgrade                # Upgrade packages
uv export                 # Export to requirements.txt
uv pip freeze             # Show installed packages
```

### Development Commands

```bash
uv sync --dev             # Install dev dependencies
uv sync --all-extras      # Install all optional dependencies
uv run pytest            # Run tests
uv run black .            # Format code
uv run mypy src/          # Type checking
```

## Troubleshooting

### Common Issues

1. **Slow initial setup**: First run may be slow due to caching
2. **Lock file conflicts**: Run `uv lock` to regenerate
3. **Version conflicts**: Check dependency compatibility
4. **Platform issues**: Use `--resolution` flag for cross-platform

### Debug Commands

```bash
uv --verbose sync         # Verbose output
uv cache clean            # Clear cache
uv pip check              # Check for conflicts
```

## Migration Guide

### From pip + requirements.txt

1. Create `pyproject.toml`
2. Move dependencies to `[project.dependencies]`
3. Run `uv sync`
4. Delete `requirements.txt` (optional)

### From Poetry

1. Keep `pyproject.toml`
2. Remove Poetry-specific sections
3. Update to UV-compatible format
4. Run `uv sync`

### From Pipenv

1. Export Pipfile to requirements.txt
2. Create pyproject.toml
3. Add dependencies with `uv add`
4. Remove Pipfile

## Resources

- [UV Documentation](https://docs.astral.sh/uv/)
- [PyProject.toml Specification](https://peps.python.org/pep-0621/)
- [Python Packaging Guide](https://packaging.python.org/)
- [UV GitHub Repository](https://github.com/astral-sh/uv)
