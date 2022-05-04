from precisely import assert_that, equal_to


def assert_raises_str(exception_type, expected_str, func):
    error = assert_raises(exception_type, func)
    assert_that(str(error), equal_to(expected_str))


def assert_raises(exception_type, func):
    try:
        func()
    except exception_type as error:
        return error
    else:
        raise AssertionError("Did not raise {0}".format(exception_type))
