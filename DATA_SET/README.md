# Economics Machine Learning Dataset

## Dataset Description
This dataset contains monthly economic indicators from January 2020 to June 2024, designed for machine learning projects in economics and quantitative analysis.

## Features

| Column | Description | Unit |
|--------|-------------|------|
| **Date** | Monthly observation date | YYYY-MM-DD |
| **GDP_Growth_Rate** | Quarter-on-Quarter GDP Growth | Percentage (%) |
| **Unemployment_Rate** | National Unemployment Rate | Percentage (%) |
| **Inflation_Rate** | Consumer Price Index Inflation | Percentage (%) |
| **Interest_Rate** | Central Bank Base Interest Rate | Percentage (%) |
| **Stock_Market_Index** | Major Stock Market Index Level | Index Points |
| **Consumer_Confidence** | Consumer Confidence Index | Index (0-100) |
| **Investment_Rate** | Gross Fixed Capital Formation | Percentage of GDP |
| **Exports** | Total Exports | Billions of Currency Units |
| **Imports** | Total Imports | Billions of Currency Units |
| **Government_Spending** | Government Expenditure | Billions of Currency Units |
| **Private_Consumption** | Private Consumption Expenditure | Billions of Currency Units |
| **Industrial_Production** | Industrial Production Index | Index (2015=100) |
| **Housing_Index** | Real Estate/Housing Index | Index Points |
| **Target_Economic_Output** | Economic Growth Target Variable | Percentage (%) |

## Dataset Characteristics
- **Time Period**: January 2020 - June 2024 (54 months)
- **Frequency**: Monthly
- **Total Records**: 54
- **Total Features**: 15
- **Target Variable**: Target_Economic_Output (Economic Growth Prediction)

## Use Cases
This dataset is suitable for:
- Economic forecasting and prediction models
- Time series analysis
- Regression analysis (predicting GDP growth)
- Correlation analysis between economic indicators
- Machine learning model development (XGBoost, Random Forest, Neural Networks)
- Feature importance analysis
- Economic indicator relationships study

## Key Observations
- Period covers significant economic events (COVID-19 pandemic, recovery, inflation surge, interest rate hikes)
- Natural variations in economic cycles from recession to recovery
- Strong relationships between multiple indicators

## Suggested Models
1. **Linear/Ridge Regression** - Baseline model
2. **Random Forest** - Non-linear relationships
3. **XGBoost/LightGBM** - Advanced gradient boosting
4. **LSTM Networks** - Time series forecasting
5. **Vector AutoRegression (VAR)** - Multiple time series analysis

