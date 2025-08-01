"""
Tests for utility functions.
"""

import pytest
import pandas as pd
from pathlib import Path
import tempfile
import yaml

from src.utils import (
    load_config, save_config, load_data, save_data, 
    get_project_root
)


def test_get_project_root():
    """Test getting project root directory."""
    root = get_project_root()
    assert root.is_dir()
    assert (root / "pyproject.toml").exists()


def test_load_save_config(temp_dir):
    """Test configuration loading and saving."""
    config = {"test_key": "test_value", "nested": {"key": "value"}}
    config_path = temp_dir / "config.yaml"
    
    # Test saving
    save_config(config, config_path)
    assert config_path.exists()
    
    # Test loading
    loaded_config = load_config(config_path)
    assert loaded_config == config


def test_load_save_data_csv(temp_dir, sample_data):
    """Test loading and saving CSV data."""
    csv_path = temp_dir / "test_data.csv"
    
    # Test saving
    save_data(sample_data, csv_path)
    assert csv_path.exists()
    
    # Test loading
    loaded_data = load_data(csv_path)
    pd.testing.assert_frame_equal(loaded_data, sample_data)


def test_load_save_data_parquet(temp_dir, sample_data):
    """Test loading and saving Parquet data."""
    parquet_path = temp_dir / "test_data.parquet"
    
    # Test saving
    save_data(sample_data, parquet_path)
    assert parquet_path.exists()
    
    # Test loading
    loaded_data = load_data(parquet_path)
    pd.testing.assert_frame_equal(loaded_data, sample_data)


def test_unsupported_format(temp_dir, sample_data):
    """Test handling of unsupported file formats."""
    unsupported_path = temp_dir / "test_data.txt"
    
    with pytest.raises(ValueError, match="Unsupported file format"):
        save_data(sample_data, unsupported_path)
    
    # Create a dummy file
    unsupported_path.touch()
    
    with pytest.raises(ValueError, match="Unsupported file format"):
        load_data(unsupported_path)
