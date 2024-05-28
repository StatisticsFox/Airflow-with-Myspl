

# Connecting Airflow and mysql
Airfflow와 mysql을 연동하는 과정을 담은 레포입니다. 다른 프로젝트에서 재사용 가능합니다.

## CONTENTS
1. [환경 설정](#1-environment)
2. [docker-compose.yaml 생성](#2-create-docker-composeyaml)
3. [Dockerfile 생성](#3-create-dockerfile)
4. [Docker 이미지 빌드](#4-build-docker-image)
5. [.env 파일 생성](#5-create-env-file)


## 1. environment
- Computer: Mac m1 Pro
- Memory: Ram 16GB
- bandwidth: 100GB/s
- SSD capacity: 1TB
- Processor: 8 core CPU

## 2. Create docker-compose.yaml
```zsh
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.3.3/docker-compose.yaml'
```
그 후 생성된 yaml 파일의 services: 부분에 아래처럼 mysql을 입력해주자
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


