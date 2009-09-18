from functools import wraps

__all__ = ['with_context']

class Context(object):
    def fake(self):
        return Fake()

class Fake(object):
    def __init__(self):
        self._provides = {}
    
    def provides(self, method_name):
        def accept_anything(*args, **kwargs):
            return None
        self._provides[method_name] = accept_anything
        return self
    
    def has_attr(self, **kwargs):
        for kwarg in kwargs:
            setattr(self, kwarg, kwargs[kwarg])
            
    def __getattribute__(self, name):
        my = lambda name: object.__getattribute__(self, name)
        if name in my('_provides'):
            return self._provides[name]
        return my(name)

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
