:mod:`funk.tools`
============

.. module:: funk

.. function:: value_object(**kwargs)

    Creates an object with attributes set the values in *kwargs*. For instance::
    
        author = value_object(first_name="Joe", last_name="Bloggs")
        
        assert author.first_name == "Joe"
        assert author.last_name == "Bloggs"
