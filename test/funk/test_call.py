from nose.tools import assert_equals
from funk.tools import assert_raises_str

from funk.error import FunkyError
from funk.call import Call
from funk.call import IntegerCallCount
from funk.matchers import Matcher

def test_has_name_returns_true_if_passed_name_matches_method_name():
    call = Call('save')
    assert call.has_name('save')
    assert not call.has_name('saved')
    assert not call.has_name('sav')

def test_returns_none_if_no_return_value_specified():
    call = Call('save')
    assert call() is None

def test_returns_return_value_if_set():
    return_value = 'Oh noes!'
    call = Call('save')
    call.returns(return_value)
    assert call() is return_value

def test_raises_exception_if_exception_given():
    error = RuntimeError("Boo!")
    call = Call('save').raises(error)
    try:
        call()
        raise AssertionError("Should have thrown RuntimeError")
    except RuntimeError, e:
        assert e is error

def test_accepts_returns_true_if_with_args_not_called():
    call = Call('save')
    assert call.accepts((), {})
    assert call.accepts((1, 2, 3), {"name": "Bob"})

def test_accepts_returns_true_if_arguments_match_those_set_by_with_args():
    call = Call('save')
    call.with_args(1, 2, name="Bob")
    assert not call.accepts((), {})
    assert not call.accepts((1, 2, 3), {"name": "Bob"})
    assert not call.accepts((1, ), {"name": "Bob"})
    assert call.accepts((1, 2), {"name": "Bob"})

def test_accepts_returns_true_if_call_count_is_greater_than_zero():
    call = Call('save', IntegerCallCount(2))
    assert call.accepts([], {})
    call()
    assert call.accepts([], {})
    call()
    assert not call.accepts([], {})

def test_not_specifying_call_count_allows_any_number_of_calls():
    call = Call('save')
    for x in range(0, 1000):
        assert call.accepts([], {})
        call()

def test_error_is_raised_if_called_too_many_times():
    call = Call('save', IntegerCallCount(2))
    call()
    call()
    assert_raises_str(FunkyError, "Cannot call any more times", call)
    
def test_error_is_raised_if_called_with_wrong_arguments():
    call = Call('save')
    call.with_args("positional")
    call("positional")
    assert_raises_str(FunkyError, "Called with wrong arguments", lambda: call("wrong"))

def test_is_satisfied_if_called_as_many_times_as_initial_call_count():
    call = Call('save', IntegerCallCount(2))
    assert not call.is_satisfied()
    call()
    assert not call.is_satisfied()
    call()
    assert call.is_satisfied()

def test_str_of_call_with_no_arguments_only_has_name_of_call():
    call = Call('save')
    assert_equals('save', str(call))

def test_str_of_call_with_arguments_shows_those_arguments():
    call = Call('save').with_args("one", "two", foo="bar", key="word")
    assert_equals('save(one, two, foo=bar, key=word)', str(call))

def test_call_that_allows_any_number_of_calls_is_always_satisfied():
    call = Call('save')
    for x in range(0, 1000):
        assert call.is_satisfied()
        call()
        
def test_can_use_matchers_instead_of_values_for_positional_arguments_when_using_with_args():
    class BlahMatcher(Matcher):
        def matches(self, other, failure_output):
            return other == "Blah"
            
    return_value = "Whoopee!"
    call = Call('save').with_args(BlahMatcher()).returns(return_value)
    
    assert call.accepts(["Blah"], {})
    assert not call.accepts([], {})
    assert not call.accepts([], {'key': 'word'})
    assert not call.accepts(["positional"], {})
    assert not call.accepts(["positional"], {'key': 'word'})
    assert call("Blah") is return_value

def test_can_use_matchers_instead_of_values_for_keyword_arguments_when_using_with_args():
    class BlahMatcher(Matcher):
        def matches(self, other, failure_output):
            return other == "Blah"
            
    return_value = "Whoopee!"
    call = Call('save').with_args(value=BlahMatcher()).returns(return_value)
    
    assert call.accepts([], {'value': 'Blah'})
    assert not call.accepts([], {})
    assert not call.accepts([], {'key': 'word'})
    assert not call.accepts(["positional"], {})
    assert not call.accepts(["blah", "positional"], {})
    assert not call.accepts(["positional"], {'key': 'word'})
    assert not call.accepts([], {'key': 'word', 'value': 'Blah'})
    assert call(value="Blah") is return_value
