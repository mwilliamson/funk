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

Suppose we have an API for a file storage service.
We want to list the names of all files,
but the API limits the number of names it will return at a time.
Therefore, we need to write some code that will keep making requests to the API
until all names have been retrieved.

.. code-block:: python

    def fetch_names(file_storage):
        has_more = True
        token = None
        names = []
        
        while has_more:
            response = file_storage.names(token=token)
            names += response.names
            token = response.next_token
            has_more = token is not None
        
        return names    
        

    import funk

    @funk.with_mocks
    def test_request_for_names_until_all_names_are_fetched(mocks):
        file_storage = mocks.mock(FileStorage)
        
        mocks.allows(file_storage).names(token=None).returns(mocks.data(
            next_token="<token 1>",
            names=["a", "b"],
        ))
        mocks.allows(file_storage).names(token="<token 1>").returns(mocks.data(
            next_token="<token 2>",
            names=["c", "d"],
        ))
        mocks.allows(file_storage).names(token="<token 2>").returns(mocks.data(
            next_token=None,
            names=["e"],
        ))
        
        assert fetch_names(file_storage) == ["a", "b", "c", "d", "e"]

By using a mock object instead of a real instance of ``FileStorage``,
we can run our tests without a running instance of the file storage system.
We also avoid relying on the implementation of ``FileStorage``,
making our tests more focused and less brittle.
