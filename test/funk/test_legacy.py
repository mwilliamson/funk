from nose.tools import assert_raises
from nose.tools import assert_equals

from funk.legacy import with_context
from funk import expects
from funk import allows
from funk import set_attr

@with_context
def test_can_set_attributes_on_mock_objects(context):
    name = "the_blues"
    mock = context.mock()
    mock.set_attr(name=name)
    
    assert_equals(name, mock.name)
    assert_equals(name, mock.name)

@with_context
def test_can_set_attributes_that_override_methods_on_mock(context):
    value = "I am not an animal! I am a human being!"
    mock = context.mock()
    assert callable(mock.expects)
    assert callable(mock.allows)
    assert callable(mock.set_attr)
    mock.set_attr(expects=value, allows=value, set_attr=value)
    assert not callable(mock.expects)
    assert not callable(mock.allows)
    assert not callable(mock.set_attr)
    assert_equals(mock.expects, value)
    assert_equals(mock.allows, value)
    assert_equals(mock.set_attr, value)

@with_context
def test_providing_a_method_without_specifying_arguments_allows_method_to_be_called_any_times_with_any_arguments(context):
    return_value = "foo"
    
    mock = context.mock()
    mock.allows('save').returns(return_value)
    
    assert mock.save() is return_value
    assert mock.save(1, 2) is return_value
    assert mock.save() is return_value
    assert mock.save(name="Bob") is return_value


@with_context
def test_can_expect_methods_that_override_methods_on_mock(context):
    value_expects = "It was one of those all-night wicker places"
    value_allows = "We shot a lot of people together"
    value_set_attr = "It's a big building with patients, but that's not important right now."
    mock = context.mock()
    
    mock.expects('allows').returns(value_allows)
    mock.expects('set_attr').returns(value_set_attr)
    mock.expects('expects').returns(value_expects)
    
    assert mock.expects() is value_expects
    assert mock.allows() is value_allows
    assert mock.set_attr() is value_set_attr
    assert_raises(AssertionError, mock.expects)

@with_context
def test_can_allow_methods_that_override_methods_on_mock(context):
    value_expects = "It was one of those all-night wicker places"
    value_allows = "We shot a lot of people together"
    value_set_attr = "It's a big building with patients, but that's not important right now."
    mock = context.mock()
    
    mock.allows('set_attr').returns(value_set_attr)
    mock.allows('expects').returns(value_expects)
    mock.allows('allows').returns(value_allows)
    
    assert mock.expects() is value_expects
    assert mock.allows() is value_allows
    assert mock.set_attr() is value_set_attr

@with_context
def test_can_use_expects_function_when_expects_method_has_been_mocked(context):
    value_expects = "In colour!"
    value_save = "Coffee? Yes, I know."
    mock = context.mock()
    
    mock.expects('expects').returns(value_expects)
    expects(mock, 'save').returns(value_save)

    assert mock.expects() is value_expects
    assert mock.save() is value_save

@with_context
def test_can_use_allows_function_when_allows_method_has_been_mocked(context):
    value_allows = "In colour!"
    value_save = "Coffee? Yes, I know."
    mock = context.mock()
    
    mock.allows('allows').returns(value_allows)
    allows(mock, 'save').returns(value_save)

    assert mock.allows() is value_allows
    assert mock.save() is value_save

@with_context
def test_can_use_set_attr_function_when_set_attr_method_has_been_mocked(context):
    value_set_attr = "In colour!"
    value_save = "Coffee? Yes, I know."
    mock = context.mock()
    
    mock.set_attr(set_attr=value_set_attr)
    set_attr(mock, save=value_save)

    assert mock.set_attr is value_set_attr
    assert mock.save is value_save

@with_context
def test_can_expect_call(context):
    to_return = "What's that Skippy?"
    mock = context.mock()
    mock.expects_call().returns(to_return)
    assert mock() is to_return
    assert_raises(AssertionError, mock)
    
@with_context
def test_can_allow_call(context):
    to_return = "What's that Skippy?"
    mock = context.mock()
    mock.allows_call().returns(to_return)
    assert mock() is to_return
    assert mock() is to_return
