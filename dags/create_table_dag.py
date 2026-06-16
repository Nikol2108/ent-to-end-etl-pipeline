from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta

create_sql = """
    CREATE TABLE IF NOT EXISTS spotify_data (
        track_id VARCHAR(50) PRIMARY KEY,
        track_name VARCHAR(255),
        track_number INT,
        track_popularity INT,
        track_duration_ms INT,
        explicit BOOLEAN,
        artist_name VARCHAR(255),
        artist_popularity INT,
        artist_followers BIGINT,
        artist_genres TEXT,
        album_id VARCHAR(50),
        album_name VARCHAR(255),
        album_release_date DATE,
        album_total_tracks INT,
        album_type VARCHAR(50)
    );
"""

@dag(
    dag_id='create_spotify_table_v.6',
    start_date=datetime(2026, 6, 8),
    schedule=None, 
    catchup=False,
    tags=['setup', 'postgres', 'aws', 'taskflow']
)
def setup_target_db_dag():

    @task(task_id='create_spotify_table')
    def create_table():
        pg_hook = PostgresHook(postgres_conn_id='aws_postgres_conn')
        
        pg_hook.run(create_sql)
        
        print("Table 'spotify_data' creation on AWS PostgreSQL.")

    create_table()

setup_target_db_dag()