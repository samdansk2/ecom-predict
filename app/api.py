import joblib
import torch
from transformers import AutoTokenizer, AutoModel
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
from pathlib import Path

# --- Get project root directory ---
PROJECT_ROOT = Path(__file__).parent.parent

# --- Load Models ---
xgb_model = joblib.load(PROJECT_ROOT / "models" / "xgboost" / "xgb_model.pkl")
mlp_model = joblib.load(PROJECT_ROOT / "models" / "nn" / "mlp_model.pkl")
meta_model = joblib.load(PROJECT_ROOT / "models" / "meta" / "meta_model.pkl")

# --- Load Transformer ---
model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
bert_model = AutoModel.from_pretrained(model_name)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
bert_model.to(device)

# --- FastAPI App ---
app = FastAPI(title="Product Success Prediction API")

# --- Input Schema ---
class ProductInput(BaseModel):
    category: str
    price: float
    review_score: float
    review_count: int
    product_name: str
    monthly_sales: list  # 12 months sales data

# --- Generate Text Embedding ---
def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=16)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        outputs = bert_model(**inputs)
    return outputs.last_hidden_state[:, 0, :].cpu().numpy().flatten()

# --- API Endpoint ---
@app.post("/predict")
def predict(input_data: ProductInput):
    # Extract features
    sales = np.array(input_data.monthly_sales)
    total_sales = sales.sum()
    avg_sales = sales.mean()
    sales_variability = sales.std()
    sales_trend = (sales[-3:].mean() / sales[:3].mean()) if sales[:3].mean() > 0 else 1
    
    # Price bucket encoding
    price_bucket_low = 1 if input_data.price <= 200 else 0
    price_bucket_high = 1 if input_data.price >= 500 else 0
    
    # Encode category (dummy logic, in real case use full one-hot)
    category_features = {
        "Clothing": [1, 0, 0, 0, 0],
        "Home & Kitchen": [0, 1, 0, 0, 0],
        "Toys": [0, 0, 1, 0, 0],
        "Books": [0, 0, 0, 1, 0],
        "Electronics": [0, 0, 0, 0, 1]
    }
    cat_vector = category_features.get(input_data.category, [0, 0, 0, 0, 0])
    
    # Get text embedding
    emb = get_embedding(input_data.product_name)
    
    # Combine features
    numeric_features = [
        input_data.price, input_data.review_score, input_data.review_count,
        total_sales, avg_sales, sales_variability, sales_trend,
        price_bucket_low, price_bucket_high
    ] + cat_vector
    combined_features = np.concatenate([numeric_features, emb])
    combined_features = combined_features.reshape(1, -1)
    
    # Base model predictions
    xgb_pred = xgb_model.predict_proba(combined_features)[:, 1]
    mlp_pred = mlp_model.predict_proba(combined_features)[:, 1]
    
    # Stacked prediction
    stack_input = np.column_stack((xgb_pred, mlp_pred))
    final_pred_proba = meta_model.predict_proba(stack_input)[:, 1][0]
    final_pred_label = int(final_pred_proba >= 0.5)
    
    return {
        "success_probability": float(final_pred_proba),
        "prediction": "Success" if final_pred_label == 1 else "Fail"
    }
