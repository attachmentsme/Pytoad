import unittest
from pytoad import Connection

class TestConnection(unittest.TestCase):
    
    def test_sane_xml_generated(self):
        connection = Connection()
        
        try:
            exception = Exception('test exception')
            raise exception
        except:
            pass
        
        xml = connection._generate_xml(exception)
                
        self.assertTrue("http://www.example.com" in xml)
        self.assertTrue("test_sane_xml_generated" in xml)