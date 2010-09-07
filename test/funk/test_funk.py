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

@funk.with_context
def test_can_set_attributes_on_mock_objects(context):
    name = "the_blues"
    mock = context.mock()
    set_attr(mock, name=name)
    
    assert_equals(name, mock.name)
    assert_equals(name, mock.name)

@funk.with_context
def test_allowing_a_method_without_specifying_arguments_allows_method_to_be_called_no_times(context):
    mock = context.mock()
    allows(mock).save

@funk.with_context
def test_allowing_a_method_without_specifying_arguments_allows_method_to_be_called_any_times_with_any_arguments(context):
    return_value = "foo"
    
    mock = context.mock()
    allows(mock).save.returns(return_value)
    
    assert mock.save() is return_value
    assert mock.save(1, 2) is return_value
    assert mock.save() is return_value
    assert mock.save(name="Bob") is return_value

@funk.with_context
def test_can_specify_no_arguments_when_using_allows(context):
    return_value = "foo"
    
    mock = context.mock()
    allows(mock).save.with_args().returns(return_value)
    
    assert mock.save() is return_value
    assert_raises(UnexpectedInvocationError, lambda: mock.save("positional"))
    assert_raises(UnexpectedInvocationError, lambda: mock.save(key="word"))
    assert_raises(UnexpectedInvocationError, lambda: mock.save("one", "two", key="word", foo="bar"))
    assert mock.save() is return_value

@funk.with_context
def test_can_specify_arguments_using_equality_on_instances_when_using_allows(context):
    return_value = "foo"
    
    mock = context.mock()
    allows(mock).save.with_args("one", "two", key="word", foo="bar").returns(return_value)
    
    assert mock.save("one", "two", key="word", foo="bar") is return_value
    assert_raises(UnexpectedInvocationError, lambda: mock.save())
    assert_raises(UnexpectedInvocationError, lambda: mock.save("positional"))
    assert_raises(UnexpectedInvocationError, lambda: mock.save(key="word"))
    assert mock.save("one", "two", key="word", foo="bar") is return_value

@funk.with_context
def test_same_method_can_return_different_values_for_different_arguments_using_allows(context):
    return_foo = "foo"
    return_bar = "bar"
    
    mock = context.mock()
    allows(mock).save.with_args("one", "two", key="word", foo="bar").returns(return_foo)
    allows(mock).save.with_args("positional").returns(return_bar)
    
    assert mock.save("one", "two", key="word", foo="bar") is return_foo
    assert_raises(UnexpectedInvocationError, lambda: mock.save())
    assert mock.save("positional") is return_bar
    assert_raises(UnexpectedInvocationError, lambda: mock.save(key="word"))
    assert mock.save("one", "two", key="word", foo="bar") is return_foo
    
@funk.with_context
def test_unexpected_invocation_is_raised_if_method_is_defined_on_base_class(context):
    class UserRepository(object):
        def fetch_all(self):
            pass
    mock = context.mock(UserRepository)
    
    assert_raises(UnexpectedInvocationError, lambda: mock.fetch_all())
    
@funk.with_context
def test_no_expectations_listed_if_none_set(context):
    class UserRepository(object):
        def fetch_all(self):
            pass
    mock = context.mock(UserRepository)
    
    assert_raises_str(UnexpectedInvocationError,
"""Unexpected invocation: user_repository.fetch_all()
The following expectations on user_repository.fetch_all did not match:
    No expectations set.""",
                      lambda: mock.fetch_all())

@funk.with_context
def test_name_of_mock_is_used_in_exceptions_and_expectations_on_that_method_are_shown(context):
    unnamed = context.mock()
    named = context.mock(name='database')
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
    
