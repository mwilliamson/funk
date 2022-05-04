from nose.tools import assert_equals

from funk.util import arguments_str
from funk.util import function_call_str
from funk.util import method_call_str
from funk.util import function_call_str_multiple_lines

def test_arguments_str_shows_positional_and_keyword_arguments():
    assert_equals('1, two, foo=bar, key=word',
                  arguments_str((1, "two"), {'foo': 'bar', 'key': 'word'}))

def test_function_call_str_shows_name_of_function_and_arguments():
    assert_equals('save(1, two, foo=bar, key=word)',
                  function_call_str("save", (1, "two"), {'foo': 'bar', 'key': 'word'}))

def test_method_call_str_shows_name_of_object_and_method_and_arguments():
    assert_equals('database.save(1, two, foo=bar, key=word)',
                  method_call_str("database", "save", (1, "two"), {'foo': 'bar', 'key': 'word'}))

def test_function_call_str_multiple_lines_displays_arguments_on_separate_lines():
    assert_equals('save(1,\n     two,\n     foo=bar,\n     key=word)',
                  function_call_str_multiple_lines("save", (1, "two"), {'foo': 'bar', 'key': 'word'}))
