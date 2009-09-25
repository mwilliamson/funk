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
    failure_out = []
    if not matcher.matches(value, failure_out):
        raise AssertionError("Expected: %s\nbut got: %s" % (matcher, ''.join(failure_out)))
