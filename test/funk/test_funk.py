from nose.tools import assert_raises
from nose.tools import assert_equals

import funk
from funk import FunkyError
from funk import expects
from funk import allows
from funk import set_attr
from funk import expects_call
from funk import allows_call
from funk.tools import assert_raises_str
from funk.matchers import Matcher
from funk import UnexpectedInvocationError

@funk.with_mocks
def test_can_set_attributes_on_mock_objects(mocks):
    name = "the_blues"
    mock = mocks.mock()
    set_attr(mock, name=name)
    
    assert_equals(name, mock.name)
    assert_equals(name, mock.name)

@funk.with_mocks
def test_allowing_a_method_without_specifying_arguments_allows_method_to_be_called_no_times(mocks):
    mock = mocks.mock()
    allows(mock).save

@funk.with_mocks
def test_allowing_a_method_without_specifying_arguments_allows_method_to_be_called_any_times_with_any_arguments(mocks):
    return_value = "foo"
    
    mock = mocks.mock()
    allows(mock).save.returns(return_value)
    
    assert mock.save() is return_value
    assert mock.save(1, 2) is return_value
    assert mock.save() is return_value
    assert mock.save(name="Bob") is return_value

@funk.with_mocks
def test_can_specify_no_arguments_when_using_allows(mocks):
    return_value = "foo"
    
    mock = mocks.mock()
    allows(mock).save.with_args().returns(return_value)
    
    assert mock.save() is return_value
    assert_raises(UnexpectedInvocationError, lambda: mock.save("positional"))
    assert_raises(UnexpectedInvocationError, lambda: mock.save(key="word"))
    assert_raises(UnexpectedInvocationError, lambda: mock.save("one", "two", key="word", foo="bar"))
    assert mock.save() is return_value

@funk.with_mocks
def test_can_specify_arguments_using_equality_on_instances_when_using_allows(mocks):
    return_value = "foo"
    
    mock = mocks.mock()
    allows(mock).save.with_args("one", "two", key="word", foo="bar").returns(return_value)
    
    assert mock.save("one", "two", key="word", foo="bar") is return_value
    assert_raises(UnexpectedInvocationError, lambda: mock.save())
    assert_raises(UnexpectedInvocationError, lambda: mock.save("positional"))
    assert_raises(UnexpectedInvocationError, lambda: mock.save(key="word"))
    assert mock.save("one", "two", key="word", foo="bar") is return_value

@funk.with_mocks
def test_same_method_can_return_different_values_for_different_arguments_using_allows(mocks):
    return_foo = "foo"
    return_bar = "bar"
    
    mock = mocks.mock()
    allows(mock).save.with_args("one", "two", key="word", foo="bar").returns(return_foo)
    allows(mock).save.with_args("positional").returns(return_bar)
    
    assert mock.save("one", "two", key="word", foo="bar") is return_foo
    assert_raises(UnexpectedInvocationError, lambda: mock.save())
    assert mock.save("positional") is return_bar
    assert_raises(UnexpectedInvocationError, lambda: mock.save(key="word"))
    assert mock.save("one", "two", key="word", foo="bar") is return_foo
    
@funk.with_mocks
def test_unexpected_invocation_is_raised_if_method_is_defined_on_base_class(mocks):
    class UserRepository(object):
        def fetch_all(self):
            pass
    mock = mocks.mock(UserRepository)
    
    assert_raises(UnexpectedInvocationError, lambda: mock.fetch_all())
    
@funk.with_mocks
def test_no_expectations_listed_if_none_set(mocks):
    class UserRepository(object):
        def fetch_all(self):
            pass
    mock = mocks.mock(UserRepository)
    
    assert_raises_str(UnexpectedInvocationError,
"""Unexpected invocation: user_repository.fetch_all()
The following expectations on user_repository.fetch_all did not match:
    No expectations set.""",
                      lambda: mock.fetch_all())

