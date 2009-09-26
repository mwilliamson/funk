from funk.util import arguments_str

__all__ = ['any_value', 'is_a', 'has_attr', 'equal_to']

class Matcher(object):
    pass

class AnyValue(Matcher):
    def matches(self, value, mismatch_output):
        return True
        
    def __str__(self):
        return "<any value>"

def any_value():
    return AnyValue()

class IsA(Matcher):
    def __init__(self, type_):
        self._type = type_
        
    def matches(self, value, mismatch_output):
        if not isinstance(value, self._type):
            mismatch_output.append("got %s" % self._describe(type(value)))
            return False
        return True
        
    def __str__(self):
        return self._describe(self._type)
        
    def _describe(self, value_type):
        if value_type.__module__ == "__builtin__":
            module_prefix = ''
        else:
            module_prefix = '%s.' % value_type.__module__
        return "<value of type: %s%s>" % (module_prefix, value_type.__name__)

def is_a(type_):
    return IsA(type_)

class HasAttr(Matcher):
    def __init__(self, attributes):
        self._attributes = attributes
        
    def matches(self, value, mismatch_output):
        for key in self._attributes:
            if not hasattr(value, key):
                mismatch_output.append("value was missing attribute: %s" % key)
                return False
            attr_value = getattr(value, key)
            if attr_value != self._attributes[key]:
                mismatch_output.append("got <value with attribute: %s=%s>" % (key, attr_value))
                return False
        return True
        
    def __str__(self):
        return "<value with attributes: %s>" % arguments_str([], self._attributes)
    
def has_attr(**attributes):
    return HasAttr(attributes)

class EqualTo(Matcher):
    def __init__(self, value):
        self._value = value
        
    def matches(self, other, mismatch_output):
        if self._value != other:
            mismatch_output.append(str(other))
            return False
        return True
        
    def __str__(self):
        return str(self._value)
        
def equal_to(value):
    return EqualTo(value)
