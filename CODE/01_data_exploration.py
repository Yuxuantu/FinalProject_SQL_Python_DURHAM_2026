"""
Data Exploration and Analysis Script
Exploratory Data Analysis for Economics ML Dataset
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Configuration
DATA_PATH = "../DATA_SET/Economics_ML_Dataset.csv"
OUTPUT_DIR = "./analysis_results"

# Create output directory
Path(OUTPUT_DIR).mkdir(exist_ok=True)

# Load dataset
print("Loading dataset...")
df = pd.read_csv(DATA_PATH)
df['Date'] = pd.to_datetime(df['Date'])

print("\n" + "="*80)
print("DATASET OVERVIEW")
print("="*80)
print(f"\nDataset shape: {df.shape}")
print(f"Time period: {df['Date'].min()} to {df['Date'].max()}")
print(f"\nColumn names and types:\n{df.dtypes}")

print("\n" + "="*80)
print("BASIC STATISTICS")
print("="*80)
print(df.describe())

print("\n" + "="*80)
print("MISSING VALUES")
print("="*80)
missing = df.isnull().sum()
if missing.sum() == 0:
    print("No missing values detected!")
else:
    print(missing[missing > 0])

print("\n" + "="*80)
print("CORRELATION ANALYSIS")
print("="*80)
# Calculate correlations with target variable
numeric_df = df.select_dtypes(include=[np.number])
correlations = numeric_df.corr()['Target_Economic_Output'].sort_values(ascending=False)
print("\nFeature correlations with Target_Economic_Output:")
print(correlations)

# Create correlation heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(correlations.corr(), annot=True, fmt='.2f', cmap='coolwarm', center=0)
plt.title('Feature Correlation Heatmap')
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/correlation_heatmap.png', dpi=300, bbox_inches='tight')
print(f"\n✓ Correlation heatmap saved to {OUTPUT_DIR}/correlation_heatmap.png")

print("\n" + "="*80)
print("TIME SERIES ANALYSIS")
print("="*80)

# Plot key economic indicators over time
fig, axes = plt.subplots(3, 2, figsize=(14, 10))
fig.suptitle('Economic Indicators Over Time', fontsize=14, fontweight='bold')

axes[0, 0].plot(df['Date'], df['GDP_Growth_Rate'], marker='o', linewidth=2)
axes[0, 0].set_title('GDP Growth Rate (%)')
axes[0, 0].grid(True, alpha=0.3)

axes[0, 1].plot(df['Date'], df['Unemployment_Rate'], marker='o', color='red', linewidth=2)
axes[0, 1].set_title('Unemployment Rate (%)')
axes[0, 1].grid(True, alpha=0.3)

axes[1, 0].plot(df['Date'], df['Inflation_Rate'], marker='o', color='green', linewidth=2)
axes[1, 0].set_title('Inflation Rate (%)')
axes[1, 0].grid(True, alpha=0.3)

axes[1, 1].plot(df['Date'], df['Interest_Rate'], marker='o', color='orange', linewidth=2)
axes[1, 1].set_title('Interest Rate (%)')
axes[1, 1].grid(True, alpha=0.3)

axes[2, 0].plot(df['Date'], df['Consumer_Confidence'], marker='o', color='purple', linewidth=2)
axes[2, 0].set_title('Consumer Confidence Index')
axes[2, 0].grid(True, alpha=0.3)

axes[2, 1].plot(df['Date'], df['Stock_Market_Index'], marker='o', color='brown', linewidth=2)
axes[2, 1].set_title('Stock Market Index')
axes[2, 1].grid(True, alpha=0.3)

for ax in axes.flat:
    ax.tick_params(axis='x', rotation=45)
    ax.set_xlabel('Date')

plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/economic_indicators_timeseries.png', dpi=300, bbox_inches='tight')
print(f"✓ Time series plot saved to {OUTPUT_DIR}/economic_indicators_timeseries.png")

# Distribution analysis
print("\n" + "="*80)
print("DISTRIBUTION ANALYSIS")
print("="*80)

fig, axes = plt.subplots(2, 3, figsize=(14, 8))
fig.suptitle('Feature Distributions', fontsize=14, fontweight='bold')

features_to_plot = ['GDP_Growth_Rate', 'Unemployment_Rate', 'Inflation_Rate', 
                    'Interest_Rate', 'Consumer_Confidence', 'Stock_Market_Index']

for idx, feature in enumerate(features_to_plot):
    ax = axes[idx // 3, idx % 3]
    ax.hist(df[feature], bins=15, edgecolor='black', alpha=0.7)
    ax.set_title(f'{feature}')
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('Value')
    ax.set_ylabel('Frequency')

plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/distribution_analysis.png', dpi=300, bbox_inches='tight')
print(f"✓ Distribution plot saved to {OUTPUT_DIR}/distribution_analysis.png")

print("\n" + "="*80)
print("KEY INSIGHTS")
print("="*80)
print(f"\nTarget Variable Statistics:")
print(f"  Mean: {df['Target_Economic_Output'].mean():.3f}%")
print(f"  Std Dev: {df['Target_Economic_Output'].std():.3f}%")
print(f"  Min: {df['Target_Economic_Output'].min():.3f}%")
print(f"  Max: {df['Target_Economic_Output'].max():.3f}%")

print(f"\nStrongest Positive Correlations with Target:")
top_corr = correlations[correlations < 1.0].nlargest(5)
for feature, corr in top_corr.items():
    print(f"  {feature}: {corr:.3f}")

print("\n" + "="*80)
print("✓ Exploratory Data Analysis Complete!")
print("="*80)
