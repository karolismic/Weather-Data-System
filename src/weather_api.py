import requests
import json
import numpy as np
from datetime import datetime, timedelta
import os

def fetch_weather_data(latitude, longitude, api_key, days=7):
    """Fetch weather data for specified days back from today."""
    end_time = datetime.now()
    start_time = end_time - timedelta(days=days)
    url = f"https://api.tomorrow.io/v4/timelines?location={latitude},{longitude}&fields=temperature,precipitationIntensity&units=metric&timesteps=1h&apikey={api_key}&startTime={start_time.isoformat()}Z&endTime={end_time.isoformat()}Z"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

def process_weather_data(hourly_temps, start_of_week, start_of_last_seven_days):
    """Process weather data to calculate required statistics for defined periods."""
    def get_temp_stats(temps):
        return np.max(temps), np.min(temps), np.std(temps)

    def rain_hours_count(temps):
        return sum(1 for temp in temps if temp['values'].get('precipitationIntensity', 0) > 0.1)

    results = {}
    today = datetime.now().date()
    for hour in hourly_temps:
        date = datetime.fromisoformat(hour['startTime']).date()
        temp = hour['values']['temperature']
        rain = hour['values'].get('precipitationIntensity', 0) > 0.1
        
        if date not in results:
            results[date] = {'temps': [], 'max_temp': -np.inf, 'min_temp': np.inf, 'rain_hours': 0}
        
        results[date]['temps'].append(temp)
        if temp > results[date]['max_temp']:
            results[date]['max_temp'] = temp
            results[date]['max_city'] = hour['city_name']
        if temp < results[date]['min_temp']:
            results[date]['min_temp'] = temp
            results[date]['min_city'] = hour['city_name']
        if rain:
            results[date]['rain_hours'] += 1

    # Calculate aggregates
    aggregate_results = {}
    for date, data in results.items():
        max_temp, min_temp, std_temp = get_temp_stats(data['temps'])
        aggregate_results[date] = {
            'max_temp': max_temp,
            'min_temp': min_temp,
            'std_temp': std_temp,
            'max_city': data['max_city'],
            'min_city': data['min_city'],
            'rain_hours': data['rain_hours']
        }

    # Return specific period data
    return {
        'today': aggregate_results.get(today),
        'yesterday': aggregate_results.get(today - timedelta(days=1)),
        'current_week': {k: v for k, v in aggregate_results.items() if k >= start_of_week},
        'last_seven_days': {k: v for k, v in aggregate_results.items() if k >= start_of_last_seven_days}
    }

def main():
    config_path = "configs/config.json"
    try:
        with open(config_path) as config_file:
            config = json.load(config_file)
        api_key = config['api_keys']['open_weather']

        results = {}
        for city in config['cities']:
            city_name = city['name']
            latitude = city['latitude']
            longitude = city['longitude']
            weather_data = fetch_weather_data(latitude, longitude, api_key, days=7)
            if weather_data:
                hourly_temps = weather_data['data']['timelines'][0]['intervals']
                start_of_week = datetime.now().date() - timedelta(days=datetime.now().weekday())
                start_of_last_seven_days = datetime.now().date() - timedelta(days=6)
                city_results = process_weather_data(hourly_temps, start_of_week, start_of_last_seven_days)
                results[city_name] = city_results
            else:
                print(f"Failed to fetch detailed data for {city_name}.")

        # Save the results to a JSON file
        with open('weather_results.json', 'w') as f:
            json.dump(results, f, indent=4)
        print("Results have been saved to 'weather_results.json'.")
    except FileNotFoundError:
        print(f"The file {config_path} does not exist.")
    except json.JSONDecodeError:
        print("Error decoding the JSON file.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()


