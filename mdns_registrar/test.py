from MdnsService import MdnsService
from time import sleep

def test_MdnsService():
    # Create the mDNS Service instance
    mdns = MdnsService()

    # Test add_record method:
    try:
        mdns.add_record("test_app", "127.0.0.2", 8001)
        print("Test add_record: PASS")
    except Exception as e:
        print("Test add_record: FAIL")
        print(e)

    # Sleep for a bit to allow record to propagate if necessary
    sleep(5)

    # Test modify_record method:
    try:
        mdns.modify_record("test_app", "127.0.0.3", 8002)
        print("Test modify_record: PASS")
    except Exception as e:
        print("Test modify_record: FAIL")
        print(e)

    # Sleep for a bit to allow record to propagate if necessary
    sleep(5)

    # Test remove_record method:
    try:
        mdns.remove_record("test_app")
        print("Test remove_record: PASS")
    except Exception as e:
        print("Test remove_record: FAIL")
        print(e)

    # Clean up - close the mDNS Service instance
    mdns.close()  

if __name__ == "__main__":
    test_MdnsService()