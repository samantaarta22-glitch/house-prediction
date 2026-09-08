import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from datetime import datetime
import io
import base64

# ============ PAGE CONFIG ============
st.set_page_config(
    page_title="Nexus Property AI | Advanced Analytics", 
    layout="wide", 
    page_icon="🌌",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/nexus-property-ai',
        'Report a bug': 'https://github.com/nexus-property-ai/issues',
        'About': '# Nexus Property AI v2.0\nAdvanced Real Estate Analytics Platform'
    }
)

# ============ FUTURISTIC CSS ============
st.markdown("""
<style>
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Header: jangan di-hide total, cukup bikin transparan 
    biar tombol hamburger (☰) buat toggle sidebar tetap keliatan */
    [data-testid="stHeader"] {
    background: transparent !important;
    }
    [data-testid="stHeader"] [data-testid="stToolbarActions"] {
    visibility: hidden;
    }
    
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #1a1a3a 50%, #24243e 100%);
        color: #e0e6ed;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0a1f 0%, #1a1a3a 100%);
        border-right: 1px solid rgba(0, 242, 254, 0.2);
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #00f2fe !important;
    }
    
    /* Header Styling */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 15px;
        border: 1px solid rgba(0, 242, 254, 0.2);
        box-shadow: 0 0 20px rgba(0, 242, 254, 0.1);
        margin-bottom: 2rem;
    }
    .main-header h1 {
        color: #00f2fe;
        text-shadow: 0 0 10px rgba(0, 242, 254, 0.5);
        margin: 0;
        font-weight: 800;
        letter-spacing: 2px;
    }
    
    /* Metric Cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(0, 242, 254, 0.3);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 242, 254, 0.4);
        border-color: #00f2fe;
    }
    .metric-card h3 {
        color: #a0aec0;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin: 0;
    }
    .metric-card h1 {
        color: #00f2fe;
        font-size: 2rem;
        margin: 10px 0 0 0;
        text-shadow: 0 0 8px rgba(0, 242, 254, 0.4);
    }
    
    /* Prediction Result */
    .prediction-result {
        background: linear-gradient(135deg, rgba(0, 242, 254, 0.1), rgba(79, 172, 254, 0.1));
        border: 2px solid #00f2fe;
        border-radius: 15px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 0 30px rgba(0, 242, 254, 0.3);
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { box-shadow: 0 0 15px rgba(0, 242, 254, 0.3); }
        50% { box-shadow: 0 0 30px rgba(0, 242, 254, 0.6); }
    }
    
    /* Button Styling */
    .stButton>button {
        background: linear-gradient(90deg, #00f2fe, #4facfe);
        color: #0f0c29;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        box-shadow: 0 4px 15px rgba(0, 242, 254, 0.4);
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(0, 242, 254, 0.6);
    }
    
    /* Sidebar Navigation */
    .nav-item {
        padding: 12px 20px;
        margin: 5px 0;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        border-left: 3px solid transparent;
    }
    .nav-item:hover {
        background: rgba(0, 242, 254, 0.1);
        border-left-color: #00f2fe;
    }
    .nav-item.active {
        background: rgba(0, 242, 254, 0.2);
        border-left-color: #00f2fe;
        color: #00f2fe;
    }
    
    /* Info Box */
    .info-box {
        background: rgba(255, 255, 255, 0.03);
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #00f2fe;
        margin: 15px 0;
    }
    
    /* History Card */
    .history-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(0, 242, 254, 0.2);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        transition: all 0.3s ease;
    }
    .history-card:hover {
        background: rgba(0, 242, 254, 0.1);
        border-color: #00f2fe;
    }
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
    }
    ::-webkit-scrollbar-thumb {
        background: #00f2fe;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #4facfe;
    }
</style>
""", unsafe_allow_html=True)

# ============ SESSION STATE INITIALIZATION ============
if 'prediction_history' not in st.session_state:
    st.session_state.prediction_history = []
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Dashboard'
if 'filters' not in st.session_state:
    st.session_state.filters = {
        'cities': [],
        'price_range': (0, 10000000),
        'bedrooms_min': 0
    }

