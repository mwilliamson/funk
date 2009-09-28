:mod:`funk`
============

.. module:: funk

.. function:: with_context

    A decorator for test methods. Supplies an instance of :class:`~funk.Context`
    as the keyword argument *context*::
    
        @with_context
        def test_some_function(context):
            # context is an instance of Context
            some_mock = context.mock()
            ...
            
    At the end of test, ``context.verify()`` will be called, so there is no
    need to call it yourself.

.. class:: Context

    .. method:: __init__
    
        Create a new context, with no expectations set up.
        
    .. method:: mock
    
        Create a new :class:`~funk.Mock` tied to this context.
        
    .. method:: verify
    
        Verifies that all mocks created with this context have had their
        expectations satisified. If this is not the case, an :class:`AssertionError`
        will be raised.
        
.. class:: Mock

    When a method is called, the first mocked call that will accept the given
    arguments is used. For instance::
    
        database = context.mock()
        database.allows('save').with_args("positional").returns(return_one)
        database.allows('save').with_args(key="word").returns(return_two)
        
        assert database.save(key="word") is return_two
        assert database.save("positional") is return_one
        
    Some calls can only be called a specified number of times -- specifically,
    :func:`~funk.Mock.expects` only the created call to be called once. For instance::
    
        database = context.mock()
        database.expects('save').with_args().returns(return_one)
        database.allows('save').with_args().returns(return_two)
        
        assert database.save() is return_one
        assert database.save() is return_two
        assert database.save() is return_two
        
    The first call to ``database.save`` returns the first return value since
    the arguments match, and it was declared first. However, subsequent calls
    return the second return value since using ``database`` means that call
    can be matched only once, where the call created by ``database.allows`` can
    be called any number of times.

    .. method:: hasattr(**kwargs)
    
        Sets attributes on the mocked object. For instance::
        
            mock = context.mock()
            mock.has_attr(key='word', something='else')
            assert mock.key == 'word'
            assert mock.something == 'else'

    .. method:: expects(method_name)
    
        Expect a call to the method named *method_name*. If the method is not
        called, an :class:`AssertionError` is raised. This particular call
        can be called once, but you can add further calls to the same method.
        For instance, this will not raise :class:`AssertionError`::
        
            mock = context.mock()
            mock.expects('save')
            mock.expects('save')
            
            mock.save()
            mock.save()
        
        However, a third call ``mock.save`` would raise an `AssertionError`.
        
        This method returns an instance of :class:`~funk.call.Call`, which allows
        the expected method call to be customised.
        
    .. method:: allows(method_name)
    
        Similar to :func:`funk.Mock.expects`, expect that the method can be called
        any number of times, including none.

.. module:: call

.. class:: Call
    
    Allows an expected call to be configured. By default, the call will accept
    any parameters, and will return :const:`None`. That is::
    
        database = context.mock()
        database.allows('save')
        
        assert database.save() is None
        assert database.save("positional") is None
        assert database.save("positional", key="word") is None
    
    .. method:: with_args(*args, **kwargs)
    
        Allow this call to only accept the given arguments. For instance::
        
            database = context.mock()
            database.allows('save').with_args('positional', key='word').returns(return_value)
            assert database.save('positional', key='word') is return_value
            database.save() # Raises AssertionError
            
        Matchers can also be used to specify allowed arguments::
        
            from funk.matchers import is_a
            
            ...
        
            calculator = context.mock()
            calculator.allows('add').with_args(is_a(int), is_a(int)).returns(return_value)
            assert calculator.add(4, 9) is return_value
    
    .. method:: raises(exception)
    
        Causes this call to raise *exception* when called.
    
    .. method:: returns(value)
    
        Causes this call to return *value*::
        
            database = context.mock()
            database.allows('save').returns(return_value)
            
            assert database.save() is return_value
            assert database.save("positional") is return_value
            
        The same method can return different values. For instance::
        
            database = context.mock()
            database.expects('save').returns(return_one)
            database.expects('save').returns(return_two)
            
            assert database.save() is return_one
            assert database.save() is return_two
        
