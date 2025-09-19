import joblib
import pandas as pd
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import os
import warnings
from typing import Dict, List, Tuple
from collections import Counter
warnings.filterwarnings('ignore')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load the improved models from Phase 6 with calibration
try:
    # Load the complete model package from Phase 6
    model_package = joblib.load(os.path.join(BASE_DIR, "../models/final/all_models_phase6.pkl"))

    # Extract components
    all_models = model_package['models']
    scaler = model_package['scaler']
    feature_columns = model_package['feature_columns']
    best_model_name = model_package['best_model']

    # Use the best performing model (calibrated ensemble)
    # The calibrated ensemble is stored as a dict with 'model' key
    calibrated_ensemble_data = all_models[best_model_name]
    if isinstance(calibrated_ensemble_data, dict) and 'model' in calibrated_ensemble_data:
        primary_model = calibrated_ensemble_data['model']
        calibration_data = calibrated_ensemble_data.get('calibration_data', None)
    else:
        primary_model = calibrated_ensemble_data
        calibration_data = None

    # Also keep individual models for fallback
    xgb_model_data = all_models.get('xgboost')
    if isinstance(xgb_model_data, dict) and 'model' in xgb_model_data:
        xgb_model = xgb_model_data['model']
    else:
        xgb_model = xgb_model_data

    rf_model_data = all_models.get('random_forest')
    if isinstance(rf_model_data, dict) and 'model' in rf_model_data:
        rf_model = rf_model_data['model']
    else:
        rf_model = rf_model_data

    print(f"Loaded best model: {best_model_name}")
    print(f"Feature columns expected: {len(feature_columns)}")
except Exception as e:
    print(f"Error loading new models, falling back to old models: {e}")
    # Fallback to old models if new ones fail to load
    xgb_model = joblib.load(os.path.join(BASE_DIR, "../models/optimized/xgboost_optimized.pkl"))
    primary_model = xgb_model
    scaler = None
    feature_columns = None

# Load the engineered features dataset for better predictions
lookup_path = os.path.join(BASE_DIR, "../data/raw/ecommerce_sales.csv")
lookup_df = pd.read_csv(lookup_path)

# Also load engineered features if available
engineered_path = os.path.join(BASE_DIR, "../data/processed/ecommerce_sales_engineered.csv")
if os.path.exists(engineered_path):
    engineered_df = pd.read_csv(engineered_path)
    print(f"Loaded engineered features from {engineered_path}")
else:
    engineered_df = None
    print("No engineered features found, using basic features only")

model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
bert_model = AutoModel.from_pretrained(model_name)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
bert_model.to(device)

app = FastAPI(title="Product Success Prediction API")

