from nose.tools import assert_equals

from funk.matchers import any_value
from funk.matchers import is_a
from funk.matchers import has_attr
from funk.matchers import equal_to

def test_any_value_matches_everything():
    assert any_value().matches("foo")
    assert any_value().matches(1)
    assert any_value().matches(type)

def test_any_value_str():
    assert_equals(str(any_value()), "<any value>")

def test_is_a_matches_on_type():
    assert is_a(type).matches(basestring)
    assert is_a(basestring).matches("foo")

def test_is_a_str_shows_type():
    class SomeClass(object):
        pass
    assert_equals(str(is_a(SomeClass)), "<type: test.funk.test_matchers.SomeClass>")

def test_has_attr_matches_on_attributes():
    class Rectangle(object):
        def __init__(self, width, height):
            self.width = width
            self.height = height
            
    matcher = has_attr(width=40, height=20)
    
    assert matcher.matches(Rectangle(40, 20))
    assert not matcher.matches(Rectangle(50, 20))
    assert not matcher.matches(Rectangle(40, 30))
    
def test_has_attr_str_contains_all_attributes():
    assert_equals(str(has_attr(what="else", key="word")), "<attributes: what=else, key=word>")

def test_equal_to_matches_on_equality():
    assert equal_to(1).matches(1)
    assert equal_to("Blah").matches("Blah")
    assert not equal_to(1).matches("Blah")
    assert not equal_to("Blah").matches(1)

def test_equal_to_str_uses_value_str():
    assert_equals(str(equal_to("Blah")), "Blah")
