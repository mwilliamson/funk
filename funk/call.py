from funk.error import FunkyError

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
    _return_value = None
    _allowed_args = None
    _allowed_kwargs = None
    
    def __init__(self, name, call_count=InfiniteCallCount()):
        self._name = name
        self._call_count = call_count
    
    def has_name(self, name):
        return self._name == name
    
    def accepts(self, args, kwargs):
        if self._call_count.none_remaining():
            return False
        if self._allowed_args is not None and self._allowed_args != args:
            return False
        if self._allowed_kwargs is not None and self._allowed_kwargs != kwargs:
            return False
        return True
    
    def __call__(self, *args, **kwargs):
        if self._call_count.none_remaining():
            raise FunkyError("")
        self._call_count.decrement()
        return self._return_value
    
    def with_args(self, *args, **kwargs):
        self._allowed_args = args
        self._allowed_kwargs = kwargs
        return self
    
    def returns(self, return_value):
        self._return_value = return_value

    def is_satisfied(self):
        return self._call_count.is_satisfied()
