import os
import simplejson as json

class Environment(object):
    
    def __init__(self):
        self._load_environment()
    
    def _load_json_file(self, file_name):
        if os.path.exists(file_name):
            file = open(file_name, 'r')
            json_object = json.loads(file.read())
            file.close()
            return json_object
        return {}
    
    def _load_environment(self):
    
        config_directory = 'config/'
        if os.environ.has_key('PYTOAD_CONFIG_DIRECTORY'):
            config_directory = os.environ['PYTOAD_CONFIG_DIRECTORY']
        
        self.__dict__.update( self._load_json_file("%s/environment.default.json" % config_directory) )
        self.__dict__.update( self._load_json_file("%s/environment.json" % config_directory) )