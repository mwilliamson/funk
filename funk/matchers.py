from funk.util import arguments_str

__all__ = ['any_value', 'is_a', 'has_attr', 'equal_to', 'not_', 'all_of', 'any_of']

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

class Not(Matcher):
    def __init__(self, matcher):
        self._matcher = matcher

    def matches(self, value, mismatch_output):
        if self._matcher.matches(value, []):
            mismatch_output.append('got value matching: %s' % self._matcher)
            return False
        return True

    def __str__(self):
        return "not %s" % self._matcher

def not_(matcher):
    return Not(matcher)

class AllOf(Matcher):
    def __init__(self, matchers):
        self._matchers = matchers
        
    def matches(self, value, mismatch_output):
        for matcher in self._matchers:
            if not matcher.matches(value, mismatch_output):
                return False
        return True
        
    def __str__(self):
        return _join_matchers(' and ', self._matchers)

def all_of(*matchers):
    return AllOf(matchers)
    
class AnyOf(Matcher):
    def __init__(self, matchers):
        self._matchers = matchers
        
    def matches(self, value, mismatch_output):
        if not any([matcher.matches(value, []) for matcher in self._matchers]):
            mismatch_output.append('did not match any of: %s' % _join_matchers(', ', self._matchers))
            return False
        return True
        
    def __str__(self):
        return _join_matchers(' or ', self._matchers)
    
def any_of(*matchers):
    return AnyOf(matchers)

def _join_matchers(glue, matchers):
    return glue.join(["(%s)" % matcher for matcher in matchers])
