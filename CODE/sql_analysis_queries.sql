-- ============================================================================
-- SQL QUERIES FOR ECONOMIC DATA ANALYSIS
-- ============================================================================
-- This script demonstrates SQL queries for analyzing the Economics ML Dataset
-- Note: These can be executed in SQLite, PostgreSQL, MySQL, or other SQL databases

-- ============================================================================
-- 1. BASIC DATA EXPLORATION QUERIES
-- ============================================================================

-- View all data ordered by date
SELECT * FROM economics_data
ORDER BY Date DESC;

-- Count records and identify date range
SELECT 
    COUNT(*) as total_records,
    MIN(Date) as start_date,
    MAX(Date) as end_date,
    DATEDIFF(day, MIN(Date), MAX(Date)) + 1 as total_days
FROM economics_data;

-- ============================================================================
-- 2. DESCRIPTIVE STATISTICS QUERIES
-- ============================================================================

-- Overall statistics for key economic indicators
SELECT 
    'GDP_Growth_Rate' as indicator,
    ROUND(AVG(GDP_Growth_Rate), 4) as mean_value,
    ROUND(STDEV(GDP_Growth_Rate), 4) as std_dev,
    ROUND(MIN(GDP_Growth_Rate), 4) as min_value,
    ROUND(MAX(GDP_Growth_Rate), 4) as max_value,
    ROUND(MAX(GDP_Growth_Rate) - MIN(GDP_Growth_Rate), 4) as range_value
FROM economics_data

UNION ALL

SELECT 
    'Unemployment_Rate' as indicator,
    ROUND(AVG(Unemployment_Rate), 4) as mean_value,
    ROUND(STDEV(Unemployment_Rate), 4) as std_dev,
    ROUND(MIN(Unemployment_Rate), 4) as min_value,
    ROUND(MAX(Unemployment_Rate), 4) as max_value,
    ROUND(MAX(Unemployment_Rate) - MIN(Unemployment_Rate), 4) as range_value
FROM economics_data

UNION ALL

SELECT 
    'Inflation_Rate' as indicator,
    ROUND(AVG(Inflation_Rate), 4) as mean_value,
    ROUND(STDEV(Inflation_Rate), 4) as std_dev,
    ROUND(MIN(Inflation_Rate), 4) as min_value,
    ROUND(MAX(Inflation_Rate), 4) as max_value,
    ROUND(MAX(Inflation_Rate) - MIN(Inflation_Rate), 4) as range_value
FROM economics_data;

-- ============================================================================
-- 3. TEMPORAL ANALYSIS QUERIES
-- ============================================================================

-- Year-over-year comparison
SELECT 
    YEAR(Date) as year,
    MONTH(Date) as month,
    ROUND(AVG(GDP_Growth_Rate), 3) as avg_gdp_growth,
    ROUND(AVG(Unemployment_Rate), 3) as avg_unemployment,
    ROUND(AVG(Inflation_Rate), 3) as avg_inflation,
    ROUND(AVG(Stock_Market_Index), 2) as avg_stock_index
FROM economics_data
GROUP BY YEAR(Date), MONTH(Date)
ORDER BY year DESC, month DESC;

-- Quarterly aggregation
SELECT 
    YEAR(Date) as year,
    CEILING(MONTH(Date) / 3.0) as quarter,
    COUNT(*) as months_in_quarter,
    ROUND(AVG(GDP_Growth_Rate), 3) as avg_gdp_growth,
    ROUND(AVG(Target_Economic_Output), 3) as avg_target_output,
    ROUND(MAX(Stock_Market_Index), 2) as max_stock_index,
    ROUND(MIN(Stock_Market_Index), 2) as min_stock_index
FROM economics_data
GROUP BY YEAR(Date), CEILING(MONTH(Date) / 3.0)
ORDER BY year DESC, quarter DESC;

-- ============================================================================
-- 4. CORRELATION AND RELATIONSHIP ANALYSIS
-- ============================================================================

-- Identify periods of high unemployment and low GDP growth
SELECT 
    Date,
    Unemployment_Rate,
    GDP_Growth_Rate,
    Inflation_Rate,
    Consumer_Confidence,
    Target_Economic_Output
FROM economics_data
WHERE Unemployment_Rate > 5.0 
  AND GDP_Growth_Rate < 2.0
ORDER BY Date;

