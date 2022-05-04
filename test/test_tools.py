from nose.tools import assert_equals
from precisely import assert_that, any_of, equal_to

from funk.tools import data

def test_value_object_sets_attributes_to_passed_keyword_arguments():
    obj = data(width=20, height=40)
    assert_equals(obj.width, 20)
    assert_equals(obj.height, 40)

def test_value_object_str_shows_attributes():
    obj = data(width=20, height=40)
    assert_that(str(obj), any_of(
        equal_to("Data(width=20, height=40)"),
        equal_to("Data(height=40, width=20)"),
    ))

def test_value_object_str_shows_updated_attributes():
    obj = data(width=20)
    obj.width = 30
    assert_equals(str(obj), "Data(width=30)")

def test_value_object_repr_is_same_as_str():
    obj = data(width=20)
    assert_equals(repr(obj), "Data(width=20)")
