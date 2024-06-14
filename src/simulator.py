import json
import numpy as np
from datetime import datetime

def read_weather_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data['data']['timelines'][0]['intervals']

def compute_aggregates(data):
    aggregates = {}
    for entry in data:
        city_name = entry['city_name']
        if city_name not in aggregates:
            aggregates[city_name] = {
                'temperatures': [],
                'rain_hours_last_day': 0,
                'rain_hours_last_week': 0,
                'max_temp': float('-inf'),
                'min_temp': float('inf'),
                'max_city_hourly': None,
                'min_city_hourly': None
            }
        temp = entry['values']['temperature']
        rain = entry['values']['precipitationIntensity']
        aggregates[city_name]['temperatures'].append(temp)

        if temp > aggregates[city_name]['max_temp']:
            aggregates[city_name]['max_temp'] = temp
            aggregates[city_name]['max_city_hourly'] = entry['startTime']
        if temp < aggregates[city_name]['min_temp']:
            aggregates[city_name]['min_temp'] = temp
            aggregates[city_name]['min_city_hourly'] = entry['startTime']

        # Assuming the datetime from the entry is today or the last seven days
        date = datetime.fromisoformat(entry['startTime'][:-1])  # Remove the 'Z' for parsing
        if (datetime.now() - date).days < 1:
            if rain > 0.1:
                aggregates[city_name]['rain_hours_last_day'] += 1
        if (datetime.now() - date).days < 7:
            if rain > 0.1:
                aggregates[city_name]['rain_hours_last_week'] += 1

    for city, agg in aggregates.items():
        agg['std_temp'] = np.std(agg['temperatures'])
        del agg['temperatures']  # Remove raw temperatures to clean up output

    return aggregates

def main():
    file_path = 'weather_results.json'  # Adjust path if necessary
    weather_data = read_weather_data(file_path)
    aggregates = compute_aggregates(weather_data)
    
    # Save the results to a JSON file
    with open('aggregated_weather_data.json', 'w') as f:
        json.dump(aggregates, f, indent=4)

    print("Aggregated data has been saved to 'aggregated_weather_data.json'.")

if __name__ == "__main__":
    main()


