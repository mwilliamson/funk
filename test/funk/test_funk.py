from nose.tools import assert_raises
from nose.tools import assert_equals

import funk
from funk import FunkyError
from funk.tools import assert_raises_str
from funk.matchers import Matcher

@funk.with_context
def test_can_create_a_mock_object(context):
    mock = context.mock()

@funk.with_context
def test_can_set_attributes_on_mock_objects(context):
    name = "the_blues"
    mock = context.mock()
    mock.has_attr(name=name)
    
    assert_equals(name, mock.name)
    assert_equals(name, mock.name)

@funk.with_context
def test_providing_a_method_without_specifying_arguments_allows_method_to_be_called_no_times(context):
    mock = context.mock()
    mock.provides('save')

@funk.with_context
def test_providing_a_method_without_specifying_arguments_allows_method_to_be_called_any_times_with_any_arguments(context):
    return_value = "foo"
    
    mock = context.mock()
    mock.provides('save').returns(return_value)
    
    assert mock.save() is return_value
    assert mock.save(1, 2) is return_value
    assert mock.save() is return_value
    assert mock.save(name="Bob") is return_value

@funk.with_context
def test_can_specify_no_arguments_when_using_provides(context):
    return_value = "foo"
    
    mock = context.mock()
    mock.provides('save').with_args().returns(return_value)
    
    assert mock.save() is return_value
    assert_raises_str(AssertionError, "Unexpected invocation: unnamed.save(positional)", lambda: mock.save("positional"))
    assert_raises_str(AssertionError, "Unexpected invocation: unnamed.save(key=word)", lambda: mock.save(key="word"))
    assert_raises_str(AssertionError, "Unexpected invocation: unnamed.save(one, two, foo=bar, key=word)", lambda: mock.save("one", "two", key="word", foo="bar"))
    assert mock.save() is return_value

@funk.with_context
def test_can_specify_arguments_using_equality_on_instances_when_using_provides(context):
    return_value = "foo"
    
    mock = context.mock()
    mock.provides('save').with_args("one", "two", key="word", foo="bar").returns(return_value)
    
    assert mock.save("one", "two", key="word", foo="bar") is return_value
    assert_raises_str(AssertionError, "Unexpected invocation: unnamed.save()", lambda: mock.save())
    assert_raises_str(AssertionError, "Unexpected invocation: unnamed.save(positional)", lambda: mock.save("positional"))
    assert_raises_str(AssertionError, "Unexpected invocation: unnamed.save(key=word)", lambda: mock.save(key="word"))
    assert mock.save("one", "two", key="word", foo="bar") is return_value

@funk.with_context
def test_same_method_can_return_different_values_for_different_arguments_using_provides(context):
    return_foo = "foo"
    return_bar = "bar"
    
    mock = context.mock()
    mock.provides('save').with_args("one", "two", key="word", foo="bar").returns(return_foo)
    mock.provides('save').with_args("positional").returns(return_bar)
    
    assert mock.save("one", "two", key="word", foo="bar") is return_foo
    assert_raises_str(AssertionError, "Unexpected invocation: unnamed.save()", lambda: mock.save())
    assert mock.save("positional") is return_bar
    assert_raises_str(AssertionError, "Unexpected invocation: unnamed.save(key=word)", lambda: mock.save(key="word"))
    assert mock.save("one", "two", key="word", foo="bar") is return_foo

@funk.with_context
def test_name_of_mock_is_used_in_exceptions(context):
    unnamed = context.mock()
    named = context.mock('database')
    unnamed.provides('save').with_args("positional")
    named.provides('save').with_args("positional")
    
    assert_raises_str(AssertionError, "Unexpected invocation: unnamed.save()", lambda: unnamed.save())
    assert_raises_str(AssertionError, "Unexpected invocation: database.save()", lambda: named.save())

@funk.with_context
def test_expected_methods_can_be_called_once_with_any_arguments_if_no_arguments_specified(context):
    return_value = "Oh my!"
    mock = context.mock()
    mock.expects('save').returns(return_value)
    
    assert mock.save("positional", key="word") is return_value

