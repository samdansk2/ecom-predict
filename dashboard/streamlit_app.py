import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# ------------------- Streamlit UI -------------------
st.set_page_config(page_title="Product Success Prediction", page_icon="🛒", layout="wide")

# Custom CSS for attractive background and styling
st.markdown("""
<style>
    /* Dark gradient background for modern look */
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #1e3c72 100%);
        background-attachment: fixed;
    }
    
    /* Main content area with semi-transparent background */
    .main .block-container {
        padding-top: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        margin-top: 1rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    /* Success prediction card */
    .success-card {
        background: linear-gradient(135deg, #28a745, #34ce57);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
    }
    
    /* Failure prediction card */
    .fail-card {
        background: linear-gradient(135deg, #dc3545, #fd7e14);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(220, 53, 69, 0.3);
    }
    
    /* Ensure inputs are clearly visible with semi-transparent background */
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid #667eea !important;
        color: #2c3e50 !important;
        font-weight: 500 !important;
        backdrop-filter: blur(10px);
    }
    
    .stTextInput > div > div > input:focus {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-color: #4c63d2 !important;
        box-shadow: 0 0 0 0.3rem rgba(102, 126, 234, 0.4) !important;
        color: #2c3e50 !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #6c757d !important;
        font-weight: 400;
    }
    
    /* Style buttons */
    .stButton > button {
        background: linear-gradient(135deg, #48c78e, #5ddc96);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(72, 199, 142, 0.4);
    }
    
    /* Headers with better contrast and visibility on dark background */
    h1 {
        color: #ffffff !important;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #48c78e, #5ddc96);
        color: white !important;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(72, 199, 142, 0.3);
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    h2, h3 {
        color: #ffffff !important;
        font-weight: 600;
        text-shadow: 0 1px 3px rgba(0,0,0,0.5);
    }
    
    h4, h5, h6 {
        color: #f8f9fa !important;
        font-weight: 500;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
    }
    
    /* Sub-headings and general text visibility on dark background */
    .stMarkdown h3 {
        background: rgba(255, 255, 255, 0.1);
        padding: 0.5rem 1rem;
        border-radius: 8px;
        border-left: 4px solid #48c78e;
        color: #ffffff !important;
        backdrop-filter: blur(10px);
    }
    
    /* All text elements for better visibility on dark background */
    p, div, span, label {
        color: #f8f9fa !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
    }
    
    /* Labels for input fields */
    .stTextInput > label {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        margin-bottom: 0.5rem !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
    }
    
    /* Metrics styling - Semi-transparent background with border */
    .stMetric {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        border-left: 4px solid #48c78e;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
    }
    
    .stMetric [data-testid="metric-container"] {
        background: transparent;
        border: none;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Tabs styling - Semi-transparent background */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 5px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 10px 20px;
        color: #ffffff;
        font-weight: 600;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(5px);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #48c78e, #5ddc96);
        color: white;
    }
    
    /* Visualization containers with better text visibility */
    .visualization-section {
        background: rgba(255, 255, 255, 0.1);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 15px rgba(0,0,0,0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
    }
    
    .visualization-section p, .visualization-section strong {
        color: #ffffff !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, #48c78e, #5ddc96);
    }
    
    /* Remove white backgrounds from containers */
    .stContainer {
        background: transparent;
    }
    
    /* Sidebar styling if present */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Additional overrides for white backgrounds */
    .stMarkdown {
        background: transparent;
    }
    
    /* Info/warning/error boxes */
    .stAlert {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 8px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Data frames if any */
    .stDataFrame {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 8px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Plotly chart containers with dark theme */
    .js-plotly-plot {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Override any remaining white backgrounds */
    [data-testid="stVerticalBlock"] {
        background: transparent;
    }
    
    [data-testid="stHorizontalBlock"] {
        background: transparent;
    }
    
    /* Success/Error message boxes */
    .stSuccess {
        background: rgba(40, 167, 69, 0.1);
        border-left: 4px solid #28a745;
        backdrop-filter: blur(10px);
    }
    
    .stError {
        background: rgba(220, 53, 69, 0.1);
        border-left: 4px solid #dc3545;
        backdrop-filter: blur(10px);
    }
    
    .stWarning {
        background: rgba(255, 193, 7, 0.1);
        border-left: 4px solid #ffc107;
        backdrop-filter: blur(10px);
    }
    
    /* Additional text visibility improvements */
    .stMarkdown p {
        background: transparent;
        padding: 0.5rem;
        border-radius: 5px;
        color: #f8f9fa !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
    }
    
    /* Metric labels and values */
    .stMetric [data-testid="metric-container"] > div {
        color: #ffffff !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
    }
    
    /* Tab labels */
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 10px 20px;
        color: #ffffff !important;
        font-weight: 600;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(5px);
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
    }
    
        .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #48c78e, #5ddc96);
        color: white !important;
        text-shadow: none;
        border: 1px solid transparent;
    }    /* Button text visibility */
    .stButton > button {
        color: white !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.2) !important;
    }
    
    /* Warning/Error/Success message text */
    .stAlert > div {
        color: #ffffff !important;
        font-weight: 500 !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
    }
    
    /* Additional text visibility fixes for all elements */
    .stMarkdown, .stMarkdown p, .stMarkdown div, .stMarkdown span,
    .stText, .stText p, .stText div, .stText span,
    [data-testid="stMarkdownContainer"], [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] div, [data-testid="stMarkdownContainer"] span,
    .element-container, .element-container p, .element-container div, .element-container span {
        color: #f8f9fa !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
    }
    
    /* Ensure all tab content text is visible */
    .stTabs [data-baseweb="tab-panel"] p, .stTabs [data-baseweb="tab-panel"] div,
    .stTabs [data-baseweb="tab-panel"] span, .stTabs [data-baseweb="tab-panel"] strong {
        color: #ffffff !important;
        background: transparent !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
    }
    
    /* Visualization section text - force white text */
    .visualization-section *, .visualization-section p, .visualization-section div,
    .visualization-section span, .visualization-section strong, .visualization-section em {
        color: #ffffff !important;
        background: transparent !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
    }
    
    /* All markdown content in tabs and sections */
    .stTabs .stMarkdown, .stTabs .stMarkdown *,
    .visualization-section .stMarkdown, .visualization-section .stMarkdown * {
        color: #ffffff !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
    }
    
    /* Override any remaining dark text */
    * {
        color: #f8f9fa !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
    }
    
    /* Input fields should have dark text on light background */
    .stTextInput > div > div > input,
    .stTextInput > div > div > input:focus {
        color: #2c3e50 !important;
        text-shadow: none !important;
    }
    
    /* Specific overrides for white text elements */
    .success-card *, .fail-card *, .stButton button *,
    h1, h1 *, .stTabs [aria-selected="true"] * {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load the processed dataset for visualizations"""
    data_path = "../data/processed/ecommerce_sales_featured.csv"
    try:
        df = pd.read_csv(data_path)
        return df
    except FileNotFoundError:
        # Try alternative path
        data_path = "data/processed/ecommerce_sales_featured.csv"
        try:
            df = pd.read_csv(data_path)
            return df
        except FileNotFoundError:
            return None

def create_category_distribution_chart(df):
    """Create category distribution pie chart"""
    category_columns = [col for col in df.columns if col.startswith('category_')]
    category_data = []
    
    for col in category_columns:
        category_name = col.replace('category_', '')
        count = df[col].sum()
        category_data.append({'Category': category_name, 'Count': count})
    
    category_df = pd.DataFrame(category_data)
    
    fig = px.pie(category_df, 
                 values='Count', 
                 names='Category',
                 title="📊 Product Category Distribution",
                 color_discrete_sequence=px.colors.qualitative.Set3)
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12, color='white'),
        title_font_size=16,
        title_font_color='white'
    )
    
    return fig

