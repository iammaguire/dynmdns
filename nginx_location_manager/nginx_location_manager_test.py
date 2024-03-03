import unittest
from unittest import mock
from nginx_location_manager.nginx import NginxLocationManager

class TestNginxLocationManager(unittest.TestCase):

    def setUp(self):
        self.manager = NginxLocationManager()

    @mock.patch("nginx_location_manager.nginx.os.system", return_value=0)
    def test_add_location(self, mock_system):
        # Add new test app
        self.manager.add_location("test_app", "http://localhost:5001")
        
        # Try adding test app again, expect ValueError
        with self.assertRaises(ValueError):
            self.manager.add_location("test_app", "http://localhost:5001")
        
        # Try adding test app with invalid address, expect ValueError
        with self.assertRaises(ValueError):
            self.manager.add_location("test_app_2", ":")

    @mock.patch("nginx_location_manager.nginx.os.system", return_value=0)
    def test_reload_nginx(self, mock_system):
        # Test whether nginx reload works
        try:
            self.manager.reload_nginx()
            # If there's no exception, pass the test
            pass
        except Exception as e:
            self.fail("Failed to reload nginx: " + str(e))


if __name__ == '__main__':
    unittest.main()