-- Find best performing periods (high GDP growth, low unemployment)
SELECT 
    Date,
    GDP_Growth_Rate,
    Unemployment_Rate,
    Inflation_Rate,
    Stock_Market_Index,
    Target_Economic_Output
FROM economics_data
WHERE GDP_Growth_Rate > (SELECT AVG(GDP_Growth_Rate) FROM economics_data)
  AND Unemployment_Rate < (SELECT AVG(Unemployment_Rate) FROM economics_data)
ORDER BY GDP_Growth_Rate DESC;

-- ============================================================================
-- 5. TRADE ANALYSIS
-- ============================================================================

-- Trade balance analysis
SELECT 
    Date,
    Exports,
    Imports,
    ROUND((Exports - Imports), 2) as trade_balance,
    ROUND(((Exports - Imports) / Imports * 100), 2) as balance_percentage,
    ROUND((Exports + Imports), 2) as total_trade,
    ROUND((Exports / (Exports + Imports) * 100), 2) as export_percentage
FROM economics_data
ORDER BY Date;

-- Trade trends by year
SELECT 
    YEAR(Date) as year,
    ROUND(AVG(Exports), 2) as avg_exports,
    ROUND(AVG(Imports), 2) as avg_imports,
    ROUND(AVG(Exports - Imports), 2) as avg_trade_balance,
    ROUND(SUM(Exports), 2) as total_exports,
    ROUND(SUM(Imports), 2) as total_imports
FROM economics_data
GROUP BY YEAR(Date)
ORDER BY year DESC;

-- ============================================================================
-- 6. CONSUMPTION AND INVESTMENT ANALYSIS
-- ============================================================================

-- Expenditure composition analysis
SELECT 
    Date,
    Private_Consumption,
    Government_Spending,
    Investment_Rate,
    Exports,
    Imports,
    ROUND((Private_Consumption + Government_Spending + Investment_Rate * 1000 + Exports - Imports), 2) as implied_gdp,
    ROUND(
        (Private_Consumption / (Private_Consumption + Government_Spending + Investment_Rate * 1000) * 100), 2
    ) as consumption_share
FROM economics_data
ORDER BY Date;

-- Investment performance correlation
SELECT 
    ROUND(
        (SUM((Investment_Rate - (SELECT AVG(Investment_Rate) FROM economics_data)) * 
             (Target_Economic_Output - (SELECT AVG(Target_Economic_Output) FROM economics_data))) 
        / (STDEV(Investment_Rate) * STDEV(Target_Economic_Output))), 4
    ) as investment_output_correlation,
    ROUND(
        (SUM((Private_Consumption - (SELECT AVG(Private_Consumption) FROM economics_data)) * 
             (Target_Economic_Output - (SELECT AVG(Target_Economic_Output) FROM economics_data))) 
        / (STDEV(Private_Consumption) * STDEV(Target_Economic_Output))), 4
    ) as consumption_output_correlation
FROM economics_data;

-- ============================================================================
-- 7. MONETARY POLICY ANALYSIS
-- ============================================================================

-- Interest rate impact on indicators
SELECT 
    Date,
    Interest_Rate,
    Stock_Market_Index,
    Consumer_Confidence,
    Inflation_Rate,
    ROUND(Stock_Market_Index - LAG(Stock_Market_Index) OVER (ORDER BY Date), 2) as market_change,
    ROUND(Interest_Rate - LAG(Interest_Rate) OVER (ORDER BY Date), 3) as interest_rate_change
FROM economics_data
ORDER BY Date;

-- Interest rate regimes analysis
SELECT 
    CASE 
        WHEN Interest_Rate < 0.5 THEN 'Very Low'
        WHEN Interest_Rate < 1.5 THEN 'Low'
        WHEN Interest_Rate < 2.5 THEN 'Moderate'
        ELSE 'High'
    END as interest_regime,
    COUNT(*) as count,
    ROUND(AVG(GDP_Growth_Rate), 3) as avg_gdp_growth,
    ROUND(AVG(Stock_Market_Index), 2) as avg_stock_index,
    ROUND(AVG(Inflation_Rate), 3) as avg_inflation,
    ROUND(AVG(Consumer_Confidence), 2) as avg_confidence
FROM economics_data
GROUP BY CASE 
    WHEN Interest_Rate < 0.5 THEN 'Very Low'
    WHEN Interest_Rate < 1.5 THEN 'Low'
    WHEN Interest_Rate < 2.5 THEN 'Moderate'
    ELSE 'High'
