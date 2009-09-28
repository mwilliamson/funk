from nose.tools import assert_equals

from funk.matchers import any_value
from funk.matchers import is_a
from funk.matchers import has_attr
from funk.matchers import equal_to
from funk.matchers import not_
from funk.matchers import all_of
from funk.matchers import any_of

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

def test_all_of_passes_if_all_matchers_satisfied():
    class Rectangle(object):
        def __init__(self, width, height):
            self.width = width
            self.height = height
    
    class NotARectangle(object):
        def __init__(self, width):
            self.width = width
    
    matcher = all_of(is_a(Rectangle), has_attr(width=20))
    assert matcher.matches(Rectangle(20, 40), [])
    assert not matcher.matches(NotARectangle(20), [])
    assert not matcher.matches(Rectangle(30, 40), [])
    assert not matcher.matches("Rectangle", [])

def test_all_of_str_is_conjunction_of_passed_matchers():
    class Rectangle(object):
        pass
    is_a_rectangle = is_a(Rectangle)
    is_20_wide = has_attr(width=20)
    matcher = all_of(is_a_rectangle, is_20_wide)
    assert_equals("(%s) and (%s)" % (is_a_rectangle, is_20_wide), str(matcher))

def test_all_of_does_not_write_to_mismatch_output_if_it_matches():
    class Rectangle(object):
        def __init__(self, width, height):
            self.width = width
            self.height = height
    mismatch_description = []
    matcher = all_of(is_a(Rectangle), has_attr(width=20))
    assert matcher.matches(Rectangle(20, 40), mismatch_description)
    assert not mismatch_description

def test_all_of_describes_first_failing_match_if_match_fails():
    class Rectangle(object):
        pass
    
    expected_output = []
    is_a(Rectangle).matches("Rectangle", expected_output)
    
    mismatch_output = []
    matcher = all_of(any_value(), is_a(Rectangle), has_attr(width=20))
    matcher.matches("Rectangle", mismatch_output)
    assert_equals(expected_output, mismatch_output)

def test_any_of_passes_if_any_matchers_satisfied():
    class Rectangle(object):
        def __init__(self, width, height):
            self.width = width
            self.height = height
    
    class NotARectangle(object):
        def __init__(self, width):
            self.width = width
    
    matcher = any_of(is_a(Rectangle), has_attr(width=20))
    assert matcher.matches(Rectangle(20, 40), [])
    assert matcher.matches(NotARectangle(20), [])
    assert matcher.matches(Rectangle(30, 40), [])
    assert not matcher.matches("Rectangle", [])

def test_any_of_str_is_disjunction_of_passed_matchers():
    class Rectangle(object):
        pass
    is_a_rectangle = is_a(Rectangle)
    is_20_wide = has_attr(width=20)
    matcher = any_of(is_a_rectangle, is_20_wide)
    assert_equals("(%s) or (%s)" % (is_a_rectangle, is_20_wide), str(matcher))
    
def test_any_of_does_not_write_to_mismatch_output_if_it_matches():
    class Rectangle(object):
        def __init__(self, width, height):
            self.width = width
            self.height = height
    
    class NotARectangle(object):
        def __init__(self, width):
            self.width = width
            
    mismatch_description = []
    matcher = any_of(is_a(Rectangle), has_attr(width=20))
    assert matcher.matches(Rectangle(20, 40), mismatch_description)
    assert matcher.matches(NotARectangle(20), mismatch_description)
    assert matcher.matches(Rectangle(30, 40), mismatch_description)
    assert not mismatch_description

def test_any_of_describes_all_matchers_when_match_fails():
    class FalseMatcher(object):
        def __init__(self, description):
            self.description = description
            
        def matches(self, value, output):
            return False
            
        def __str__(self):
            return self.description
    
    expected_output = []
    is_a_rectangle = FalseMatcher("is a rectangle")
    is_a_rectangle.matches("Rectangle", expected_output)
    is_20_wide = FalseMatcher("is 20 wide")
    is_20_wide.matches("Rectangle", expected_output)
    expected_output = 'did not match any of: (is a rectangle), (is 20 wide)'
    
    mismatch_output = []
    matcher = any_of(is_a_rectangle, is_20_wide)
    matcher.matches("Rectangle", mismatch_output)
    assert_equals([expected_output], mismatch_output)
