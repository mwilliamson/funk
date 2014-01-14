from . import pycompat
from .util import arguments_str


__all__ = ['any_value', 'is_a', 'has_attr', 'equal_to', 'not_', 'all_of',
           'any_of', 'is_', 'contains_exactly']

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
        module = value_type.__module__
        if module == pycompat.builtin_module_name:
            module_prefix = ''
        else:
            module_prefix = '%s.' % value_type.__module__
        return "<value of type: %s%s>" % (module_prefix, value_type.__name__)

def is_a(type_):
    return IsA(type_)

class HasAttr(Matcher):
    def __init__(self, attributes):
        self._attributes = {}
        for key, value in pycompat.iteritems(attributes):
            self._attributes[key] = self._to_matcher(value)
        
    def matches(self, value, mismatch_output):
        for key in sorted(pycompat.iterkeys(self._attributes)):
            if not hasattr(value, key):
                mismatch_output.append("value was missing attribute: %s" % key)
                return False
            attr_value = getattr(value, key)
            if not self._attributes[key].matches(attr_value, []):
                mismatch_output.append("got <value with attribute: %s=%s>" % (key, attr_value))
                return False
        return True
        
    def _to_matcher(self, value):
        if isinstance(value, Matcher):
            return value
        return equal_to(value)
        
    def __str__(self):
        return "<value with attributes: %s>" % arguments_str([], self._attributes)
    
def has_attr(**attributes):
    return HasAttr(attributes)

class EqualTo(Matcher):
    def __init__(self, value):
        self._value = value
        
    def matches(self, other, mismatch_output):
        if self._value != other:
            mismatch_output.append("got %s" % repr(other))
            return False
        return True
        
    def __str__(self):
        return repr(self._value)
        
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
    
class Is(Matcher):
    def __init__(self, value):
        self._value = value
        
    def matches(self, other, mismatch_output):
        if self._value is not other:
            mismatch_output.append("got: %s" % (other, ))
            return False
        return True
        
    def __str__(self):
        return "<is: %s>" % (str(self._value), )
        
def is_(value):
    return Is(value)

def _is_iterable(value):
    try:
        iter(value)
        return True
    except TypeError:
        return False

class ContainsExactly(Matcher):
    def __init__(self, matchers):
        self._matchers = matchers
        
    def matches(self, original, mismatch_output):
        if not _is_iterable(original):
            mismatch_output.append("was not iterable %s" % (self._got_str(original), ))
            return False
        other = list(original)
        for matcher in self._matchers:
            matched = False
            for index, element in enumerate(other):
                if matcher.matches(element, []):
                    matched = True
                    other.pop(index)
                    break
            if not matched:
                mismatch_output.append("iterable did not contain element: %s %s" % (matcher, self._got_str(original)))
                return False
        if len(other) > 0:
            mismatch_output.append("iterable contained extra elements: %s %s" % (", ".join(map(repr, other)), self._got_str(original)))
            return False
        return True
    
    def _got_str(self, original):
        return "(got: %s)" % (repr(original), )
    
    def __str__(self):
        return "<iterable containing exactly: %s>" % (", ".join(map(str, self._matchers)), )

def contains_exactly(*matchers):
    return ContainsExactly(map(to_matcher, matchers))

def to_matcher(value):
    if isinstance(value, Matcher):
        return value
    return equal_to(value)
