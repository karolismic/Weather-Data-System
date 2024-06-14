-- Create a table for cities
CREATE TABLE IF NOT EXISTS cities (
    city_id SERIAL PRIMARY KEY,
    city_name VARCHAR(100) UNIQUE,
    country_name VARCHAR(100)
);

-- Create a table for storing hourly weather data
CREATE TABLE IF NOT EXISTS weather_data (
    weather_id SERIAL PRIMARY KEY,
    city_id INTEGER REFERENCES cities(city_id),
    record_time TIMESTAMP WITHOUT TIME ZONE,
    temperature DECIMAL(4, 2),
    precipitation DECIMAL(5, 2),
    weather_description TEXT
);