# ============ LOAD DATA & MODELS ============
@st.cache_resource
def load_model_artifacts():
    model = joblib.load('house_price_model.pkl')
    city_mapping = joblib.load('city_mapping.pkl')
    zip_mapping = joblib.load('zip_mapping.pkl')
    feature_columns = joblib.load('feature_columns.pkl')
    city_list = joblib.load('city_list.pkl')
    metrics = joblib.load('model_metrics.pkl')
    return model, city_mapping, zip_mapping, feature_columns, city_list, metrics

@st.cache_data
def load_data():
    df_clean = pd.read_csv('house_clean_final.csv')
    test_data = pd.read_csv('test_data_with_predictions.csv')
    importance_df = pd.read_csv('feature_importance.csv')
    comparison_df = pd.read_csv('model_comparison.csv')
    return df_clean, test_data, importance_df, comparison_df

model, city_mapping, zip_mapping, feature_columns, city_list, metrics = load_model_artifacts()
df_clean, test_data, importance_df, comparison_df = load_data()

# ============ HELPER FUNCTIONS ============
def get_filtered_data(df, filters):
    """Apply global filters to dataframe"""
    filtered = df.copy()
    
    if filters['cities']:
        filtered = filtered[filtered['city'].isin(filters['cities'])]
    
    filtered = filtered[
        (filtered['price'] >= filters['price_range'][0]) & 
        (filtered['price'] <= filters['price_range'][1])
    ]
    
    if filters['bedrooms_min'] > 0:
        filtered = filtered[filtered['bedrooms'] >= filters['bedrooms_min']]
    
    return filtered

def create_metric_card(title, value, icon="📊"):
    """Create a styled metric card"""
    return f"""
    <div class="metric-card">
        <h3>{icon} {title}</h3>
        <h1>{value}</h1>
    </div>
    """

def add_to_history(prediction_data):
    """Add prediction to session state history"""
    prediction_data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    prediction_data['id'] = len(st.session_state.prediction_history) + 1
    st.session_state.prediction_history.insert(0, prediction_data)
    
    # Keep only last 20 predictions
    if len(st.session_state.prediction_history) > 20:
        st.session_state.prediction_history = st.session_state.prediction_history[:20]

def download_csv(df, filename="data_export.csv"):
    """Create download button for CSV"""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">📥 Download CSV</a>'
    return href