@funk.with_context
def test_unexpected_invocations_display_method_name_and_parameters(context):
    class Database(object):
        def save(self):
            pass
            
    mock = context.mock(Database)
    allows(mock).save.with_args()
    
    assert_raises_str(UnexpectedInvocationError,
"""Unexpected invocation: database.save(positional)
The following expectations on database.save did not match:
    database.save() [wrong number of positional arguments]""",
                      lambda: mock.save("positional"))
    assert_raises_str(UnexpectedInvocationError,
"""Unexpected invocation: database.save(key=word)
The following expectations on database.save did not match:
    database.save() [unexpected keyword arguments: key]""",
                      lambda: mock.save(key="word"))
    assert_raises_str(UnexpectedInvocationError,
"""Unexpected invocation: database.save(one, two, foo=bar, key=word)
The following expectations on database.save did not match:
    database.save() [wrong number of positional arguments]""",
                      lambda: mock.save("one", "two", key="word", foo="bar"))
    
    mock = context.mock(Database)
    allows(mock).save.with_args(1)
    
    assert_raises_str(UnexpectedInvocationError,
"""Unexpected invocation: database.save()
The following expectations on database.save did not match:
    database.save(1) [wrong number of positional arguments]""",
                      lambda: mock.save())

@funk.with_context
def test_if_name_is_not_provided_type_is_converted_to_name_if_supplied(context):
    class UserRepository(object):
        def fetch_all(self):
            pass
    mock = context.mock(UserRepository)
    allows(mock).fetch_all()
    assert_raises_str(UnexpectedInvocationError,
"""Unexpected invocation: user_repository.fetch_all(2)
The following expectations on user_repository.fetch_all did not match:
    user_repository.fetch_all() [wrong number of positional arguments]""",
                      lambda: mock.fetch_all(2))

@funk.with_context
def test_expected_methods_can_be_called_once_with_any_arguments_if_no_arguments_specified(context):
    return_value = "Oh my!"
    mock = context.mock()
    expects(mock).save.returns(return_value)
    
    assert mock.save("positional", key="word") is return_value

@funk.with_context
def test_expected_methods_cannot_be_called_more_than_once(context):
    mock = context.mock()
    expects(mock).save.returns("Oh my!")
    
    mock.save("positional", key="word")
    
    assert_raises(UnexpectedInvocationError, lambda: mock.save("positional", key="word"))

@funk.with_context
def test_expected_methods_can_be_called_in_any_order(context):
    return_no_args = "Alone!"
    return_positional = "One is the loneliest number"
    
    mock = context.mock()
    expects(mock).save.with_args().returns(return_no_args)
    expects(mock).save.with_args("positional").returns(return_positional)
    
    assert mock.save("positional") is return_positional
    assert mock.save() is return_no_args
    
    assert_raises(UnexpectedInvocationError, lambda: mock.save("positional"))
    assert_raises(UnexpectedInvocationError, lambda: mock.save())

@funk.with_context
def test_mocks_can_raise_exceptions(context):
    mock = context.mock()
    expects(mock).save.raises(RuntimeError("Oh noes!"))
    assert_raises(RuntimeError, lambda: mock.save("anything"))

@funk.with_context
def test_method_expectations_are_used_in_the_order_they_are_defined(context):
    first = "One is the loneliest number"
    second = "Two can be as bad as one"
    mock = context.mock()
    expects(mock).save.returns(first)
    expects(mock).save.returns(second)
    
    assert mock.save() is first
    assert mock.save() is second
    
def test_function_raises_exception_if_expectations_are_not_satisfied():
    @funk.with_context
    def function(context):
        mock = context.mock()
        expects(mock).save
        
    assert_raises_str(AssertionError,
                      "Not all expectations were satisfied. Expected call: unnamed.save",
                      function)
def test_method_arguments_described_when_not_all_expectations_are_satisfied():
    @funk.with_context
    def function(context):
        mock = context.mock()
        expects(mock).save.with_args("positional", key="word")
        
    assert_raises_str(AssertionError,
                      "Not all expectations were satisfied. Expected call: unnamed.save('positional', key='word')",
                      function)

@funk.with_context
def test_mocks_can_expect_calls(context):
    return_value = "Hello!"
    mock = context.mock(name='save')
    assert_raises(UnexpectedInvocationError, mock)
    expects_call(mock).returns(return_value)
    assert mock() is return_value
    assert_raises(UnexpectedInvocationError, mock)
    assert_raises(UnexpectedInvocationError, lambda: mock("positional", key="word"))
    
@funk.with_context
def test_mocks_can_expect_calls_with_args(context):
    return_value = "Hello!"
    mock = context.mock(name='save')
    expects_call(mock).with_args("positional").returns(return_value)
    assert_raises(UnexpectedInvocationError, mock)
    assert_raises(UnexpectedInvocationError, lambda: mock("positional", key="word"))
    assert mock("positional") is return_value

