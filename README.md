# Sparkify Postgres

- [About](#about)
- [Database Design](#database-design)
- [ETL Pipeline Design](#etl-pipeline-design)
- [Getting Started](#getting-started)
- [Directory Strucure](#directory-structure)
- [References](#references)

## About

A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. Currently there is no easy way for Sparkify's analytics team to query their data to better understand their user's listening behaviour. In order to help out Sparkify's analytics team, we'll create an ETL (Extract, Transform and Load) Pipeline to extract user activity and song data from JSON files and ingest the data into a Postgres Database.  

## Database Design

### Data

The data consists of JSON logs on user activity (**log_data**) and song meta data (**song_data**)

### Database Schema

Using the song and log datasets, we'll create a star schema optimized for queries on song play analysis. This includes the following tables:


- Fact table: **songplays**.
- Dimension tables: **songs**, **artists**, **users**, **time**. 

![sparkify-postgres-schema](sparkify-postgres-schema.png)

## ETL Pipeline Design

The ETL pipline comprises the following components:

- ETL of song data into songs table from song_data JSON files.
- ETL of artist data into artists table from song_data JSON files.
- ETL of time data into time table from log_data JSON files.
- ETL of user data into users table from log_data JSON files.
- ETL of songplay data into songplays table from log_data JSON files.

## Getting Started

### Tech Stack

- Docker
- Jupyter Notebook
- Postgres

### Build the containers

Ensure docker is installed.

```cmd

docker compose build

```

### Start the containers

```cmd

docker compose up

```

Docker compose will spin up two containers:

- sparkifydb (a postgres database)
- jupyter (jupyter notebook container)

### Create the Database Schema

Run create_tables.py:

```cmd

docker-compose run --rm jupyter_notebook python src/scripts/create_tables.py

```

### Execute ETL Pipeline

Run etl.py:

```cmd

docker compose run --rm jupyter_notebook python src/scripts/etl.py

```

Alternatively, you can run the python scripts from a shell in the container:

```cmd

docker exec -it jupyter bash 

```

## Directory Structure

```
├── services
|    └── jupyter
|        └── Dockerfile         <- Docker file for jupter notebook.
|
|
├── src                         <- Source code for use in this project.
|   ├── notebooks           
|   |   └── etl.ipynb           <- Notebook for ETL development.
|   |         
|   └── scripts  
|       ├── etl.py              <- Script to execute ETL pipeline.
|       ├── create_tables.py    <- Script to create database and tables.
|       └── sql_queries.py      <- Script with SQL queries.
|      
|
├── docker-compose.yml          <- Docker-compose file for running the services.
|
|
├── README.md                   <- README for developers using this project.
├── poetry.lock                 <- The poetry.lock file for reproducing the analysis environment.
└── pyproject.toml              <- The pyproject.toml file for reproducing the analysis environment.
```

## References

This project is part of the [Udacity Data Engineering nanodegree](https://www.udacity.com/course/data-engineer-nanodegree--nd027).

- [Docker documentation](https://docs.docker.com/)
- [Jupyter notebook image](https://hub.docker.com/r/jupyter/minimal-notebook/tags/)
- [Markdown guide](https://www.markdownguide.org/basic-syntax/)
- [Poetry documentation](https://python-poetry.org/docs/)
- [Amazon Redshift documentation](https://aws.amazon.com/redshift/)
- [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html)
