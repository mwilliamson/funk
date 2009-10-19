Getting started with Funk
=========================

Let's say we have a :class:`TagRepository` class, which has a :func:`fetch_all`
method on it. This class will go and fetch instances of :class:`Tag` from the
database for us. The :class:`Tag` class looks like this::

    class Tag(object):
        def __init__(self, name):
            self.name = name

We also have a class that we'd like to test, called :class:`TagDisplayer`. Its
constructor takes a :class:`TagRepository`, and has a method :func:`display_all`.
We expect that this method will grab all of the tags from the respository,
and write their names into a string, separated by new lines. So, we can write
our test function like so (I'm using nose as the testing framework, but other
testing frameworks should work just fine)::

    from nose.tools import assert_equals
    from funk import with_context
    from funk import expects

    @with_context
    def test_tag_displayer_writes_all_tag_names_onto_separate_lines(context):
        tag_repository = context.mock(name='tag_repository')
        expects(tag_repository).fetch_all(sorted=False).returns([Tag('python'), Tag('debian')])
        
        tag_displayer = TagDisplayer(tag_repository)
        assert_equals(tag_displayer.display_all(), 'python\ndebian')

Note the that test method takes a context as an argument.
If necessary, you can build you own instances by calling :class:`funk.Context`.
This is the object that allows you to create mocks, by calling :func:`~funk.Context.mock`.

It's probably worth deconstructing the expectation setup here. We start with
the simpler expectation::

    expects(tag_repository).fetch_all

This means that we expect ``fetch_all`` to be called on ``tag_repository`` with
any possible arguments exactly once. If it is called, it will return :const:`None`.

So, we need to specify the arguments we expect it to be called with. While you
can set up both positional and keyword arguments, we expect a single keyword
argument. We can set up this expectation in two ways. The first is as above::

    expects(tag_repository).fetch_all(sorted=False)
    
Alternatively (and equivalently)::

    expects(tag_repository).fetch_all.with_args(sorted=False)
    
Finally, we set the return value using :func:`~funk.call.Call.returns`::

    expects(tag_repository).fetch_all(sorted=False).returns([Tag('python'), Tag('debian')])
    
Note that we could have called :func:`~funk.call.Call.returns` without setting up
the arguments. This is useful when you just don't care what the arguments are,
but the return values are important. For instance::

    expects(tag_repository).fetch_all.returns([Tag('python'), Tag('debian')])

Since the :class:`TagDisplayer` has been written to have its dependencies injected,
inserting the mocked tag repository into the tag displayer is extremely
straightforward -- simply pass it in via the constructor.

If the method is working correctly, then the test will pass. But what if the
test is not working correctly? One possibility is that the tag displayer calls
the wrong method -- for instance, it might try to call the non-existant method
:func:`fetch_all_tags`. If this happens, the test fails::

    AttributeError: 'Mock' object has no attribute 'fetch_all_tags'
    
Alternatively, we might call :func:`fetch_all` with a single argument, ``'spam'``,
instead of the correct keyword argument::

    AssertionError: Unexpected invocation: tag_repository.fetch_all(spam)

If we call the method with the correct arguments twice::

    AssertionError: Unexpected invocation: tag_repository.fetch_all(sorted=False)
    
If we don't call the method at all, the test will fail since the mock did not
have all of its expected methods called::

    AssertionError: Not all expectations were satisfied. Expected call: tag_repository.fetch_all(sorted=False)

But what if we don't want the test to fail if the method is not called? We can use
:func:`~funk.allows` instead of :func:`~funk.expects`. They both
behave in the same manner, except that :func:`~funk.expects` will expect exactly one
matching call, whereas :func:`~funk.allows` will allow any number of calls, including
none.

