"""
Utility functions for the DSA Python Sales Analysis project.
"""

from pathlib import Path
from typing import Any, Dict, Optional
import pandas as pd
import yaml


def load_config(config_path: Path) -> Dict[str, Any]:
    """Load configuration from YAML file."""
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)


def save_config(config: Dict[str, Any], config_path: Path) -> None:
    """Save configuration to YAML file."""
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, 'w') as file:
        yaml.dump(config, file, default_flow_style=False)


def load_data(file_path: Path, **kwargs) -> pd.DataFrame:
    """Load data from various file formats."""
    if file_path.suffix == '.csv':
        return pd.read_csv(file_path, **kwargs)
    elif file_path.suffix in ['.xlsx', '.xls']:
        return pd.read_excel(file_path, **kwargs)
    elif file_path.suffix == '.parquet':
        return pd.read_parquet(file_path, **kwargs)
    else:
        raise ValueError(f"Unsupported file format: {file_path.suffix}")


def save_data(df: pd.DataFrame, file_path: Path, **kwargs) -> None:
    """Save DataFrame to various file formats."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    if file_path.suffix == '.csv':
        df.to_csv(file_path, index=False, **kwargs)
    elif file_path.suffix in ['.xlsx', '.xls']:
        df.to_excel(file_path, index=False, **kwargs)
    elif file_path.suffix == '.parquet':
        df.to_parquet(file_path, **kwargs)
    else:
        raise ValueError(f"Unsupported file format: {file_path.suffix}")


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent


def setup_logging(log_level: str = "INFO") -> None:
    """Setup logging configuration."""
    import logging
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('logs/dsa_analysis.log')
        ]
    )
