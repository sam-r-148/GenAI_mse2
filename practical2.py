from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def collect_data():
    print("Collecting data from the server...")
    print("CPU Usage: 70")
    print("Memory Usage: 80")
    print("Error rate: 10")
    
def process_data():
    print("Processing the collected data...")
    
def detect_anamoly():
    CPU = 70
    if CPU > 80:
        print("ALERT!!! High CPU Usage")
    else:
        print("Normal CPU Usage")
        
def saving_results():
    print("Saving the results to the database...")

        
        
with DAG(
dag_id="practical2_aiops_dag",
start_date=datetime(2026,9,8),
schedule=None,
catchup=False
) as dag:
        collect=PythonOperator(
            task_id="collect-data",
            python_callable=collect_data,
        )
        process=PythonOperator(
            task_id="process_data",
            python_callable=process_data,
        )
        detect=PythonOperator(
            task_id="detect-anamoly",
            python_callable=detect_anamoly,
        )
        saving=PythonOperator(
            task_id="saving-results",
            python_callable=saving_results,
        )
        
        collect >> process >> detect >> saving

    
