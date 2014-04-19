Funk: A mocking framework for Python
====================================

Funk is a mocking framework for Python, influenced heavily by `JMock <http://www.jmock.org/>`_.
Funk helps to test modules in isolation by allowing mock objects to be used in place of "real" objects.
Funk is licensed under the 2-clause BSD licence.

Installation
------------

.. code-block:: sh

    $ pip install funk

Example
-------

Let's say we have a ``TagRepository`` class,
which has a ``fetch_all`` method on it.
This method will fetch all instances of ``Tag`` from the database for us.

We also have a class that we'd like to test, called ``TagDisplayer``.
Its constructor takes a ``TagRepository``,
and has a method ``display_all``.
We want to test that this method will grab all of the tags from the repository,
sort them into alphabetical order,
and write their names into a string separated by new lines.

.. code-block:: python

    from nose.tools import assert_equals
    import funk
    from funk import expects

    @funk.with_context
    def test_writes_all_tag_names_onto_separate_lines(context):
        tag_repository = context.mock(TagRepository)
        
        expects(tag_repository).fetch_all(sorted=False)
            .returns([Tag('python'), Tag('debian')])
        
        tag_displayer = TagDisplayer(tag_repository)
        assert_equals(tag_displayer.display_all(), 'python\ndebian')

By using a mock object instead of a real instance of ``TagRepository``,
we avoid relying on a correct implementation of ``TagRepository``.
We can also run the test without a running database.
