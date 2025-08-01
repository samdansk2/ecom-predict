"""
Test configuration and fixtures for the DSA Python Sales Analysis project.
"""

import pytest
from pathlib import Path
import pandas as pd
import tempfile
import shutil


@pytest.fixture
def project_root():
    """Get the project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture
def sample_data():
    """Create sample sales data for testing."""
    data = {
        'date': pd.date_range('2023-01-01', periods=100, freq='D'),
        'product_id': ['P001', 'P002', 'P003', 'P004'] * 25,
        'sales_amount': [100.0, 150.0, 200.0, 75.0] * 25,
        'quantity': [1, 2, 1, 3] * 25,
        'customer_id': range(1, 101),
        'region': ['North', 'South', 'East', 'West'] * 25
    }
    return pd.DataFrame(data)


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)
