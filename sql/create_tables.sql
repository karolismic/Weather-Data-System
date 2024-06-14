-- Drop tables if they already exist to ensure a clean setup
-- Caution: This will remove all existing data, use only during initial setup or make sure you have backups if this is a production environment
DROP TABLE IF EXISTS weather_data;
DROP TABLE IF EXISTS cities;

-- Create the table for storing city information
CREATE TABLE cities (
    city_id SERIAL PRIMARY KEY,
    city_name VARCHAR(100) UNIQUE NOT NULL,  -- Ensure city_name is unique and not nullable
    country_name VARCHAR(100)
);

-- Create the table for storing hourly weather data
CREATE TABLE weather_data (
    weather_id SERIAL PRIMARY KEY,
    city_id INTEGER NOT NULL REFERENCES cities(city_id),
    record_time TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    temperature DECIMAL(4, 2),
    precipitation DECIMAL(5, 2),
    weather_description TEXT
);

-- Optional: Indexes can be created to improve the performance of queries involving these columns
CREATE INDEX idx_weather_city_id ON weather_data (city_id);
CREATE INDEX idx_weather_record_time ON weather_data (record_time);