def create_success_rate_chart(df):
    """Create success rate by category bar chart"""
    category_columns = [col for col in df.columns if col.startswith('category_')]
    success_data = []
    
    for col in category_columns:
        category_name = col.replace('category_', '')
        category_products = df[df[col] == 1]
        if len(category_products) > 0:
            success_rate = category_products['success'].mean() * 100
            success_data.append({'Category': category_name, 'Success Rate': success_rate})
    
    success_df = pd.DataFrame(success_data)
    success_df = success_df.sort_values('Success Rate', ascending=True)
    
    fig = px.bar(success_df, 
                 x='Success Rate', 
                 y='Category',
                 orientation='h',
                 title="🎯 Success Rate by Product Category",
                 color='Success Rate',
                 color_continuous_scale='Viridis')
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12, color='white'),
        title_font_size=16,
        title_font_color='white',
        xaxis_title="Success Rate (%)",
        yaxis_title="Category",
        xaxis=dict(color='white'),
        yaxis=dict(color='white')
    )
    
    return fig

def create_price_vs_success_scatter(df):
    """Create price vs success probability scatter plot"""
    sample_df = df.sample(min(500, len(df)))
    
    sample_df = sample_df.copy()
    if 'review_count' in sample_df.columns:
        min_review = sample_df['review_count'].min()
        if min_review < 0:
            sample_df['review_count_size'] = (sample_df['review_count'] - min_review) + 5
            sample_df['review_count_size'] = sample_df['review_count_size'] * (45 / sample_df['review_count_size'].max())
        else:
            sample_df['review_count_size'] = sample_df['review_count']
        size_col = 'review_count_size'
    else:
        size_col = None
    
    fig = px.scatter(sample_df, 
                     x='price', 
                     y='avg_sales_per_month',
                     color='success',
                     size=size_col,
                     title="💰 Price vs Sales Performance",
                     labels={'price': 'Price (Normalized)', 
                             'avg_sales_per_month': 'Average Sales per Month',
                             'success': 'Success'},
                     color_discrete_map={0: '#ff6b6b', 1: '#51cf66'})
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12, color='white'),
        title_font_size=16,
        title_font_color='white',
        xaxis=dict(color='white'),
        yaxis=dict(color='white')
    )
    
    return fig

