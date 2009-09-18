from nose.tools import assert_raises

import funk
from funk import FunkException

@funk.with_context
def test_can_create_a_fake_object(context):
    fake = context.fake()

def test_calling_function_wrapped_in_with_context_raises_exception_if_context_already_set():
    @funk.with_context
    def some_function(context):
        pass
        
    assert_raises(FunkException, lambda: some_function(context=None))
