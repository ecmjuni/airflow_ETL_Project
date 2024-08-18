from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

# Utils Modules
from utils.movies_etl_process import movies_etl_process

etl_process = movies_etl_process()

def raw_layer():
    print("Start Raw")
    etl_process.movie_web_scraping()
    print("Ends Raw")

def silver_layer():
    print("Start Silver")
    etl_process.cleanning_dataframe()
    print("End Silver")

def gold_layer():
    print("Start Gold")
    etl_process.filtering_to_gold()
    print("End Gold")

dag = DAG(
    'movies_orchestration',
    default_args={'start_date': days_ago(1)},
    schedule_interval='0 0 * * *',
    catchup=False
)

execute_raw = PythonOperator(
    task_id='raw_layer',
    python_callable=raw_layer,
    dag=dag
)

execute_silver = PythonOperator(
    task_id='silver_layer',
    python_callable=silver_layer,
    dag=dag
)

execute_gold = PythonOperator(
    task_id='gold_layer',
    python_callable=gold_layer,
    dag=dag
)

# Set the dependencies between the tasks
execute_raw >> execute_silver >> execute_gold