from nose.tools import assert_raises

from funk.tools import assert_raises_str
from funk.tools import assert_that
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

def test_assert_that_passes_if_matcher_returns_true():
    class TrueMatcher(Matcher):
        def matches(self, value):
            return True
            
    assert_that("Anything", TrueMatcher())

def test_assert_that_raises_assertion_error_if_matcher_returns_false():
    class FalseMatcher(Matcher):
        def matches(self, value):
            return False
            
    assert_raises(AssertionError, lambda: assert_that("Anything", FalseMatcher()))

def test_assert_that_raises_assertion_error_describing_expected_and_actual_results():
    class FalseMatcher(Matcher):
        def matches(self, value):
            return False
            
        def __str__(self):
            return "<no possible value>"
            
    assert_raises_str(AssertionError, "Expected: <no possible value>\nbut got: Anything", lambda: assert_that("Anything", FalseMatcher()))
