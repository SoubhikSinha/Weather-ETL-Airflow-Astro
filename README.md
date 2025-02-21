# Weather (ETL) : Apache Airflow - Astro

<br>

## Acknowledgement
I would like to extend my sincere thanks to  [Krish Naik](https://github.com/krishnaik06)  for his invaluable content and guidance, which helped me build this project. This project wouldn't have been possible without his educational resources.

<br>

## About the Project
This project implements an [ETL (Extract, Transform, Load)](https://cloud.google.com/learn/what-is-etl) pipeline using [Apache Airflow](https://airflow.apache.org/) to fetch weather data from the [Open-Meteo API ](https://open-meteo.com/)and store it in a PostgreSQL database. The workflow is automated using Airflow DAGs and runs on a daily schedule.

<br>

## Project Workflow
The ETL pipeline follows three major steps :

1.  **Extraction** : Fetches real-time weather data using the Open-Meteo API by providing latitude and longitude as inputs.
    
2.  **Transformation** : Extracts relevant weather parameters such as temperature, wind speed, wind direction, and weather code. The transformed data is formatted into a structured JSON-like format.
    
3.  **Loading** : The processed weather data is inserted into a PostgreSQL database, ensuring persistence and availability for analysis.
