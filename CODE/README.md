# Economics ML Project - Code Documentation

## Overview
This directory contains Python and SQL scripts for analyzing the Economics dataset and building machine learning models to predict economic growth.

## Project Structure

```
CODE/
├── 01_data_exploration.py        # Exploratory Data Analysis (EDA)
├── 02_machine_learning_model.py  # ML Model Development
├── sql_analysis_queries.sql      # SQL Analysis Queries
├── requirements.txt              # Python Dependencies
├── README.md                      # This file
└── model_results/                # Output directory for models and results
    ├── predictions_comparison.png
    ├── feature_importance.png
    ├── model_performance_comparison.png
    ├── residuals_analysis.png
    ├── model_results.txt
    ├── model_comparison.csv
    └── feature_importance.csv
```

## Prerequisites

### Python Installation
```bash
# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### SQL Database (Optional)
The SQL queries can be executed in:
- SQLite
- PostgreSQL
- MySQL
- Microsoft SQL Server
- Other SQL-compatible databases

## Scripts Description

### 1. Data Exploration Script (`01_data_exploration.py`)

**Purpose**: Perform comprehensive exploratory data analysis

**What it does**:
- Loads the economics dataset
- Displays basic statistics and data overview
- Identifies missing values
- Calculates correlations between variables
- Creates visualization plots:
  - Correlation heatmap
  - Time series plots for key indicators
  - Distribution analysis plots

**Usage**:
```bash
python 01_data_exploration.py
```

**Output**:
- Console output with statistics
- Three PNG files in `analysis_results/`:
  - `correlation_heatmap.png` - Feature correlation visualization
  - `economic_indicators_timeseries.png` - Time series trends
  - `distribution_analysis.png` - Distribution histograms

### 2. Machine Learning Model Script (`02_machine_learning_model.py`)

**Purpose**: Build and evaluate machine learning models

**What it does**:
- Loads and prepares data
- Splits data into training (80%) and test (20%) sets
- Builds three ML models:
  1. **Linear Regression** - Baseline linear model
  2. **Ridge Regression** - Regularized linear model
  3. **Random Forest** - Ensemble tree-based model

- Evaluates models using:
  - R² Score (coefficient of determination)
  - RMSE (Root Mean Squared Error)
  - MAE (Mean Absolute Error)
  - Cross-validation scores (5-fold)

- Performs feature importance analysis
- Creates visualizations comparing model performance

**Usage**:
```bash
python 02_machine_learning_model.py
```

**Output**:
- Console output with detailed model performance metrics
- Seven files in `model_results/`:
  - `predictions_comparison.png` - Predicted vs actual values
  - `feature_importance.png` - Top 10 important features
  - `model_performance_comparison.png` - Performance metrics comparison
  - `residuals_analysis.png` - Residual plots
  - `model_results.txt` - Complete text report
  - `model_comparison.csv` - Model metrics in CSV format
  - `feature_importance.csv` - Feature importance rankings

### 3. SQL Analysis Queries (`sql_analysis_queries.sql`)

**Purpose**: Provide SQL queries for data analysis in databases

**Categories of queries**:
1. **Basic Exploration** - Data overview and date ranges
2. **Descriptive Statistics** - Mean, std dev, min/max for indicators
3. **Temporal Analysis** - Year-over-year and quarterly comparisons
4. **Correlation Analysis** - Relationships between variables
5. **Trade Analysis** - Import/export trends and balance
6. **Consumption & Investment** - Expenditure composition
7. **Monetary Policy** - Interest rate impact analysis
8. **Market Confidence** - Consumer sentiment trends
9. **Predictions & Targets** - Economic output categorization
10. **Advanced Analytics** - Window functions and rolling averages

**Usage**:
```sql
-- Execute in your SQL database client
-- Example: Load the CSV into a table named 'economics_data'
-- Then run any query from the file