@funk.with_context
def test_unexpected_calls_on_mocks_display_mock_name_and_parameters(context):
    return_value = "Hello!"
    mock = context.mock(name='save')
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
"""Unexpected invocation: save(positional, key=word)
The following expectations on save did not match:
    save [expectation has already been satisfied]""",
                      lambda: mock("positional", key="word"))
    
def test_function_raises_exception_if_expectations_of_calls_on_mock_are_not_satisfied():
    @funk.with_context
    def function(context):
        mock = context.mock()
        expects_call(mock)
        
    assert_raises_str(AssertionError,
                      "Not all expectations were satisfied. Expected call: unnamed",
                      function)

def test_function_arguments_described_when_not_all_expectations_are_satisfied():
    @funk.with_context
    def function(context):
        mock = context.mock()
        expects_call(mock).with_args("positional", key="word")
        
    assert_raises_str(AssertionError,
                      "Not all expectations were satisfied. Expected call: unnamed('positional', key='word')",
                      function)
    
@funk.with_context
def test_mocks_can_allow_calls(context):
    return_value = "Hello!"
    mock = context.mock(name='save')
    allows_call(mock).returns(return_value)
    assert mock() is return_value
    assert mock() is return_value
    mock("positional", key="word") is return_value

@funk.with_context
def test_mocks_can_allow_calls_with_args(context):
    return_value = "Hello!"
    mock = context.mock(name='save')
    allows_call(mock).with_args("positional").returns(return_value)
    
    assert mock("positional") is return_value
    
    assert_raises(UnexpectedInvocationError, mock)
    assert_raises(UnexpectedInvocationError, lambda: mock("positional", key="word"))

@funk.with_context
def test_can_use_expects_to_expect_call_with_the_same_syntax_that_it_will_be_called_with(context):
    to_save = "Let's go!"
    return_value = "Yippee!"
    database = context.mock()
    expects(database).save(to_save).returns(return_value)
    assert_raises(UnexpectedInvocationError, lambda: database.save())
    assert database.save(to_save) is return_value
    assert_raises(UnexpectedInvocationError, lambda: database.save(to_save))

@funk.with_context
def test_can_use_allows_to_allow_call_with_the_same_syntax_that_it_will_be_called_with(context):
    to_save = "Let's go!"
    return_value = "Yippee!"
    database = context.mock()
    allows(database).save(to_save).returns(return_value)
    assert_raises(UnexpectedInvocationError, lambda: database.save())
    assert database.save(to_save) is return_value
    assert database.save(to_save) is return_value

@funk.with_context
def test_can_expect_call_without_specifying_arguments_with_the_same_syntax_that_it_will_be_called_with(context):
    to_save = "Let's go!"
    return_value = "Yippee!"
    database = context.mock()
    expects(database).save.returns(return_value)
    assert database.save(to_save) is return_value
    assert_raises(UnexpectedInvocationError, lambda: database.save(to_save))
    
@funk.with_context
def test_can_allow_call_without_specifying_arguments_with_the_same_syntax_that_it_will_be_called_with(context):
    to_save = "Let's go!"
    return_value = "Yippee!"
    database = context.mock()
    allows(database).save.returns(return_value)
    assert database.save(to_save) is return_value
    assert database.save(to_save) is return_value
    assert database.save() is return_value

@funk.with_context
def test_can_expect_calls_with_the_same_syntax_that_it_will_be_called_with(context):
    to_print = "Hello, hello, hello, what's going on here then?"
    to_return = "There are four lights!"
    printer = context.mock()
    
    expects_call(printer)(to_print).returns(to_return)
    
    assert printer(to_print) is to_return
    
@funk.with_context
def test_can_allow_calls_with_the_same_syntax_that_it_will_be_called_with(context):
    to_print = "Hello, hello, hello, what's going on here then?"
    to_return = "There are four lights!"
    printer = context.mock()
    
    allows_call(printer)(to_print).returns(to_return)
    
    assert printer(to_print) is to_return

