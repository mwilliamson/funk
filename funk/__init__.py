from functools import wraps
from funk.error import FunkyError
from funk.call import Call
from funk.call import IntegerCallCount
from funk.call import InfiniteCallCount

__all__ = ['with_context']

class Context(object):
    def fake(self, name='unnamed'):
        return Fake(name)

class Fake(object):
    def __init__(self, name):
        self._name = name
        self._mocked_calls = MockedCalls(name)
    
    def expects(self, method_name):
        return self._mocked_calls.add(method_name, IntegerCallCount(1))
    
    def provides(self, method_name):
        return self._mocked_calls.add(method_name, InfiniteCallCount())
    
    def has_attr(self, **kwargs):
        for kwarg in kwargs:
            setattr(self, kwarg, kwargs[kwarg])
            
    def __getattribute__(self, name):
        my = lambda name: object.__getattribute__(self, name)
        mocked_calls = my('_mocked_calls')
        if name in mocked_calls:
            return mocked_calls.for_method(name)
        return my(name)

class MockedCalls(object):
    def __init__(self, fake_name):
        self._calls = []
        self._fake_name = fake_name
    
    def accepts(self, name, args, kwargs):
        return any([call.accepts(args, kwargs) for call in self.for_method(name)])
    
    def add(self, method_name, call_count):
        call = Call(method_name, call_count)
        self._calls.append(call)
        return call
    
    def for_method(self, name):
        method_calls = filter(lambda call: call.has_name(name), self._calls)
        return MockedCallsForMethod(name, method_calls, self._fake_name)
    
    def __contains__(self, name):
        return any([call.has_name(name) for call in self._calls])

class MockedCallsForMethod(object):
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

def with_context(test_function):
    @wraps(test_function)
    def test_function_with_context(*args, **kwargs):
        if 'context' in kwargs:
            raise FunkyError("context has already been set")
        kwargs['context'] = Context()
        test_function(*args, **kwargs)
    
    return test_function_with_context
