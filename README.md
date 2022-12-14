## Background

I created this code repository to explore Apache Airflow in greater detail as I read articles online as well as following along with the book [Data Pipelines with Apache Airflow ](https://www.manning.com/books/data-pipelines-with-apache-airflow).

## Requirements

- Python3 (I will be using [PyEnv](https://github.com/pyenv/pyenv) with version 3.10.4)
- Docker
- Basic understanding of Docker Compose

### Setting Up The Python Environment

Assuming you are using Pyenv you can type the following into your terminal:

```zsh
pyenv local 3.10.4;
pyenv virtualenv apache-airflow;
pyenv activate apache-airflow;
```

### Setting Up Apache Airflow With Docker Compose

The official Apache Airflow docs have a great tutorial for [Running Airflow in Docker](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html) which is what I followed.

I made a few additional changes to the docker-compose.yml file based on notes in the Running Airflow in Docker docs with my intended use case in mind.

These were:

- Adding `extra_hosts: - "host.docker.internal:host-gateway"` in the airflow-worker service. 
- Added an additional Postgres database service that would be used by dbt and Great Expectations. Because there are two Postgres instances I changed the port on this to avoid a conflict.
- Added a Docker proxy service in order to use the Airflow DockerOperator to launch Docker images on my local machine.

After this I followed the steps to initalise Airflow and bring the services up using Docker Compose.

### Setting up dbt

With your Python3 environment active you can type the following in your terminal:

```zsh
pip install dbt-postgres
```

Then to setup a starter project:

```zsh
dbt init airflow_dbt
```

To run dbt we are going to need a profiles.yml which you can [more information about in the official dbt docs](https://docs.getdbt.com/reference/warehouse-profiles/postgres-profile)

```yml
airflow_dbt: # Name of the dbt project used in the dbt init command
  target: dev
  outputs:
    dev:
      type: postgres
      host: host.docker.internal # This is the extra_host that we added in the airflow-worker service in docker-compose.yaml
      user: root
      password: password
      port: 5434 # This is the port I changed the dbt Postgres service to
      dbname: dbt
      schema: test
      threads: 1
      connect_timeout: 10 # default 10 seconds
```

### Building The Custom Docker Images for dbt and Great Expectations

```docker
docker build -f docker_images/Dockerfile.dbt . -t custom-dbt                            

docker build -f docker_images/Dockerfile.greatExpectations . -t custom-greatexpectations                          
```

### Setting Up Great Expectations

```zsh
pip install great_expectations sqlalchemy psycopg2
```

```
great_expectations init
```