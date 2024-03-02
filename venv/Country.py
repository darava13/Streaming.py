import json
import requests
import redis
from db_config import get_redis_connection


def fetch_data_from_api():
    """Fetch JSON data from the API."""
    url = 'https://therundown-therundown-v1.p.rapidapi.com/sports/2/teams'
    headers = {
        'X-RapidAPI-Key': 'ea96d35cbfmsh3bf1f7df4d8a2d0p144a48jsn97312e4be3c5',
        'X-RapidAPI-Host': 'therundown-therundown-v1.p.rapidapi.com'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx errors
        return response.json()  # Extract JSON data from the response
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None

def main():
    # Fetch JSON data from the API
    api_data = fetch_data_from_api()

    if api_data:
        # Connect to Redis
        r = get_redis_connection()

        # Insert JSON data into Redis using the JSON.SET command
        r.execute_command('JSON.SET', 'countries_data', '.', json.dumps(api_data))
        
        print("Data inserted into RedisJSON successfully!")
    else:
        print("Failed to fetch data from the API.")

if __name__ == "__main__":
    main()
