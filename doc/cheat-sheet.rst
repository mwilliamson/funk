Cheat Sheet
===========

Writing a test using Funk
-------------------------

::

    import funk

    @funk.with_context
    def test_tag_displayer_writes_all_tag_names_in_alphabetical_order_onto_separate_lines(context):
        # Create mocks
        # Set up expectations
        # Call code under test
        # Perform assertions

For instance::

    from nose.tools import assert_equals
    import funk
    from funk import expects

    @funk.with_context
    def test_tag_displayer_writes_all_tag_names_in_alphabetical_order_onto_separate_lines(context):
        tag_repository = context.mock(TagRepository)
        expects(tag_repository).fetch_all(sorted=False).returns([Tag('python'), Tag('debian')])
        
        tag_displayer = TagDisplayer(tag_repository)
        assert_equals(tag_displayer.display_all(), 'debian\npython')

Creating mock objects
---------------------

::

    # Only methods defined on TagRepository can be mocked
    tag_repository = context.mock(TagRepository)
    
    # Without a base class, any method can be mocked
    database = context.mock(name="database")
        
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

    from funk.matchers import is_a, has_attr, and, any_value
    # ...
    expects(database).save(and(is_a(Tag), has_attr(name="python")), commit=any_value())
    
+---------------------------+--------------------------------------------------------------------------------------------------------+
| ``any_value()``           | Matches anything                                                                                       |
+---------------------------+--------------------------------------------------------------------------------------------------------+
| ``is_a(type_)``           | Matches ``actual`` if ``isinstance(actual, type_)``                                                    |
+---------------------------+--------------------------------------------------------------------------------------------------------+
| ``has_attr(**attrs)``     | Matches ``actual`` if, for each ``(key, value)`` pair in ``**attrs``, ``actual.key`` matches ``value`` |
+---------------------------+--------------------------------------------------------------------------------------------------------+
| ``equal_to(value)``       | Matches ``actual`` if ``actual == value``                                                              |
+---------------------------+--------------------------------------------------------------------------------------------------------+
| ``is_(value)``            | Matches ``actual`` if ``actual is value``                                                              |
+---------------------------+--------------------------------------------------------------------------------------------------------+
| ``not_(matcher)``         | Matches ``actual`` if ``matcher`` does not match ``actual``                                            |
+---------------------------+--------------------------------------------------------------------------------------------------------+
| ``all_of(*matchers)``     | Matches ``actual`` if, for each ``matcher`` in ``matchers``, ``matcher`` matches ``actual``            |
+---------------------------+--------------------------------------------------------------------------------------------------------+
| ``any_of(*matchers)``     | Matches ``actual`` if there is a matcher in ``matchers`` that matches ``actual``                       |
+---------------------------+--------------------------------------------------------------------------------------------------------+

Actions
^^^^^^^
+------------------------------------+-----------------------------------------------------------------------+
| (No action)                        |  Returns ``None``.                                                    |
+------------------------------------+-----------------------------------------------------------------------+
|``raises(e)``                       |  Raise ``e``.                                                         |
+------------------------------------+-----------------------------------------------------------------------+
|``returns(value)``                  |  Returns ``value``.                                                   |
+------------------------------------+-----------------------------------------------------------------------+
