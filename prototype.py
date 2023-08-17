import requests
import urllib.parse
import json
from prettytable import PrettyTable

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
table.field_names = ["ID", "First Name", "Last Name", "Number", "Position"]

# Add each player to the table
for player in players:
    table.add_row([player["id"], player["firstName"], player["lastName"], player["number"], player["position"]])

# Print the table
print(table)
