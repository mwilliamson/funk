from functools import wraps
from funk.error import FunkyError
from funk.call import Call
from funk.call import IntegerCallCount
from funk.call import InfiniteCallCount
from funk.util import method_call_str
from funk.util import function_call_str

__all__ = ['with_context']

class Context(object):
    def __init__(self):
        self._fakes = []
    
    def fake(self, name='unnamed'):
        fake = Fake(name)
        self._fakes.append(fake)
        return fake
        
    def verify(self):
        for fake in self._fakes:
            fake._verify()

class Fake(object):
    def __init__(self, name):
        self._name = name
        self._mocked_calls = MockedCalls(name)
    
    def expects(self, method_name):
        return self._mocked_calls.add(method_name, IntegerCallCount(1))
    
    def provides(self, method_name):
        return self._mocked_calls.add(method_name, InfiniteCallCount())
    
    def expects_call(self):
        return self.expects(self)
    
    def has_attr(self, **kwargs):
        for kwarg in kwargs:
            setattr(self, kwarg, kwargs[kwarg])
            
    def __getattribute__(self, name):
        my = lambda name: object.__getattribute__(self, name)
        mocked_calls = my('_mocked_calls')
        if name in mocked_calls:
            return mocked_calls.for_method(name)
        return my(name)
        
    def __call__(self, *args, **kwargs):
        return self._mocked_calls.for_self(self)(*args, **kwargs)
        
    def _verify(self):
        self._mocked_calls.verify()

class MockedCalls(object):
    def __init__(self, fake_name):
        self._calls = []
        self._fake_name = fake_name
    
    def add(self, method_name, call_count):
        call = Call(method_name, call_count)
        self._calls.append(call)
        return call
    
    def for_self(self, fake):
        calls = filter(lambda call: call.has_name(fake), self._calls)
        return MockedCallsForFunction(self._fake_name, calls)
    
    def for_method(self, name):
        method_calls = filter(lambda call: call.has_name(name), self._calls)
        return MockedCallsForFunction("%s.%s" %(self._fake_name, name), method_calls)
    
    def __contains__(self, name):
        return any([call.has_name(name) for call in self._calls])
        
    def verify(self):
        for call in self._calls:
            if not call.is_satisfied():
                raise AssertionError("Not all expectations were satisfied. Expected call: %s.%s" % (self._fake_name, call))

class MockedCallsForFunction(object):
    def __init__(self, name, calls):
        self._name = name
        self._calls = calls
        
    def __call__(self, *args, **kwargs):
        for call in self._calls:
            if call.accepts(args, kwargs):
                return call(*args, **kwargs)
        
        call_str = function_call_str(self._name, args, kwargs)
        raise AssertionError("Unexpected invocation: %s" % call_str)

def with_context(test_function):
    @wraps(test_function)
    def test_function_with_context(*args, **kwargs):
        if 'context' in kwargs:
            raise FunkyError("context has already been set")
        context = Context()
        kwargs['context'] = context
        test_function(*args, **kwargs)
        context.verify()
    
    return test_function_with_context
