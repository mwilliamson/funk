from nose.tools import assert_raises
from nose.tools import assert_equals

import funk
from funk import FunkException

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
    assert_raises_str(AssertionError, "Unexpected method call: save(positional)", lambda: fake.save("positional"))
    assert_raises_str(AssertionError, "Unexpected method call: save(key=word)", lambda: fake.save(key="word"))
    assert_raises_str(AssertionError, "Unexpected method call: save(one, two, foo=bar, key=word)", lambda: fake.save("one", "two", key="word", foo="bar"))
    assert fake.save() is return_value

def test_calling_function_wrapped_in_with_context_raises_exception_if_context_already_set():
    @funk.with_context
    def some_function(context):
        pass
        
    assert_raises(FunkException, lambda: some_function(context=None))

def assert_raises_str(exception, message, function):
    try:
        function()
        raise AssertionException("%s was not raised" % exception)
    except exception, e:
        assert_equals(message, str(e))