# ------------------- Home Page -------------------
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Product Success Prediction</title>
        <style>
            body { font-family: Arial; max-width: 600px; margin: auto; padding: 20px; }
            h1 { color: #333; }
            label { display: block; margin-top: 10px; }
            input, button { width: 100%; padding: 10px; margin-top: 5px; }
            button { background-color: #4CAF50; color: white; border: none; cursor: pointer; }
            button:hover { background-color: #45a049; }
            .result { margin-top: 20px; padding: 15px; background: #f4f4f4; border-radius: 8px; }
            .success { background-color: #d4edda; border: 2px solid #28a745; color: #155724; }
            .fail { background-color: #f8d7da; border: 2px solid #dc3545; color: #721c24; }
            .result-heading { font-weight: bold; font-size: 20px; margin-bottom: 10px; color: #333; }
            .result-item { margin: 5px 0; }
            .probability { font-size: 16px; font-weight: bold; }
            .info { background-color: #d1ecf1; border: 1px solid #bee5eb; color: #0c5460; padding: 10px; margin: 10px 0; border-radius: 5px; }
        </style>
    </head>
    <body>
        <h1>Product Success Prediction</h1>

        <label>Product Name</label>
        <input id="product_name" type="text" placeholder="e.g. Sports Shoes">

        <button onclick="predict()">Predict</button>

        <div id="output" class="result"></div>

        <script>
            async function predict() {
                let data = {
                    product_name: document.getElementById('product_name').value
                };

                if (!data.product_name.trim()) {
                    document.getElementById('output').innerHTML = '<div class="result fail">Please enter a product name!</div>';
                    return;
                }

                document.getElementById('output').innerHTML = '<div class="result">Predicting...</div>';

                try {
                    let response = await fetch('/predict', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(data)
                    });

                    let result = await response.json();

                    // Check if product was not found
                    if (result.error && result.error === "Product not found") {
                        document.getElementById('output').innerHTML = `
                            <div class="result fail">
                                <div class="result-heading">Product Not Found</div>
                                <div class="result-item">${result.message}</div>
                            </div>
                        `;
                        return;
                    }

                    let resultClass = result.prediction === "Success" ? "success" : "fail";
                    let probabilityPercent = (result.success_probability * 100).toFixed(1);

                    // Build the output HTML
                    let outputHtml = `
                        <div class="result-heading">Prediction Result</div>
                        <div class="result ${resultClass}">
                            <div class="result-item"><strong>Product:</strong> ${result.product_name}</div>
                            <div class="result-item"><strong>Category:</strong> ${result.category}</div>
                            <div class="result-item probability"><strong>Success Probability:</strong> ${probabilityPercent}%</div>
                            <div class="result-item"><strong>Prediction:</strong> ${result.prediction}</div>
                    `;

                    // Add aggregation info if multiple products were found
                    if (result.aggregation_info) {
                        outputHtml += `
                            <div class="info">
                                <strong>Note:</strong> Found ${result.aggregation_info.products_analyzed} products with this name.
                                <br>Aggregation Method: ${result.aggregation_info.method}
                                <br>Success Rate: ${(result.aggregation_info.success_rate * 100).toFixed(1)}%
                            </div>
                        `;
                    }

                    outputHtml += '</div>';
                    document.getElementById('output').innerHTML = outputHtml;

                } catch (error) {
                    document.getElementById('output').innerHTML = '<div class="result fail">Failed to get prediction. Please try again.</div>';
                }
            }
        </script>
    </body>
    </html>
    """

class ProductInput(BaseModel):
    product_name: str

def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=16)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        outputs = bert_model(**inputs)
    return outputs.last_hidden_state[:, 0, :].cpu().numpy().flatten()

def safe_get_value(row, col, default):
    return row[col].values[0] if col in row.columns and not pd.isna(row[col].values[0]) else default

def create_engineered_features(row_data):
    """Create the same engineered features used during model training"""
    features = {}

    # Extract basic data
    price = row_data.get('price', 299.0)
    review_score = row_data.get('review_score', 4.0)
    review_count = row_data.get('review_count', 50)
    category = row_data.get('category', 'Clothing')

    # Get monthly sales data
    monthly_cols = [f'sales_month_{i}' for i in range(1, 13)]
    monthly_sales = np.array([row_data.get(col, 40) for col in monthly_cols])

    # Basic sales metrics
    total_sales = monthly_sales.sum()
    avg_sales = monthly_sales.mean()
    sales_std = monthly_sales.std()

    # Growth rates
    growth_rates = []
    for i in range(11):
        if monthly_sales[i] > 0:
            growth = (monthly_sales[i+1] - monthly_sales[i]) / monthly_sales[i]
        else:
            growth = 0
        growth_rates.append(growth)
        features[f'growth_month_{i+1}_to_{i+2}'] = growth

    features['avg_growth_rate'] = np.mean(growth_rates) if growth_rates else 0
    features['growth_volatility'] = np.std(growth_rates) if len(growth_rates) > 1 else 0

    # Sales trend slope
    months = np.arange(1, 13)
    if sales_std > 0:
        slope, _ = np.polyfit(months, monthly_sales, 1)
    else:
        slope = 0
    features['trend_slope'] = slope

    # Early vs late performance
    early_sales = monthly_sales[:6].mean()
    late_sales = monthly_sales[6:].mean()
    features['early_sales'] = early_sales
    features['late_sales'] = late_sales
    features['early_late_ratio'] = late_sales / (early_sales + 1)

    # Price category features
    features['price_bucket_low'] = 1 if price < 100 else 0
    features['price_bucket_medium'] = 1 if 100 <= price < 300 else 0
    features['price_bucket_high'] = 1 if 300 <= price < 500 else 0
    features['price_bucket_premium'] = 1 if price >= 500 else 0

    # Review features
    features['review_strength'] = review_score * np.log1p(review_count)
    features['has_many_reviews'] = 1 if review_count > 100 else 0
    features['review_quality'] = review_score / 5.0

    # Sales performance metrics
    features['total_sales'] = total_sales
    features['avg_sales_per_month'] = avg_sales
    features['sales_consistency'] = 1 / (1 + sales_std / (avg_sales + 1))
    features['sales_cv'] = sales_std / (avg_sales + 1)

    # Category relative performance (simplified without full dataset)
    features['sales_vs_category'] = total_sales / 6000  # Normalized estimate
    features['price_vs_category'] = price / 250  # Normalized estimate
    features['review_vs_category'] = review_score / 3.5  # Normalized estimate

    # Peak and trough analysis
    features['peak_month'] = int(np.argmax(monthly_sales) + 1)
    features['trough_month'] = int(np.argmin(monthly_sales) + 1)
    features['peak_trough_ratio'] = monthly_sales.max() / (monthly_sales.min() + 1)

    # Add original features
    features['price'] = price
    features['review_score'] = review_score
    features['review_count'] = review_count

    # Add monthly sales
    for i, val in enumerate(monthly_sales, 1):
        features[f'sales_month_{i}'] = val

    # Category encoding
    categories = ['Clothing', 'Electronics', 'Health', 'Home & Kitchen', 'Sports', 'Toys']
    for cat in categories:
        features[f'category_{cat}'] = 1 if category == cat else 0

    return features

def smooth_probability(p, temperature=2.0):
    """Apply temperature scaling and bounds to smooth extreme probabilities"""
    # Apply temperature scaling to reduce confidence
    logit = np.log(p / (1 - p + 1e-10))
    scaled_logit = logit / temperature
    smoothed = 1 / (1 + np.exp(-scaled_logit))

    # Apply additional bounds to prevent extreme predictions
    if smoothed < 0.02:
        smoothed = 0.1 + (smoothed * 4)  # Map 0-2% to 10-18%
    elif smoothed < 0.1:
        smoothed = 0.15 + (smoothed - 0.02) * 2  # Map 2-10% to 15-31%
    elif smoothed > 0.98:
        smoothed = 0.82 + (1 - smoothed) * 4  # Map 98-100% to 82-90%
    elif smoothed > 0.9:
        smoothed = 0.75 + (smoothed - 0.9) * 0.7  # Map 90-98% to 75-82%

    return smoothed

def get_prediction_for_single_product(product_row) -> Tuple[float, str, str]:
    """
    Get prediction for a single product row
    Returns: (probability, prediction_label, category)
    """
    # Extract category
    category = product_row['category'].values[0] if 'category' in product_row.columns else "Unknown"

    # Check if we should use engineered features
    if feature_columns is not None:
        # Use pre-computed engineered features if available
        feature_values = []
        for col in feature_columns:
            if col in product_row.columns:
                value = product_row[col].values[0]
                # Handle NaN values
                if pd.isna(value):
                    value = 0
                feature_values.append(value)
            else:
                # Missing feature, use default
                feature_values.append(0)

        features_array = np.array(feature_values).reshape(1, -1)

        # Apply scaling if scaler is available
        if scaler is not None:
            try:
                features_array = scaler.transform(features_array)
            except:
                pass
    else:
        # Create engineered features on the fly
        row_data = {}
        for col in product_row.columns:
            row_data[col] = product_row[col].values[0]

        features_dict = create_engineered_features(row_data)

        if feature_columns is not None:
            feature_values = [features_dict.get(col, 0) for col in feature_columns]
        else:
            feature_values = list(features_dict.values())

        features_array = np.array(feature_values).reshape(1, -1)

        if scaler is not None:
            try:
                features_array = scaler.transform(features_array)
            except:
                pass

    # Make prediction with the best model
    if hasattr(primary_model, 'predict_proba'):
        pred_proba = primary_model.predict_proba(features_array)
        if len(pred_proba.shape) > 1 and pred_proba.shape[1] > 1:
            final_pred_proba = pred_proba[0, 1]
        else:
            final_pred_proba = pred_proba[0]
    else:
        final_pred_proba = float(primary_model.predict(features_array)[0])

    # Apply smoothing to reduce bimodal distribution
    final_pred_proba = smooth_probability(final_pred_proba)

    # Determine prediction label
    prediction = "Success" if final_pred_proba >= 0.5 else "Fail"

    return final_pred_proba, prediction, category

@app.post("/predict")
def predict(input_data: ProductInput):
    try:
        print(f"\nReceived product: {input_data.product_name}")

        # Try to find product in engineered dataset first
        if engineered_df is not None:
            all_matches = engineered_df[engineered_df['product_name'].str.lower() == input_data.product_name.lower()]
            use_engineered = True
        else:
            # Fallback to raw dataset
            all_matches = lookup_df[lookup_df['product_name'].str.lower() == input_data.product_name.lower()]
            use_engineered = False

        # Check if product exists
        if all_matches.empty:
            return {
                "error": "Product not found",
                "product_name": input_data.product_name,
                "message": f"The product '{input_data.product_name}' was not found in our database."
            }

        print(f"Found {len(all_matches)} product(s) with name '{input_data.product_name}'")

        # CASE 1: Single product - return direct prediction
        if len(all_matches) == 1:
            print("Single product found - returning direct prediction")

            probability, prediction, category = get_prediction_for_single_product(all_matches)

            return {
                "product_name": input_data.product_name,
                "category": category,
                "success_probability": round(float(probability), 4),
                "prediction": prediction,
                "model_version": "v2.0-calibrated"
            }

        # CASE 2: Multiple products - use aggregation
        else:
            print(f"Multiple products found ({len(all_matches)}) - using aggregation")

            # Get predictions for all matching products
            predictions = []
            probabilities = []
            categories = []

            for idx, row in all_matches.iterrows():
                # Get single row dataframe for this product
                single_row = all_matches.loc[[idx]]

                prob, pred, cat = get_prediction_for_single_product(single_row)

                predictions.append(pred)
                probabilities.append(prob)
                categories.append(cat)

                print(f"  Product ID {row['product_id']}: {pred} (prob: {prob:.3f})")

            # Determine final prediction using aggregation rules
            # Rule 1: Try MODE (most common prediction)
            prediction_counts = Counter(predictions)
            most_common = prediction_counts.most_common(1)[0]  # Returns (value, count)

            # Check if there's a clear winner (not a tie)
            if len(prediction_counts) == 1 or (len(prediction_counts) == 2 and
                                               prediction_counts.most_common(2)[0][1] !=
                                               prediction_counts.most_common(2)[1][1]):
                # Use MODE - there's a clear most common prediction
                final_prediction = most_common[0]
                final_probability = np.mean([p for i, p in enumerate(probabilities)
                                            if predictions[i] == final_prediction])
                aggregation_method = "Mode (most common)"

                print(f"Using MODE: {final_prediction} appeared {most_common[1]}/{len(predictions)} times")

            else:
                # TIE or no clear winner - use MEAN
                mean_probability = np.mean(probabilities)
                final_probability = mean_probability
                final_prediction = "Success" if mean_probability >= 0.5 else "Fail"
                aggregation_method = "Mean (tie in mode)"

                print(f"Using MEAN: probability={mean_probability:.3f} -> {final_prediction}")

            # Get most common category
            category_counts = Counter(categories)
            most_common_category = category_counts.most_common(1)[0][0]

            # Calculate success rate for additional info
            success_count = sum(1 for p in predictions if p == "Success")
            success_rate = success_count / len(predictions)

            return {
                "product_name": input_data.product_name,
                "category": most_common_category,
                "success_probability": round(float(final_probability), 4),
                "prediction": final_prediction,
                "model_version": "v2.0-calibrated-aggregated",
                "aggregation_info": {
                    "products_analyzed": len(all_matches),
                    "method": aggregation_method,
                    "success_rate": round(success_rate, 4),
                    "individual_predictions": {
                        "Success": success_count,
                        "Fail": len(predictions) - success_count
                    }
                }
            }

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal Error: {str(e)}")