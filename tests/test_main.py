"""
Tests for the main CLI module.
"""

import pytest
from unittest.mock import patch
import sys
from pathlib import Path

from src.main import main


def test_main_default_args():
    """Test main function with default arguments."""
    test_args = ["dsa-analyze"]
    
    with patch.object(sys, 'argv', test_args):
        with patch('sys.exit') as mock_exit:
            with patch('builtins.print') as mock_print:
                main()
                mock_print.assert_called()
                mock_exit.assert_called_with(0)


def test_main_custom_args():
    """Test main function with custom arguments."""
    test_args = [
        "dsa-analyze",
        "--data-path", "custom/path/data.csv",
        "--output-dir", "custom/output",
        "--analysis-type", "preprocessing"
    ]
    
    with patch.object(sys, 'argv', test_args):
        with patch('sys.exit') as mock_exit:
            with patch('builtins.print') as mock_print:
                main()
                mock_print.assert_called()
                mock_exit.assert_called_with(0)


def test_main_invalid_analysis_type():
    """Test main function with invalid analysis type."""
    test_args = [
        "dsa-analyze",
        "--analysis-type", "invalid_type"
    ]
    
    with patch.object(sys, 'argv', test_args):
        with pytest.raises(SystemExit):
            main()