def create_review_analysis_chart(df):
    """Create review score vs success rate analysis"""
    df['review_score_bin'] = pd.cut(df['review_score'], bins=5, labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])
    
    review_success = df.groupby('review_score_bin', observed=False)['success'].mean().reset_index()
    review_success['success_rate'] = review_success['success'] * 100
    
    fig = px.bar(review_success,
                 x='review_score_bin',
                 y='success_rate',
                 title="⭐ Review Score Impact on Success Rate",
                 color='success_rate',
                 color_continuous_scale='RdYlGn')
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12, color='white'),
        title_font_size=16,
        title_font_color='white',
        xaxis_title="Review Score Range",
        yaxis_title="Success Rate (%)",
        xaxis=dict(color='white'),
        yaxis=dict(color='white')
    )
    
    return fig

st.markdown("""
    <h1 style='text-align: center; color: #ffffff; font-size: 3rem; margin-bottom: 0.5rem; text-shadow: 0 2px 4px rgba(0,0,0,0.5);'>
        🛒 Product Success Prediction Dashboard
    </h1>
    <p style='text-align: center; color: #e9ecef; font-size: 1.2rem; margin-bottom: 2rem; text-shadow: 0 1px 2px rgba(0,0,0,0.3);'>
        🚀 Discover your product's potential with AI-powered predictions!
    </p>
""", unsafe_allow_html=True)

