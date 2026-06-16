from datetime import datetime, timedelta
from airflow.sdk import dag, task
from airflow.providers.mongo.hooks.mongo import MongoHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
import json
import pandas as pd
import numpy as np



default_args = {
    'owner': 'Nikol',
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}

target_fields = [
        'track_id', 'track_name', 'track_number', 'track_popularity',
        'track_duration_ms', 'explicit', 'artist_name', 'artist_popularity',
        'artist_followers', 'artist_genres', 'album_id', 'album_name',
        'album_release_date', 'album_total_tracks', 'album_type'
        ]


@dag(
    dag_id='etl_pipeline_v.1.5',
    default_args=default_args,
    description='Extracts from MongoDB, transforms, and loads to AWS PostgreSQL',
    start_date=datetime(2026, 1, 1),
    schedule='@daily',
    catchup=False,
    tags=['etl', 'spotify', 'mongodb']
)


def mongodb_etl():

    @task()
    def extract_from_mongodb():
        hook = MongoHook(mongo_conn_id="mongodb_conn")
        collection = hook.get_collection("SpotifyData", "Project_ETL")
        documents = list(collection.find({}, {"_id": 0}))

        raw_spotify_data = '/tmp/raw_data.json'
        with open(raw_spotify_data, 'w') as f:
            json.dump(documents, f, default=str) 
                        
        return raw_spotify_data
    


    @task()
    def transform_data(raw_spotify_data):

        df = pd.read_json(raw_spotify_data)

        df = df.drop_duplicates(subset=['track_id'])
        df = df[df['track_name'].notna() & (df['track_name'].str.strip() != "")]

        cols_to_clean = ['artist_name', 'artist_genres']
        for col in cols_to_clean:
            df[col] = df[col].astype(str).str.replace(r"[\[\]']", "", regex=True).str.strip()

        invalid_genres = ['', 'None', 'null', 'nan']
        df.loc[df['artist_genres'].isin(invalid_genres), 'artist_genres'] = 'Unknown'
        df = df.dropna(subset=['album_release_date'])

        df['album_release_date'] = pd.to_datetime(df['album_release_date'], errors='coerce').dt.strftime('%Y-%m-%d')

        numeric_cols = ['track_number', 'track_popularity', 'track_duration_ms', 
                        'artist_popularity', 'artist_followers', 'album_total_tracks']
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        df['explicit'] = df['explicit'].astype(bool)


        df = df.replace({np.nan: None, pd.NaT: None})
        df = df.dropna()

        for col in numeric_cols:
            df[col] = df[col].astype(int)


        df = df[target_fields]
        after_clean_data = '/tmp/clean_data.csv'
        df.to_csv(after_clean_data, index=False, header=False)
    
        return after_clean_data


    @task()
    def load_to_postgres(after_clean_data):
        cols_str = ', '.join(target_fields)
        pg_hook = PostgresHook(postgres_conn_id='aws_postgres_conn')
        
        conn = pg_hook.get_conn()
        cursor = conn.cursor()

        cursor.execute("CREATE TEMP TABLE temp_spotify (LIKE spotify_data);")

        copy_sql = f"COPY temp_spotify ({cols_str}) FROM STDIN WITH CSV"
        with open(after_clean_data, 'r') as f:
            cursor.copy_expert(copy_sql, f)

        upsert_sql = f"""
            INSERT INTO spotify_data ({cols_str})
            SELECT * FROM temp_spotify
            ON CONFLICT (track_id) DO UPDATE SET
                track_name = EXCLUDED.track_name,
                track_number = EXCLUDED.track_number,
                track_popularity = EXCLUDED.track_popularity,
                track_duration_ms = EXCLUDED.track_duration_ms,
                explicit = EXCLUDED.explicit,
                artist_name = EXCLUDED.artist_name,
                artist_popularity = EXCLUDED.artist_popularity,
                artist_followers = EXCLUDED.artist_followers,
                artist_genres = EXCLUDED.artist_genres,
                album_id = EXCLUDED.album_id,
                album_name = EXCLUDED.album_name,
                album_release_date = EXCLUDED.album_release_date,
                album_total_tracks = EXCLUDED.album_total_tracks,
                album_type = EXCLUDED.album_type;
        """
        cursor.execute(upsert_sql)
        
        conn.commit()

    
    raw_data = extract_from_mongodb()
    cleaned_data = transform_data(raw_data)
    load_data = load_to_postgres(cleaned_data)


mongodb_etl()