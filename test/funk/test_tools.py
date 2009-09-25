from nose.tools import assert_raises

from funk.tools import assert_raises_str

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
