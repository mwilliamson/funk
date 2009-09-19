class Infinity(object):
    def __eq__(self, other):
        return isinstance(other, type(self))
        
    def __sub__(self, by):
        return self

class Call(object):
    _return_value = None
    _allowed_args = None
    _allowed_kwargs = None
    
    def __init__(self, name, call_count=Infinity()):
        self._name = name
        self._call_count = call_count
    
    def has_name(self, name):
        return self._name == name
    
    def accepts(self, args, kwargs):
        if self._call_count == 0:
            return False
        if self._allowed_args is not None and self._allowed_args != args:
            return False
        if self._allowed_kwargs is not None and self._allowed_kwargs != kwargs:
            return False
        return True
    
    def __call__(self, *args, **kwargs):
        self._call_count -= 1
        return self._return_value
    
    def with_args(self, *args, **kwargs):
        self._allowed_args = args
        self._allowed_kwargs = kwargs
        return self
    
    def returns(self, return_value):
        self._return_value = return_value
