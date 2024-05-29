
# Connecting Airflow and mysql
Airfflow와 mysql을 연동하는 과정을 담은 레포입니다. 다른 프로젝트에서 재사용 가능합니다.

## CONTENTS
1. [환경 설정](#1-environment)
2. [docker-compose.yaml 생성](#2-create-docker-composeyaml)
3. [Dockerfile 생성](#3-create-dockerfile)
4. [Docker 이미지 빌드](#4-build-docker-image)
5. [.env 파일 생성](#5-create-env-file)
6. [docker-compose up](#6-docker-comose-up)
7. [Mysql connect](#7-Mysql-connect)
8. [Create Test DAG file](#8-Create-Test-DAG-file)
9. [Check DB connection](#9-Check-DB-connection)
## 1. environment
- Computer: Mac m1 Pro
- Memory: Ram 16GB
- bandwidth: 100GB/s
- SSD capacity: 1TB
- Processor: 8 core CPU

## 2. Create docker-compose.yaml
먼저 아래 명령어를 통해 docker-compose.yaml파일을 다운받아 준다. 
```zsh
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.3.3/docker-compose.yaml'
```

그 후 생성된 yaml 파일의 services: 부분에 아래처럼 mysql service를 입력해주자
```yaml
 mysql:

    image: mysql:8
    environment:
      - MYSQL_ROOT_PASSWORD=root
    volumes:
      - ./mysql_data:/var/lib/mysql-files/
      - ./mysql.cnf:/etc/mysql/mysql.cnf
    ports:
      3306:3306
```

## 3. Create Dockerfile
아래 내용으로 Dockerfile을 만들어준다.

```Dockerfile
FROM apache/airflow:2.3.3
COPY requirements.txt /requirements.txt
RUN pip install --user --upgrade pip
RUN pip install --no-cache-dir --user -r /requirements.txt
'''

또한 pymysql을 사용하여 mysql을 대체할 예정이기에 requirements.txt파일을 만들고 pymysql을 집어넣어준다.

```txt
PyMySQL==1.0.2
```

## 4. Build docker image
이제 아래 명령어로 도커이미지를 만들어준다. 

```zsh
docker build . --tag extending_airflow:second
```
또한 docker-compose파일의 이미지 또한 새로 만든 이미지로 수정해준다.

```yaml
image: ${AIRFLOW_IMAGE_NAME:-extending_airflow:second}
```

## 5. Create .env file
UID 오류를 예방하기 위해 UID와 GID를 환경변수 파일에 생성해준다. 

```.env
AIRFLOW_UID=50000
AIRFLOW_GID=0
```

## 6. docker-comose up
localhost:8080에 들어가보면 아래처럼 성공적으로 airflow에 접속한 것을 알 수 있다. <br> 
초기 ID:PW는 airflow:airflow다. 
<img width="1508" alt="image" src="https://github.com/StatisticsFox/Airflow-with-Myspl/assets/92065443/ed063082-576f-44c4-9d26-4cb69e67f11b">

## 7. Mysql connect
아래처럼 mysql을 연동해준다. 아래 ID 혹은 PW는 본인이 설저한 것으로 넣어주도록 하자
<img width="635" alt="image" src="https://github.com/StatisticsFox/Airflow-with-Mysql/assets/92065443/58bf6217-37d2-435a-b2b0-953f83b829be">

## 8. Create Test DAG file
DAGS 폴더를 참조
```py
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
```

## 9. Check DB connection
잘 연결된것을 확인 가능하다. 
<img width="603" alt="image" src="https://github.com/StatisticsFox/Airflow-with-Mysql/assets/92065443/5ca69352-b2ae-48ce-a179-c76892ad8c0d">



