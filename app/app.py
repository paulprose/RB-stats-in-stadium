from flask import Flask, jsonify
import threading
import time
import datetime
import requests

app = Flask(__name__)
app.config.from_object('config')
home_squad_id = app.config['HOME_SQUAD_ID']

# Global variable to hold the latest fetched JSON data
latest_data = {}


def fetch_data():
    """Function to fetch data from an external URL and update the global variable."""
    global latest_data
    global home_squad_data
    global away_squad_data
    id_from_config = app.config['GAME_ID']
    url = f"https://connectlive.cfl.ca/json/2023/stats/{id_from_config}.json"
    
    while True:
        try:
            response = requests.get(url)  # Replace with your URL
            if response.status_code == 200:
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                app.logger.info(f"Got response OK: {response}")
                app.logger.info(f"Updating data at {timestamp}")
                latest_data = response.json()
            else:
                app.logger.error(f"Error: Received status code {response.status_code}")
        except Exception as e:
            app.logger.error(f"Failed to fetch data: {e}")

        home_squad_data = []
        away_squad_data = []
        for player in latest_data[0]["players"]:
            if player["squadId"] == home_squad_id:
                home_squad_data.append(player)
            else:
                away_squad_data.append(player)            

        time.sleep(10)  # Fetch data every 10 seconds

@app.route('/latest_data', methods=['GET'])
def get_latest_data():
    """Route to get the latest fetched JSON data."""
    return jsonify(latest_data)

@app.route('/home_squad', methods=['GET'])
def get_home_squad():
    """Route to get the latest fetched JSON data."""
    return jsonify(home_squad_data)

@app.route('/away_squad', methods=['GET'])
def get_away_squad():
    """Route to get the latest fetched JSON data."""
    return jsonify(away_squad_data)

@app.route('/HOME_PASSING', methods=['GET'])
def get_home_passing():
    """Route to get the top 3 passing players on the home squad sorted by passing succeeded yards."""
    sorted_home_passing = sorted(home_squad_data, key=lambda x: x['stats'].get('passesSucceededYards', 0), reverse=True)[:1]
    response_data = []
    for player in sorted_home_passing:
        response_data.append({
            'FirstName': player['firstName'],
            'FastName': player['lastName'],
            'passesSucceeded': player['stats'].get('passesSucceeded', 0),
            'passesSucceededYards': player['stats'].get('passesSucceededYards', 0),
            'passesAttempted': player['stats'].get('passesAttempted', 0),
        })
    return jsonify(response_data)

@app.route('/AWAY_PASSING', methods=['GET'])
def get_away_passing():
    """Route to get the top 3 passing players on the away squad sorted by passing succeeded yards."""
    sorted_away_passing = sorted(away_squad_data, key=lambda x: x['stats'].get('passesSucceededYards', 0), reverse=True)[:1]
    response_data = []
    for player in sorted_away_passing:
        response_data.append({
            'FirstName': player['firstName'],
            'FastName': player['lastName'],
            'passesSucceeded': player['stats'].get('passesSucceeded', 0),
            'passesSucceededYards': player['stats'].get('passesSucceededYards', 0),
            'passesAttempted': player['stats'].get('passesAttempted', 0),
        })
    return jsonify(response_data)


@app.route('/HOME_RUSHING', methods=['GET'])
def get_home_rushing():
    """Route to get the top 3 rushing players on the home squad sorted by rushing yards."""
    sorted_home_rushing = sorted(home_squad_data, key=lambda x: x['stats'].get('rushingYards', 0), reverse=True)[:3]
    response_data = []
    for player in sorted_home_rushing:
        response_data.append({
            'FirstName': player['firstName'],
            'FastName': player['lastName'],
            'rushingYards': player['stats'].get('rushingYards', 0),
            'rushes': player['stats'].get('rushes', 0),
        })
    return jsonify(response_data)

@app.route('/AWAY_RUSHING', methods=['GET'])
def get_away_rushing():
    """Route to get the top 3 rushing players on the away squad sorted by rushing yards."""
    sorted_away_rushing = sorted(away_squad_data, key=lambda x: x['stats'].get('rushingYards', 0), reverse=True)[:3]
    response_data = []
    for player in sorted_away_rushing:
        response_data.append({
            'FirstName': player['firstName'],
            'FastName': player['lastName'],
            'rushingYards': player['stats'].get('rushingYards', 0),
            'rushes': player['stats'].get('rushes', 0),
        })
    return jsonify(response_data)

@app.route('/HOME_RECEIVING', methods=['GET'])
def get_home_receiving():
    """Route to get the top 3 receiving players on the home squad sorted by receiving yards."""
    sorted_home_receiving = sorted(home_squad_data, key=lambda x: x['stats'].get('receivingYards', 0), reverse=True)[:3]
    response_data = []
    for player in sorted_home_receiving:
        response_data.append({
            'FirstName': player['firstName'],
            'FastName': player['lastName'],
            'receivingYards': player['stats'].get('receivingYards', 0),
            'receptions': player['stats'].get('receptions', 0),
        })
    return jsonify(response_data)

@app.route('/AWAY_RECEIVING', methods=['GET'])
def get_away_receiving():
    """Route to get the top 3 receiving players on the away squad sorted by receiving yards."""
    sorted_away_receiving = sorted(away_squad_data, key=lambda x: x['stats'].get('receivingYards', 0), reverse=True)[:3]
    response_data = []
    for player in sorted_away_receiving:
        response_data.append({
            'FirstName': player['firstName'],
            'FastName': player['lastName'],
            'receivingYards': player['stats'].get('receivingYards', 0),
            'receptions': player['stats'].get('receptions', 0),
        })
    return jsonify(response_data)

@app.route('/HOME_DEFENSE', methods=['GET'])
def get_home_defence():
    """Route to get the top 3 defensive players on the home squad sorted by total solo tackles"""
    sorted_home_defence = sorted(home_squad_data, key=lambda x: x['stats'].get('tacklesSolo', 0), reverse=True)[:3]
    response_data = []
    for player in sorted_home_defence:
        response_data.append({
            'FirstName': player['firstName'],
            'FastName': player['lastName'],
            'tacklesSolo': player['stats'].get('tacklesSolo', 0)
        })
    return jsonify(response_data)


@app.route('/AWAY_DEFENSE', methods=['GET'])
def get_away_defence():
    """Route to get the top 3 defensive players on the away squad sorted by total solo tackles"""
    sorted_away_defence = sorted(away_squad_data, key=lambda x: x['stats'].get('tacklesSolo', 0), reverse=True)[:3]
    response_data = []
    for player in sorted_away_defence:
        response_data.append({
            'FirstName': player['firstName'],
            'FastName': player['lastName'],
            'tacklesSolo': player['stats'].get('tacklesSolo', 0)
        })
    return jsonify(response_data)

if __name__ == "__main__":
    # Set up logging
    import logging
    logging.basicConfig(level=logging.INFO)

    # Start the background thread
    daemon = threading.Thread(target=fetch_data, daemon=True, name='BackgroundFetch')
    daemon.start()
    
    # Run the Flask app
    app.run(debug=False)  # Temporarily turn off debug mode for testing
