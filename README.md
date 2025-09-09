# E-Commerce Sales Predictor

An advanced e-commerce sales prediction system that leverages machine learning to predict product sales outcome, forecast sales trends, analyze customer behavior, and provide actionable insights. The system combines traditional ML models with deep learning approaches and includes a comprehensive Streamlit dashboard for real-time analysis and predictions.

## Features

### Core Capabilities
- 🚀 **Advanced ML Pipeline**: Multi-model ensemble with XGBoost, LightGBM, and Neural Networks
- 📊 **Interactive Dashboard**: Real-time Streamlit interface for sales analysis and predictions
- 🤖 **Ensemble Learning**: Meta-learning approach combining multiple models for superior accuracy
- 🔍 **Customer Segmentation**: RFM analysis and clustering for customer insights
- 📱 **API Service**: FastAPI endpoints for programmatic access to predictions

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
   git clone https://github.com/samdansk2/ecom-predict.git
   cd ecom-predict
   
   # Run the setup script
   # On Windows:
   .\scripts\setup-dev.ps1
   
   # On macOS/Linux:
   ./scripts/setup-dev.sh
   ```

3. **Create environment**:
    ```bash
    # pyproject.toml is configured for uv
    uv init

    uv venv
    # Install dependencies
    uv pip install -r requirements.txt
   ```

## Usage

### Running the Complete System

**Important**: The Streamlit dashboard requires the FastAPI server to be running for prediction functionality.

#### Step 1: Start the FastAPI Server (Required)
```bash
# Start the prediction API server first
uv run uvicorn app.api:app --reload

# The API will be available at http://localhost:8000
# Keep this terminal window open
```

#### Step 2: Start the Streamlit Dashboard
```bash
# In a new terminal window, start the dashboard
streamlit run dashboard/streamlit_app.py

# Access the dashboard at http://localhost:8501
```

## Contributing

1. Fork the repository
2. Create a feature branch 
3. Push to the branch 
4. Open a Pull Request

## Acknowledgments

- Built with [UV](https://github.com/astral-sh/uv) for fast Python package management
- Uses modern Python packaging standards with pyproject.toml
- Implements best practices for ML project structure
- Inspired by real-world e-commerce challenges

## Support

For issues, questions, or suggestions, please open an issue on GitHub or contact the maintainers.