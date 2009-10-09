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

@funk.with_context
def test_can_create_a_mock_object(context):
    mock = context.mock()

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
    assert_raises_str(AssertionError, "Unexpected invocation: unnamed.save(positional)", lambda: mock.save("positional"))
    assert_raises_str(AssertionError, "Unexpected invocation: unnamed.save(key=word)", lambda: mock.save(key="word"))
    assert_raises_str(AssertionError, "Unexpected invocation: unnamed.save(one, two, foo=bar, key=word)", lambda: mock.save("one", "two", key="word", foo="bar"))
    assert mock.save() is return_value

@funk.with_context
def test_can_specify_arguments_using_equality_on_instances_when_using_allows(context):
    return_value = "foo"
    
    mock = context.mock()
    allows(mock).save.with_args("one", "two", key="word", foo="bar").returns(return_value)
    
    assert mock.save("one", "two", key="word", foo="bar") is return_value
    assert_raises_str(AssertionError, "Unexpected invocation: unnamed.save()", lambda: mock.save())
    assert_raises_str(AssertionError, "Unexpected invocation: unnamed.save(positional)", lambda: mock.save("positional"))
    assert_raises_str(AssertionError, "Unexpected invocation: unnamed.save(key=word)", lambda: mock.save(key="word"))
    assert mock.save("one", "two", key="word", foo="bar") is return_value

@funk.with_context
def test_same_method_can_return_different_values_for_different_arguments_using_allows(context):
    return_foo = "foo"
    return_bar = "bar"
    
    mock = context.mock()
    allows(mock).save.with_args("one", "two", key="word", foo="bar").returns(return_foo)
    allows(mock).save.with_args("positional").returns(return_bar)
    
    assert mock.save("one", "two", key="word", foo="bar") is return_foo
    assert_raises_str(AssertionError, "Unexpected invocation: unnamed.save()", lambda: mock.save())
    assert mock.save("positional") is return_bar
    assert_raises_str(AssertionError, "Unexpected invocation: unnamed.save(key=word)", lambda: mock.save(key="word"))
    assert mock.save("one", "two", key="word", foo="bar") is return_foo

@funk.with_context
def test_name_of_mock_is_used_in_exceptions(context):
    unnamed = context.mock()
    named = context.mock(name='database')
    allows(unnamed).save.with_args("positional")
    allows(named).save.with_args("positional")
    
    assert_raises_str(AssertionError, "Unexpected invocation: unnamed.save()", lambda: unnamed.save())
    assert_raises_str(AssertionError, "Unexpected invocation: database.save()", lambda: named.save())

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
    
    assert_raises_str(AssertionError,
                      "Unexpected invocation: unnamed.save(positional, key=word)",
                      lambda: mock.save("positional", key="word"))

@funk.with_context
def test_expected_methods_can_be_called_in_any_order(context):
    return_no_args = "Alone!"
    return_positional = "One is the loneliest number"
    
    mock = context.mock()
    expects(mock).save.with_args().returns(return_no_args)
    expects(mock).save.with_args("positional").returns(return_positional)
    
    assert mock.save("positional") is return_positional
    assert mock.save() is return_no_args
    
    assert_raises_str(AssertionError,
                      "Unexpected invocation: unnamed.save(positional)",
                      lambda: mock.save("positional"))
                      
    assert_raises_str(AssertionError,
                      "Unexpected invocation: unnamed.save()",
                      lambda: mock.save())

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
                      "Not all expectations were satisfied. Expected call: unnamed.save(positional, key=word)",
                      function)

@funk.with_context
def test_mocks_can_expect_calls(context):
    return_value = "Hello!"
    mock = context.mock(name='save')
    assert_raises_str(AssertionError, "Unexpected invocation: save()", mock)
    expects_call(mock).returns(return_value)
    assert mock() is return_value
    assert_raises_str(AssertionError, "Unexpected invocation: save()", mock)
    assert_raises_str(AssertionError, "Unexpected invocation: save(positional, key=word)", lambda: mock("positional", key="word"))
    