Different expectations on the same method
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sometimes, we expect the same method to be called more than once, but we might
want it to behave differently on successive calls. For instance, let's say we
have a database object that can delete objects from the database. The first time
we call :func:`delete` on a tag, it should return :const:`True` to indicate a
successful deletion. On any subsequent calls, it should return :const:`False`
since the tag has already been deleted. For instance::

    database = context.mock('database')
    expects(database).delete(tag).returns(True)
    allows(database).delete(tag).returns(False)
    
    # To demonstrate the behaviour of the mocked database
    assert database.delete(tag) is True
    assert database.delete(tag) is False
    assert database.delete(tag) is False
    
The first call to ``database.delete`` returns the first return value since
the arguments match, and it was declared first. However, subsequent calls
return the second return value since using :func:`~funk.expects` means that call
can be matched only once, where the call created by :func:`~funk.allows` can
be matched any number of times.

We might also decide to set up another expectation so that deleting any other
tag returns :const:`False`::

    database = context.mock('database')
    expects(database).delete(tag).returns(True)
    allows(database).delete(tag).returns(False)
    allows(database).delete.returns(False)
    
    # To demonstrate the behaviour of the mocked database
    assert database.delete(tag) is True
    assert database.delete(tag) is False
    assert database.delete(tag) is False
    assert database.delete(another_tag) is False
    assert database.delete(42) is False
    assert database.delete(number=42) is False
    
While the above assertions will pass, we probably didn't want to allow those two
final call. While we want to allow any tag to be used, we shouldn't allow
any arguments. To solve this problem, we can use a matcher like so::

    from funk.matcher import is_a
    ...
    
    database = context.mock('database')
    expects(database).delete(tag).returns(True)
    allows(database).delete(tag).returns(False)
    allows(database).delete(is_a(Tag)).returns(False)
    
    # To demonstrate the behaviour of the mocked database
    assert database.delete(tag) is True
    assert database.delete(tag) is False
    assert database.delete(tag) is False
    assert database.delete(another_tag) is False
    database.delete(42) # Unexpected invocation, raises AssertionError
    database.delete(number=42) # Unexpected invocation, raises AssertionError

Note that we define the generic expectation after the other expectations. If
we'd written the test like so::

    database = context.mock('database')
    allows(database).delete(is_a(Tag)).returns(False)
    expects(database).delete(tag).returns(True)
    allows(database).delete(tag).returns(False)

Then even the first call to ``database.delete(tag)`` would return :const:`False`
since the first matching expectation for that call returns :const:`False`.

Base classes
^^^^^^^^^^^^

Using our earlier example, we had a :class:`TagRepository`. It had a method
:func:`fetch_all` that we expected to be called, so we set up the test like so::

    from nose.tools import assert_equals
    from funk import with_context
    from funk import expects

    @with_context
    def test_tag_displayer_writes_all_tag_names_onto_separate_lines(context):
        tag_repository = context.mock(name='tag_repository')
        expects(tag_repository).fetch_all(sorted=False).returns([Tag('python'), Tag('debian')])
        
        tag_displayer = TagDisplayer(tag_repository)
        assert_equals(tag_displayer.display_all(), 'python\ndebian')

We then decide to rename the method :func:`fetch_all` to :func:`get_all`. However,
this unit test will still pass without changing the :class:`TagDisplayer` since
we're still mocking a method called :func:`fetch_all`. To help in this situation,
you can pass in a base class for mocks::

    tag_repository = context.mock(TagRepository, name='tag_repository')

Now, Funk will only allow you to expect and allow methods that are defined on
:class:`TagRepository`. Running the test as is causes an :class:`AssertionError`
to be raised::

    Method 'fetch_all' is not defined on type object 'TagRepository'

Two words of caution about using this feature. Firstly, this only works if
the method is explicitly defined on the base class. This is often not the case
if the method is dynamically generated, such as by overriding
:func:`__getattribute__` on the type.

Secondly, this is no substitute for integration testing. While its true that the
unit test above would not have failed, there should have been some integration
test in your system that would have failed due to the method name change. The
aim of allowing you to specify the base class is so that you can find that
failure a little quicker.
