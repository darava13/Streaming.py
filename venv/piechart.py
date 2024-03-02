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

def create_pie_chart(api_data):
    """Create pie chart for distribution of team abbreviations."""
    teams = api_data.get('teams', [])
    abbreviations = [team.get('abbreviation', 'Unknown') for team in teams]

    # Count the occurrences of each abbreviation
    abbreviation_counts = {}
    for abbreviation in abbreviations:
        abbreviation_counts[abbreviation] = abbreviation_counts.get(abbreviation, 0) + 1

    # Plotting
    plt.figure(figsize=(8, 8))
    plt.pie(abbreviation_counts.values(), labels=abbreviation_counts.keys(), autopct='%1.1f%%', startangle=140)
    plt.title('Distribution of Team Abbreviations')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

    plt.show()

def main():
    # Retrieve JSON data from Redis
    api_data = retrieve_data_from_redis()

    if api_data:
        # Create pie chart
        create_pie_chart(api_data)
    else:
        print("Failed to retrieve data from Redis.")

if __name__ == "__main__":
    main()
