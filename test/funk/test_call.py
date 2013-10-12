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
    except RuntimeError as e:
        assert e is error

def test_accepts_returns_true_if_with_args_not_called():
    call = Call('save')
    assert call.accepts((), {}, [])
    assert call.accepts((1, 2, 3), {"name": "Bob"}, [])

def test_accepts_returns_true_if_arguments_match_those_set_by_with_args():
    call = Call('save')
    call.with_args(1, 2, name="Bob")
    assert not call.accepts((), {}, [])
    assert not call.accepts((1, 2, 3), {"name": "Bob"}, [])
    assert not call.accepts((1, ), {"name": "Bob"}, [])
    assert call.accepts((1, 2), {"name": "Bob"}, [])

def test_accepts_returns_true_if_call_count_is_greater_than_zero():
    call = Call('save', IntegerCallCount(2))
    assert call.accepts([], {}, [])
    call()
    assert call.accepts([], {}, [])
    call()
    assert not call.accepts([], {}, [])

def test_not_specifying_call_count_allows_any_number_of_calls():
    call = Call('save')
    for x in range(0, 1000):
        assert call.accepts([], {}, [])
        call()

def test_error_is_raised_if_called_too_many_times():
    call = Call('save', IntegerCallCount(2))
    call()
    call()
    assert_raises_str(FunkyError, "Cannot call any more times", lambda: call())
    
def test_error_is_raised_if_called_with_wrong_arguments():
    call = Call('save')
    call.with_args("positional")
    call("positional")
    assert_raises_str(FunkyError, "Called with wrong arguments", lambda: call(["wrong"], {}))

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
    assert_equals("save('one', 'two', foo='bar', key='word')", str(call))

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
    
    assert call.accepts(["Blah"], {}, [])
    assert not call.accepts([], {}, [])
    assert not call.accepts([], {'key': 'word'}, [])
    assert not call.accepts(["positional"], {}, [])
    assert not call.accepts(["positional"], {'key': 'word'}, [])
    assert call("Blah") is return_value

def test_can_use_matchers_instead_of_values_for_keyword_arguments_when_using_with_args():
    class BlahMatcher(Matcher):
        def matches(self, other, failure_output):
            return other == "Blah"
            
    return_value = "Whoopee!"
    call = Call('save').with_args(value=BlahMatcher()).returns(return_value)
    
    assert call.accepts([], {'value': 'Blah'}, [])
    assert not call.accepts([], {}, [])
    assert not call.accepts([], {'key': 'word'}, [])
    assert not call.accepts(["positional"], {}, [])
    assert not call.accepts(["blah", "positional"], {}, [])
    assert not call.accepts(["positional"], {'key': 'word'}, [])
    assert not call.accepts([], {'key': 'word', 'value': 'Blah'}, [])
    assert call(value="Blah") is return_value

def test_calling_in_sequence_adds_call_to_sequence():
    class StubbedSequence(object):
        def __init__(self):
            self.calls = []
        
        def add_expected_call(self, call):
            self.calls.append(call)
        
    sequence = StubbedSequence()
    call = Call('save').in_sequence(sequence)
    assert_equals(sequence.calls, [call])

def test_calling_call_registers_call_with_sequences():
    class StubbedSequence(object):
        def __init__(self):
            self.expected_calls = []
            self.actual_calls = []
        
        def add_expected_call(self, call):
            self.expected_calls.append(call)
            
        def add_actual_call(self, call):
            self.actual_calls.append(call)
            
    first_sequence = StubbedSequence()
    second_sequence = StubbedSequence()
    call = Call('save').in_sequence(first_sequence)
    
    call()
    assert_equals(first_sequence.actual_calls, [call])

def test_mismatch_description_indicates_when_expectation_has_already_been_satisfied():
    call = Call('save', IntegerCallCount(1)).with_args()
    call()
    mismatch_description = []
    call.accepts([], {}, mismatch_description)
    assert_equals(''.join(mismatch_description), "save() [expectation has already been satisfied]")

def test_mismatch_description_indicates_when_number_of_positional_arguments_is_wrong():
    call = Call('save').with_args()
    mismatch_description = []
    call.accepts(["banana"], {}, mismatch_description)
    assert_equals(''.join(mismatch_description), "save() [wrong number of positional arguments]")

def test_mismatch_description_indicates_whether_positional_arguments_matched_or_not():
    call = Call('save').with_args("apple", "banana")
    mismatch_description = []
    call.accepts(["coconut", "banana"], {}, mismatch_description)
    assert_equals(''.join(mismatch_description), "save('apple' [got 'coconut'],\n     'banana' [matched])")

def test_mismatch_description_indicates_whether_keyword_argument_is_missing():
    call = Call('save').with_args(fruit="banana", vegetable="cucumber", salad="caesar")
    mismatch_description = []
    call.accepts([], {"fruit": "banana"}, mismatch_description)
    assert_equals(''.join(mismatch_description),
                  "save(fruit='banana', salad='caesar', vegetable='cucumber') [missing keyword arguments: salad, vegetable]")

def test_mismatch_description_indicates_whether_keyword_arguments_matched_or_not():
    call = Call('save').with_args(vegetable="cucumber", fruit="banana")
    mismatch_description = []
    call.accepts([], {"vegetable": "cucumber", "fruit": "coconut"}, mismatch_description)
    assert_equals(''.join(mismatch_description), "save(fruit='banana' [got 'coconut'],\n     vegetable='cucumber' [matched])")

def test_mismatch_description_shows_both_mismatching_positional_and_keyword_arguments():
    call = Call('save').with_args("eggs", "potatoes", vegetable="cucumber", fruit="banana")
    mismatch_description = []
    call.accepts(["duck", "potatoes"], {"vegetable": "cucumber", "fruit": "coconut"}, mismatch_description)
    assert_equals(''.join(mismatch_description),
                  "save('eggs' [got 'duck'],\n     'potatoes' [matched],\n     fruit='banana' [got 'coconut'],\n     vegetable='cucumber' [matched])")
