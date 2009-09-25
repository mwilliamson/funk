from funk.error import FunkyError
from funk.util import function_call_str
from funk.matchers import Matcher
from funk.matchers import equal_to

class InfiniteCallCount(object):
    def none_remaining(self):
        return False
        
    def decrement(self):
        pass
        
    def is_satisfied(self):
        return True

class IntegerCallCount(object):
    def __init__(self, count):
        self._count = count
    
    def none_remaining(self):
        return self._count <= 0
        
    def decrement(self):
        self._count -= 1
        
    def is_satisfied(self):
        return self.none_remaining()

class Call(object):
    _allowed_args = None
    _allowed_kwargs = None
    
    def __init__(self, name, call_count=InfiniteCallCount()):
        self._name = name
        self._call_count = call_count
        self._action = lambda: None
    
    def has_name(self, name):
        return self._name == name
    
    def accepts(self, args, kwargs):
        if self._call_count.none_remaining():
            return False
        if self._allowed_args is not None:
            if len(self._allowed_args) != len(args):
                return False
            if not all(map(lambda (matcher, arg): matcher.matches(arg, []), zip(self._allowed_args, args))):
                return False
        if self._allowed_kwargs is not None:
            if len(self._allowed_kwargs) != len(kwargs):
                return False
            for key in self._allowed_kwargs:
                if key not in kwargs:
                    return False
                if not self._allowed_kwargs[key].matches(kwargs[key], []):
                    return False
        return True
    
    def __call__(self, *args, **kwargs):
        if self._call_count.none_remaining():
            raise FunkyError("Cannot call any more times")
        if not self.accepts(args, kwargs):
            raise FunkyError("Called with wrong arguments")
        self._call_count.decrement()
        action = self._action
        return action()
    
    def with_args(self, *args, **kwargs):
        self._allowed_args = tuple(map(self._to_matcher, args))
        self._allowed_kwargs = dict([(key, self._to_matcher(kwargs[key])) for key in kwargs])
        return self
    
    def returns(self, return_value):
        self._action = lambda: return_value
        return self

    def raises(self, error):
        def action():
            raise error
        self._action = action
        return self

    def is_satisfied(self):
        return self._call_count.is_satisfied()

    def _to_matcher(self, value):
        if isinstance(value, Matcher):
            return value
        return equal_to(value)

    def __str__(self):
        if self._allowed_args is not None:
            return function_call_str(self._name, map(str, self._allowed_args), self._allowed_kwargs)
        return self._name
