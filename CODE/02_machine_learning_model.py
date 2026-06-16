"""
Machine Learning Model for Economic Growth Prediction
Builds and evaluates multiple models for predicting economic output
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import warnings
warnings.filterwarnings('ignore')

# Configuration
DATA_PATH = "../DATA_SET/Economics_ML_Dataset.csv"
OUTPUT_DIR = "./model_results"

# Create output directory
Path(OUTPUT_DIR).mkdir(exist_ok=True)

print("\n" + "="*80)
print("MACHINE LEARNING MODEL DEVELOPMENT")
print("="*80)

# Load and prepare data
print("\nLoading and preparing data...")
df = pd.read_csv(DATA_PATH)
df['Date'] = pd.to_datetime(df['Date'])

# Features and target
X = df.drop(['Date', 'Target_Economic_Output'], axis=1)
y = df['Target_Economic_Output']

feature_names = X.columns.tolist()
print(f"Number of features: {len(feature_names)}")
print(f"Features: {feature_names}")
print(f"Target variable: Target_Economic_Output")
print(f"Dataset size: {X.shape[0]} samples")

# Split data
print("\nSplitting data into train (80%) and test (20%)...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"Training set: {X_train.shape[0]} samples")
print(f"Test set: {X_test.shape[0]} samples")

# Standardize features
print("\nStandardizing features...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("\n" + "="*80)
print("MODEL 1: LINEAR REGRESSION (Baseline)")
print("="*80)

lr_model = LinearRegression()
lr_model.fit(X_train_scaled, y_train)
y_pred_lr = lr_model.predict(X_test_scaled)

lr_mse = mean_squared_error(y_test, y_pred_lr)
lr_mae = mean_absolute_error(y_test, y_pred_lr)
lr_r2 = r2_score(y_test, y_pred_lr)
lr_rmse = np.sqrt(lr_mse)

print(f"\nPerformance Metrics:")
print(f"  R² Score: {lr_r2:.4f}")
print(f"  RMSE: {lr_rmse:.4f}")
print(f"  MAE: {lr_mae:.4f}")

# Feature importance for Linear Regression
lr_importance = pd.DataFrame({
    'Feature': feature_names,
    'Coefficient': lr_model.coef_
}).sort_values('Coefficient', key=abs, ascending=False)
print(f"\nTop 5 Important Features:")
print(lr_importance.head())

print("\n" + "="*80)
print("MODEL 2: RIDGE REGRESSION (Regularized)")
print("="*80)

ridge_model = Ridge(alpha=1.0)
ridge_model.fit(X_train_scaled, y_train)
y_pred_ridge = ridge_model.predict(X_test_scaled)

ridge_mse = mean_squared_error(y_test, y_pred_ridge)
ridge_mae = mean_absolute_error(y_test, y_pred_ridge)
ridge_r2 = r2_score(y_test, y_pred_ridge)
ridge_rmse = np.sqrt(ridge_mse)

print(f"\nPerformance Metrics:")
print(f"  R² Score: {ridge_r2:.4f}")
print(f"  RMSE: {ridge_rmse:.4f}")
print(f"  MAE: {ridge_mae:.4f}")

print("\n" + "="*80)
print("MODEL 3: RANDOM FOREST (Ensemble)")
print("="*80)

rf_model = RandomForestRegressor(
    n_estimators=100,
    max_depth=10,
    min_samples_split=5,
    random_state=42,
    n_jobs=-1
)
rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test)

rf_mse = mean_squared_error(y_test, y_pred_rf)
rf_mae = mean_absolute_error(y_test, y_pred_rf)
rf_r2 = r2_score(y_test, y_pred_rf)
rf_rmse = np.sqrt(rf_mse)

print(f"\nPerformance Metrics:")
print(f"  R² Score: {rf_r2:.4f}")
print(f"  RMSE: {rf_rmse:.4f}")
print(f"  MAE: {rf_mae:.4f}")

# Feature importance for Random Forest
rf_importance = pd.DataFrame({
    'Feature': feature_names,
    'Importance': rf_model.feature_importances_
}).sort_values('Importance', ascending=False)

print(f"\nTop 5 Important Features:")
print(rf_importance.head())

# Cross-validation scores
print("\n" + "="*80)
print("CROSS-VALIDATION ANALYSIS (5-Fold)")
print("="*80)

cv_scores_lr = cross_val_score(LinearRegression(), X_train_scaled, y_train, 
                                cv=5, scoring='r2')
cv_scores_rf = cross_val_score(RandomForestRegressor(n_estimators=100, random_state=42), 
                                X_train, y_train, cv=5, scoring='r2')

print(f"\nLinear Regression CV R² Scores: {cv_scores_lr}")
print(f"  Mean: {cv_scores_lr.mean():.4f}, Std: {cv_scores_lr.std():.4f}")

print(f"\nRandom Forest CV R² Scores: {cv_scores_rf}")
print(f"  Mean: {cv_scores_rf.mean():.4f}, Std: {cv_scores_rf.std():.4f}")

# Model Comparison
print("\n" + "="*80)
print("MODEL COMPARISON")
print("="*80)

comparison_df = pd.DataFrame({
    'Model': ['Linear Regression', 'Ridge Regression', 'Random Forest'],
    'R² Score': [lr_r2, ridge_r2, rf_r2],
    'RMSE': [lr_rmse, ridge_rmse, rf_rmse],
    'MAE': [lr_mae, ridge_mae, rf_mae]
})

print("\n", comparison_df.to_string(index=False))

# Visualizations
print("\n" + "="*80)
print("GENERATING VISUALIZATIONS")
print("="*80)

# Prediction comparison
fig, axes = plt.subplots(1, 3, figsize=(16, 4))
fig.suptitle('Predicted vs Actual Values (Test Set)', fontsize=14, fontweight='bold')

models = [
    ('Linear Regression', y_pred_lr, lr_r2),
    ('Ridge Regression', y_pred_ridge, ridge_r2),
    ('Random Forest', y_pred_rf, rf_r2)
]

for idx, (name, y_pred, r2) in enumerate(models):
    ax = axes[idx]
    ax.scatter(y_test, y_pred, alpha=0.6, s=50)
    ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    ax.set_xlabel('Actual Values')
    ax.set_ylabel('Predicted Values')
    ax.set_title(f'{name}\nR² = {r2:.4f}')
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/predictions_comparison.png', dpi=300, bbox_inches='tight')
print(f"✓ Predictions comparison saved")

# Feature importance (Random Forest)
fig, ax = plt.subplots(figsize=(10, 6))
rf_importance_top = rf_importance.head(10)
ax.barh(rf_importance_top['Feature'], rf_importance_top['Importance'], color='steelblue')
ax.set_xlabel('Importance Score')
ax.set_title('Top 10 Features - Random Forest Model')
ax.invert_yaxis()
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/feature_importance.png', dpi=300, bbox_inches='tight')
print(f"✓ Feature importance plot saved")

# Model performance comparison
fig, axes = plt.subplots(1, 3, figsize=(14, 4))
fig.suptitle('Model Performance Comparison', fontsize=14, fontweight='bold')

metrics = ['R² Score', 'RMSE', 'MAE']
models_names = ['Linear', 'Ridge', 'Random Forest']
values = [
    [lr_r2, ridge_r2, rf_r2],
    [lr_rmse, ridge_rmse, rf_rmse],
    [lr_mae, ridge_mae, rf_mae]
]

colors = ['#3498db', '#e74c3c', '#2ecc71']
for idx, (metric, vals) in enumerate(zip(metrics, values)):
    ax = axes[idx]
    bars = ax.bar(models_names, vals, color=colors, alpha=0.7, edgecolor='black')
    ax.set_ylabel(metric)
    ax.set_title(metric)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.4f}', ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/model_performance_comparison.png', dpi=300, bbox_inches='tight')
print(f"✓ Model performance comparison saved")

# Residuals analysis
fig, axes = plt.subplots(1, 3, figsize=(16, 4))
fig.suptitle('Residuals Analysis (Test Set)', fontsize=14, fontweight='bold')

residuals_data = [
    ('Linear Regression', y_test - y_pred_lr),
    ('Ridge Regression', y_test - y_pred_ridge),
    ('Random Forest', y_test - y_pred_rf)
]

for idx, (name, residuals) in enumerate(residuals_data):
    ax = axes[idx]
    ax.scatter(y_pred_rf if idx == 2 else (y_pred_ridge if idx == 1 else y_pred_lr), 
               residuals, alpha=0.6, s=50)
    ax.axhline(y=0, color='r', linestyle='--', lw=2)
    ax.set_xlabel('Predicted Values')
    ax.set_ylabel('Residuals')
    ax.set_title(f'{name}')
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/residuals_analysis.png', dpi=300, bbox_inches='tight')
print(f"✓ Residuals analysis saved")

# Save results to file
print("\n" + "="*80)
print("SAVING RESULTS")
print("="*80)

results_text = f"""
MACHINE LEARNING MODEL RESULTS
================================

