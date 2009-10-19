:mod:`funk.matchers`
====================

.. module:: funk.matchers

.. class:: Matcher

    The base class for any matcher. A matcher must implement the method
    :func:`~funk.matchers.Matcher.matches`. It should also provide its own
    implementation of :func:`__str__`, to describe what values it matches.
    
    .. method:: matches(value, mismatch_output)
    
        Returns :const:`True` if this matcher matches *value*, :const:`False` otherwise.
        
        If the matcher matches *value*, then *mismatch_output* should not be used.
        Otherwise, the reason for the mismatch should be written to *mismatch_output*
        using ``mismatch_output.append``.
    
    An example matcher is :class:`IsAnInt` (this is generalised in :func:`~funk.matchers.is_a`)::
    
        class IsAnInt(Matcher):
            def matches(self, value, mismatch_output):
                if not isinstance(value, int):
                    mismatch_output.append("value was of type %s" % type(value).__name__)
                    return False
                return True
                
            def __str__(self):
                return "<value of type: int>"

.. function:: any_value

    Matches all values

.. function:: is_a(type_)

    Matches any value that is an instance of *type_*.

.. function:: has_attr(**attributes)

    Matches *actual* if, for every pair *(key, value)* in *attributes*,
    ``actual.key == value``.

.. function:: equal_to(value)

    Matches any value equal to *value*.

.. function:: not_(matcher)

    Negates the given matcher. For instance, ``not_(equal_to(20))`` will match
    any value not equal to 20.

.. function:: all_of(*matchers)

    Matches a value if all of the passed matchers match the value.

.. function:: any_of(*matchers)

    Matches a value if any of the passed matchers match the value.
