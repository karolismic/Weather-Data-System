import psycopg2
from dotenv import load_dotenv
import os
import json
import matplotlib.pyplot as plt
import numpy as np

def ingest_weather_data(cursor, json_file_path):
    """Ingest weather data from a JSON file into the database."""
    with open(json_file_path, 'r') as file:
        data = json.load(file)['data']['timelines'][0]['intervals']

    for entry in data:
        city_name = entry['city_name']
        # Insert city if not already present and fetch its ID
        cursor.execute("""
            INSERT INTO cities (city_name)
            VALUES (%s) ON CONFLICT (city_name) DO NOTHING;
        """, (city_name,))
        cursor.execute("SELECT city_id FROM cities WHERE city_name = %s;", (city_name,))
        city_id = cursor.fetchone()[0]

        # Insert weather data entries
        cursor.execute("""
            INSERT INTO weather_data (city_id, record_time, temperature, precipitation)
            VALUES (%s, %s, %s, %s);
        """, (city_id, entry['startTime'], entry['values']['temperature'], entry['values']['precipitationIntensity']))

def main():
    load_dotenv(r'C:\Users\Karolis\Documents\Github repository\kmicku-DE2v2.2.5\kmicku-DE2v2.2.5\configs\.env')
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        cursor = conn.cursor()
        print("Connected to the database successfully.")

        # Execute SQL to create tables
        create_tables_path = os.getenv('CREATE_TABLES_SQL_PATH')
        if create_tables_path:
            with open(create_tables_path, 'r') as file:
                cursor.execute(file.read())
            conn.commit()
            print("Tables created successfully.")

        # Ingest weather data from JSON
        weather_data_path = os.getenv('WEATHER_DATA_JSON_PATH')
        if weather_data_path:
            ingest_weather_data(cursor, weather_data_path)
            conn.commit()
            print("Weather data ingested successfully.")

    except psycopg2.OperationalError as e:
        print("Failed to connect to the database:", e)
    except psycopg2.DatabaseError as e:
        print("Database error:", e)
    except Exception as e:
        print("An error occurred:", e)
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
        print("Database connection closed.")

if __name__ == "__main__":
    main()