DATASET INFORMATION
-------------------
Total Samples: {X.shape[0]}
Number of Features: {len(feature_names)}
Train/Test Split: 80/20

MODEL PERFORMANCE COMPARISON
----------------------------

1. LINEAR REGRESSION (Baseline)
   R² Score: {lr_r2:.4f}
   RMSE: {lr_rmse:.4f}
   MAE: {lr_mae:.4f}
   CV Mean R²: {cv_scores_lr.mean():.4f}

2. RIDGE REGRESSION (Regularized)
   R² Score: {ridge_r2:.4f}
   RMSE: {ridge_rmse:.4f}
   MAE: {ridge_mae:.4f}

3. RANDOM FOREST (Ensemble)
   R² Score: {rf_r2:.4f}
   RMSE: {rf_rmse:.4f}
   MAE: {rf_mae:.4f}
   CV Mean R²: {cv_scores_rf.mean():.4f}

BEST MODEL: {'Random Forest' if rf_r2 == max(lr_r2, ridge_r2, rf_r2) else 'Linear Regression' if lr_r2 == max(lr_r2, ridge_r2, rf_r2) else 'Ridge Regression'}
Best R² Score: {max(lr_r2, ridge_r2, rf_r2):.4f}

TOP 5 FEATURES (Random Forest)
------------------------------
{rf_importance.head().to_string(index=False)}

