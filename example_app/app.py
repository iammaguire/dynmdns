from flask import Flask
from dynhost_register import AppRegistrationClient
import threading
import time
import logging

app = Flask(__name__)

# Wrap registration in a function
def register_app(app_name): 
    time.sleep(5) # Wait for server to start
    client = AppRegistrationClient()
    response = client.register_app(app_name, port=5000, ifname='eth0')

    if response['status'] == 'success':
        app.logger.info(response['message'])
    else:
        app.logger.error(response['message'])

def run_server():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    
    # Use threading to start server and registration concurrently
    server_thread = threading.Thread(target=run_server)
    server_thread.start()

    register_app('test_app')

    server_thread.join()