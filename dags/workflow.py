from airflow.operators.mysql_operator import MySqlOperator
from airflow import DAG
from datetime import datetime, timedelta
import pymysql
pymysql.install_as_MySQLdb()

# 현재 날짜를 start_date로 설정
default_args = {
    "owner": "airflow",
    "start_date": datetime.now(),  # 현재 날짜로 설정
    "retries": 1,
    "retry_delay": timedelta(minutes=1)
}

with DAG(
    dag_id="workflow",
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False  # 과거 날짜에 대해 작업이 실행되지 않도록 설정
) as dag:
    
    create_table = MySqlOperator(
        task_id="create_table",
        mysql_conn_id="mysql_db",
        sql="CREATE DATABASE qweql",
    )
