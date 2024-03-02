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

def create_bar_chart(api_data):
    """Create bar chart for team records."""
    teams = api_data.get('teams', [])
    team_names = [team.get('name', 'Unknown') for team in teams]
    team_records = [team.get('record', '0-0') for team in teams]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(team_names, team_records, color='skyblue')
    ax.set_xlabel('Records')
    ax.set_ylabel('Teams')
    ax.set_title('Team Records')

    plt.show()

def main():
    # Retrieve JSON data from Redis
    api_data = retrieve_data_from_redis()

    if api_data:
        # Create bar chart
        create_bar_chart(api_data)
    else:
        print("Failed to retrieve data from Redis.")

if __name__ == "__main__":
    main()
