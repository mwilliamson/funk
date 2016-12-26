class FileStorage(object):
    def names(self):
        pass


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
