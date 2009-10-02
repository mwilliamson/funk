from nose.tools import assert_equals

def assert_raises_str(exception, message, function):
    passed = True
    try:
        function()
        passed = False
    except exception, e:
        assert_equals(message, str(e))
    if not passed:
        raise AssertionError("%s was not raised" % exception.__name__)

def assert_that(value, matcher):
    mismatch_output = []
    if not matcher.matches(value, mismatch_output):
        raise AssertionError("Expected: %s\nbut: %s" % (matcher, ''.join(mismatch_output)))

class ValueObject(object):
    def __init__(self, attributes):
        for key in attributes:
            setattr(self, key, attributes[key])

def value_object(**kwargs):
    return ValueObject(kwargs)
