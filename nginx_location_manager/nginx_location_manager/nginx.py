import os
from urllib.parse import urlparse

class NginxLocationManager():
    def __init__(self, nginx_config_path="/etc/nginx/sites-available/tdmx"):
        self.nginx_config_path = nginx_config_path
        self.temp_path = nginx_config_path + '_temp'

    def add_location(self, app_name, address):
        result = urlparse(address)

        # A valid URL always has a scheme(e.g. http) and a netloc(e.g. localhost:5001)
        if not all([result.scheme, result.netloc]):
            raise ValueError(f'Invalid address: {address}')

        with open(self.nginx_config_path, 'r') as file:
            file_data = file.read()

        # Check if app_name already exists in config
        if f" location /{app_name} " in file_data:
            raise ValueError(f'location block for {app_name} already exists')

        new_location_block = f"""
        location /{app_name} {{
            proxy_pass {address};
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }}"""

        # find the place of last closing bracket for server block
        i = file_data.rfind("}")
        new_data = file_data[:i] + new_location_block + file_data[i:]

        # write data to a temporary file
        with open(self.temp_path, 'w') as temp_file:
            temp_file.write(new_data)

        # Validate the new config file
        validation_status = os.system(f"/usr/sbin/nginx -t -c {self.temp_path} > /dev/null 2>&1")
        if validation_status != 0:
            os.remove(self.temp_path)
            raise ValueError(f'Invalid syntax in new config for {app_name}')

        # If validation is successful, replace the original file with the new one
        os.rename(self.temp_path, self.nginx_config_path)
        return True

    def reload_nginx(self):
        reload_status = os.system("sudo systemctl reload nginx > /dev/null 2>&1")
        if reload_status != 0:
            raise RuntimeError("Failed to reload Nginx")