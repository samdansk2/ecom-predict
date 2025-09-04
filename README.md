# E-Commerce Sales Predictor

An advanced e-commerce sales prediction system that leverages machine learning to forecast sales trends, analyze customer behavior, and provide actionable insights. The system combines traditional ML models with deep learning approaches and includes a comprehensive Streamlit dashboard for real-time analysis and predictions.

## Features

### Core Capabilities
- 🚀 **Advanced ML Pipeline**: Multi-model ensemble with XGBoost, LightGBM, and Neural Networks
- 📊 **Interactive Dashboard**: Real-time Streamlit interface for sales analysis and predictions
- 🤖 **Ensemble Learning**: Meta-learning approach combining multiple models for superior accuracy
- 📈 **Time Series Analysis**: Sophisticated temporal feature engineering for sales forecasting
- 🔍 **Customer Segmentation**: RFM analysis and clustering for customer insights
- 🎯 **Product Analytics**: Category performance and product recommendation features
- 📱 **API Service**: FastAPI endpoints for programmatic access to predictions
- 🧪 **A/B Testing**: Statistical testing framework for marketing experiments
- 📉 **Anomaly Detection**: Identify unusual sales patterns and outliers
- 🌍 **Geographic Analysis**: Regional sales patterns and market insights

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

3. **Activate the virtual environment**:
   ```bash
   # UV automatically manages the virtual environment
   # Commands will be run with: uv run <command>
   ```

## Usage

### Streamlit Dashboard (Primary Interface)

```bash
# Start the interactive dashboard
streamlit run dashboard/streamlit_app.py

# Access the dashboard at http://localhost:8501
```

The dashboard provides:
- **Real-time Predictions**: Upload data or use sample data for instant predictions
- **Sales Analytics**: Interactive charts for sales trends, patterns, and forecasts
- **Customer Insights**: RFM segmentation and customer behavior analysis
- **Product Performance**: Category analysis and product recommendations
- **Model Comparison**: Compare predictions across different models
- **A/B Test Results**: Statistical analysis of marketing experiments

### FastAPI Application

```bash
# Start the prediction API server
uv run uvicorn app.api:app --reload

# The API will be available at http://localhost:8000
# Documentation at http://localhost:8000/docs
```

API Endpoints:
- `POST /predict`: Single prediction endpoint
- `POST /batch_predict`: Batch predictions for multiple samples
- `GET /model_info`: Get model performance metrics
- `POST /retrain`: Trigger model retraining with new data


## Project Structure

```
ecom-predict/
├── .github/                # GitHub configuration
│   └── workflows/          # CI/CD workflows
├── app/                    # Application code
│   └── api.py             # FastAPI prediction endpoints
├── dashboard/              # Dashboard interface
│   └── streamlit_app.py   # Streamlit dashboard
├── data/
│   ├── raw/               # Raw data files
│   │   └── ecommerce_sales.csv
│   └── processed/         # Processed data files
│       ├── ecommerce_sales_preprocessed.csv
│       ├── ecommerce_sales_featured.csv
│       └── ecommerce_sales_with_embeddings.csv
├── docs/                   # Documentation
│   └── uv-best-practices.md
├── models/                 # Trained ML models
│   ├── xgboost/           # XGBoost model files
│   │   └── xgb_model.pkl
│   ├── nn/                # Neural network model files
│   │   └── mlp_model.pkl
│   └── meta/              # Meta-ensemble model
│       └── meta_model.pkl
├── notebooks/              # Jupyter notebooks
│   ├── data_preprocessing.ipynb
│   ├── feature_engineering.ipynb
│   ├── text_processing.ipynb
│   ├── model_training_and_predictions.ipynb
│   ├── ensemble_and_evaluation.ipynb
│   └── least_selling_products_analysis.ipynb
├── results/                # Analysis results
│   ├── least_selling_products_bar_chart.html
│   └── price_vs_selling_percentage_scatter.html
├── scripts/               # Development scripts
│   ├── setup-dev.ps1     # Windows setup script
│   └── setup-dev.sh      # Unix setup script
├── .gitignore            # Git ignore patterns
├── README.md             # This file
├── pyproject.toml        # Python project configuration
└── requirements.txt      # Python dependencies
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting (`uv run pytest`, `uv run pre-commit run --all-files`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Acknowledgments

- Built with [UV](https://github.com/astral-sh/uv) for fast Python package management
- Uses modern Python packaging standards with pyproject.toml
- Implements best practices for ML project structure
- Inspired by real-world e-commerce challenges

## Support

For issues, questions, or suggestions, please open an issue on GitHub or contact the maintainers.