@funk.with_context
def test_expected_methods_cannot_be_called_more_than_once(context):
    mock = context.mock()
    mock.expects('save').returns("Oh my!")
    
    assert mock.save("positional", key="word")
    
    assert_raises_str(AssertionError,
                      "Unexpected invocation: unnamed.save(positional, key=word)",
                      lambda: mock.save("positional", key="word"))

@funk.with_context
def test_expected_methods_can_be_called_in_any_order(context):
    return_no_args = "Alone!"
    return_positional = "One is the loneliest number"
    
    mock = context.mock()
    mock.expects("save").with_args().returns(return_no_args)
    mock.expects("save").with_args("positional").returns(return_positional)
    
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
    mock.expects('save').raises(RuntimeError("Oh noes!"))
    assert_raises(RuntimeError, lambda: mock.save("anything"))

@funk.with_context
def test_method_expectations_are_used_in_the_order_they_are_defined(context):
    first = "One is the loneliest number"
    second = "Two can be as bad as one"
    mock = context.mock()
    mock.expects('save').returns(first)
    mock.expects('save').returns(second)
    
    assert mock.save() is first
    assert mock.save() is second

def test_function_raises_exception_if_expectations_are_not_satisfied():
    @funk.with_context
    def function(context):
        mock = context.mock()
        mock.expects("save")
        
    assert_raises_str(AssertionError,
                      "Not all expectations were satisfied. Expected call: unnamed.save",
                      function)

@funk.with_context
def test_mocks_can_expect_calls(context):
    return_value = "Hello!"
    mock = context.mock('save')
    assert_raises_str(AssertionError, "Unexpected invocation: save()", mock)
    mock.expects_call().returns(return_value)
    assert mock() is return_value
    assert_raises_str(AssertionError, "Unexpected invocation: save()", mock)
    assert_raises_str(AssertionError, "Unexpected invocation: save(positional, key=word)", lambda: mock("positional", key="word"))
    
@funk.with_context
def test_mocks_can_expect_calls_with_args(context):
    return_value = "Hello!"
    mock = context.mock('save')
    assert_raises_str(AssertionError, "Unexpected invocation: save()", mock)
    mock.expects_call().with_args("positional").returns(return_value)
    assert_raises_str(AssertionError, "Unexpected invocation: save()", mock)
    assert_raises_str(AssertionError, "Unexpected invocation: save(positional, key=word)", lambda: mock("positional", key="word"))
    assert mock("positional") is return_value
    
def test_function_raises_exception_if_expectations_of_calls_on_mock_are_not_satisfied():
    @funk.with_context
    def function(context):
        mock = context.mock()
        mock.expects_call()
        
    assert_raises_str(AssertionError,
                      "Not all expectations were satisfied. Expected call: unnamed",
                      function)
    
@funk.with_context
def test_mocks_can_provide_calls(context):
    return_value = "Hello!"
    mock = context.mock('save')
    assert_raises_str(AssertionError, "Unexpected invocation: save()", mock)
    mock.provides_call().returns(return_value)
    assert mock() is return_value
    assert mock() is return_value
    mock("positional", key="word") is return_value
    
@funk.with_context
def test_mocks_can_provide_calls_with_args(context):
    return_value = "Hello!"
    mock = context.mock('save')
    assert_raises_str(AssertionError, "Unexpected invocation: save()", mock)
    mock.provides_call().with_args("positional").returns(return_value)
    
    assert mock("positional") is return_value
    
    assert_raises_str(AssertionError, "Unexpected invocation: save()", mock)
    assert_raises_str(AssertionError, "Unexpected invocation: save(positional, key=word)", lambda: mock("positional", key="word"))

@funk.with_context
def test_can_use_matchers_instead_of_values_for_positional_arguments(context):
    class BlahMatcher(Matcher):
        def matches(self, other, failure_output):
            return other == "Blah"
            
    return_value = "Whoopee!"
    mock = context.mock()
    mock.expects('save').with_args(BlahMatcher()).returns(return_value)
    
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
    mock.expects('save').with_args(value=BlahMatcher()).returns(return_value)
    
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
