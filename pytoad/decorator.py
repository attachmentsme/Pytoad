from pytoad import Connection

def pytoad_decorator(monitored_exceptions=[], PytoadConnectionClass=Connection):
    monitored_exceptions = tuple(monitored_exceptions) or Exception
    def wrap(f):
        def wrapped_f(*args, **kwargs):
            try:
                f(*args, **kwargs)
            except monitored_exceptions, e:
                connection = PytoadConnectionClass()
                connection.send_to_hoptoad(e)
        return wrapped_f
    return wrap
