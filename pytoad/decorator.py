from pytoad import Connection

def pytoad_decorator(monitored_exceptions=[], PytoadConnectionClass=Connection):
    def wrap(f):
                
        def wrapped_f(*args, **kwargs):
            try:
                f( *args, **kwargs )
            except Exception, exception:
                
                exception_monitored = False
                
                if not monitored_exceptions:
                    exception_monitored = True

                for monitored_exception in monitored_exceptions:
                                        
                    if exception.__class__.__name__ == monitored_exception.__name__:
                        exception_monitored = True
                        break

                if exception_monitored:
                    connection = PytoadConnectionClass()
                    connection.send_to_hoptoad(exception)
                else:
                    raise exception
                
        return wrapped_f
        
    return wrap