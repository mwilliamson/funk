from nose.tools import assert_equals

def assert_raises_str(exception, message, function, *args, **kwargs):
    passed = True
    try:
        function(*args, **kwargs)
        passed = False
    except exception as e:
        assert_equals(message, str(e))
    if not passed:
        raise AssertionError("%s was not raised" % exception.__name__)

def assert_that(value, matcher):
    mismatch_output = []
    if not matcher.matches(value, mismatch_output):
        raise AssertionError("Expected: %s\nbut: %s" % (matcher, ''.join(mismatch_output)))

class ValueObject(object):
    def __init__(self, attributes):
        self._keys = attributes.keys()
        for key in attributes:
            setattr(self, key, attributes[key])

    def __str__(self):
        attributes = {}
        for key in self._keys:
            attributes[key] = getattr(self, key)
        return "<value_object: %s>" % attributes
    
    def __repr__(self):
        return str(self)

def value_object(**kwargs):
    return ValueObject(kwargs)