@funk.with_mocks
def test_name_of_mock_is_used_in_exceptions_and_expectations_on_that_method_are_shown(mocks):
    unnamed = mocks.mock()
    named = mocks.mock(name='database')
    allows(unnamed).save.with_args("positional")
    allows(named).save.with_args("positional")
    
    assert_raises_str(UnexpectedInvocationError,
"""Unexpected invocation: unnamed.save()
The following expectations on unnamed.save did not match:
    unnamed.save('positional') [wrong number of positional arguments]""",
                      lambda: unnamed.save())
    assert_raises_str(UnexpectedInvocationError,
"""Unexpected invocation: database.save()
The following expectations on database.save did not match:
    database.save('positional') [wrong number of positional arguments]""",
                      lambda: named.save())
    
@funk.with_mocks
def test_unexpected_invocations_display_method_name_and_parameters(mocks):
    class Database(object):
        def save(self):
            pass
            
    mock = mocks.mock(Database)
    allows(mock).save.with_args()
    
    assert_raises_str(UnexpectedInvocationError,
"""Unexpected invocation: database.save('positional')
The following expectations on database.save did not match:
    database.save() [wrong number of positional arguments]""",
                      lambda: mock.save("positional"))
    assert_raises_str(UnexpectedInvocationError,
"""Unexpected invocation: database.save(key='word')
The following expectations on database.save did not match:
    database.save() [unexpected keyword arguments: key]""",
                      lambda: mock.save(key="word"))
    assert_raises_str(UnexpectedInvocationError,
"""Unexpected invocation: database.save('one', 'two', foo='bar', key='word')
The following expectations on database.save did not match:
    database.save() [wrong number of positional arguments]""",
                      lambda: mock.save("one", "two", key="word", foo="bar"))
    
    mock = mocks.mock(Database)
    allows(mock).save.with_args(1)
    
    assert_raises_str(UnexpectedInvocationError,
"""Unexpected invocation: database.save()
The following expectations on database.save did not match:
    database.save(1) [wrong number of positional arguments]""",
                      lambda: mock.save())

@funk.with_mocks
def test_argument_mismatches_are_show_on_separate_lines(mocks):
    mock = mocks.mock(name="database")
    allows(mock).save("Apples", "Bananas")
    
    assert_raises_str(UnexpectedInvocationError,
"""Unexpected invocation: database.save('Apples', 'Peaches')
The following expectations on database.save did not match:
    database.save('Apples' [matched],
                  'Bananas' [got 'Peaches'])""",
                      lambda: mock.save("Apples", "Peaches"))

@funk.with_mocks
def test_if_name_is_not_provided_type_is_converted_to_name_if_supplied(mocks):
    class UserRepository(object):
        def fetch_all(self):
            pass
    mock = mocks.mock(UserRepository)
    allows(mock).fetch_all()
    assert_raises_str(UnexpectedInvocationError,
"""Unexpected invocation: user_repository.fetch_all(2)
The following expectations on user_repository.fetch_all did not match:
    user_repository.fetch_all() [wrong number of positional arguments]""",
                      lambda: mock.fetch_all(2))

@funk.with_mocks
def test_expected_methods_can_be_called_once_with_any_arguments_if_no_arguments_specified(mocks):
    return_value = "Oh my!"
    mock = mocks.mock()
    expects(mock).save.returns(return_value)
    
    assert mock.save("positional", key="word") is return_value

@funk.with_mocks
def test_expected_methods_cannot_be_called_more_than_once(mocks):
    mock = mocks.mock()
    expects(mock).save.returns("Oh my!")
    
    mock.save("positional", key="word")
    
    assert_raises(UnexpectedInvocationError, lambda: mock.save("positional", key="word"))

@funk.with_mocks
def test_expected_methods_can_be_called_in_any_order(mocks):
    return_no_args = "Alone!"
    return_positional = "One is the loneliest number"
    
    mock = mocks.mock()
    expects(mock).save.with_args().returns(return_no_args)
    expects(mock).save.with_args("positional").returns(return_positional)
    
    assert mock.save("positional") is return_positional
    assert mock.save() is return_no_args
    
    assert_raises(UnexpectedInvocationError, lambda: mock.save("positional"))
    assert_raises(UnexpectedInvocationError, lambda: mock.save())

