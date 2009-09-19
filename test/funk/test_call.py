from funk import Call

def test_has_name_returns_true_if_passed_name_matches_method_name():
    call = Call('save')
    assert call.has_name('save')
    assert not call.has_name('saved')
    assert not call.has_name('sav')

def test_returns_none_if_no_return_value_specified():
    call = Call('save')
    assert call() is None

def test_returns_return_value_if_set():
    return_value = 'Oh noes!'
    call = Call('save')
    call.returns(return_value)
    assert call() is return_value

def test_accepts_returns_true_if_with_args_not_called():
    call = Call('save')
    assert call.accepts((), {})
    assert call.accepts((1, 2, 3), {"name": "Bob"})

def test_accepts_returns_true_if_arguments_match_those_set_by_with_args():
    call = Call('save')
    call.with_args(1, 2, name="Bob")
    assert not call.accepts((), {})
    assert not call.accepts((1, 2, 3), {"name": "Bob"})
    assert not call.accepts((1, ), {"name": "Bob"})
    assert call.accepts((1, 2), {"name": "Bob"})