INTERPRETATION
--------------
The Random Forest model performs best with R² Score of {rf_r2:.4f}, explaining 
{rf_r2*100:.2f}% of the variance in economic output. The model's predictions 
have an average error (MAE) of {rf_mae:.4f}%.

Key drivers of economic growth:
{chr(10).join([f'  {i+1}. {row["Feature"]} ({row["Importance"]:.4f})' for i, row in rf_importance.head(5).iterrows()])}
"""

with open(f'{OUTPUT_DIR}/model_results.txt', 'w') as f:
    f.write(results_text)

print(f"✓ Results saved to {OUTPUT_DIR}/model_results.txt")

# Save comparison CSV
comparison_df.to_csv(f'{OUTPUT_DIR}/model_comparison.csv', index=False)
print(f"✓ Model comparison saved to {OUTPUT_DIR}/model_comparison.csv")

# Save feature importance CSV
rf_importance.to_csv(f'{OUTPUT_DIR}/feature_importance.csv', index=False)
print(f"✓ Feature importance saved to {OUTPUT_DIR}/feature_importance.csv")

print("\n" + "="*80)
print("✓ MODEL DEVELOPMENT COMPLETE!")
print("="*80)
print(f"\nAll results saved to: {OUTPUT_DIR}/")
print(f"Generated files:")
print(f"  - predictions_comparison.png")
print(f"  - feature_importance.png")
print(f"  - model_performance_comparison.png")
print(f"  - residuals_analysis.png")
print(f"  - model_results.txt")
print(f"  - model_comparison.csv")
print(f"  - feature_importance.csv")
