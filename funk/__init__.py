from functools import wraps

class Context(object):
    def fake(self):
        return None

def with_context(test_function):
    @wraps(test_function)
    def test_function_with_context(*args, **kwargs):
        kwargs['context'] = Context()
        test_function(*args, **kwargs)
    
    return test_function_with_context
