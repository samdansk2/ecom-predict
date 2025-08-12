import joblib
import pandas as pd
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import os

# ------------------- Load Models -------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
xgb_model = joblib.load(os.path.join(BASE_DIR, "../models/xgboost/xgb_model.pkl"))
mlp_model = joblib.load(os.path.join(BASE_DIR, "../models/nn/mlp_model.pkl"))
meta_model = joblib.load(os.path.join(BASE_DIR, "../models/meta/meta_model.pkl"))

# ------------------- Load Dataset -------------------
lookup_path = os.path.join(BASE_DIR, "../data/raw/ecommerce_sales.csv")
lookup_df = pd.read_csv(lookup_path)

# ------------------- Transformer Setup -------------------
model_name = "distilbert-base-uncased"  # ensure same as training
tokenizer = AutoTokenizer.from_pretrained(model_name)
bert_model = AutoModel.from_pretrained(model_name)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
bert_model.to(device)

# ------------------- FastAPI App -------------------
app = FastAPI(title="Product Success Prediction API")

# ------------------- Home Page -------------------
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Product Price Prediction</title>
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
        </style>
    </head>
    <body>
        <h1>Product Price Prediction</h1>
        
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
                    
                    let resultClass = result.prediction === "Success" ? "success" : "fail";
                    let probabilityPercent = (result.success_probability * 100).toFixed(1);
                    
                    document.getElementById('output').innerHTML = `
                        <div class="result-heading">Prediction Result</div>
                        <div class="result ${resultClass}">
                            <div class="result-item"><strong>Product:</strong> ${result.product_name}</div>
                            <div class="result-item"><strong>Category:</strong> ${result.category}</div>
                            <div class="result-item probability"><strong>Success Probability:</strong> ${probabilityPercent}%</div>
                            <div class="result-item"><strong>Prediction:</strong> ${result.prediction}</div>
                        </div>
                    `;
                } catch (error) {
                    document.getElementById('output').innerHTML = '<div class="result fail">Failed to get prediction. Please try again.</div>';
                }
            }
        </script>
    </body>
    </html>
    """

# ------------------- Input Schema -------------------
class ProductInput(BaseModel):
    product_name: str

# ------------------- Helper Functions -------------------
def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=16)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        outputs = bert_model(**inputs)
    return outputs.last_hidden_state[:, 0, :].cpu().numpy().flatten()

def safe_get_value(row, col, default):
    return row[col].values[0] if col in row.columns and not pd.isna(row[col].values[0]) else default

def standardize_features(price, review_score, review_count, total_sales, avg_sales_per_month):
    """Apply the same standardization used during training"""
    # These are the exact parameters from the training scaler
    means = np.array([2.47677130e+02, 3.02760000e+00, 5.26506000e+02, 6.01991200e+03, 5.01659333e+02])
    stds = np.array([144.53566113, 1.17065718, 282.12876132, 991.77752559, 82.64812713])
    
    raw_values = np.array([price, review_score, review_count, total_sales, avg_sales_per_month])
    standardized = (raw_values - means) / stds
    
    return standardized

# ------------------- Prediction Endpoint -------------------
@app.post("/predict")
def predict(input_data: ProductInput):
    try:
        print(f"Received product: {input_data.product_name}")

        # Lookup product
        product_row = lookup_df[lookup_df['product_name'].str.lower() == input_data.product_name.lower()]

        if product_row.empty:
            raise HTTPException(status_code=404, detail="Product not found")
        
        category = safe_get_value(product_row, 'category', "Clothing")
        price = safe_get_value(product_row, 'price', 299.0)
        review_score = safe_get_value(product_row, 'review_score', 4.0)
        review_count = safe_get_value(product_row, 'review_count', 50)

        monthly_cols = [col for col in product_row.columns if 'sales_month' in col]
        if monthly_cols:
            monthly_sales = product_row[monthly_cols].values.flatten()
        else:
            monthly_sales = np.array([40] * 12)

        # Derived features
        total_sales = monthly_sales.sum()
        avg_sales = monthly_sales.mean()
        sales_variability = monthly_sales.std()
        sales_trend = (monthly_sales[-3:].mean() / monthly_sales[:3].mean()) if monthly_sales[:3].mean() > 0 else 1
        price_bucket_low = 1 if price <= 200 else 0
        price_bucket_high = 1 if price >= 500 else 0

        # Standardize the numeric features that were normalized during training
        standardized_features = standardize_features(price, review_score, review_count, total_sales, avg_sales)
        std_price, std_review_score, std_review_count, std_total_sales, std_avg_sales = standardized_features

        # Category encoding - Match training format (one-hot with boolean columns)
        # Based on the processed data: category_Clothing, category_Electronics, category_Health, category_Home & Kitchen, category_Sports, category_Toys
        category_features = {
            "Clothing": [1, 0, 0, 0, 0, 0],
            "Electronics": [0, 1, 0, 0, 0, 0], 
            "Health": [0, 0, 1, 0, 0, 0],
            "Home & Kitchen": [0, 0, 0, 1, 0, 0],
            "Sports": [0, 0, 0, 0, 1, 0],
            "Toys": [0, 0, 0, 0, 0, 1],
            "Books": [0, 0, 0, 0, 0, 0]  # Books category doesn't appear in training data, so all zeros
        }
        cat_vector = category_features.get(category, [0, 0, 0, 0, 0, 0])  # Default to all zeros if unknown category

        # Embedding
        emb = get_embedding(input_data.product_name)

        # Combine features - Use standardized versions for the numeric features that were normalized
        numeric_features = [
            std_price, std_review_score, std_review_count, std_total_sales, std_avg_sales,  # Standardized features
            sales_variability, sales_trend, price_bucket_low, price_bucket_high  # Non-standardized features
        ] + cat_vector
        combined_features = np.concatenate([numeric_features, emb]).reshape(1, -1)

        # Ensure correct shape for model
        required_features = 796  # based on training
        current_features = combined_features.shape[1]
        if current_features < required_features:
            padding = np.zeros((1, required_features - current_features))
            combined_features = np.hstack((combined_features, padding))
        elif current_features > required_features:
            combined_features = combined_features[:, :required_features]

        # Model predictions
        xgb_pred = xgb_model.predict_proba(combined_features)[:, 1]
        mlp_pred = mlp_model.predict_proba(combined_features)[:, 1]
        stack_input = np.column_stack((xgb_pred, mlp_pred))
        final_pred_proba = meta_model.predict_proba(stack_input)[:, 1][0]
        final_pred_label = int(final_pred_proba >= 0.5)

        return {
            "product_name": input_data.product_name,
            "category": category,
            "success_probability": round(float(final_pred_proba), 4),
            "prediction": "Success" if final_pred_label == 1 else "Fail"
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal Error: {str(e)}")
