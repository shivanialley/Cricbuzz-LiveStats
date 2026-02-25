import mlflow
import mlflow.sklearn
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

class MLflowTracker:
    def __init__(self):
        self.tracking_uri = os.getenv('MLFLOW_TRACKING_URI', 'http://localhost:5000')
        self.experiment_name = os.getenv('MLFLOW_EXPERIMENT_NAME', 'cricbuzz_analytics')
        
        mlflow.set_tracking_uri(self.tracking_uri)
        
        try:
            mlflow.set_experiment(self.experiment_name)
        except:
            mlflow.create_experiment(self.experiment_name)
            mlflow.set_experiment(self.experiment_name)
    
    def log_api_call(self, endpoint, response_time, status_code, data_size):
        try:
            with mlflow.start_run(run_name=f"api_call_{datetime.now().strftime('%Y%m%d_%H%M%S')}"):
                mlflow.log_param("endpoint", endpoint)
                mlflow.log_param("timestamp", datetime.now().isoformat())
                mlflow.log_metric("response_time_ms", response_time)
                mlflow.log_metric("status_code", status_code)
                mlflow.log_metric("data_size_bytes", data_size)
                mlflow.set_tag("type", "api_call")
                mlflow.set_tag("success", status_code == 200)
        except Exception as e:
            print(f"MLflow logging error: {e}")
    
    def log_query_performance(self, query_name, execution_time, rows_returned):
        try:
            with mlflow.start_run(run_name=f"query_{query_name}_{datetime.now().strftime('%H%M%S')}"):
                mlflow.log_param("query_name", query_name)
                mlflow.log_param("timestamp", datetime.now().isoformat())
                mlflow.log_metric("execution_time_ms", execution_time)
                mlflow.log_metric("rows_returned", rows_returned)
                mlflow.set_tag("type", "sql_query")
        except Exception as e:
            print(f"MLflow logging error: {e}")
    
    def log_data_quality(self, table_name, total_rows, null_count, duplicate_count):
        try:
            with mlflow.start_run(run_name=f"data_quality_{table_name}"):
                mlflow.log_param("table_name", table_name)
                mlflow.log_param("timestamp", datetime.now().isoformat())
                mlflow.log_metric("total_rows", total_rows)
                mlflow.log_metric("null_count", null_count)
                null_percentage = (null_count / total_rows * 100) if total_rows > 0 else 0
                mlflow.log_metric("null_percentage", null_percentage)
                mlflow.log_metric("duplicate_count", duplicate_count)
                mlflow.set_tag("type", "data_quality")
        except Exception as e:
            print(f"MLflow logging error: {e}")

tracker = MLflowTracker()