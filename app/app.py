from flask import Flask, jsonify
import threading
import time
import datetime
import requests

app = Flask(__name__)
app.config.from_object('config')

# Global variable to hold the latest fetched JSON data
latest_data = {}


def fetch_data():
    """Function to fetch data from an external URL and update the global variable."""
    global latest_data
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

        time.sleep(10)  # Fetch data every 10 seconds

@app.route('/latest_data', methods=['GET'])
def get_latest_data():
    """Route to get the latest fetched JSON data."""
    return jsonify(latest_data)

if __name__ == "__main__":
    # Set up logging
    import logging
    logging.basicConfig(level=logging.INFO)

    # Start the background thread
    daemon = threading.Thread(target=fetch_data, daemon=True, name='BackgroundFetch')
    daemon.start()
    
    # Run the Flask app
    app.run(debug=False)  # Temporarily turn off debug mode for testing
