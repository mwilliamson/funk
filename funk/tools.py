from nose.tools import assert_equals

def assert_raises_str(exception, message, function):
    try:
        function()
        raise AssertionError("%s was not raised" % exception)
    except exception, e:
        assert_equals(message, str(e))