df = load_data()

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("""
        <div style='background: rgba(72, 199, 142, 0.15); padding: 2rem; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.3); border-left: 5px solid #48c78e; backdrop-filter: blur(10px);'>
            <h3 style='color: #ffffff; margin-top: 0; text-shadow: 0 1px 2px rgba(0,0,0,0.3);'>🔮 Make a Prediction</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")  # Add some space
    
    product_name = st.text_input("Product Name", placeholder="e.g. Sports Shoes, Laptop, Skincare Set")

    if st.button("🔮 Predict Success", type="primary"):
        if not product_name.strip():
            st.warning("⚠️ Please enter a valid product name.")
        else:
            try:
                # Call FastAPI endpoint
                response = requests.post("http://localhost:8000/predict", json={"product_name": product_name})
                
                if response.status_code == 200:
                    result = response.json()

                    if "error" in result:
                        st.error(f"❌ {result['message']}")
                    else:
                        prob = result["success_probability"] * 100
                        label = result["prediction"]

                        if label == "Success":
                            st.markdown("""
                            <div class="success-card">
                                <h3>✅ Prediction: SUCCESS</h3>
                                <p>This product has high potential!</p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown("""
                            <div class="fail-card">
                                <h3>❌ Prediction: NEEDS IMPROVEMENT</h3>
                                <p>Consider optimizing this product.</p>
                            </div>
                            """, unsafe_allow_html=True)

                        st.markdown("---")
                        st.subheader("📊 Prediction Details")
                        
                        metric_col1, metric_col2 = st.columns(2)
                        with metric_col1:
                            st.metric(label="🎯 Success Probability", value=f"{prob:.1f}%")
                        with metric_col2:
                            st.metric(label="📂 Category", value=result['category'])
                        
                        st.write(f"**Product:** {result['product_name']}")
                        st.progress(float(result["success_probability"]))

                else:
                    st.error(f"Server Error: {response.status_code}")
            except Exception as e:
                st.error(f"Connection Failed ❌\n{e}")

with col2:
    st.markdown("""
        <div style='background: rgba(72, 199, 142, 0.15); padding: 2rem; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.3); border-left: 5px solid #48c78e; backdrop-filter: blur(10px);'>
            <h3 style='color: #ffffff; margin-top: 0; text-shadow: 0 1px 2px rgba(0,0,0,0.3);'>📈 Quick Stats</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("") 
    
    if df is not None:
        total_products = len(df)
        success_rate = df['success'].mean() * 100
        
        metric_col1, metric_col2 = st.columns(2)
        with metric_col1:
            st.metric("📦 Products", f"{total_products:,}")
        with metric_col2:
            st.metric("🎯 Success Rate", f"{success_rate:.1f}%")
    else:
        st.info("📊 Analytics data not available")

if df is not None:
    st.markdown("---")
    st.markdown("""
        <h2 style='text-align: center; color: #ffffff; margin: 2rem 0; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.5);'>
            📊 Market Analytics & Insights
        </h2>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Categories", "🎯 Success Rates", "💰 Price Analysis", "⭐ Reviews"])
    
    with tab1:
        st.markdown('<div class="visualization-section">', unsafe_allow_html=True)
        fig1 = create_category_distribution_chart(df)
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown("**Insight:** This shows the distribution of products across different categories in our dataset.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="visualization-section">', unsafe_allow_html=True)
        fig2 = create_success_rate_chart(df)
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("**Insight:** Compare success rates across categories to identify the most promising markets.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="visualization-section">', unsafe_allow_html=True)
        fig3 = create_price_vs_success_scatter(df)
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown("**Insight:** Explore the relationship between pricing strategy and sales performance.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<div class="visualization-section">', unsafe_allow_html=True)
        fig4 = create_review_analysis_chart(df)
        st.plotly_chart(fig4, use_container_width=True)
        st.markdown("**Insight:** See how customer reviews impact product success rates.")
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #ffffff; padding: 2rem; background: rgba(72, 199, 142, 0.15); border-radius: 10px; margin-top: 2rem; backdrop-filter: blur(10px); border: 1px solid rgba(72, 199, 142, 0.3);'>
    <h4 style='color: #ffffff; text-shadow: 0 1px 2px rgba(0,0,0,0.3);'>🚀 AI-Powered Product Success Prediction</h4>
    <p style='color: #e9ecef; text-shadow: 0 1px 2px rgba(0,0,0,0.3);'>Leverage machine learning to predict product performance and make data-driven decisions.</p>
</div>
""", unsafe_allow_html=True)
