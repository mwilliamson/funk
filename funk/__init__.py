from functools import wraps

__all__ = ['with_context']

class Context(object):
    def fake(self):
        return Fake()

class Fake(object):
    def __init__(self):
        self._provides = {}
    
    def provides(self, method_name):
        call = Call(method_name)
        self._provides[method_name] = call
        return call
    
    def has_attr(self, **kwargs):
        for kwarg in kwargs:
            setattr(self, kwarg, kwargs[kwarg])
            
    def __getattribute__(self, name):
        my = lambda name: object.__getattribute__(self, name)
        if name in my('_provides'):
            return self._provides[name]
        return my(name)

class Call(object):
    _return_value = None
    _allowed_args = None
    _allowed_kwargs = None
    
    def __init__(self, name):
        self._name = name
    
    def __call__(self, *args, **kwargs):
        if self._allowed_args is not None and self._allowed_args != list(args) or self._allowed_kwargs is not None and self._allowed_kwargs != kwargs:
            args_str = list(args[:])
            args_str += ['%s=%s' % (key, kwargs[key]) for key in kwargs]
            raise AssertionError("Unexpected method call: %s(%s)" % (self._name, ', '.join(args_str)))
        
        return self._return_value
    
    def with_args(self):
        self._allowed_args = []
        self._allowed_kwargs = {}
        return self
    
    def returns(self, return_value):
        self._return_value = return_value

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