# ============ SIDEBAR ============
with st.sidebar:
    st.markdown("## 🌌 NEXUS AI")
    st.markdown("---")
    
    # Navigation Menu
    st.markdown("### 🧭 NAVIGATION")
    pages = ["Dashboard", "Data Explorer", "Analytics", "Prediction", "History", "Model Specs"]
    
    for page in pages:
        if st.button(f"{'📊' if page == 'Dashboard' else '🔍' if page == 'Data Explorer' else '📈' if page == 'Analytics' else '🎯' if page == 'Prediction' else '📜' if page == 'History' else '⚙️'} {page}", 
                     use_container_width=True,
                     key=f"nav_{page}"):
            st.session_state.current_page = page
            st.rerun()
    
    st.markdown("---")
    
    # Global Filters
    st.markdown("### 🎛️ GLOBAL FILTERS")
    
    selected_cities = st.multiselect(
        "Filter by City",
        options=city_list,
        default=st.session_state.filters['cities'],
        help="Select cities to filter data"
    )
    st.session_state.filters['cities'] = selected_cities
    
    price_range = st.slider(
        "Price Range ($)",
        min_value=0,
        max_value=int(df_clean['price'].max()),
        value=st.session_state.filters['price_range'],
        step=50000,
        help="Filter by price range"
    )
    st.session_state.filters['price_range'] = price_range
    
    bedrooms_min = st.number_input(
        "Min Bedrooms",
        min_value=0,
        max_value=10,
        value=st.session_state.filters['bedrooms_min'],
        help="Show only houses with at least this many bedrooms"
    )
    st.session_state.filters['bedrooms_min'] = bedrooms_min
    
    if st.button("🔄 Reset Filters", use_container_width=True):
        st.session_state.filters = {
            'cities': [],
            'price_range': (0, int(df_clean['price'].max())),
            'bedrooms_min': 0
        }
        st.rerun()
    
    st.markdown("---")
    
    # Quick Stats
    st.markdown("### 📊 QUICK STATS")
    filtered_df = get_filtered_data(df_clean, st.session_state.filters)
    
    st.metric("Filtered Records", f"{len(filtered_df):,}")
    st.metric("Avg Price", f"${filtered_df['price'].mean():,.0f}")
    st.metric("Median Sqft", f"{filtered_df['sqft_living'].median():,.0f}")
    
    st.markdown("---")
    
    # Model Info
    st.markdown("### 🤖 MODEL STATUS")
    st.success("✅ Model Loaded")
    st.info(f"R² Score: {metrics['r2']:.4f}")
    st.warning(f"MAE: ${metrics['mae']:,.0f}")
    
    st.markdown("---")
    
        # Credits
    st.markdown("### ℹ️ ABOUT")
    st.markdown("""
    **Nexus Property AI v2.0**  
    Advanced Real Estate Analytics Platform  
    👤 *Created by: **Samantha Arta Sinuhaji***
    
    Built with:
    - Streamlit
    - Plotly
    - Random Forest
    
    © 2026 Nexus AI
    """)


# ============ MAIN CONTENT ============
current_page = st.session_state.current_page

# Apply global filters
filtered_df = get_filtered_data(df_clean, st.session_state.filters)