@funk.with_mocks
def test_mocks_can_raise_exceptions(mocks):
    mock = mocks.mock()
    expects(mock).save.raises(RuntimeError("Oh noes!"))
    assert_raises(RuntimeError, lambda: mock.save("anything"))

@funk.with_mocks
def test_method_expectations_are_used_in_the_order_they_are_defined(mocks):
    first = "One is the loneliest number"
    second = "Two can be as bad as one"
    mock = mocks.mock()
    expects(mock).save.returns(first)
    expects(mock).save.returns(second)
    
    assert mock.save() is first
    assert mock.save() is second
    
def test_function_raises_exception_if_expectations_are_not_satisfied():
    @funk.with_mocks
    def function(mocks):
        mock = mocks.mock()
        expects(mock).save
        
    assert_raises_str(AssertionError,
                      "Not all expectations were satisfied. Expected call: unnamed.save",
                      function)
def test_method_arguments_described_when_not_all_expectations_are_satisfied():
    @funk.with_mocks
    def function(mocks):
        mock = mocks.mock()
        expects(mock).save.with_args("positional", key="word")
        
    assert_raises_str(AssertionError,
                      "Not all expectations were satisfied. Expected call: unnamed.save('positional', key='word')",
                      function)

@funk.with_mocks
def test_mocks_can_expect_calls(mocks):
    return_value = "Hello!"
    mock = mocks.mock(name='save')
    assert_raises(UnexpectedInvocationError, mock)
    expects_call(mock).returns(return_value)
    assert mock() is return_value
    assert_raises(UnexpectedInvocationError, mock)
    assert_raises(UnexpectedInvocationError, lambda: mock("positional", key="word"))
    
@funk.with_mocks
def test_mocks_can_expect_calls_with_args(mocks):
    return_value = "Hello!"
    mock = mocks.mock(name='save')
    expects_call(mock).with_args("positional").returns(return_value)
    assert_raises(UnexpectedInvocationError, mock)
    assert_raises(UnexpectedInvocationError, lambda: mock("positional", key="word"))
    assert mock("positional") is return_value

@funk.with_mocks
def test_unexpected_calls_on_mocks_display_mock_name_and_parameters(mocks):
    return_value = "Hello!"
    mock = mocks.mock(name='save')
    assert_raises_str(UnexpectedInvocationError,
"""Unexpected invocation: save()
The following expectations on save did not match:
    No expectations set.""",
                      mock)
    expects_call(mock).returns(return_value)
    mock()
    assert_raises_str(UnexpectedInvocationError,
"""Unexpected invocation: save()
The following expectations on save did not match:
    save [expectation has already been satisfied]""",
                      mock)
    assert_raises_str(UnexpectedInvocationError,
"""Unexpected invocation: save('positional', key='word')
The following expectations on save did not match:
    save [expectation has already been satisfied]""",
                      lambda: mock("positional", key="word"))
    
def test_function_raises_exception_if_expectations_of_calls_on_mock_are_not_satisfied():
    @funk.with_mocks
    def function(mocks):
        mock = mocks.mock()
        expects_call(mock)
        
    assert_raises_str(AssertionError,
                      "Not all expectations were satisfied. Expected call: unnamed",
                      function)

def test_function_arguments_described_when_not_all_expectations_are_satisfied():
    @funk.with_mocks
    def function(mocks):
        mock = mocks.mock()
        expects_call(mock).with_args("positional", key="word")
        
    assert_raises_str(AssertionError,
                      "Not all expectations were satisfied. Expected call: unnamed('positional', key='word')",
                      function)
    
@funk.with_mocks
def test_mocks_can_allow_calls(mocks):
    return_value = "Hello!"
    mock = mocks.mock(name='save')
    allows_call(mock).returns(return_value)
    assert mock() is return_value
    assert mock() is return_value
    mock("positional", key="word") is return_value

