from nose.tools import assert_equals

from funk.util import arguments_str
from funk.util import function_call_str
from funk.util import method_call_str

def test_arguments_str_shows_positional_and_keyword_arguments():
    assert_equals('one, two, foo=bar, key=word',
                  arguments_str(("one", "two"), {'foo': 'bar', 'key': 'word'}))

def test_function_call_str_shows_name_of_function_and_arguments():
    assert_equals('save(one, two, foo=bar, key=word)',
                  function_call_str("save", ("one", "two"), {'foo': 'bar', 'key': 'word'}))

def test_method_call_str_shows_name_of_object_and_method_and_arguments():
    assert_equals('database.save(one, two, foo=bar, key=word)',
                  method_call_str("database", "save", ("one", "two"), {'foo': 'bar', 'key': 'word'}))
