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
        expects(database).save("positional").returns(return_one)
        expects(database).save(key="word").returns(return_two)
        
        assert database.save(key="word") is return_two
        assert database.save("positional") is return_one
        
    Some calls can only be called a specified number of times -- specifically,
    :func:`~funk.expects` only the created call to be called once. For instance::
    
        database = context.mock()
        expects(database).save().returns(return_one)
        allows(database.save().returns(return_two)
        
        assert database.save() is return_one
        assert database.save() is return_two
        assert database.save() is return_two
        
    The first call to ``database.save`` returns the first return value since
    the arguments match, and it was declared first. However, subsequent calls
    return the second return value since using :func:`~funk.expects` means that call
    can be matched only once, where the call created by :func:`~funk.allows` can
    be matched any number of times.

.. function:: set_attr(mock, **kwargs)

    Sets attributes on the mocked object. For instance::
    
        mock = context.mock()
        set_attr(mock, key='word', something='else')
        assert mock.key == 'word'
        assert mock.something == 'else'

.. function:: expects(mock)

    Create an object to expect a method call on *mock*.  If the method is not
    called, an :class:`AssertionError` is raised. For instance, to expect
    a method call save::
    
        database = context.mock()
        expects(database).save
    
    By default, this expectation will allow any arguments. Expected arguments 
    can be set by calling the returned value. For instance, to expect
    the keyword argument *sorted* with a value of :const:`False`::
    
        expects(database).save(sorted=False)

    To customise the expectation further, use the methods on :class:`~funk.call.Call`.
    
.. function:: allows(method_name)

    Similar to :func:`funk.expects`, expect that the method can be called
    any number of times, including none.

.. module:: funk.call

.. class:: Call
    
    Allows an expected call to be configured. By default, the call will accept
    any parameters, and will return :const:`None`. That is::
    
        database = context.mock()
        allows(database).save
        
        assert database.save() is None
        assert database.save("positional") is None
        assert database.save("positional", key="word") is None
    
    .. method:: with_args(*args, **kwargs)
    
        Allow this call to only accept the given arguments. For instance::
        
            database = context.mock()
            allows(database).save.with_args('positional', key='word').returns(return_value)
            assert database.save('positional', key='word') is return_value
            database.save() # Raises AssertionError
        
        Note that this is completely equivalent to::
        
            database = context.mock()
            allows(database).save('positional', key='word').returns(return_value)
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
            allows(database).save.returns(return_value)
            
            assert database.save() is return_value
            assert database.save("positional") is return_value
            
        The same method can return different values. For instance::
        
            database = context.mock()
            expects(database).save.returns(return_one)
            expects(database).save.returns(return_two)
            
            assert database.save() is return_one
            assert database.save() is return_two
        
