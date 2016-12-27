from nose.tools import assert_equals

from funk.tools import value_object

def test_value_object_sets_attributes_to_passed_keyword_arguments():
    obj = value_object(width=20, height=40)
    assert_equals(obj.width, 20)
    assert_equals(obj.height, 40)

def test_value_object_str_shows_attributes():
    obj = value_object(width=20)
    assert_equals(str(obj), "<value_object: {'width': 20}>")

def test_value_object_str_shows_updated_attributes():
    obj = value_object(width=20)
    obj.width = 30
    assert_equals(str(obj), "<value_object: {'width': 30}>")

def test_value_object_repr_is_same_as_str():
    obj = value_object(width=20)
    assert_equals(repr(obj), "<value_object: {'width': 20}>")
