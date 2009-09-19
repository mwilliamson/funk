from functools import wraps

__all__ = ['with_context']

class Context(object):
    def fake(self):
        return Fake()

class Fake(object):
    def __init__(self):
        self._provided_calls = ProvidedCalls()
    
    def provides(self, method_name):
        return self._provided_calls.add(method_name)
    
    def has_attr(self, **kwargs):
        for kwarg in kwargs:
            setattr(self, kwarg, kwargs[kwarg])
            
    def __getattribute__(self, name):
        my = lambda name: object.__getattribute__(self, name)
        provided_calls = my('_provided_calls')
        if name in provided_calls:
            return provided_calls.for_name(name)
        return my(name)

class ProvidedCalls(object):
    def __init__(self):
        self._calls = []
    
    def accepts(self, name, args, kwargs):
        return any([call.accepts(name, args, kwargs) for call in self._calls])
    
    def add(self, method_name):
        call = Call(method_name)
        self._calls.append(call)
        return call
    
    def for_name(self, name):
        return ProvidedCallsForMethod(name, filter(lambda call: call.has_name(name), self._calls))
    
    def __contains__(self, name):
        return any([call.has_name(name) for call in self._calls])

class ProvidedCallsForMethod(object):
    def __init__(self, name, calls):
        self._name = name
        self._calls = calls
        
    def __call__(self, *args, **kwargs):
        for call in self._calls:
            if call.accepts(self._name, args, kwargs):
                return call(*args, **kwargs)
        
        args_str = list(args[:])
        args_str += ['%s=%s' % (key, kwargs[key]) for key in kwargs]
        raise AssertionError("Unexpected method call: %s(%s)" % (self._name, ', '.join(args_str)))

class Call(object):
    _return_value = None
    _allowed_args = None
    _allowed_kwargs = None
    
    def __init__(self, name):
        self._name = name
    
    def has_name(self, name):
        return self._name == name
    
    def accepts(self, name, args, kwargs):
        if self._name != name:
            return False
        if self._allowed_args is not None and self._allowed_args != args:
            return False
        if self._allowed_kwargs is not None and self._allowed_kwargs != kwargs:
            return False
        return True
    
    def __call__(self, *args, **kwargs):
        return self._return_value
    
    def with_args(self, *args, **kwargs):
        self._allowed_args = args
        self._allowed_kwargs = kwargs
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