# ============ PAGE: DASHBOARD ============
if current_page == 'Dashboard':
    st.markdown("""
    <div class="main-header">
        <h1>🌌 NEXUS PROPERTY AI</h1>
        <p>Advanced Predictive Analytics for Real Estate Valuation</p>
    </div>
    """, unsafe_allow_html=True)
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(create_metric_card("Total Records", f"{len(filtered_df):,}", "📊"), unsafe_allow_html=True)
    with col2:
        st.markdown(create_metric_card("Median Price", f"${filtered_df['price'].median():,.0f}", "💰"), unsafe_allow_html=True)
    with col3:
        st.markdown(create_metric_card("Cities", f"{filtered_df['city'].nunique()}", "🏙️"), unsafe_allow_html=True)
    with col4:
        st.markdown(create_metric_card("Model R²", f"{metrics['r2']:.4f}", "🎯"), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Info Box
    st.markdown("""
    <div class="info-box">
        <b>📌 Welcome to Nexus Property AI!</b><br>
        Platform ini menggunakan machine learning untuk memprediksi harga rumah di area Washington State, USA. 
        Gunakan sidebar untuk navigasi dan filter data secara real-time.
    </div>
    """, unsafe_allow_html=True)
    
    # Charts Section
    st.markdown("### 📈 KEY VISUALIZATIONS")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### Price Distribution")
        fig = px.histogram(filtered_df, x='price', nbins=50, marginal='box', 
                          color_discrete_sequence=['#00f2fe'], template='plotly_dark')
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                         font_color='#e0e6ed', showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("##### Living Area vs Price")
        fig = px.scatter(filtered_df.sample(min(1000, len(filtered_df))), 
                        x='sqft_living', y='price', 
                        color='bedrooms', color_continuous_scale='ice',
                        template='plotly_dark', opacity=0.6)
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                         font_color='#e0e6ed')
        st.plotly_chart(fig, use_container_width=True)
    
    # Top Cities
    st.markdown("##### 🏙️ Top 15 Cities by Median Price")
    top_cities = filtered_df['city'].value_counts().head(15).index
    city_price = filtered_df[filtered_df['city'].isin(top_cities)].groupby('city')['price'].median().sort_values(ascending=True)
    
    fig = px.bar(x=city_price.values, y=city_price.index, orientation='h',
                color=city_price.values, color_continuous_scale='ice', template='plotly_dark')
    fig.update_layout(yaxis_title="City", xaxis_title="Median Price ($)",
                     plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                     font_color='#e0e6ed', showlegend=False, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # Download Button
    st.markdown(download_csv(filtered_df.head(1000), "filtered_data.csv"), unsafe_allow_html=True)

# ============ PAGE: DATA EXPLORER ============
elif current_page == 'Data Explorer':
    st.markdown("## 🔍 DATA EXPLORER")
    st.markdown("Explore the dataset with interactive filters and visualizations.")
    
    # Advanced Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        bedroom_filter = st.multiselect("Bedrooms", sorted(filtered_df['bedrooms'].unique()),
                                       default=sorted(filtered_df['bedrooms'].unique())[:3])
    
    with col2:
        waterfront_filter = st.selectbox("Waterfront", ["All", "Yes", "No"])
    
    with col3:
        condition_filter = st.slider("Condition Range", 1, 5, (1, 5))
    
    # Apply filters
    explorer_df = filtered_df.copy()
    if bedroom_filter:
        explorer_df = explorer_df[explorer_df['bedrooms'].isin(bedroom_filter)]
    if waterfront_filter != "All":
        explorer_df = explorer_df[explorer_df['waterfront'] == (1 if waterfront_filter == "Yes" else 0)]
    explorer_df = explorer_df[(explorer_df['condition'] >= condition_filter[0]) & 
                             (explorer_df['condition'] <= condition_filter[1])]
    
    st.markdown(f"**Showing {len(explorer_df):,} records**")
    
    # Interactive Table
    st.markdown("### 📋 Interactive Data Table")
    st.dataframe(
        explorer_df.head(500),
        use_container_width=True,
        height=400
    )
    
    # Export
    st.markdown(download_csv(explorer_df, "explorer_data.csv"), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Visualizations
    st.markdown("### 📊 DISTRIBUTION ANALYSIS")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### Price by Bedrooms")
        fig = px.box(explorer_df, x='bedrooms', y='price', color='bedrooms',
            template='plotly_dark')
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                         font_color='#e0e6ed', showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("##### Condition Distribution")
        condition_counts = explorer_df['condition'].value_counts().sort_index()
        fig = px.bar(x=condition_counts.index, y=condition_counts.values,
                    color=condition_counts.values, color_continuous_scale='plasma',
                    template='plotly_dark')
        fig.update_layout(xaxis_title="Condition", yaxis_title="Count",
                         plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                         font_color='#e0e6ed', showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # 3D Visualization
    st.markdown("### 🎮 3D VISUALIZATION")
    st.markdown("Interactive 3D scatter plot: Sqft Living vs Lot vs Price")
    
    fig = px.scatter_3d(explorer_df.sample(min(500, len(explorer_df))),
                       x='sqft_living', y='sqft_lot', z='price',
                       color='bedrooms', size='bathrooms',
                       color_continuous_scale='ice',
                       template='plotly_dark', opacity=0.7)
    fig.update_layout(scene=dict(
        xaxis_title='Sqft Living',
        yaxis_title='Sqft Lot',
        zaxis_title='Price ($)'
    ), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
    font_color='#e0e6ed', height=600)
    st.plotly_chart(fig, use_container_width=True)

# ============ PAGE: ANALYTICS ============
elif current_page == 'Analytics':
    st.markdown("## 📈 ANALYTICS & INSIGHTS")
    st.markdown("Deep dive into feature relationships and model performance.")
    
    # Feature Importance
    st.markdown("### 🎯 FEATURE IMPORTANCE")
    top_features = importance_df.head(15).sort_values('importance', ascending=True)
    
    fig = px.bar(top_features, x='importance', y='feature', orientation='h',
                color='importance', color_continuous_scale='plasma', template='plotly_dark')
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                     font_color='#e0e6ed', showlegend=False, coloraxis_showscale=False,
                     height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Correlation Heatmap
    st.markdown("### 🔥 CORRELATION ANALYSIS")
    numeric_cols = ['price', 'bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot',
               'floors', 'waterfront', 'view', 'condition', 'sqft_basement']
    corr = filtered_df[numeric_cols].corr()
    
    fig = px.imshow(corr, text_auto=".2f", color_continuous_scale='rdbu_r',
                   aspect="auto", template='plotly_dark')
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                     font_color='#e0e6ed', coloraxis_showscale=False, height=600)
    st.plotly_chart(fig, use_container_width=True)
    
    # Model Performance
    st.markdown("### 📊 MODEL PERFORMANCE")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### Predicted vs Actual")
        fig = px.scatter(test_data, x='actual_price', y='predicted_price',
                        opacity=0.5, color_discrete_sequence=['#ff007f'], template='plotly_dark')
        max_val = max(test_data['actual_price'].max(), test_data['predicted_price'].max())
        fig.add_trace(go.Scatter(x=[0, max_val], y=[0, max_val], mode='lines',
                                name='Perfect Prediction', line=dict(dash='dash', color='#00f2fe')))
        fig.update_layout(xaxis_title="Actual Price ($)", yaxis_title="Predicted Price ($)",
                         plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                         font_color='#e0e6ed')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("##### Residual Distribution")
        residuals = test_data['actual_price'] - test_data['predicted_price']
        fig = px.histogram(x=residuals, nbins=50, marginal='box',
                          color_discrete_sequence=['#7b2cbf'], template='plotly_dark')
        fig.add_vline(x=0, line_dash="dash", line_color="#00f2fe")
        fig.update_layout(xaxis_title="Residual ($)", yaxis_title="Count",
                         plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                         font_color='#e0e6ed', showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Price by Year Built
    st.markdown("### 📅 PRICE TRENDS BY YEAR")
    year_price = filtered_df.groupby('yr_built')['price'].median().reset_index()
    
    fig = px.line(year_price, x='yr_built', y='price',
                 color_discrete_sequence=['#00f2fe'], template='plotly_dark')
    fig.update_layout(xaxis_title="Year Built", yaxis_title="Median Price ($)",
                     plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                     font_color='#e0e6ed')
    fig.update_traces(line=dict(width=3))
    st.plotly_chart(fig, use_container_width=True)

# ============ PAGE: PREDICTION ============
elif current_page == 'Prediction':
    st.markdown("## 🎯 PREDICTION TERMINAL")
    st.markdown("Enter property specifications to get AI-powered price estimation.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏗️ Physical Specifications")
        bedrooms = st.number_input("Bedrooms", min_value=0, max_value=10, value=3)
        bathrooms = st.number_input("Bathrooms", min_value=0.0, max_value=8.0, value=2.0, step=0.25)
        sqft_living = st.number_input("Living Area (sqft)", min_value=200, max_value=15000, value=1800)
        sqft_lot = st.number_input("Lot Area (sqft)", min_value=200, max_value=1000000, value=5000)
        floors = st.selectbox("Floors", [1.0, 1.5, 2.0, 2.5, 3.0])
        waterfront = st.selectbox("Waterfront View?", [0, 1], format_func=lambda x: "Yes" if x==1 else "No")
    
    with col2:
        st.markdown("### 🌟 Condition & Features")
        view = st.slider("View Score (0-4)", 0, 4, 0)
        condition = st.slider("Condition Score (1-5)", 1, 5, 3)
        sqft_basement = st.number_input("Basement Area (sqft)", min_value=0, max_value=5000, value=0)
        house_age = st.number_input("House Age (years)", min_value=0, max_value=130, value=20)
        is_renovated = st.selectbox("Ever Renovated?", [0, 1], format_func=lambda x: "Yes" if x==1 else "No")
        years_since_renovation = st.number_input("Years Since Renovation/Built", min_value=0, max_value=130, value=20)
    
    st.markdown("---")
    st.markdown("### 📍 Location Data")
    col1, col2 = st.columns(2)
    with col1:
        city = st.selectbox("City", city_list)
    with col2:
        zip_code = st.number_input("ZIP Code", min_value=98000, max_value=99000, value=98103)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🚀 EXECUTE PREDICTION", use_container_width=True):
        with st.spinner("🔄 Processing prediction..."):
            time.sleep(0.5)  # Simulate processing
            
            # Feature Engineering
            global_mean = np.mean(list(city_mapping.values()))
            city_enc = city_mapping.get(city, global_mean)
            zip_enc = zip_mapping.get(zip_code, global_mean)
            
            sqft_living_per_bathroom = sqft_living / (bathrooms + 1)
            lot_to_living_ratio = sqft_lot / sqft_living
            total_rooms = bedrooms + bathrooms
            bath_bed_ratio = bathrooms / (bedrooms + 1)
            
            input_data = pd.DataFrame([{
                'bedrooms': bedrooms, 'bathrooms': bathrooms, 'sqft_living': sqft_living,
                'sqft_lot': sqft_lot, 'floors': floors, 'waterfront': waterfront,
                'view': view, 'condition': condition, 'sqft_basement': sqft_basement,
                'house_age': house_age, 'is_renovated': is_renovated,
                'years_since_renovation': years_since_renovation,
                'city_target_enc': city_enc, 'zip_target_enc': zip_enc,
                'sqft_living_per_bathroom': sqft_living_per_bathroom,
                'lot_to_living_ratio': lot_to_living_ratio,
                'total_rooms': total_rooms, 'bath_bed_ratio': bath_bed_ratio
            }])[feature_columns]
            
            prediction = model.predict(input_data)[0]
            
            # Save to history
            prediction_record = {
                'id': len(st.session_state.prediction_history) + 1,
                'prediction': prediction,
                'city': city,
                'bedrooms': bedrooms,
                'bathrooms': bathrooms,
                'sqft_living': sqft_living,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            add_to_history(prediction_record)
            
            # Display Result
            st.markdown(f"""
            <div class="prediction-result">
                <h2>ESTIMATED MARKET VALUE</h2>
                <h1>${prediction:,.0f}</h1>
                <p style="color: #a0aec0; margin-top: 10px;">
                    Confidence Interval (±MAE): <b style="color:#00f2fe;">${prediction - metrics['mae']:,.0f}</b> — <b style="color:#00f2fe;">${prediction + metrics['mae']:,.0f}</b>
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.success("✅ Prediction saved to history!")

# ============ PAGE: HISTORY ============
elif current_page == 'History':
    st.markdown("## 📜 PREDICTION HISTORY")
    st.markdown("View and analyze your past predictions.")
    
    if len(st.session_state.prediction_history) == 0:
        st.info("📭 No predictions yet. Make your first prediction in the Prediction tab!")
    else:
        # Summary Stats
        col1, col2, col3, col4 = st.columns(4)
        predictions_df = pd.DataFrame(st.session_state.prediction_history)
        
        with col1:
            st.markdown(create_metric_card("Total Predictions", len(predictions_df), "📊"), unsafe_allow_html=True)
        with col2:
            st.markdown(create_metric_card("Avg Prediction", f"${predictions_df['prediction'].mean():,.0f}", "💰"), unsafe_allow_html=True)
        with col3:
            st.markdown(create_metric_card("Highest", f"${predictions_df['prediction'].max():,.0f}", "📈"), unsafe_allow_html=True)
        with col4:
            st.markdown(create_metric_card("Lowest", f"${predictions_df['prediction'].min():,.0f}", "📉"), unsafe_allow_html=True)
        
        st.markdown("---")
        
        # History Timeline
        st.markdown("### 📅 Prediction Timeline")
        fig = px.line(predictions_df, x='timestamp', y='prediction',
                     markers=True, color_discrete_sequence=['#00f2fe'],
                     template='plotly_dark')
        fig.update_layout(xaxis_title="Time", yaxis_title="Predicted Price ($)",
                         plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                         font_color='#e0e6ed')
        st.plotly_chart(fig, use_container_width=True)
        
        # History Table
        st.markdown("### 📋 Detailed History")
        st.dataframe(predictions_df, use_container_width=True, height=400)
        
        # Export
        st.markdown(download_csv(predictions_df, "prediction_history.csv"), unsafe_allow_html=True)
        
        # Clear History
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.prediction_history = []
            st.rerun()

# ============ PAGE: MODEL SPECS ============
elif current_page == 'Model Specs':
    st.markdown("## ⚙️ MODEL SPECIFICATIONS")
    st.markdown("Technical details and optimization journey.")
    
    # Model Comparison
    st.markdown("### 📊 MODEL COMPARISON")
    st.dataframe(
        comparison_df.style.format({'R2': '{:.4f}', 'RMSE': '${:,.0f}', 'MAE': '${:,.0f}'}),
        use_container_width=True,
        height=250
    )
    
    # R² Evolution
    st.markdown("### 📈 R² SCORE EVOLUTION")
    fig = px.line(comparison_df, x='Stage', y='R2', markers=True,
                 color_discrete_sequence=['#00f2fe'], template='plotly_dark')
    fig.update_layout(xaxis_title="Optimization Stage", yaxis_title="R² Score",
                     plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                     font_color='#e0e6ed')
    fig.update_traces(line=dict(width=4), marker=dict(size=10))
    st.plotly_chart(fig, use_container_width=True)
    
    # Optimization Pipeline
    st.markdown("### 🛠️ OPTIMIZATION PIPELINE")
    
    with st.expander("📌 Stage 1: Baseline Model"):
        st.markdown("""
        - Random Forest dengan parameter default
        - City encoded menggunakan frequency encoding
        - **R² Score**: {:.4f}
        """.format(comparison_df.iloc[0]['R2']))
    
    with st.expander("📌 Stage 2: Target Encoding + Tuning"):
        st.markdown("""
        - Mengganti city dengan target encoding (K-Fold, leakage-free)
        - Hyperparameter tuning via RandomizedSearchCV
        - **R² Score**: {:.4f}
        """.format(comparison_df.iloc[1]['R2']))
    
    with st.expander("📌 Stage 3: Final Model (Current)"):
        st.markdown("""
        - Menambahkan target encoding untuk `zip` (lebih granular)
        - Interaction features: `lot_to_living_ratio`, `total_rooms`, `bath_bed_ratio`, `sqft_living_per_bathroom`
        - Re-tuning hyperparameters
        - **R² Score**: {:.4f}
        """.format(comparison_df.iloc[2]['R2']))
    
    # Hyperparameters
    st.markdown("### 🧬 BEST HYPERPARAMETERS")
    st.json({
        'n_estimators': metrics['n_estimators'],
        'min_samples_split': metrics['min_samples_split'],
        'min_samples_leaf': metrics['min_samples_leaf'],
        'max_depth': metrics.get('max_depth', 'None'),
        'max_features': metrics.get('max_features', 'sqrt')
    })
    
    # Model Metrics
    st.markdown("### 📊 PERFORMANCE METRICS")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(create_metric_card("R² Score", f"{metrics['r2']:.4f}", "🎯"), unsafe_allow_html=True)
    with col2:
        st.markdown(create_metric_card("MAE", f"${metrics['mae']:,.0f}", "📏"), unsafe_allow_html=True)
    with col3:
        st.markdown(create_metric_card("RMSE", f"${metrics['rmse']:,.0f}", "📐"), unsafe_allow_html=True)

# ============ FOOTER ============
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #a0aec0; padding: 20px;">
    <p>🌌 Nexus Property AI v2.0 | Advanced Real Estate Analytics Platform</p>
    <p>Built with Streamlit, Plotly, and Machine Learning</p>
    <p>© 2026 Nexus AI. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)