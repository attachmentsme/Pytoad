from pytoad import Connection

def pytoad_decorator(monitored_exceptions=[], PytoadConnectionClass=Connection):
    def wrap(f):
        def wrapped_f(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception, e:
                if e.__class__ in monitored_exceptions or not monitored_exceptions:
                    connection = PytoadConnectionClass()
                    connection.send_to_hoptoad(e)
                else:
                    raise e
        return wrapped_f
    return wrap
