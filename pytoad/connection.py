import sys, urllib2, traceback
from pytoad.environment import Environment
from xmlbuilder import XMLBuilder

class Connection(object):
    
    INSTANCE_VARIABLES = ['use_ssl', 'api_key', 'environment_name', 'name', 'version', 'url']
    TIMEOUT = 5
    
    def __init__(self, **kwargs):
        self.use_ssl = True
        self.logger = None
        self._load_instance_variables(kwargs)
        self._load_environment_variables()
        self.hoptoad_url = self._get_hoptoad_url()
    
    def _load_instance_variables(self, kwargs):
        for k, v in kwargs.items():
            if  k in self.INSTANCE_VARIABLES:
                self.__dict__[k] = v
                
    def _load_environment_variables(self):
        self.environment = Environment()
        for k in self.INSTANCE_VARIABLES:
            if not self.__dict__.get(k, None) and self.environment.__dict__.get(k, None):
                self.__dict__[k] = self.environment.__dict__[k]
        
    def _get_hoptoad_url(self):
        url_suffix = 'airbrake.io/notifier_api/v2/notices'
        if self.use_ssl:
            return "https://%s" % url_suffix
        else:
            return "http://%s" % url_suffix
        
    def send_to_hoptoad(self, exception, additional_information=None):
        try:
            headers = { 'Content-Type': 'text/xml' }
            request = urllib2.Request(self.hoptoad_url, self._generate_xml(exception, additional_information), headers)
            response = urllib2.urlopen(request, timeout=self.TIMEOUT)
            status = response.getcode()
            if status == 200:
                pass
            if status == 403:
                raise Exception("Cannot use SSL")
            if status == 422:
                raise Exception("Invalid XML sent to Hoptoad")
            if status == 500:
                raise Exception("Hoptoad has hopped the toad")
        except Exception, e:
            if self.logger:
                self.logger.warn(str(e))
            else:
                print str(e)
            
    def _generate_xml(self, exception, additional_information=None):
        _,_,trace = sys.exc_info()
        
        xml = XMLBuilder()
        
        tb_dict = {}
        tb = traceback.extract_tb(trace)
        
        if tb:
            tb = tb[0]
            tb_dict['filename'] = tb[0]
            tb_dict['line_number'] = tb[1]
            tb_dict['function_name'] = tb[2]
        
        message = str(exception)
        if additional_information:
            message = 'error: %s, additional info: %s' % (message, additional_information)
        
        with xml.notice(version = 2.0):
            xml << ('api-key', self.api_key)
            with xml.notifier:
                xml << ('name', self.name)
                xml << ('version', self.version)
                xml << ('url', self.url)
            with xml('server-environment'):
                xml << ('environment-name', self.environment_name)
            with xml.error:
                xml << ('class', exception.__class__.__name__)
                xml << ('message', message)
                with xml.backtrace:
                    xml << ('line', {
                        'file':tb_dict.get('filename', 'unknown'),
                        'number':tb_dict.get('line_number', 'unknown'),
                        'method':tb_dict.get('function_name', 'unknown')
                    })
                
        return str(xml)