from funk.util import arguments_str

__all__ = ['any_value', 'is_a', 'has_attr', 'equal_to']

class Matcher(object):
    pass

class AnyValue(Matcher):
    def matches(self, other):
        return True
        
    def __str__(self):
        return "<any value>"

def any_value():
    return AnyValue()

class IsA(Matcher):
    def __init__(self, type_):
        self._type = type_
        
    def matches(self, other):
        return isinstance(other, self._type)
        
    def __str__(self):
        return "<value of type: %s.%s>" % (self._type.__module__, self._type.__name__)

def is_a(type_):
    return IsA(type_)

class HasAttr(Matcher):
    def __init__(self, attributes):
        self._attributes = attributes
        
    def matches(self, other):
        return all((getattr(other, key) == self._attributes[key] for key in self._attributes))
        
    def __str__(self):
        return "<value with attributes: %s>" % arguments_str([], self._attributes)
    
def has_attr(**attributes):
    return HasAttr(attributes)

class EqualTo(Matcher):
    def __init__(self, value):
        self._value = value
        
    def matches(self, other):
        return self._value == other
        
    def __str__(self):
        return str(self._value)
        
def equal_to(value):
    return EqualTo(value)
