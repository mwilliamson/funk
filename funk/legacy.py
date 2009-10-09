from funk import with_context as base_with_context
from funk import Mock as BaseMock
from funk import expects
from funk import allows
from funk import expects_call
from funk import allows_call
from funk import set_attr

def with_context(test_function):
    return base_with_context(test_function, Mock)

class Mock(BaseMock):
    def expects(self, method_name):
        return expects(self, method_name)
    
    def allows(self, method_name):
        return allows(self, method_name)
    
    def expects_call(self):
        return expects_call(self)
    
    def allows_call(self):
        return allows_call(self)
    
    def set_attr(self, **kwargs):
        set_attr(self, **kwargs)
