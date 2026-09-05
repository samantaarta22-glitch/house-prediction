import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="House Price Predictor", layout="wide", page_icon="🏠")

# ============ LOAD ARTIFACTS ============
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

# ============ HEADER ============
st.title("🏠 USA House Price Predictor")
st.caption("Predicting house prices in the Seattle & Greater Washington State area using Random Forest + Optimization Random Search")

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview", "🔍 Analytics", "🎯 Price Prediction", "⚙️ Model Details"
])

# ============ TAB 1: OVERVIEW ============
with tab1:
    st.header("Dataset Overview")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Records", f"{len(df_clean):,}")
    col2.metric("Median Price", f"${df_clean['price'].median():,.0f}")
    col3.metric("Number of Cities", f"{df_clean['city'].nunique()}")
    col4.metric("Model R²", f"{metrics['r2']:.4f}")

    st.markdown("""
    This dataset contains historical house sale records from the Washington State area, USA.
    Before use, the data went through a cleaning process to remove invalid price values
    (zero prices and extreme outliers identified as corrupted data).
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Price Distribution")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.histplot(df_clean['price'], bins=50, kde=True, ax=ax, color='#1f77b4')
        ax.set_xlabel("Price ($)")
        st.pyplot(fig)

    with col2:
        st.subheader("Living Area Distribution")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.histplot(df_clean['sqft_living'], bins=50, kde=True, ax=ax, color='#ff7f0e')
        ax.set_xlabel("Sqft Living")
        st.pyplot(fig)

    st.subheader("Median Price by City (Top 15)")
    top_cities = df_clean['city'].value_counts().head(15).index
    city_price = df_clean[df_clean['city'].isin(top_cities)].groupby('city')['price'].median().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(city_price.index[::-1], city_price.values[::-1], color='#2ca02c')
    ax.set_xlabel("Median Price ($)")
    st.pyplot(fig)

    st.subheader("Waterfront vs Non-Waterfront")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(x='waterfront', y='price', data=df_clean, ax=ax)
    ax.set_xticklabels(['Non-Waterfront', 'Waterfront'])
    st.pyplot(fig)

# ============ TAB 2: ANALYTICS ============
with tab2:
    st.header("Analytics & Model Insight")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Feature Importance")
        fig, ax = plt.subplots(figsize=(8, 6))
        top_features = importance_df.head(10)
        ax.barh(top_features['feature'][::-1], top_features['importance'][::-1], color='#9467bd')
        ax.set_xlabel("Importance")
        st.pyplot(fig)

    with col2:
        st.subheader("Correlation Heatmap")
        numeric_cols = ['price', 'bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot',
                         'floors', 'waterfront', 'view', 'condition', 'sqft_basement']
        corr = df_clean[numeric_cols].corr()
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0, ax=ax, cbar=False)
        st.pyplot(fig)

    st.subheader("Predicted vs Actual (Test Set)")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(test_data['actual_price'], test_data['predicted_price'], alpha=0.4, color='#d62728')
    max_val = max(test_data['actual_price'].max(), test_data['predicted_price'].max())
    ax.plot([0, max_val], [0, max_val], 'k--', label='Perfect Prediction')
    ax.set_xlabel("Actual Price ($)")
    ax.set_ylabel("Predicted Price ($)")
    ax.legend()
    st.pyplot(fig)

    st.subheader("Residual Distribution (Prediction Error)")
    residuals = test_data['actual_price'] - test_data['predicted_price']
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(residuals, bins=50, kde=True, ax=ax, color='#8c564b')
    ax.axvline(0, color='black', linestyle='--')
    ax.set_xlabel("Residual ($) — Actual minus Predicted")
    st.pyplot(fig)

    st.subheader("Sqft Living vs Price (colored by prediction error)")
    fig, ax = plt.subplots(figsize=(10, 6))
    abs_error = np.abs(residuals)
    scatter = ax.scatter(test_data['sqft_living'], test_data['actual_price'],
                          c=abs_error, cmap='YlOrRd', alpha=0.6)
    plt.colorbar(scatter, label='Absolute Error ($)')
    ax.set_xlabel("Sqft Living")
    ax.set_ylabel("Actual Price ($)")
    st.pyplot(fig)

# ============ TAB 3: PREDICTION ============
with tab3:
    st.header("Predict a New House Price")

    col1, col2 = st.columns(2)

    with col1:
        bedrooms = st.number_input("Number of Bedrooms", min_value=0, max_value=10, value=3)
        bathrooms = st.number_input("Number of Bathrooms", min_value=0.0, max_value=8.0, value=2.0, step=0.25)
        sqft_living = st.number_input("Living Area (sqft)", min_value=200, max_value=15000, value=1800)
        sqft_lot = st.number_input("Lot Area (sqft)", min_value=200, max_value=1000000, value=5000)
        floors = st.selectbox("Number of Floors", [1.0, 1.5, 2.0, 2.5, 3.0])
        waterfront = st.selectbox("Waterfront?", [0, 1], format_func=lambda x: "Yes" if x==1 else "No")

    with col2:
        view = st.slider("View Score (0-4)", 0, 4, 0)
        condition = st.slider("Condition Score (1-5)", 1, 5, 3)
        sqft_basement = st.number_input("Basement Area (sqft)", min_value=0, max_value=5000, value=0)
        house_age = st.number_input("House Age (years)", min_value=0, max_value=130, value=20)
        is_renovated = st.selectbox("Ever Renovated?", [0, 1], format_func=lambda x: "Yes" if x==1 else "No")
        years_since_renovation = st.number_input("Years Since Renovation/Built", min_value=0, max_value=130, value=20)

    city = st.selectbox("City", city_list)
    zip_code = st.number_input("ZIP Code", min_value=98000, max_value=99000, value=98103)

    if st.button("Predict Price", type="primary"):
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
        st.success(f"### Estimated Price: ${prediction:,.0f}")

        st.caption(f"Reasonable range (±model MAE): ${prediction - metrics['mae']:,.0f} — ${prediction + metrics['mae']:,.0f}")

# ============ TAB 4: MODEL DETAILS ============
with tab4:
    st.header("Model Details & Optimization Journey")

    st.markdown("""
    This model went through several optimization iterations. Here's the comparison:
    """)

    st.dataframe(
        comparison_df.style.format({'R2': '{:.4f}', 'RMSE': '${:,.0f}', 'MAE': '${:,.0f}'}),
        use_container_width=True
    )

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(comparison_df['Stage'], comparison_df['R2'], marker='o', linewidth=2, color='#1f77b4')
    ax.set_ylabel("R² Score")
    ax.set_xticklabels(comparison_df['Stage'], rotation=15, ha='right')
    ax.grid(alpha=0.3)
    st.pyplot(fig)

    st.markdown("""
    **What was done at each stage:**
    1. **Baseline** — Random Forest with default params, city encoded using frequency encoding
    2. **Target Encoding + Tuning** — replaced city with target encoding (K-Fold, leakage-free), hyperparameter tuning via RandomizedSearchCV
    3. **Final Model** — added target encoding for `zip` (more granular than city), added interaction features (`lot_to_living_ratio`, `total_rooms`, `bath_bed_ratio`, `sqft_living_per_bathroom`), re-tuned hyperparameters

    **Best hyperparameters (final model):**
    """)
    st.json({
        'n_estimators': metrics['n_estimators'],
        'min_samples_split': metrics['min_samples_split'],
        'min_samples_leaf': metrics['min_samples_leaf'],
    })