-- Example: Get yearly averages
SELECT 
    YEAR(Date) as year,
    ROUND(AVG(GDP_Growth_Rate), 3) as avg_gdp_growth,
    ROUND(AVG(Unemployment_Rate), 3) as avg_unemployment
FROM economics_data
GROUP BY YEAR(Date);
```

## Running the Complete Analysis

**Option 1: Run scripts sequentially**
```bash
# 1. First run the exploration
python 01_data_exploration.py

# 2. Then run the ML model
python 02_machine_learning_model.py
```

**Option 2: Use in Jupyter Notebook**
```bash
# Copy the code from Python scripts into Jupyter cells
jupyter notebook
```

## Model Performance Summary

The machine learning models are evaluated on their ability to predict **Target_Economic_Output** (economic growth percentage).

### Key Metrics Explained

- **R² Score**: Ranges from 0 to 1. Higher is better. Represents proportion of variance explained.
- **RMSE**: Lower is better. Measures average prediction error in percentage points.
- **MAE**: Lower is better. Mean absolute error in percentage points.
- **Cross-validation**: Tests model stability across different data splits.

### Expected Results

The Random Forest model typically outperforms linear models because:
- Economics data has non-linear relationships
- Multiple interaction effects between indicators
- Tree ensemble methods capture complexity better

## Interpreting Results

### Feature Importance
Top features typically include:
- **GDP_Growth_Rate** - Current economic growth
- **Stock_Market_Index** - Market sentiment
- **Consumer_Confidence** - Economic sentiment
- **Inflation_Rate** - Price pressures
- **Unemployment_Rate** - Labor market health

### Model Comparison
- **Linear Regression**: Fast, interpretable, good baseline
- **Ridge Regression**: Better generalization, reduces overfitting
- **Random Forest**: Best accuracy, captures non-linearity, slower

## Data Requirements

The scripts expect:
- CSV file format
- Date column in YYYY-MM-DD format
- 15 numeric feature columns
- 1 target variable column
- No missing values (pre-cleaned data)

## Troubleshooting

**Import Error**: Make sure all dependencies are installed
```bash
pip install -r requirements.txt
```

**File not found**: Ensure you run scripts from the CODE directory
```bash
cd /workspaces/FinalProject_SQL_Python_DURHAM_2026/CODE
python 01_data_exploration.py
```

**Memory issues**: For larger datasets, modify script to process in chunks

## Performance Tips

1. Use Ridge or Linear Regression for faster execution
2. Random Forest can be slow for very large datasets
3. Consider feature selection to reduce dimensionality
4. Use cross-validation for robust performance estimates

## Advanced Customization

### Modifying Models
Edit `02_machine_learning_model.py`:
- Change `test_size` for different train/test split
- Adjust `n_estimators` for Random Forest complexity
- Modify feature scaling method

### Adding New Models
```python
from sklearn.ensemble import GradientBoostingRegressor

gb_model = GradientBoostingRegressor()
gb_model.fit(X_train, y_train)
```

### Feature Engineering
```python
# Add polynomial features
from sklearn.preprocessing import PolynomialFeatures
poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X_train)
```

## Further Analysis Ideas

1. **Time Series Models**: ARIMA, LSTM for temporal dependencies
2. **Ensemble Methods**: Stacking, voting classifiers
3. **Hyperparameter Tuning**: GridSearchCV, RandomizedSearchCV
4. **Feature Engineering**: Create interaction terms, lag variables
5. **Outlier Detection**: Identify and handle anomalies
6. **Model Deployment**: Save models with pickle/joblib for production

## References

- [Scikit-learn Documentation](https://scikit-learn.org/)
- [Pandas Documentation](https://pandas.pydata.org/)
- [Machine Learning Basics](https://developers.google.com/machine-learning/crash-course)

## Author Notes

This project demonstrates:
- End-to-end machine learning pipeline
- Data exploration and preparation
- Model selection and evaluation
- SQL analysis techniques
- Visualization and reporting

Perfect for master thesis analysis!

---

Last Updated: 2026-06-16
