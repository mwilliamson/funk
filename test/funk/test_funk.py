from nose.tools import assert_raises
from nose.tools import assert_equals

import funk
from funk import FunkyError
from funk.tools import assert_raises_str
from funk.matchers import Matcher

@funk.with_context
def test_can_create_a_fake_object(context):
    fake = context.fake()

@funk.with_context
def test_can_set_attributes_on_fake_objects(context):
    name = "the_blues"
    fake = context.fake()
    fake.has_attr(name=name)
    
    assert_equals(name, fake.name)
    assert_equals(name, fake.name)

@funk.with_context
def test_providing_a_method_without_specifying_arguments_allows_method_to_be_called_no_times(context):
    fake = context.fake()
    fake.provides('save')

@funk.with_context
def test_providing_a_method_without_specifying_arguments_allows_method_to_be_called_any_times_with_any_arguments(context):
    return_value = "foo"
    
    fake = context.fake()
    fake.provides('save').returns(return_value)
    
    assert fake.save() is return_value
    assert fake.save(1, 2) is return_value
    assert fake.save() is return_value
    assert fake.save(name="Bob") is return_value

@funk.with_context
def test_can_specify_no_arguments_when_using_provides(context):
    return_value = "foo"
    
    fake = context.fake()
    fake.provides('save').with_args().returns(return_value)
    
    assert fake.save() is return_value
    assert_raises_str(AssertionError, "Unexpected invocation: unnamed.save(positional)", lambda: fake.save("positional"))
    assert_raises_str(AssertionError, "Unexpected invocation: unnamed.save(key=word)", lambda: fake.save(key="word"))
    assert_raises_str(AssertionError, "Unexpected invocation: unnamed.save(one, two, foo=bar, key=word)", lambda: fake.save("one", "two", key="word", foo="bar"))
    assert fake.save() is return_value

@funk.with_context
def test_can_specify_arguments_using_equality_on_instances_when_using_provides(context):
    return_value = "foo"
    
    fake = context.fake()
    fake.provides('save').with_args("one", "two", key="word", foo="bar").returns(return_value)
    
    assert fake.save("one", "two", key="word", foo="bar") is return_value
    assert_raises_str(AssertionError, "Unexpected invocation: unnamed.save()", lambda: fake.save())
    assert_raises_str(AssertionError, "Unexpected invocation: unnamed.save(positional)", lambda: fake.save("positional"))
    assert_raises_str(AssertionError, "Unexpected invocation: unnamed.save(key=word)", lambda: fake.save(key="word"))
    assert fake.save("one", "two", key="word", foo="bar") is return_value

@funk.with_context
def test_same_method_can_return_different_values_for_different_arguments_using_provides(context):
    return_foo = "foo"
    return_bar = "bar"
    
    fake = context.fake()
    fake.provides('save').with_args("one", "two", key="word", foo="bar").returns(return_foo)
    fake.provides('save').with_args("positional").returns(return_bar)
    
    assert fake.save("one", "two", key="word", foo="bar") is return_foo
    assert_raises_str(AssertionError, "Unexpected invocation: unnamed.save()", lambda: fake.save())
    assert fake.save("positional") is return_bar
    assert_raises_str(AssertionError, "Unexpected invocation: unnamed.save(key=word)", lambda: fake.save(key="word"))
    assert fake.save("one", "two", key="word", foo="bar") is return_foo

@funk.with_context
def test_name_of_fake_is_used_in_exceptions(context):
    unnamed = context.fake()
    named = context.fake('database')
    unnamed.provides('save').with_args("positional")
    named.provides('save').with_args("positional")
    
    assert_raises_str(AssertionError, "Unexpected invocation: unnamed.save()", lambda: unnamed.save())
    assert_raises_str(AssertionError, "Unexpected invocation: database.save()", lambda: named.save())

@funk.with_context
def test_expected_methods_can_be_called_once_with_any_arguments_if_no_arguments_specified(context):
    return_value = "Oh my!"
    fake = context.fake()
    fake.expects('save').returns(return_value)
    
    assert fake.save("positional", key="word") is return_value

