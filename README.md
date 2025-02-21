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

<br>

## How to Run the Project ?
(NOTE : This project was carried out on a [Macintosh](https://www.apple.com/mac/) machine)


### **1. Clone the Repository**

Clone the repository to your local machine :

```bash
git clone https://github.com/SoubhikSinha/Weather-ETL-Airflow-Astro.git
```

<br>

### **2. Install Prerequisites**
Ensure that Docker is installed and running on your system. Install Astro CLI using Homebrew:
```bash
brew install astro
```

Install Apache Airflow using pip:
```bash
pip install apache-airflow
```
_(Optional: Create a virtual environment before installation.)_

<br>

### **3. Initialize the Astro Project**
```bash
astro dev init
```

<br>

### **4. Start the Workflow**
```bash
astro dev start
```
If any modifications are made, restart the workflow:
```bash
astro dev restart
```

<br>

### **5. Configure Airflow Connections**
Navigate to the Airflow UI (`http://localhost:8080`) and configure the necessary connections under **Admin > Connections**:

#### **PostgreSQL Connection**

-   **Connection Id**: `postgres_default`
    
-   **Connection Type**: `Postgres`
    
-   **Host**: _(Find the project containers and copy the name of the_ `_postgres_` _container)_
    
-   **Database**: `postgres`
    
-   **Login**: `postgres`
    
-   **Password**: `postgres`
    
-   **Port**: `5432`
    

#### **Open-Meteo API Connection**

-   **Connection Id**: `open_meteo_api`
    
-   **Connection Type**: `HTTP`
    
-   **Host**: `https://api.open-meteo.com`
  
<br>

### **6. Run the DAG**

1.  Go to the Airflow UI and locate the `weather-etl-pipeline` DAG under **DAGs**.
    
2.  Click on the **Trigger DAG** button (`▶️`) to execute the pipeline.
    
3.  Monitor the execution logs under **Admin > XComs** for each ETL step.
    
<br>

### **7. Verify Data Storage**

To confirm successful data storage, use [DBeaver](https://dbeaver.io/download/) or any SQL client to query the PostgreSQL database and validate the weather data records.
