from airflow import DAG
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.postgres.hooks.postgres import PostgresHook # This will help to push data into PostgreDB
from airflow.decorators import task # To create task inside DAG
from airflow.utils.dates import days_ago
from datetime import datetime
import json


'''
ABOUT THE APPLLICATION 👇

We will provide the LATITUDE and LONGITUDE and using a weather application API
we shall probably be able to retreive the weather condition of that place
'''

# LATITUDE and LONGITUDE for the desired location (say, San Francisco)
LATITUDE = '37.773972'
LONGITUDE = '-122.431297'
POSTGRES_CONN_ID = 'postgres_default'
API_CONN_ID = 'open_meteo_api' # Connection Name

default_args = {
    'owner' : 'airflow',
    'start_date' : days_ago(1),
}


# Creating DAG
with DAG(dag_id = 'weather_etl_pipeline',
         default_args = default_args,
         schedule = '@daily', # The workflow will be run daily
         catchup = False
) as dags:
    @task()
    def extract_weather_data(): # STEP 1 : Extraction 🌟
        """Extract weather data from Open-Meteo API using Airflow Connection."""

        # Using HttpHook to get the connection details from Airflow connection
        http_hook = HttpHook(http_conn_id = API_CONN_ID, method = 'GET')

        # Building the API end point
        # URL : https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current_weather=true
        # Example usage : https://api.open-meteo.com/v1/forecast?latitude=37.773972&longitude=-122.431297&current_weather=true
        endpoint = f'/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current_weather=true'

        # Making the request via the HTTP Hook
        response = http_hook.run(endpoint)

        if response.status_code == 200: # If fetching is successful
            return response.json()
        else:
            raise Exception(f"Failed to Fetch Weather Data : {response.status_code}")
    

    @task
    def transform_weather_data(weather_data): # STEP 2 : Transformation 🌟
        """Transform the extracted weather data."""

        # Error Handling
        if 'current_weather' not in weather_data:
            raise KeyError("Missing 'current_weather' in API response")

        current_weather = weather_data['current_weather']

        transformed_data = {
            'latitude' : float(LATITUDE),
            'longitude' : float(LONGITUDE),
            'temperature' : current_weather['temperature'],
            'windspeed' : current_weather['windspeed'],
            'winddirection' : current_weather['winddirection'],
            'weathercode' : current_weather['weathercode'],
            'timestamp': datetime.utcnow()
        }
        return transformed_data


    @task
    def load_weather_data(transformed_data): # STEP 3 : Loading 🌟
        """Load transformed data into PostgreSQL"""

        pg_hook = PostgresHook(postgres_conn_id = POSTGRES_CONN_ID)
        conn = pg_hook.get_conn()
        cursor = conn.cursor()

        # Creating table (if it doesn't exist)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_data (
                       latitude FLOAT,
                       longitude FLOAT,
                       temperature FLOAT,
                       windspeed FLOAT,
                       winddirection FLOAT,
                       weathercode INT,
                       timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # Inserting transformed data into the above table
        cursor.execute("""
        INSERT INTO weather_data (latitude, longitude, temperature, windspeed, winddirection, weathercode, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            transformed_data['latitude'],
            transformed_data['longitude'],
            transformed_data['temperature'],
            transformed_data['windspeed'],
            transformed_data['winddirection'],
            transformed_data['weathercode'],
            transformed_data['timestamp']
        ))

        conn.commit()
        cursor.close()
        conn.close()
    
    # DAG Workflow - ETL Pipeline
    weather_data = extract_weather_data() # STEP 1 : Extraction 🌟
    transformed_data = transform_weather_data(weather_data=weather_data) # STEP 2 : Transformation 🌟
    load_weather_data(transformed_data=transformed_data) # STEP 3 : Loading 🌟