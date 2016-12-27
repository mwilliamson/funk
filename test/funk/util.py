from nose.tools import assert_equals


def assert_raises_str(exception_type, expected_str, func):
    error = assert_raises(exception_type, func)
    assert_equals(expected_str, str(error))


def assert_raises(exception_type, func):
    try:
        func()
    except exception_type as error:
        return error
    else:
        raise AssertionError("Did not raise {0}".format(exception_type))
