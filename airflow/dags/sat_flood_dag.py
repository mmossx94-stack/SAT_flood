
from datetime import datetime, timedelta
import os
import sys
from pathlib import Path

from airflow import DAG
from airflow.operators.python import PythonOperator

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS_DIR = PROJECT_ROOT / 'scripts'
sys.path.append(str(SCRIPTS_DIR))

try:
    from upload_to_gspread import run_etl
except ImportError:
    def run_etl(*args, **kwargs):
        raise ImportError('upload_to_gspread.py could not be imported. Check PYTHONPATH.')

default_args = {
    'owner': 'sat_flood_team',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'sat_flood_pipeline',
    default_args=default_args,
    description='Apache Airflow DAG for Google Trends and Flood Data ETL to Google Sheets',
    schedule_interval='0 */2 * * *',
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['sat_flood', 'google_trends', 'gspread', 'gas'],
)

def task_run_etl(**kwargs):
    spreadsheet_id = os.getenv('SPREADSHEET_ID', '')
    creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 'service_account.json')
    
    success = run_etl(spreadsheet_id=spreadsheet_id, creds_path=creds_path)
    if not success:
        raise RuntimeError('ETL Task failed. Check Airflow execution logs.')

etl_operator = PythonOperator(
    task_id='run_sat_trends_and_flood_etl',
    python_callable=task_run_etl,
    dag=dag,
)
