import pandas as pd
import os
from datetime import datetime
import json

def export_to_csv(df, filename):
    """
    Export DataFrame to CSV file
    
    Args:
        df: Pandas DataFrame to export
        filename: Base name for the file (without extension)
    
    Returns:
        Full filepath of exported file
    """
    # Create exports directory if not exists
    os.makedirs('outputs/exports', exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filepath = f"outputs/exports/{filename}_{timestamp}.csv"
    
    # Export to CSV
    df.to_csv(filepath, index=False)
    
    return filepath


def export_to_excel(df, filename):
    """
    Export DataFrame to Excel file
    
    Args:
        df: Pandas DataFrame to export
        filename: Base name for the file (without extension)
    
    Returns:
        Full filepath of exported file
    """
    # Create exports directory if not exists
    os.makedirs('outputs/exports', exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filepath = f"outputs/exports/{filename}_{timestamp}.xlsx"
    
    # Export to Excel
    df.to_excel(filepath, index=False, engine='openpyxl')
    
    return filepath


def export_for_powerbi(df, filename):
    """
    Export data for Power BI integration
    Power BI files don't have timestamps - they get overwritten
    
    Args:
        df: Pandas DataFrame to export
        filename: Base name for the file (without extension)
    
    Returns:
        Full filepath of exported file
    """
    # Create Power BI exports directory if not exists
    os.makedirs('powerbi/data_exports', exist_ok=True)
    
    # Fixed filename (no timestamp) so Power BI can auto-refresh
    filepath = f"powerbi/data_exports/{filename}.csv"
    
    # Export to CSV
    df.to_csv(filepath, index=False)
    
    return filepath


def generate_report(data, report_type):
    """
    Generate analytical text report
    
    Args:
        data: Data to include in report (DataFrame or string)
        report_type: Type/name of the report
    
    Returns:
        Full filepath of generated report
    """
    # Create reports directory if not exists
    os.makedirs('outputs/reports', exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filepath = f"outputs/reports/{report_type}_{timestamp}.txt"
    
    # Write report
    with open(filepath, 'w') as f:
        f.write(f"="*60 + "\n")
        f.write(f"Report Type: {report_type}\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"="*60 + "\n\n")
        f.write(str(data))
        f.write("\n\n" + "="*60 + "\n")
    
    return filepath


def log_output(message, output_type="INFO"):
    """
    Log messages to execution output file
    
    Args:
        message: Message to log
        output_type: Type of message (INFO, WARNING, ERROR)
    """
    # Create outputs directory if not exists
    os.makedirs('outputs', exist_ok=True)
    
    filepath = 'outputs/execution.log'
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Append to log file
    with open(filepath, 'a') as f:
        f.write(f"[{timestamp}] [{output_type}] {message}\n")