"""
Main Project Runner - Economics ML Analysis
Orchestrates the complete analysis pipeline
"""

import subprocess
import sys
import os
from pathlib import Path

def run_script(script_path, description):
    """Run a Python script and handle errors"""
    print("\n" + "="*80)
    print(f"RUNNING: {description}")
    print("="*80 + "\n")
    
    try:
        subprocess.run([sys.executable, script_path], check=True)
        print(f"\n✓ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Error running {description}: {e}")
        return False
    except FileNotFoundError:
        print(f"\n✗ Script not found: {script_path}")
        return False

def main():
    """Main execution function"""
    print("\n" + "="*80)
    print("ECONOMICS MACHINE LEARNING PROJECT")
    print("Master Thesis Analysis Pipeline")
    print("="*80)
    
    # Get current directory
    current_dir = Path(__file__).parent
    
    # Check if required files exist
    print("\nChecking dependencies...")
    required_files = [
        '01_data_exploration.py',
        '02_machine_learning_model.py',
        'requirements.txt',
        '../DATA_SET/Economics_ML_Dataset.csv'
    ]
    
    all_files_exist = True
    for file in required_files:
        file_path = current_dir / file
        if file_path.exists():
            print(f"  ✓ {file} found")
        else:
            print(f"  ✗ {file} NOT FOUND")
            all_files_exist = False
    
    if not all_files_exist:
        print("\n⚠ Some required files are missing!")
        print("Please ensure all files are in place before running the analysis.")
        return False
    
    print("\n" + "="*80)
    print("PIPELINE CONFIGURATION")
    print("="*80)
    print("""
    Project Structure:
    ├── DATA_SET/
    │   └── Economics_ML_Dataset.csv
    ├── CODE/
    │   ├── 01_data_exploration.py
    │   ├── 02_machine_learning_model.py
    │   ├── sql_analysis_queries.sql
    │   ├── requirements.txt
    │   ├── README.md
    │   └── run_project.py (this file)
    └── PRESENTATION/
    
    Analysis Pipeline:
    1. Data Exploration & EDA
    2. Machine Learning Model Development
    3. Results Generation & Visualization
    """)
    
    # Ask user for confirmation
    user_input = input("\nStart the analysis pipeline? (yes/no): ").strip().lower()
    if user_input not in ['yes', 'y']:
        print("Analysis cancelled.")
        return False
    
    # Run the analysis pipeline
    print("\n" + "="*80)
    print("STARTING ANALYSIS PIPELINE")
    print("="*80)
    
    # Step 1: Data Exploration
    success1 = run_script(
        str(current_dir / '01_data_exploration.py'),
        "Data Exploration & EDA"
    )
    
    if not success1:
        print("\n⚠ Data exploration failed. Continuing with ML model...")
    
    # Step 2: Machine Learning Model
    success2 = run_script(
        str(current_dir / '02_machine_learning_model.py'),
        "Machine Learning Model Development"
    )
    
    # Final Summary
    print("\n" + "="*80)
    print("PIPELINE EXECUTION SUMMARY")
    print("="*80)
    
    if success1 and success2:
        print("\n✓ All analyses completed successfully!")
        print("\nGenerated Output Files:")
        print("  Analysis Results:")
        print("    - analysis_results/correlation_heatmap.png")
        print("    - analysis_results/economic_indicators_timeseries.png")
        print("    - analysis_results/distribution_analysis.png")
        print("\n  Model Results:")
        print("    - model_results/predictions_comparison.png")
        print("    - model_results/feature_importance.png")
        print("    - model_results/model_performance_comparison.png")
        print("    - model_results/residuals_analysis.png")
        print("    - model_results/model_results.txt")
        print("    - model_results/model_comparison.csv")
        print("    - model_results/feature_importance.csv")
        
        print("\nNext Steps:")
        print("  1. Review visualization files in analysis_results/ and model_results/")
        print("  2. Check model_results/model_results.txt for detailed findings")
        print("  3. Use CSV files for further analysis or presentation")
        print("  4. Refer to README.md for interpretation guidance")
        print("  5. For SQL analysis, use sql_analysis_queries.sql with your database")
        return True
    else:
        print("\n⚠ Some analyses failed. Please check error messages above.")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nAnalysis interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        sys.exit(1)
