import requests
import urllib.parse
import json
from prettytable import PrettyTable
import time

# Set the URL of the endpoint
url = "https://connectlive.cfl.ca/json/2023/stats/39.json"

# Send a GET request to the endpoint
response = requests.get(url)

# Decode the response data using urllib.parse
decoded_data = urllib.parse.unquote(response.text)

# Parse the JSON data using the json module
json_data = json.loads(decoded_data)

# Extract the "players" object from the top-level list
players = json_data[0]["players"]

# Create a table to display the player data
table = PrettyTable()
table.field_names = ["ID", "First Name", "Last Name", "Number", "Position", "Blocked Kicks", "Losses", "Losses Yards", "Net Offence", "Passes Attempted", "Passes Rating", "Passes Sacked", "Passes Succeeded", "Passes Succeeded Yards", "Passes Succeeded Yards Longest", "Penalties Yds", "Rushes", "Rushing Yards", "Rushing Yards Average", "Rushing Yards Longest", "Total Defensive Plays", "Touchdowns Passes"]

# Add each player and their stats to the table
for player in players:
    # Create a dictionary to store the flattened stats
    stats = {}

    # Flatten the "stats" object and add it to the dictionary
    for key, value in player["stats"].items():
        stats[key] = value

    # Add the player and their flattened stats to the table
    table.add_row([player["id"], player["firstName"], player["lastName"], player["number"], player["position"], stats.get("blockedKicks", ""), stats.get("losses", ""), stats.get("lossesYards", ""), stats.get("netOffence", ""), stats.get("passesAttempted", ""), stats.get("passesRating", ""), stats.get("passesSacked", ""), stats.get("passesSucceeded", ""), stats.get("passesSucceededYards", ""), stats.get("passesSucceededYardsLongest", ""), stats.get("penaltiesYds", ""), stats.get("rushes", ""), stats.get("rushingYards", ""), stats.get("rushingYardsAverage", ""), stats.get("rushingYardsLongest", ""), stats.get("totalDefensivePlays", ""), stats.get("touchdownsPasses", "")])

# Print the table
print(table)


# save the table as a csv file
with open('cfl.csv', 'w') as f:
    f.write(table.get_string())
    f.close()