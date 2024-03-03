import os
import sys
import logging
from mdns_registrar import MdnsService
from flask import Flask, request, jsonify

# Import specifically what you need from libraries
from systemd.journal import JournalHandler

# Configurations and Constants
HOST = '0.0.0.0'
PORT = 8000

# Initial Setup
app = Flask(__name__)
mdns = MdnsService()

def configure_logging():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    
    logger.addHandler(JournalHandler())
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)
    
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(logging.ERROR)
    werkzeug_logger.disabled = True

    app.logger.disabled = True 
    
    return logger

logger = configure_logging()

from flask import Flask, jsonify, request

@app.route('/register', methods=['POST'])
def register_app():
    data = request.json
    logger.info(f"Got request: {data}")
    app_name = data.get('app_name')
    address = data.get('address')
    port = data.get('port')
    
    if not app_name or not isinstance(app_name, str):
        return jsonify({"error": "Invalid or missing parameter: app_name"}), 400
    if not address or not isinstance(address, str):
        return jsonify({"error": "Invalid or missing parameter: address"}), 400
    if not port or not isinstance(port, int):
        return jsonify({"error": "Invalid or missing parameter: port"}), 400
    
    try:
        logger.info(f"Attempting to register app: {app_name} to {address}:{port}")
        mdns.add_record(app_name, address, port)
    except ValueError as e:
        logger.error(f"Failed to register app: {app_name}. Error: {str(e)}")
        return jsonify({"error": str(e)}), 400
    
    return jsonify({"message": f"Success: {app_name}, {address}:{port}"}), 201

if __name__ == '__main__':
    logger.info("Starting application")
    try:
        app.run(host=HOST, port=PORT)
    except Exception as e:
        logger.error(f"Couldn't start. Error: {e}")