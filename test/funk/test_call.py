from nose.tools import assert_raises

from funk.error import FunkyError
from funk.call import Call
from funk.call import IntegerCallCount

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
    assert_raises(FunkyError, call)

def test_is_satisfied_if_called_as_many_times_as_initial_call_count():
    call = Call('save', IntegerCallCount(2))
    assert not call.is_satisfied()
    call()
    assert not call.is_satisfied()
    call()
    assert call.is_satisfied()

def test_call_that_allows_any_number_of_calls_is_always_satisfied():
    call = Call('save')
    for x in range(0, 1000):
        assert call.is_satisfied()
        call()

