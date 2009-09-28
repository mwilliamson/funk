from nose.tools import assert_equals

from funk.matchers import any_value
from funk.matchers import is_a
from funk.matchers import has_attr
from funk.matchers import equal_to
from funk.matchers import not_

def test_any_value_matches_everything():
    assert any_value().matches("foo", [])
    assert any_value().matches(1, [])
    assert any_value().matches(type, [])

def test_any_value_str():
    assert_equals(str(any_value()), "<any value>")

def test_any_value_does_not_write_to_mismatch_output():
    mismatch_output = []
    any_value().matches("foo", mismatch_output)
    any_value().matches(1, mismatch_output)
    any_value().matches(type, mismatch_output)
    assert not mismatch_output

def test_is_a_matches_on_type():
    assert is_a(type).matches(basestring, [])
    assert is_a(basestring).matches("foo", [])
    assert not is_a(basestring).matches(4, [])

def test_is_a_str_shows_type():
    class SomeClass(object):
        pass
    assert_equals(str(is_a(SomeClass)), "<value of type: test.funk.test_matchers.SomeClass>")

def test_is_a_does_not_write_to_mismatch_output_if_it_matches():
    mismatch_output = []
    assert is_a(type).matches(basestring, mismatch_output)
    assert is_a(basestring).matches("foo", mismatch_output)
    assert not mismatch_output
    
def test_is_a_writes_type_of_value_if_it_does_not_match():
    class SomeClass(object):
        pass
    mismatch_output = []
    is_a(basestring).matches(SomeClass(), mismatch_output)
    assert_equals(["got <value of type: test.funk.test_matchers.SomeClass>"], mismatch_output)

def test_is_a_does_not_show_module_if_type_is_builtin():
    assert_equals("<value of type: int>", str(is_a(int)))

def test_has_attr_matches_on_attributes():
    class Rectangle(object):
        def __init__(self, width, height):
            self.width = width
            self.height = height
            
    matcher = has_attr(width=40, height=20)
    
    assert matcher.matches(Rectangle(40, 20), [])
    assert not matcher.matches(Rectangle(50, 20), [])
    assert not matcher.matches(Rectangle(40, 30), [])
    
def test_has_attr_str_contains_all_attributes():
    assert_equals(str(has_attr(what="else", key="word")), "<value with attributes: what=else, key=word>")

def test_has_attr_does_not_write_to_mismatch_output_if_values_match():
    class Rectangle(object):
        def __init__(self, width, height):
            self.width = width
            self.height = height
    mismatch_output = []
    assert has_attr(width=20).matches(Rectangle(20, None), mismatch_output)
    assert has_attr(width=20, height=40).matches(Rectangle(20, 40), mismatch_output)

def test_has_attr_describes_actual_attributes_if_present():
    class Rectangle(object):
        def __init__(self, width, height):
            self.width = width
            self.height = height
    mismatch_output = []
    has_attr(width=20, height=40).matches(Rectangle(30, 50), mismatch_output)
    
    assert_equals(["got <value with attribute: width=30>"], mismatch_output)

def test_has_attr_will_describe_missing_attributes():
    mismatch_output = []
    has_attr(width=20).matches(None, mismatch_output)
    
    assert_equals(["value was missing attribute: width"], mismatch_output)

def test_equal_to_matches_on_equality():
    assert equal_to(1).matches(1, [])
    assert equal_to("Blah").matches("Blah", [])
    assert not equal_to(1).matches("Blah", [])
    assert not equal_to("Blah").matches(1, [])

def test_equal_to_str_uses_value_str():
    assert_equals(str(equal_to("Blah")), "Blah")

def test_equal_to_does_not_write_to_mismatch_output_if_it_matches():
    mismatch_output = []
    assert equal_to("durian").matches("durian", mismatch_output)
    assert equal_to(22).matches(22, mismatch_output)
    assert not mismatch_output

def test_equal_to_writes_str_of_non_matching_values_to_mismatch_output():
    mismatch_output = []
    equal_to("got: bananas").matches(44, mismatch_output)
    assert_equals(["44"], mismatch_output)

def test_not_negates_given_matcher():
    assert not not_(equal_to(1)).matches(1, [])
    assert not not_(equal_to("Blah")).matches("Blah", [])
    assert not_(equal_to(1)).matches("Blah", [])
    assert not_(equal_to("Blah")).matches(1, [])

def test_not_to_str_prefixes_not_to_matcher_description():
    assert_equals(str(not_(equal_to("Blah"))), "not Blah")

def test_not_does_not_write_to_mismatch_output_if_it_matches():
    mismatch_output = []
    assert not_(equal_to(1)).matches("Blah", mismatch_output)
    assert not_(equal_to("Blah")).matches(1, mismatch_output)
    assert not mismatch_output

def test_not_writes_matcher_as_mismatch_description():
    mismatch_output = []
    not_(equal_to("Blah")).matches("Blah", mismatch_output)
    assert_equals(['got value matching: Blah'], mismatch_output)
