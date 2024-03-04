import os
import re
import fcntl
import struct
import socket
import logging
import requests
from requests.exceptions import RequestException

class AppRegistrationClient:
    def __init__(self, registration_url="http://tdmx.local/register"):
        self.registration_url = registration_url
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def get_my_process_port(self):
        my_pid = os.getpid()
        process_lines = os.popen('netstat -tulnep').read().split('\n')
        port_line = next((line for line in process_lines if str(my_pid) in line), None)
        if port_line:
            matches = re.search(r':(\d+)\s', port_line)
            return matches.group(1) if matches else None
        else:
            return None

    def get_ip_address(self, ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15].encode('utf-8'))
        )[20:24])

    def register_app(self, app_name, address=None, port=None, ifname="wlan0"):
        #if not port:
        #    port = int(self.get_my_process_port())

        if not port:
            error_msg = f"Failed to register app {app_name}. Could not find a port associated with the app's process."
            self.logger.error(error_msg)
            return {"status": "error", "message": error_msg}
        
        if not address:
            address = self.get_ip_address(ifname)
            
        data = {"app_name": app_name, "address": address, "port": port}

        try:
            response = requests.post(self.registration_url, json=data)
        except RequestException as e:
            self.logger.exception('Request failed.')
            return {"status": "error", "message": str(e)}

        if response.status_code == 201:
            return {"status": "success", "message": f"Successfully registered app {app_name} with address {address}:{port}"}
        else:
            return {"status": "error", "message": f"Failed to register app {app_name}. Status code: {response.status_code}, message: {response.text}"}