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