@funk.with_context
def test_mocks_can_expect_calls_with_args(context):
    return_value = "Hello!"
    mock = context.mock(name='save')
    assert_raises_str(AssertionError, "Unexpected invocation: save()", mock)
    expects_call(mock).with_args("positional").returns(return_value)
    assert_raises_str(AssertionError, "Unexpected invocation: save()", mock)
    assert_raises_str(AssertionError, "Unexpected invocation: save(positional, key=word)", lambda: mock("positional", key="word"))
    assert mock("positional") is return_value
    
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
                      "Not all expectations were satisfied. Expected call: unnamed(positional, key=word)",
                      function)
    
@funk.with_context
def test_mocks_can_allow_calls(context):
    return_value = "Hello!"
    mock = context.mock(name='save')
    assert_raises_str(AssertionError, "Unexpected invocation: save()", mock)
    allows_call(mock).returns(return_value)
    assert mock() is return_value
    assert mock() is return_value
    mock("positional", key="word") is return_value

@funk.with_context
def test_mocks_can_allow_calls_with_args(context):
    return_value = "Hello!"
    mock = context.mock(name='save')
    assert_raises_str(AssertionError, "Unexpected invocation: save()", mock)
    allows_call(mock).with_args("positional").returns(return_value)
    
    assert mock("positional") is return_value
    
    assert_raises_str(AssertionError, "Unexpected invocation: save()", mock)
    assert_raises_str(AssertionError, "Unexpected invocation: save(positional, key=word)", lambda: mock("positional", key="word"))

@funk.with_context
def test_can_use_expects_to_expect_call_with_the_same_syntax_that_it_will_be_called_with(context):
    to_save = "Let's go!"
    return_value = "Yippee!"
    database = context.mock()
    expects(database).save(to_save).returns(return_value)
    assert_raises(AssertionError, lambda: database.save())
    assert database.save(to_save) is return_value
    assert_raises(AssertionError, lambda: database.save(to_save))

@funk.with_context
def test_can_use_allows_to_allow_call_with_the_same_syntax_that_it_will_be_called_with(context):
    to_save = "Let's go!"
    return_value = "Yippee!"
    database = context.mock()
    allows(database).save(to_save).returns(return_value)
    assert_raises(AssertionError, lambda: database.save())
    assert database.save(to_save) is return_value
    assert database.save(to_save) is return_value

@funk.with_context
def test_can_expect_call_without_specifying_arguments_with_the_same_syntax_that_it_will_be_called_with(context):
    to_save = "Let's go!"
    return_value = "Yippee!"
    database = context.mock()
    expects(database).save.returns(return_value)
    assert database.save(to_save) is return_value
    assert_raises(AssertionError, lambda: database.save(to_save))
    
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
    
    assert_raises(AssertionError, lambda: mock.save())
    assert_raises(AssertionError, lambda: mock.save(key="word"))
    assert_raises(AssertionError, lambda: mock.save("positional"))
    assert_raises(AssertionError, lambda: mock.save("positional", key="word"))
    
    assert mock.save("Blah") is return_value
    
@funk.with_context
def test_can_use_matchers_instead_of_values_for_keyword_arguments(context):
    class BlahMatcher(Matcher):
        def matches(self, other, failure_output):
            return other == "Blah"
            
    return_value = "Whoopee!"
    mock = context.mock()
    expects(mock).save.with_args(value=BlahMatcher()).returns(return_value)
    
    assert_raises(AssertionError, lambda: mock.save())
    assert_raises(AssertionError, lambda: mock.save(key="word"))
    assert_raises(AssertionError, lambda: mock.save("positional"))
    assert_raises(AssertionError, lambda: mock.save("positional", key="word"))
    
    assert mock.save(value="Blah") is return_value

def test_calling_function_wrapped_in_with_context_raises_exception_if_context_already_set():
    @funk.with_context
    def some_function(context):
        pass
        
    assert_raises(FunkyError, lambda: some_function(context=None))
