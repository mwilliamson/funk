from nose.tools import assert_equals
import pytest


def assert_raises_str(exception_type, expected_str, func):
    exception_info = pytest.raises(exception_type, func)
    assert_equals(expected_str, str(exception_info.value))
