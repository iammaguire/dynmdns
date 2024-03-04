from mdns_registrar.mdns_registrar import MdnsService
import netifaces
import logging
#from systemd.journal import JournalHandler
import sys

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
#logger.addHandler(JournalHandler())

# Log to console as well
console_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(console_handler)

DEFAULT_INTERFACE='wlan0'

def broadcast_hostname(interface=DEFAULT_INTERFACE):
    mdns = MdnsService()

    try:
        # Get the IPV4 address of the specified interface
        addrs = netifaces.ifaddresses(interface)
        ip_info = addrs[netifaces.AF_INET]
        ip = ip_info[0]['addr']

        logger.info(f"Broadcasting hostname at {ip} using interface {interface}")

        mdns.add_record("tdmx", ip, 80)
        while True:
            pass
    except Exception as e:
        logger.exception(e)
        sys.exit(1)
    finally:
        mdns.close()
    
    logger.info("Terminating hostname broadcast service.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        interface = sys.argv[1]
    else:
        interface = DEFAULT_INTERFACE
    broadcast_hostname(interface)