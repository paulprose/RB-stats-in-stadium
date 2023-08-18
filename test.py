import time
import requests
import logging

logging.basicConfig(level=logging.INFO)

def fetch_data():
    logging.info("Background thread started")
    while True:
        try:
            logging.info("Fetching data...")
            response = requests.get('https://connectlive.cfl.ca/json/2023/stats/39.json')
            if response.status_code == 200:
                logging.info(f"Got response: {response.json()}")
                latest_data = response.json()
            else:
                logging.error(f"Error: Received status code {response.status_code}")
            time.sleep(10)
        except Exception as e:
            logging.error(f"Error in background thread: {e}")

fetch_data()
