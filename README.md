## Project Overview

This project aims to build a robust backend system for simulating and analyzing weather data to study global warming effects. The project involves setting up a relational database management system (RDBMS) to store hourly weather data from the largest cities in Europe, querying weather APIs to collect real-time data, and employing data analysis to validate and simulate weather conditions. This README outlines the workflow from data collection to database setup, culminating in data analysis and simulation validation.

## Objectives

- Translate project requirements into data engineering tasks.
- Set up and configure a PostgreSQL RDBMS.
- Develop Python scripts to automate data collection from weather APIs.
- Store and analyze data using SQL with a focus on scalability and performance.
- Document the solution comprehensively for future development and collaborative work.

## Data Engineering Workflow

### Step 1: Database Setup and Configuration

PostgreSQL was selected for its ability to handle large datasets and its robustness in transaction and concurrency management. Database connection details are stored securely in `.env`.

### Step 2: Data Collection via APIs

Weather data is collected hourly from the OpenWeatherMap API using Python scripts located in the `src` directory. The API keys and city coordinates are managed through `config.json`.

### Step 3: Database Schema Creation

SQL scripts located in the `sql` directory are used to create necessary tables and views for storing and analyzing the weather data. These include tables for storing hourly data and views for aggregating data on a daily and weekly basis.

### Step 4: Data Ingestion and Management

Python scripts automate the ingestion of data into the database. The main.py script fetches weather data and inserts it into the database, handling concurrency with the use of Python's threading module for efficiency. The main.py script utilizes functions defined in weather_api.py to fetch and insert data into the database, leveraging Python's threading for efficient data handling.

### Step 5: Data Analysis and Simulation Validation

The system includes SQL views and Python scripts for analyzing the weather data—calculating maximum, minimum, and standard deviations of temperatures and identifying trends in weather conditions.

### Step 6: Simulator Configuration

The simulator.py script is utilized to simulate and analyze collected weather data further. It processes and aggregates data to generate comprehensive reports on weather patterns, supporting deeper insights into climate change impacts. This script reads the structured weather data stored in the PostgreSQL database, performs various analytical operations, and validates simulated outcomes against real-world data.

## Tools and Technologies

- **Python**: Primary programming language for scripting and automation.
- **PostgreSQL**: Chosen RDBMS for data storage.
- **Docker**: Used for creating a consistent development environment.
- **Cron**: Utilized for scheduling tasks like data fetching and database backups.
- **Git**: For version control.
- **Prometheus and Grafana** (planned): For monitoring and visualizing metrics.

## Setup and Execution

### Configuring Database and Environment

- Ensure PostgreSQL is installed and running.

- Clone the repository and navigate to the project directory.

- Install required Python packages, numpy and requests:
  ```

  pip install python-dotenv
  ```
  ```

  pip install psycopg2
  ```

  ```
  pip install numpy
  ```

  ```
  pip install requests
  ```

  ```
  pip install -r requirements.txt
  ```

## Preparing the Environment

The .gitignore file is configured to exclude .env from uploads to GitHub for security. You must manually configure this file with your database and API keys:
plaintext

# Example .env structure
DB_NAME=your_database_name

DB_USER=your_database_user

DB_PASSWORD=your_password

DB_HOST=localhost

DB_PORT=5432

CREATE_TABLES_SQL_PATH=path/to/create_table.sql

INGEST_DATA_SQL_PATH=path/to/ingest_data.sql

WEATHER_RESULTS_JSON_PATH=path/to/weather_results.json

API_KEY=your_api_key

# Selecting an API

You can choose from several weather APIs for data collection:

1. [OpenWeatherMap][https://openweathermap.com]
2. [WeatherAPI][https://openweathermap.org/api]
3. [AccuWeather][https://www.accuweather.com/]
4. [WeatherStack][https://weatherstack.com/]
5. [MetOffice][https://www.tomorrow.io/]

Configure your selected API key in the .env file and adjust weather_api.py to use this service.

### Running the Application

- Update `.env` with your database credentials.

- Run the SQL scripts to set up the database schema.

- Set up cron jobs using `cron_jobs.txt` for regular script execution.

- Run 

  ```
  main.py
  ```

   to start data collection:

  ```
  css

  python src/main.py
  ```

## Testing

Unit tests should be developed for each component to ensure functionality and reliability. Integration tests can validate the workflow from API data fetch to database insertion.

## Documentation

Each script and process is documented within the code and in additional markdown files within the repository to aid in maintenance and future development.

## Future Enhancements

- Incorporate advanced machine learning models to predict weather patterns.
- Expand the database schema to include more detailed meteorological data.
- Implement Prometheus and Grafana for real-time data monitoring and alerts.

## Conclusion

This project establishes a solid foundation for weather data simulation and analysis aimed at understanding and predicting global warming effects. The infrastructure allows for scalable data collection, robust data storage, and detailed analysis, facilitating ongoing research and development.

## Author

Karolis Mickus
