Getting started with Funk
=========================

Let's say we have a :class:`TagRepository` class, which has a :func:`fetch_all`
method on it. This class will go and fetch instances of :class:`Tag` from the
database for us. The :class:`Tag` class looks like this:

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

    @with_context
    def test_tag_displayer_writes_all_tag_names_onto_separate_lines(context):
        tag_repository = context.mock('tag_repository')
        tag_repository.expects('fetch_all').with_args().returns([Tag('python'), Tag('debian')])
        
        tag_displayer = TagDisplayer(tag_repository)
        assert_equals(tag_displayer.display_all(), 'python\ndebian')

There are a few things worth noting. The first is the test method takes a context.
If necessary, you can build you own instances by calling :class:`funk.Context`.
This is the object that allows you to create mocks, by calling :func:`~funk.Context.mock`,
which takes an optional parameter for the name of the mock.

We then call :func:`~funk.Mock.expects` on the mock. This tells the mock
that we expect the method :func:`fetch_all` to be called exactly once. This
returns an object that allows us to configure this expected call -- in this case,
we expect that it will be called with no arguments, and will return a list of
two tags.

Since the :class:`TagDisplayer` has been written to have its dependencies injected,
inserting the mocked tag repository into the tag displayer is extremely
straightforward -- simply pass it in via the constructor.

If the method is working correctly, then the test will pass. But what if the
test is not working correctly? One possibility is that the tag displayer calls
the wrong method -- for instance, it might try to call the non-existant method
:func:`fetch_all_tags`. If this happens, the test fails::

    AttributeError: 'Mock' object has no attribute 'fetch_all_tags'
    
Alternatively, we might call :func:`fetch_all` with a single argument, `'spam'`,
when we should only be calling it with no arguments::

    AssertionError: Unexpected invocation: TagRepository.fetch_all(spam)
    
If we don't call the method at all, but the assertion still passes, the test
will fail since the mock did have all of its expected methods called::

    AssertionError: Not all expectations were satisfied. Expected call: tag_repository.fetch_all()

But what if we don't want the test to fail if the method is not called? We can use
:func:`~funk.Mock.allows` instead of :func:`~funk.Mock.expects`. They both
behave in the same manner, except that :func:`~expects` will expect exactly one
matching call, whereas :func:`~allows` will allow any number of calls, including
none.
