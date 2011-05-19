import unittest
from pytoad.environment import Environment

class TestEnvironment(unittest.TestCase):
    
    def test_environment_loads_properties_from_json_configuration(self):
        environment = Environment()
        self.assertEqual(environment.name, "Fake Name")