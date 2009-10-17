from functools import wraps
from funk.error import FunkyError
from funk.call import Call
from funk.call import IntegerCallCount
from funk.call import InfiniteCallCount
from funk.util import function_call_str

__all__ = ['with_context', 'Context', 'expects', 'allows', 'set_attr', 'expects_call', 'allows_call']

class Mock(object):
    def __init__(self, base, name):
        self._name = name
        self._mocked_calls = MockedCalls(base, name)
        
    def __getattribute__(self, name):
        my = lambda name: object.__getattribute__(self, name)
        mocked_calls = my('_mocked_calls')
        if name in mocked_calls:
            return mocked_calls.for_method(name)
        return my(name)
        
    def __call__(self, *args, **kwargs):
        return self._mocked_calls.for_self()(*args, **kwargs)
        
    def _verify(self):
        self._mocked_calls.verify()

class MockedCalls(object):
    def __init__(self, base, mock_name):
        self._base = base
        self._method_calls = []
        self._function_calls = []
        self._mock_name = mock_name
    
    def add_method_call(self, method_name, call_count):
        if self._base is not None:
            if not hasattr(self._base, method_name):
                raise AssertionError("Method '%s' is not defined on type object '%s'" % (method_name, self._base.__name__))
            if not callable(getattr(self._base, method_name)):
                raise AssertionError("Attribute '%s' is not callable on type object '%s'" % (method_name, self._base.__name__))
        call = Call(method_name, call_count)
        self._method_calls.append(call)
        return call
    
    def add_function_call(self, call_count):
        call = Call(self._mock_name, call_count)
        self._function_calls.append(call)
        return call
    
    def for_method(self, name):
        method_calls = filter(lambda call: call.has_name(name), self._method_calls)
        return MockedCallsForFunction("%s.%s" %(self._mock_name, name), method_calls)
    
    def for_self(self):
        return MockedCallsForFunction(self._mock_name, self._function_calls)
    
    def __contains__(self, name):
        return any([call.has_name(name) for call in self._method_calls])
        
    def verify(self):
        for call in self._method_calls:
            self._verify_call(call, "%s.%s" % (self._mock_name, call))
        for call in self._function_calls:
            self._verify_call(call, call)
                
    def _verify_call(self, call, name):
        if not call.is_satisfied():
            raise AssertionError("Not all expectations were satisfied. Expected call: %s" % name)

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

def with_context(test_function, mock_factory=None):
    @wraps(test_function)
    def test_function_with_context(*args, **kwargs):
        if 'context' in kwargs:
            raise FunkyError("context has already been set")
        context = Context(mock_factory)
        kwargs['context'] = context
        test_function(*args, **kwargs)
        context.verify()
    
    return test_function_with_context

class MethodArgumentsSetter(object):
    def __init__(self, call):
        self._call = call
    
    def __call__(self, *args, **kwargs):
        return self._call.with_args(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(self._call, name)

class ExpectationCreator(object):
    def __init__(self, expectation_setter):
        self._expectation_setter = expectation_setter
    
    def __getattribute__(self, name):
        my = lambda name: object.__getattribute__(self, name)
        return MethodArgumentsSetter(my('_expectation_setter')(name))

def expects(mock, method_name=None):
    if method_name is None:
        return ExpectationCreator(lambda method_name: expects(mock, method_name))
    return mock._mocked_calls.add_method_call(method_name, IntegerCallCount(1))

def allows(mock, method_name=None):
    if method_name is None:
        return ExpectationCreator(lambda method_name: allows(mock, method_name))
    return mock._mocked_calls.add_method_call(method_name, InfiniteCallCount())
    
def set_attr(mock, **kwargs):
    for kwarg in kwargs:
        setattr(mock, kwarg, kwargs[kwarg])

def expects_call(mock):
    return MethodArgumentsSetter(mock._mocked_calls.add_function_call(IntegerCallCount(1)))

def allows_call(mock):
    return MethodArgumentsSetter(mock._mocked_calls.add_function_call(InfiniteCallCount()))

class Context(object):
    def __init__(self, mock_factory=None):
        if mock_factory is None:
            mock_factory = Mock
        self._mocks = []
        self._mock_factory = mock_factory
    
    def mock(self, base=None, name='unnamed'):
        mock = self._mock_factory(base, name)
        self._mocks.append(mock)
        return mock
        
    def verify(self):
        for mock in self._mocks:
            mock._verify()