@funk.with_mocks
def test_mocks_can_allow_calls_with_args(mocks):
    return_value = "Hello!"
    mock = mocks.mock(name='save')
    allows_call(mock).with_args("positional").returns(return_value)
    
    assert mock("positional") is return_value
    
    assert_raises(UnexpectedInvocationError, mock)
    assert_raises(UnexpectedInvocationError, lambda: mock("positional", key="word"))

@funk.with_mocks
def test_can_use_expects_to_expect_call_with_the_same_syntax_that_it_will_be_called_with(mocks):
    to_save = "Let's go!"
    return_value = "Yippee!"
    database = mocks.mock()
    expects(database).save(to_save).returns(return_value)
    assert_raises(UnexpectedInvocationError, lambda: database.save())
    assert database.save(to_save) is return_value
    assert_raises(UnexpectedInvocationError, lambda: database.save(to_save))

@funk.with_mocks
def test_can_use_allows_to_allow_call_with_the_same_syntax_that_it_will_be_called_with(mocks):
    to_save = "Let's go!"
    return_value = "Yippee!"
    database = mocks.mock()
    allows(database).save(to_save).returns(return_value)
    assert_raises(UnexpectedInvocationError, lambda: database.save())
    assert database.save(to_save) is return_value
    assert database.save(to_save) is return_value

@funk.with_mocks
def test_can_expect_call_without_specifying_arguments_with_the_same_syntax_that_it_will_be_called_with(mocks):
    to_save = "Let's go!"
    return_value = "Yippee!"
    database = mocks.mock()
    expects(database).save.returns(return_value)
    assert database.save(to_save) is return_value
    assert_raises(UnexpectedInvocationError, lambda: database.save(to_save))
    
@funk.with_mocks
def test_can_allow_call_without_specifying_arguments_with_the_same_syntax_that_it_will_be_called_with(mocks):
    to_save = "Let's go!"
    return_value = "Yippee!"
    database = mocks.mock()
    allows(database).save.returns(return_value)
    assert database.save(to_save) is return_value
    assert database.save(to_save) is return_value
    assert database.save() is return_value

@funk.with_mocks
def test_can_expect_calls_with_the_same_syntax_that_it_will_be_called_with(mocks):
    to_print = "Hello, hello, hello, what's going on here then?"
    to_return = "There are four lights!"
    printer = mocks.mock()
    
    expects_call(printer)(to_print).returns(to_return)
    
    assert printer(to_print) is to_return
    
@funk.with_mocks
def test_can_allow_calls_with_the_same_syntax_that_it_will_be_called_with(mocks):
    to_print = "Hello, hello, hello, what's going on here then?"
    to_return = "There are four lights!"
    printer = mocks.mock()
    
    allows_call(printer)(to_print).returns(to_return)
    
    assert printer(to_print) is to_return

@funk.with_mocks
def test_sequences_do_not_raise_assertions_when_called_in_correct_order(mocks):
    log = mocks.mock()
    
    first_ordering = mocks.sequence()
    second_ordering = mocks.sequence()
    
    expects(log).write("You and your friend").in_sequence(first_ordering)
    expects(log).write("Love Over Gold").in_sequence(second_ordering)
    
    expects(log).close().in_sequence(first_ordering).in_sequence(second_ordering)
    
    allows(log).flush()
    
    log.flush()
    log.write("Love Over Gold")
    log.flush()
    log.write("You and your friend")
    log.flush()
    
    log.close()

def test_assertion_fails_if_calls_do_not_follow_sequence():
    @funk.with_mocks
    def test_function(mocks):
        file = mocks.mock(name="file")
        ordering = mocks.sequence()
        expects(file).write("Private investigations").in_sequence(ordering)
        expects(file).close().in_sequence(ordering)
        
        file.close()
        file.write("Private investigations")
        
    assert_raises_str(AssertionError,
                      "Invocation out of order. Expected file.write('Private investigations'), but got file.close().",
                      test_function)

@funk.with_mocks
def test_using_allows_in_a_sequence_allows_it_to_be_called_no_times(mocks):
    file = mocks.mock()
    ordering = mocks.sequence()
    allows(file).write.in_sequence(ordering)
    expects(file).close().in_sequence(ordering)
    
    file.close()

