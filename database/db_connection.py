import mysql.connector
import os
from dotenv import load_dotenv
from utils.logger import app_logger

load_dotenv()

def get_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME', 'cricbuzz_db'),
            port=int(os.getenv('DB_PORT', 3306))
        )
        app_logger.info("Database connection established successfully")
        return conn
    except mysql.connector.Error as e:
        app_logger.error(f"Database connection failed: {str(e)}")
        raise Exception(f"Database connection error: {str(e)}")

def test_connection():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        app_logger.info("Database connection test successful")
        return result is not None
    except Exception as e:
        app_logger.error(f"Database connection test failed: {str(e)}")
        return False