END
ORDER BY avg_gdp_growth DESC;

-- ============================================================================
-- 8. MARKET CONFIDENCE ANALYSIS
-- ============================================================================

-- Consumer sentiment and market dynamics
SELECT 
    Date,
    Consumer_Confidence,
    Stock_Market_Index,
    GDP_Growth_Rate,
    Unemployment_Rate,
    ROUND(
        (Consumer_Confidence - LAG(Consumer_Confidence) OVER (ORDER BY Date)), 2
    ) as confidence_change,
    ROUND(
        ((Stock_Market_Index - LAG(Stock_Market_Index) OVER (ORDER BY Date)) / 
         LAG(Stock_Market_Index) OVER (ORDER BY Date) * 100), 2
    ) as market_return_pct
FROM economics_data
ORDER BY Date;

-- High confidence periods analysis
SELECT 
    AVG(Consumer_Confidence) as avg_confidence_threshold,
    ROUND(AVG(GDP_Growth_Rate) FILTER (WHERE Consumer_Confidence > 85), 3) as high_conf_gdp_growth,
    ROUND(AVG(Unemployment_Rate) FILTER (WHERE Consumer_Confidence > 85), 3) as high_conf_unemployment,
    ROUND(AVG(Stock_Market_Index) FILTER (WHERE Consumer_Confidence > 85), 2) as high_conf_stock_index
FROM economics_data;

-- ============================================================================
-- 9. PREDICTIONS AND TARGETS
-- ============================================================================

-- Target economic output ranges
SELECT 
    CASE 
        WHEN Target_Economic_Output < 1.0 THEN 'Weak (< 1%)'
        WHEN Target_Economic_Output < 2.5 THEN 'Below Average (1-2.5%)'
        WHEN Target_Economic_Output < 4.0 THEN 'Good (2.5-4%)'
        ELSE 'Strong (> 4%)'
    END as growth_category,
    COUNT(*) as count,
    ROUND(AVG(GDP_Growth_Rate), 3) as avg_gdp,
    ROUND(AVG(Unemployment_Rate), 3) as avg_unemployment,
    ROUND(AVG(Inflation_Rate), 3) as avg_inflation,
    ROUND(AVG(Consumer_Confidence), 2) as avg_confidence
FROM economics_data
GROUP BY CASE 
    WHEN Target_Economic_Output < 1.0 THEN 'Weak (< 1%)'
    WHEN Target_Economic_Output < 2.5 THEN 'Below Average (1-2.5%)'
    WHEN Target_Economic_Output < 4.0 THEN 'Good (2.5-4%)'
    ELSE 'Strong (> 4%)'
END
ORDER BY count DESC;

-- ============================================================================
-- 10. ADVANCED ANALYTICS - WINDOW FUNCTIONS
-- ============================================================================

-- Rolling averages and trend analysis
SELECT 
    Date,
    GDP_Growth_Rate,
    ROUND(
        AVG(GDP_Growth_Rate) OVER (ORDER BY Date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 3
    ) as gdp_moving_avg_3m,
    ROUND(
        AVG(GDP_Growth_Rate) OVER (ORDER BY Date ROWS BETWEEN 5 PRECEDING AND CURRENT ROW), 3
    ) as gdp_moving_avg_6m,
    ROUND(
        (GDP_Growth_Rate - LAG(GDP_Growth_Rate) OVER (ORDER BY Date)), 3
    ) as gdp_change_mom,
    ROW_NUMBER() OVER (ORDER BY Date) as period_number
FROM economics_data
ORDER BY Date DESC;

-- Year-over-year growth rates
SELECT 
    Date,
    Target_Economic_Output,
    LAG(Target_Economic_Output, 12) OVER (ORDER BY Date) as target_12m_ago,
    ROUND(
        ((Target_Economic_Output - LAG(Target_Economic_Output, 12) OVER (ORDER BY Date)) / 
         LAG(Target_Economic_Output, 12) OVER (ORDER BY Date) * 100), 2
    ) as yoy_growth_pct
FROM economics_data
WHERE LAG(Target_Economic_Output, 12) OVER (ORDER BY Date) IS NOT NULL
ORDER BY Date;

-- ============================================================================
-- END OF SQL QUERIES
-- ============================================================================