@funk.with_context
def test_sequences_do_not_raise_assertions_when_called_in_correct_order(context):
    log = context.mock()
    
    first_ordering = context.sequence()
    second_ordering = context.sequence()
    
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
    @funk.with_context
    def test_function(context):
        file = context.mock(name="file")
        ordering = context.sequence()
        expects(file).write("Private investigations").in_sequence(ordering)
        expects(file).close().in_sequence(ordering)
        
        file.close()
        file.write("Private investigations")
        
    assert_raises_str(AssertionError,
                      "Invocation out of order. Expected file.write('Private investigations'), but got file.close().",
                      test_function)

@funk.with_context
def test_using_allows_in_a_sequence_allows_it_to_be_called_no_times(context):
    file = context.mock()
    ordering = context.sequence()
    allows(file).write.in_sequence(ordering)
    expects(file).close().in_sequence(ordering)
    
    file.close()

@funk.with_context
def test_using_allows_in_a_sequence_allows_it_to_be_called_many_times(context):
    file = context.mock()
    ordering = context.sequence()
    allows(file).write.in_sequence(ordering)
    expects(file).close().in_sequence(ordering)
    
    file.write("Foo")
    file.write("Bar")
    file.write("Baz")
    file.close()
    
@funk.with_context
def test_calling_allowed_call_in_wrong_place_raises_assertion_error(context):
    file = context.mock()
    ordering = context.sequence()
    allows(file).write.in_sequence(ordering)
    expects(file).close().in_sequence(ordering)
    
    file.close()
    assert_raises_str(AssertionError,
                      'Invocation out of order. Expected no more calls in sequence, but got unnamed.write.',
                      lambda: file.write("Bar"))

@funk.with_context
def test_if_mock_is_based_on_a_class_then_can_only_expect_methods_defined_on_that_class(context):
    class Database(object):
        def save(self):
            pass
            
        status = False
    
    database = context.mock(Database)
    allows(database).save
    assert_raises_str(AssertionError, "Method 'delete' is not defined on type object 'Database'", lambda: allows(database).delete)
    assert_raises_str(AssertionError, "Attribute 'status' is not callable on type object 'Database'", lambda: allows(database).status)

@funk.with_context
def test_if_mock_is_based_on_a_class_then_can_also_expect_methods_defined_on_superclass(context):
    class Database(object):
        def save(self):
            pass
    
    class DeletingDatabase(Database):
        def delete(self):
            pass
    
    database = context.mock(DeletingDatabase)
    allows(database).save
    allows(database).delete

@funk.with_context
def test_can_use_matchers_instead_of_values_for_positional_arguments(context):
    class BlahMatcher(Matcher):
        def matches(self, other, failure_output):
            return other == "Blah"
            
    return_value = "Whoopee!"
    mock = context.mock()
    expects(mock).save.with_args(BlahMatcher()).returns(return_value)
    
    assert_raises(UnexpectedInvocationError, lambda: mock.save())
    assert_raises(UnexpectedInvocationError, lambda: mock.save(key="word"))
    assert_raises(UnexpectedInvocationError, lambda: mock.save("positional"))
    assert_raises(UnexpectedInvocationError, lambda: mock.save("positional", key="word"))
    
    assert mock.save("Blah") is return_value
    
@funk.with_context
def test_can_use_matchers_instead_of_values_for_keyword_arguments(context):
    class BlahMatcher(Matcher):
        def matches(self, other, failure_output):
            return other == "Blah"
            
    return_value = "Whoopee!"
    mock = context.mock()
    expects(mock).save.with_args(value=BlahMatcher()).returns(return_value)
    
    assert_raises(UnexpectedInvocationError, lambda: mock.save())
    assert_raises(UnexpectedInvocationError, lambda: mock.save(key="word"))
    assert_raises(UnexpectedInvocationError, lambda: mock.save("positional"))
    assert_raises(UnexpectedInvocationError, lambda: mock.save("positional", key="word"))
    
    assert mock.save(value="Blah") is return_value

def test_calling_function_wrapped_in_with_context_raises_exception_if_context_already_set():
    @funk.with_context
    def some_function(context):
        pass
        
    assert_raises(FunkyError, lambda: some_function(context=None))

@funk.with_context
def test_can_mock_methods_used_internally_by_mock(context):
    mock = context.mock()
    
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
    
    based_mock = context.mock(UserRepository)
    allows(based_mock)._base
    
