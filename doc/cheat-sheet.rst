Cheat Sheet
===========

Writing a test using Funk
-------------------------

::

    import funk

    @funk.with_mocks
    def test_tag_displayer_writes_all_tag_names_in_alphabetical_order_onto_separate_lines(mocks):
        # Create mocks
        # Set up expectations
        # Call code under test
        # Perform assertions

For instance::

    from nose.tools import assert_equals
    import funk
    from funk import expects

    @funk.with_mocks
    def test_tag_displayer_writes_all_tag_names_in_alphabetical_order_onto_separate_lines(mocks):
        tag_repository = mocks.mock(TagRepository)
        expects(tag_repository).fetch_all(sorted=False).returns([Tag('python'), Tag('debian')])
        
        tag_displayer = TagDisplayer(tag_repository)
        assert_equals(tag_displayer.display_all(), 'debian\npython')

Creating mock objects
---------------------

::

    # Only methods defined on TagRepository can be mocked
    tag_repository = mocks.mock(TagRepository)
    
    # Without a base class, any method can be mocked
    database = mocks.mock(name="database")
        
Setting expectations
--------------------

:func:`~funk.expects` and :func:`~funk.allows` can be imported from :mod:`funk`.

Expectations look like this::

    <invocation-count>(<mock-object>).<method>(<arguments>).<action>

For instance::

    # Allows database.fetch_all to be called exactly once with the positional
    # argument Tag and the keyword argument sorted=False and return the list of
    # two tags. The test will fail if the method is never called::
    expects(database).fetch_all(Tag, sorted=False).returns([Tag("debian"), Tag("python")])
    
    # Allows database.save to be called any number of times, including none,
    # with any arguments. Every call to ``database.save`` will raise a TypeError.
    allows(database).save.raises(TypeError)

Invocation counts
^^^^^^^^^^^^^^^^^

+---------------------+-----------------------------------------------------------------------+
|:func:`~funk.expects`|  Expects the method to called exactly once.                           |
+---------------------+-----------------------------------------------------------------------+
|:func:`~funk.allows` |  Allows the method to be called any number of times, including none.  |
+---------------------+-----------------------------------------------------------------------+

Arguments
^^^^^^^^^

If no arguments are specified, then any arguments will be accepted. Otherwise,
both positional and keyword arguments will be checked for equality.

To use different constraints on arguments, use matchers. For instance, if
we expect to save an instance of ``Tag`` with the attribute ``name`` set to
``"python"``, and we don't care what the value of the commit argument is::

    from precisely import instance_of, has_attrs, all_of, anything
    # ...
    expects(database).save(
        all_of(instance_of(Tag), has_attrs(name="python")),
        commit=anything(),
    )
    
Actions
^^^^^^^
+------------------------------------+-----------------------------------------------------------------------+
| (No action)                        |  Returns ``None``.                                                    |
+------------------------------------+-----------------------------------------------------------------------+
|``raises(e)``                       |  Raise ``e``.                                                         |
+------------------------------------+-----------------------------------------------------------------------+
|``returns(value)``                  |  Returns ``value``.                                                   |
+------------------------------------+-----------------------------------------------------------------------+

Sequences
---------

A sequence object can be created using :meth:`~funk.Mocks.sequence`.
The sequencing on objects can then be defined using :meth:`~funk.call.Call.in_sequence`.
For instance, to ensure a file is written to before it is closed::

    file_ = mocks.mock(file)
    file_ordering = mocks.sequence()

    expects(file_).write("Eggs").in_sequence(file_ordering)
    expects(file_).close().in_sequence(file_ordering)
