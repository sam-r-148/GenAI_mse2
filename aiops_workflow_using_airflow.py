from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def collect_metrics():
    cpu = 87
    memory = 65
    response_time = 420

    print("Metrics collected:")
    print("CPU:", cpu)
    print("Memory:", memory)
    print("Response Time:", response_time, "ms")


def process_metrics():
    print("Processing server metrics...")
    print("CPU: 87")
    print("Memory: 65")
    print("Response Time: 420 ms")
    print("Metrics processed successfully")


def detect_anomaly():
    cpu = 87

    if cpu > 80:
        print("Anomaly detected: High CPU usage")
    else:
        print("No anomaly detected")


def generate_report():
    print("===== AIOps Report =====")
    print("Metrics collected successfully")
    print("Metrics processed successfully")
    print("Anomaly detection completed")
    print("========================")


with DAG(
    dag_id="aiops_workflow",
    start_date=datetime(2026, 9, 20),
    schedule=None,
    catchup=False
) as dag:

    collect_metrics_task = PythonOperator(
        task_id="collect_metrics",
        python_callable=collect_metrics
    )

    process_metrics_task = PythonOperator(
        task_id="process_metrics",
        python_callable=process_metrics
    )

    detect_anomaly_task = PythonOperator(
        task_id="detect_anomaly",
        python_callable=detect_anomaly
    )

    generate_report_task = PythonOperator(
        task_id="generate_report",
        python_callable=generate_report
    )

    collect_metrics_task >> process_metrics_task >> detect_anomaly_task >> generate_report_task