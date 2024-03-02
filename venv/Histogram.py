import json
import matplotlib.pyplot as plt
from db_config import get_redis_connection

def retrieve_data_from_redis():
    """Retrieve JSON data from Redis."""
    try:
        # Connect to Redis
        r = get_redis_connection()

        # Retrieve JSON data from Redis using the JSON.GET command
        json_data = r.execute_command('JSON.GET', 'teams_data')
        
        if json_data:
            return json.loads(json_data)
        else:
            print("No data found in Redis.")
            return None
    except Exception as e:
        print('Error retrieving data from Redis:', e)
        return None

def create_histogram_team_records(api_data):
    """Create histogram for distribution of team records."""
    teams = api_data.get('teams', [])
    records = [team.get('record', '0-0') for team in teams]

    # Extract win counts from records
    win_counts = [int(record.split('-')[0]) for record in records]

    plt.figure(figsize=(10, 6))
    plt.hist(win_counts, bins=range(min(win_counts), max(win_counts) + 2), color='skyblue', edgecolor='black', alpha=0.7)
    plt.xlabel('Wins')
    plt.ylabel('Number of Teams')
    plt.title('Distribution of Team Records')
    plt.grid(True)

    plt.show()

def main():
    # Retrieve JSON data from Redis
    api_data = retrieve_data_from_redis()

    if api_data:
        # Create histogram
        create_histogram_team_records(api_data)
    else:
        print("Failed to retrieve data from Redis.")

if __name__ == "__main__":
    main()

