import joblib
import pandas as pd
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel
from fastapi import FastAPI, HTTPException
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

# ------------------- Prediction Endpoint -------------------
@app.post("/predict")
def predict(input_data: ProductInput):
    try:
        print(f"Received product: {input_data.product_name}")

        # Lookup product
        product_row = lookup_df[lookup_df['product_name'].str.lower() == input_data.product_name.lower()]

        # Defaults for missing products
        if product_row.empty:
            print("Product not found. Using fallback defaults.")
            category = "Clothing"
            price = 299.0
            review_score = 4.0
            review_count = 50
            monthly_sales = np.array([40] * 12)
        else:
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

        # Category encoding
        category_features = {
            "Clothing": [1, 0, 0, 0, 0],
            "Home & Kitchen": [0, 1, 0, 0, 0],
            "Toys": [0, 0, 1, 0, 0],
            "Books": [0, 0, 0, 1, 0],
            "Electronics": [0, 0, 0, 0, 1]
        }
        cat_vector = category_features.get(category, [0, 0, 0, 0, 0])

        # Embedding
        emb = get_embedding(input_data.product_name)

        # Combine features
        numeric_features = [
            price, review_score, review_count,
            total_sales, avg_sales, sales_variability, sales_trend,
            price_bucket_low, price_bucket_high
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
            "prediction": "Success" if final_pred_label == 1 else "Fail",
            "note": "Defaults used" if product_row.empty else "Exact match"
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal Error: {str(e)}")
