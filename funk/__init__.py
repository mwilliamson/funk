from functools import wraps

class Context(object):
    def fake(self):
        return None

def with_context(test_function):
    @wraps(test_function)
    def test_function_with_context(*args, **kwargs):
        if 'context' in kwargs:
            raise FunkException("context has already been set")
        kwargs['context'] = Context()
        test_function(*args, **kwargs)
    
    return test_function_with_context

class FunkException(BaseException):
    def __init__(self, message):
        self.message = message
        
    def __str__(self):
        return self.message
