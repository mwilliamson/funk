from functools import wraps

__all__ = ['with_context']

class Context(object):
    def fake(self, name='unnamed'):
        return Fake(name)

class Fake(object):
    def __init__(self, name):
        self._name = name
        self._provided_calls = ProvidedCalls(name)
    
    def provides(self, method_name):
        return self._provided_calls.add(method_name)
    
    def has_attr(self, **kwargs):
        for kwarg in kwargs:
            setattr(self, kwarg, kwargs[kwarg])
            
    def __getattribute__(self, name):
        my = lambda name: object.__getattribute__(self, name)
        provided_calls = my('_provided_calls')
        if name in provided_calls:
            return provided_calls.for_method(name)
        return my(name)

class ProvidedCalls(object):
    def __init__(self, fake_name):
        self._calls = []
        self._fake_name = fake_name
    
    def accepts(self, name, args, kwargs):
        return any([call.accepts(args, kwargs) for call in self.for_method(name)])
    
    def add(self, method_name):
        call = Call(method_name)
        self._calls.append(call)
        return call
    
    def for_method(self, name):
        method_calls = filter(lambda call: call.has_name(name), self._calls)
        return ProvidedCallsForMethod(name, method_calls, self._fake_name)
    
    def __contains__(self, name):
        return any([call.has_name(name) for call in self._calls])

class ProvidedCallsForMethod(object):
    def __init__(self, name, calls, fake_name):
        self._name = name
        self._calls = calls
        self._fake_name = fake_name
        
    def __call__(self, *args, **kwargs):
        for call in self._calls:
            if call.accepts(args, kwargs):
                return call(*args, **kwargs)
        
        args_str = list(args[:])
        args_str += ['%s=%s' % (key, kwargs[key]) for key in kwargs]
        raise AssertionError("Unexpected method call: %s.%s(%s)" % (self._fake_name, self._name, ', '.join(args_str)))

class Call(object):
    _return_value = None
    _allowed_args = None
    _allowed_kwargs = None
    
    def __init__(self, name):
        self._name = name
    
    def has_name(self, name):
        return self._name == name
    
    def accepts(self, args, kwargs):
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
            raise FunkyError("context has already been set")
        kwargs['context'] = Context()
        test_function(*args, **kwargs)
    
    return test_function_with_context

class FunkyError(BaseException):
    def __init__(self, message):
        self.message = message
        
    def __str__(self):
        return self.message