@funk.with_context
def test_expected_methods_cannot_be_called_more_than_once(context):
    fake = context.fake()
    fake.expects('save').returns("Oh my!")
    
    assert fake.save("positional", key="word")
    
    assert_raises_str(AssertionError,
                      "Unexpected invocation: unnamed.save(positional, key=word)",
                      lambda: fake.save("positional", key="word"))

@funk.with_context
def test_expected_methods_can_be_called_in_any_order(context):
    return_no_args = "Alone!"
    return_positional = "One is the loneliest number"
    
    fake = context.fake()
    fake.expects("save").with_args().returns(return_no_args)
    fake.expects("save").with_args("positional").returns(return_positional)
    
    assert fake.save("positional") is return_positional
    assert fake.save() is return_no_args
    
    assert_raises_str(AssertionError,
                      "Unexpected invocation: unnamed.save(positional)",
                      lambda: fake.save("positional"))
                      
    assert_raises_str(AssertionError,
                      "Unexpected invocation: unnamed.save()",
                      lambda: fake.save())

@funk.with_context
def test_fakes_can_raise_exceptions(context):
    fake = context.fake()
    fake.expects('save').raises(RuntimeError("Oh noes!"))
    assert_raises(RuntimeError, lambda: fake.save("anything"))

@funk.with_context
def test_method_expectations_are_used_in_the_order_they_are_defined(context):
    first = "One is the loneliest number"
    second = "Two can be as bad as one"
    fake = context.fake()
    fake.expects('save').returns(first)
    fake.expects('save').returns(second)
    
    assert fake.save() is first
    assert fake.save() is second

def test_function_raises_exception_if_expectations_are_not_satisfied():
    @funk.with_context
    def function(context):
        fake = context.fake()
        fake.expects("save")
        
    assert_raises_str(AssertionError,
                      "Not all expectations were satisfied. Expected call: unnamed.save",
                      function)

@funk.with_context
def test_fakes_can_expect_calls(context):
    return_value = "Hello!"
    fake = context.fake('save')
    assert_raises_str(AssertionError, "Unexpected invocation: save()", fake)
    fake.expects_call().returns(return_value)
    assert fake() is return_value
    assert_raises_str(AssertionError, "Unexpected invocation: save()", fake)
    assert_raises_str(AssertionError, "Unexpected invocation: save(positional, key=word)", lambda: fake("positional", key="word"))
    
def test_function_raises_exception_if_expectations_of_calls_on_fake_are_not_satisfied():
    @funk.with_context
    def function(context):
        fake = context.fake()
        fake.expects_call()
        
    assert_raises_str(AssertionError,
                      "Not all expectations were satisfied. Expected call: unnamed",
                      function)
    
@funk.with_context
def test_fakes_can_provide_calls(context):
    pass

@funk.with_context
def test_can_use_matchers_instead_of_values_for_positional_arguments(context):
    class BlahMatcher(Matcher):
        def matches(self, other):
            return other == "Blah"
            
    return_value = "Whoopee!"
    fake = context.fake()
    fake.expects('save').with_args(BlahMatcher()).returns(return_value)
    
    assert_raises(AssertionError, lambda: fake.save())
    assert_raises(AssertionError, lambda: fake.save(key="word"))
    assert_raises(AssertionError, lambda: fake.save("positional"))
    assert_raises(AssertionError, lambda: fake.save("positional", key="word"))
    
    assert fake.save("Blah") is return_value
    
@funk.with_context
def test_can_use_matchers_instead_of_values_for_keyword_arguments(context):
    class BlahMatcher(Matcher):
        def matches(self, other):
            return other == "Blah"
            
    return_value = "Whoopee!"
    fake = context.fake()
    fake.expects('save').with_args(value=BlahMatcher()).returns(return_value)
    
    assert_raises(AssertionError, lambda: fake.save())
    assert_raises(AssertionError, lambda: fake.save(key="word"))
    assert_raises(AssertionError, lambda: fake.save("positional"))
    assert_raises(AssertionError, lambda: fake.save("positional", key="word"))
    
    assert fake.save(value="Blah") is return_value

def test_calling_function_wrapped_in_with_context_raises_exception_if_context_already_set():
    @funk.with_context
    def some_function(context):
        pass
        
    assert_raises(FunkyError, lambda: some_function(context=None))