@funk.with_mocks
def test_using_allows_in_a_sequence_allows_it_to_be_called_many_times(mocks):
    file = mocks.mock()
    ordering = mocks.sequence()
    allows(file).write.in_sequence(ordering)
    expects(file).close().in_sequence(ordering)
    
    file.write("Foo")
    file.write("Bar")
    file.write("Baz")
    file.close()
    
@funk.with_mocks
def test_calling_allowed_call_in_wrong_place_raises_assertion_error(mocks):
    file = mocks.mock()
    ordering = mocks.sequence()
    allows(file).write.in_sequence(ordering)
    expects(file).close().in_sequence(ordering)
    
    file.close()
    assert_raises_str(AssertionError,
                      'Invocation out of order. Expected no more calls in sequence, but got unnamed.write.',
                      lambda: file.write("Bar"))

@funk.with_mocks
def test_if_mock_is_based_on_a_class_then_can_only_expect_methods_defined_on_that_class(mocks):
    class Database(object):
        def save(self):
            pass
            
        status = False
    
    database = mocks.mock(Database)
    allows(database).save
    assert_raises_str(AssertionError, "Method 'delete' is not defined on type object 'Database'", lambda: allows(database).delete)
    assert_raises_str(AssertionError, "Attribute 'status' is not callable on type object 'Database'", lambda: allows(database).status)

@funk.with_mocks
def test_if_mock_is_based_on_a_class_then_can_also_expect_methods_defined_on_superclass(mocks):
    class Database(object):
        def save(self):
            pass
    
    class DeletingDatabase(Database):
        def delete(self):
            pass
    
    database = mocks.mock(DeletingDatabase)
    allows(database).save
    allows(database).delete

@funk.with_mocks
def test_can_use_matchers_instead_of_values_for_positional_arguments(mocks):
    class BlahMatcher(Matcher):
        def matches(self, other, failure_output):
            return other == "Blah"
            
    return_value = "Whoopee!"
    mock = mocks.mock()
    expects(mock).save.with_args(BlahMatcher()).returns(return_value)
    
    assert_raises(UnexpectedInvocationError, lambda: mock.save())
    assert_raises(UnexpectedInvocationError, lambda: mock.save(key="word"))
    assert_raises(UnexpectedInvocationError, lambda: mock.save("positional"))
    assert_raises(UnexpectedInvocationError, lambda: mock.save("positional", key="word"))
    
    assert mock.save("Blah") is return_value
    
@funk.with_mocks
def test_can_use_matchers_instead_of_values_for_keyword_arguments(mocks):
    class BlahMatcher(Matcher):
        def matches(self, other, failure_output):
            return other == "Blah"
            
    return_value = "Whoopee!"
    mock = mocks.mock()
    expects(mock).save.with_args(value=BlahMatcher()).returns(return_value)
    
    assert_raises(UnexpectedInvocationError, lambda: mock.save())
    assert_raises(UnexpectedInvocationError, lambda: mock.save(key="word"))
    assert_raises(UnexpectedInvocationError, lambda: mock.save("positional"))
    assert_raises(UnexpectedInvocationError, lambda: mock.save("positional", key="word"))
    
    assert mock.save(value="Blah") is return_value

def test_calling_function_wrapped_in_with_mocks_raises_exception_if_mocks_already_set():
    @funk.with_mocks
    def some_function(mocks):
        pass
        
    assert_raises(FunkyError, lambda: some_function(mocks=None))

@funk.with_mocks
def test_can_mock_methods_used_internally_by_mock(mocks):
    mock = mocks.mock()
    
    expects(mock)._mocked_calls
    expects(mock).save()
    allows(mock)._mocked_calls
    allows(mock).save()
    expects_call(mock)
    allows_call(mock)
    
    mock._mocked_calls()
    mock.save()
    mock()
    
    class UserRepository(object):
        def _base(self):
            pass
    
    based_mock = mocks.mock(UserRepository)
    allows(based_mock)._base
    
