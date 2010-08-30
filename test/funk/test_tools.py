from nose.tools import assert_raises
from nose.tools import assert_equals

from funk.tools import assert_raises_str
from funk.tools import assert_that
from funk.tools import value_object
from funk.matchers import Matcher

def test_assert_raises_str_passes_if_test_raises_specified_exception_with_correct_message():
    def func():
        raise AssertionError("Oh noes!")
    assert_raises_str(AssertionError, "Oh noes!", func)
    
def test_assert_raises_str_passed_if_test_raises_subtype_of_specified_exception_with_correct_message():
    def func():
        raise AssertionError("Oh noes!")
    assert_raises_str(BaseException, "Oh noes!", func)
    
def test_assert_raises_str_fails_if_wrong_exception_raised():
    def func():
        raise TypeError("Oh noes!")
    assert_raises(TypeError, lambda: assert_raises_str(KeyError, "Oh noes!", func))

def test_assert_raises_str_fails_if_no_exception_raised():
    assert_raises(AssertionError, lambda: assert_raises_str(TypeError, "Oh noes!", lambda: None))

def test_assert_raises_str_fails_if_messages_do_not_match():
    def func():
        raise TypeError("Oh dear.")
    assert_raises(AssertionError, lambda: assert_raises_str(TypeError, "Oh noes!", func))

def test_assert_raises_str_can_take_arguments_for_function_under_test():
    def func(name, number):
        if name == "Sir Galahad" and number == 42:
            raise RuntimeError("Look out!")
            
    assert_raises(RuntimeError, lambda: assert_raises_str(TypeError, "Oh noes!", func, "Sir Galahad", number=42))

def test_assert_that_passes_if_matcher_returns_true():
    class TrueMatcher(Matcher):
        def matches(self, value, failure_out):
            return True
            
    assert_that("Anything", TrueMatcher())

def test_assert_that_raises_assertion_error_if_matcher_returns_false():
    class FalseMatcher(Matcher):
        def matches(self, value, failure_out):
            return False
            
    assert_raises(AssertionError, lambda: assert_that("Anything", FalseMatcher()))

def test_assert_that_raises_assertion_error_describing_expected_and_actual_results():
    class HasZeroLength(Matcher):
        def matches(self, value, failure_out):
            if len(value):
                failure_out.append("got <value of length %s>" % len(value))
                return False
            
            return True
            
        def __str__(self):
            return "<value of length zero>"
            
    assert_that([], HasZeroLength())
    assert_raises_str(AssertionError, 
                      "Expected: <value of length zero>\nbut: got <value of length 8>",
                      lambda: assert_that("Anything", HasZeroLength()))

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
