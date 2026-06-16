#  End-to-End Spotify ETL Pipeline

##  Project Overview
This repository contains a production-grade Extract, Transform, Load (ETL) pipeline designed to process Spotify track and album data. The pipeline extracts unstructured raw data from a NoSQL database (MongoDB), performs rigorous data cleaning and transformation using Python (Pandas), and loads the structured data into a normalized relational database (AWS PostgreSQL) for analytical querying. 

The entire workflow is orchestrated via **Apache Airflow** and containerized using **Docker** to ensure a reproducible and scalable environment.

##  Tech Stack & Architecture
* **Orchestration:** Apache Airflow (TaskFlow API)
* **Source System:** MongoDB (NoSQL)
* **Processing Engine:** Python (Pandas, NumPy)
* **Target Data Warehouse:** AWS PostgreSQL (Relational)
* **Infrastructure:** Docker & Docker Compose

### Pipeline Architecture

The pipeline follows a linear Extract → Transform → Load pattern:
1. **Extract:** Connects to MongoDB via `MongoHook`, retrieves raw JSON documents, and stages them locally.
2. **Transform:** Data cleansing (removing duplicates, handling missing values), string manipulation (cleaning genres), and type casting (standardizing dates and numeric fields).
3. **Load:** Implements an **UPSERT** strategy using `ON CONFLICT (track_id)` in PostgreSQL to guarantee idempotency and prevent data duplication.

##  Repository Structure
```text
.
├── dags/
│   ├── ETL_dag.py             # Main Airflow DAG
│   └── create_table_dag.py    # Schema initialization DAG
├── .env.example               # Environment variables template
├── docker-compose.yaml        # Local cluster configuration
├── Dockerfile                 # Custom Airflow image
├── requirements.txt           # Python dependencies
└── Queries.mongodb.js         # Data exploration queries

```

##  Data Modeling & Visualizations

### Airflow DAG Workflow

Linear execution showing the successful flow of data between tasks.
![Airflow DAG Workflow](airflow_dag.jpg)

### 📈 Power BI Analytics Dashboard
I created a multi-page Power BI report connecting directly to the transformed AWS PostgreSQL database. The visuals explore artist popularity, genre distributions, album release trends, and explicit content analysis over time.

<p align="center">
  <img src="Artist Analysis.jpeg" width="45%" />
  <img src="Album Analysis.jpeg" width="45%" />
  <br>
  <img src="/Relationship Analysis.jpeg" width="45%" />
  <img src="/Time Analysis&Forecast.jpeg" width="45%" />
</p>



## 🚀 How to Run the Project Locally

### 1. Prerequisites

* Docker and Docker Compose installed.

### 2. Environment Setup

```bash
git clone [https://github.com/Nikol2108/ent-to-end-etl-pipeline.git](https://github.com/Nikol2108/ent-to-end-etl-pipeline.git)
cd ent-to-end-etl-pipeline
cp .env.example .env

```

### 3. Build and Start

```bash
docker-compose up -d --build

```

Access the Airflow UI at `http://localhost:8080`.

## 🔍 Data Quality & Validation

* **Idempotency:** Ensures the pipeline can be run multiple times safely.
* **Integrity Checks:** The transformation layer explicitly validates critical fields before loading.

```

---

### הפקודות להעלאה סופית (להריץ בטרמינל):

אחרי ששמרת את הקובץ עם התוכן הזה, תריצי את זה כדי לעדכן את הגיטהאב:

```bash
git add .
git commit -m "Restore and update full README with visualizations"
git push -f origin main

```

**טיפ:** אם שמות קבצי התמונות שלך (ה-PowerBI) שונים ממה שכתבתי בקוד (`powerbi_1.png` וכו'), פשוט תשני את השמות בקוד למה ששמור אצלך בתיקייה. עכשיו הכל יהיה מתועד ומושלם!