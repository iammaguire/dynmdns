from zeroconf import ServiceInfo, Zeroconf
import socket

class MdnsService:
    def __init__(self):
        self.zeroconf = Zeroconf()
        self.services = {}

    def add_record(self, app_name, address, port):
        if not app_name:
            raise ValueError('Invalid app name provided.')
        if not address:
            raise ValueError('Invalid address provided.')
        if not port or not isinstance(port, int):
            raise ValueError('Invalid port value provided, it must be an integer.')
        try:
            addr = socket.inet_aton(address)
        except socket.error:
            raise ValueError('Invalid IP address provided.') 

        info = ServiceInfo(
            "_http._tcp.local.",
            f"{app_name}._http._tcp.local.",
            addresses=[socket.inet_aton(address)],
            port=port,
            properties={'name': app_name},
            server=f"{app_name}.local.",
        )
        try:
            self.zeroconf.register_service(info)
        except Exception as e:
            raise ValueError(f"Failed to register service: {str(e)}")
            
        self.services[app_name] = info

    def remove_record(self, app_name):
        if app_name in self.services:
            self.zeroconf.unregister_service(self.services[app_name])
            del self.services[app_name]

    def modify_record(self, app_name, new_address, new_port):
        if app_name in self.services:
            self.remove_record(app_name)
            self.add_record(app_name, new_address, new_port)

    def close(self):
        self.zeroconf.close()