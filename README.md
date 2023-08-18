## Flask Data Fetcher
This Flask app periodically fetches JSON data from an external URL and provides an endpoint to retrieve the latest fetched data.

### Installation
1. Ensure you have Python 3.x installed. You can check your Python version with:
```
python --version
```

2. Install python requirements
```
pip install -r requirements.txt
```

### Configuration
Configuration parameters are stored in `config.py`. The main parameter to take note of is `GAME_ID`, which determines the ID portion of the URL from which the app fetches data. Modify this value as needed.
```
GAME_ID = 39
```

### Running the App

#### Using Python
```
python app.py
```

### Endpoints
`/latest_data`: Fetches the latest JSON data retrieved from the external URL. A full route would be the local ip of the server + the route

```
http://serverip/latest_data
```

#### Notes
The app fetches data from the external URL every 10 seconds and updates an internal global variable.
Ensure you modify the ID in config.py to fetch data from the desired URL.

## Setting up the Flask App as an Autostarting Linux Service
To make the Flask app start automatically on boot and run in the background as a service, we can use systemd, a system and service manager for Linux. Here's how you can set it up:

1. Create a systemd service file:
Create a new service file for your Flask app:

```
sudo nano /etc/systemd/system/flask_data_fetcher.service
```

2. Paste the following content into the editor, adjusting paths as needed:
```
[Unit]
Description=Flask Data Fetcher Service
After=network.target

[Service]
User=YOUR_USERNAME
WorkingDirectory=/path/to/your/flask_app_directory
ExecStart=/path/to/your/python /path/to/your/flask_app_directory/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Replace:
YOUR_USERNAME with the username you want the service to run under.
/path/to/your/flask_app_directory with the absolute path to the directory containing app.py.
/path/to/your/python with the path to your Python interpreter. You can get this path by running which python3.

3. Start and enable the service:
Now that you've created the service file, you can start the service with:

```
sudo systemctl start flask_data_fetcher.service
```
To check the status of your service:

```
sudo systemctl status flask_data_fetcher.service
```

If everything is working properly, you can enable the service to start on boot:
```
sudo systemctl enable flask_data_fetcher.service
```
4. Logging:
To view logs produced by your Flask app:
```
sudo journalctl -u flask_data_fetcher.service
```
This will show you logs produced by your Flask app, which is useful for debugging if something goes wrong.