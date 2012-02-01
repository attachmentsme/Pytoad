import unittest
from pytoad import pytoad_decorator
from pytoad import Connection

class MockPytoadConnection(Connection):
    
    exceptions = []
    
    def send_to_hoptoad(self, exception):
        self.exceptions.append( exception )

class TestDecorator(unittest.TestCase):

    def test_decorator_catches_all_exceptions_by_default(self):
        
        MockPytoadConnection.exceptions = []
        
        @pytoad_decorator(PytoadConnectionClass=MockPytoadConnection)
        def foobar():
            raise Exception('banana')
        
        foobar()
        
        self.assertTrue( MockPytoadConnection.exceptions )
        
    def test_decorated_functions_return(self):
        
        MockPytoadConnection.exceptions = []
        
        @pytoad_decorator(PytoadConnectionClass=MockPytoadConnection)
        def foobar():
            return 'foobar'
                
        self.assertEqual( foobar(), 'foobar' )
    
    def test_decorator_catches_only_monitored_exceptions_if_provided(self):
        
        MockPytoadConnection.exceptions = []
        
        @pytoad_decorator(monitored_exceptions=[BaseException], PytoadConnectionClass=MockPytoadConnection)
        def foobar():
            raise Exception('banana')
        
        exception_occurred = False
        try:
            foobar()
        except:
            exception_occurred = True
        
        self.assertTrue( exception_occurred )
        self.assertFalse( MockPytoadConnection.exceptions )
        
    def test_decorator_catches_multiple_monitored_exceptions(self):
        MockPytoadConnection.exceptions = []
        
        @pytoad_decorator(monitored_exceptions=[StandardError, LookupError], PytoadConnectionClass=MockPytoadConnection)
        def foo():
            raise StandardError('banana')
            
        @pytoad_decorator(monitored_exceptions=[StandardError, LookupError], PytoadConnectionClass=MockPytoadConnection)
        def bar():
            raise LookupError('apple')
        
        foo()
        bar()
        
        self.assertEqual( len( MockPytoadConnection.exceptions ), 2 )