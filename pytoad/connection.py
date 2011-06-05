import sys, urllib2, traceback
from pytoad.environment import Environment
from xmlbuilder import XMLBuilder

class Connection(object):
        
    def __init__(self, use_ssl=True):
        self.use_ssl = use_ssl
        self.environment = Environment()
        self.hoptoad_url = self._get_hoptoad_url()
        
    def _get_hoptoad_url(self):
        if self.use_ssl:
            return "https://hoptoadapp.com/notifier_api/v2/notices"
        else:
            return "http://hoptoadapp.com/notifier_api/v2/notices"
        
    def send_to_hoptoad(self, exception):
        headers = { 'Content-Type': 'text/xml' }
        request = urllib2.Request(self.hoptoad_url, self._generate_xml(exception), headers)
        response = urllib2.urlopen(request)
        status = response.getcode()
        if status == 200:
            pass
        if status == 403:
            raise Exception("Cannot use SSL")
        if status == 422:
            raise Exception("Invalid XML sent to Hoptoad")
        if status == 500:
            raise Exception("Hoptoad has hopped the toad")

    def _generate_xml(self, exception):
        _,_,trace = sys.exc_info()
        
        xml = XMLBuilder()
        
        tb_dict = {}
        tb = traceback.extract_tb(trace)
        
        if tb:
            tb = tb[0]
            tb_dict['filename'] = tb[0]
            tb_dict['line_number'] = tb[1]
            tb_dict['function_name'] = tb[2]
        
        with xml.notice(version = 2.0):
            xml << ('api-key', self.environment.api_key)
            with xml.notifier:
                xml << ('name', self.environment.name)
                xml << ('version', self.environment.version)
                xml << ('url', self.environment.url)
            with xml('server-environment'):
                xml << ('environment-name', self.environment.environment_name)
            with xml.error:
                xml << ('class', exception.__class__.__name__)
                xml << ('message', str(exception))
                with xml.backtrace:
                    xml << ('line', {
                        'file':tb_dict.get('filename', 'unknown'),
                        'number':tb_dict.get('line_number', 'unknown'),
                        'method':tb_dict.get('function_name', 'unknown')
                    })
                
        return str(xml)