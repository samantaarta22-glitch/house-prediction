# 🏠 USA House Price Predictor

Predicting house prices in the Seattle & Greater Washington State area using Random Forest, with an interactive Streamlit dashboard for exploration and prediction.

🔗 🔗 **Live Demo:** [Open the Streamlit App](https://house-prediction-pn7jwovny8dlujnhdwmuwu.streamlit.app/)

## 📸 Dashboard Preview

### Overview Page
![Overview](https://github.com/user-attachments/assets/ee54de62-b0bd-4e8b-aa84-ddff9f63b8b3)

### Prediction Terminal  
![Prediction](https://github.com/user-attachments/assets/38eebee9-00d2-448d-af9c-dc6828cef037)

### Analytics
![Analytics](https://github.com/user-attachments/assets/ca4e7e65-603b-40ee-9439-73f7e3b6f9d4)

## Overview

This project predicts house sale prices based on property specifications (size, location, condition, etc.) using historical housing data from Washington State, USA (4,140 records).

## Key Results

| Stage | R² | RMSE | MAE |
|---|---|---|---|
| Baseline (default Random Forest) | 0.5115 | $202,997 | $125,047 |
| + Target Encoding (city) + Hyperparameter Tuning | 0.6637 | $168,439 | $103,677 |
| + Target Encoding (zip) + Feature Interaction + Re-tuning | **0.7722** | **$138,630** | **$85,277** |

## Data Cleaning

The raw dataset looked clean at first glance (no explicit missing values), but contained hidden data quality issues:
- 49 rows with `price = 0` (invalid)
- Extreme outliers with unrealistic prices (e.g., $950 billion for a 3,330 sqft house) — clearly corrupted data
- 1 row with an unrealistically low price ($7,800)

After cleaning: 4,001 valid records remained.

## Feature Engineering

- **Target encoding** for `city` and `zip` (K-Fold, leakage-free) — far more informative than simple frequency encoding
- **Derived features**: house age, years since renovation, `sqft_living_per_bathroom`, `lot_to_living_ratio`, `total_rooms`, `bath_bed_ratio`
- Dropped redundant/uninformative columns: `sqft_above` (highly correlated with `sqft_living`), `country`, `street`

## Model

Random Forest Regressor, tuned via `RandomizedSearchCV` (5-fold CV, 30 candidate combinations).

**Best hyperparameters:**


## App Features

The Streamlit app has 4 sections:
1. **Overview** — dataset statistics, price distribution, median price by city
2. **Analytics** — feature importance, correlation heatmap, predicted vs actual, residual analysis
3. **Price Prediction** — interactive form to predict a new house's price
4. **Model Details** — optimization journey and hyperparameters

## Running Locally

```bash
git clone https://github.com/samantaarta22-glitch/house-prediction.git

cd house-prediction

pip install -r requirements.txt

streamlit run app.py
```

## Tech Stack

Python, pandas, scikit-learn, Streamlit, matplotlib, seaborn

## Dataset

[USA Housing Dataset](https://www.kaggle.com/datasets) — Kaggle
