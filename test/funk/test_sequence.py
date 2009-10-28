from funk.sequence import Sequence
from funk.tools import assert_raises_str

def test_sequences_do_not_raise_assertions_when_called_in_correct_order():
    class StubbedCall(object):
        def __init__(self, name):
            self._name = name
        
        def __str__(self):
            return self._name
            
        def is_satisfied(self):
            return True
            
    first_call = StubbedCall("hand(in=hand)")
    second_call = StubbedCall("why(worry)")
    
    sequence = Sequence()
    sequence.add_expected_call(first_call)
    sequence.add_expected_call(second_call)
    
    sequence.add_actual_call(first_call)
    sequence.add_actual_call(second_call)

def test_sequence_raises_assertion_error_if_actual_call_out_of_order():
    class StubbedCall(object):
        def __init__(self, name):
            self._name = name
        
        def __str__(self):
            return self._name
            
        def is_satisfied(self):
            return False
            
    first_call = StubbedCall("hand(in=hand)")
    second_call = StubbedCall("why(worry)")
    
    sequence = Sequence()
    sequence.add_expected_call(first_call)
    sequence.add_expected_call(second_call)
    assert_raises_str(AssertionError,
                      "Invocation out of order. Expected hand(in=hand), but got why(worry).",
                      lambda: sequence.add_actual_call(second_call))
    
    
def test_sequence_allows_progression_in_sequence_if_current_call_count_is_satisifed():
    class StubbedCall(object):
        def __init__(self, name):
            self._name = name
        
        def __str__(self):
            return self._name
            
        def is_satisfied(self):
            return True
    
    first_call = StubbedCall("hand(in=hand)")
    second_call = StubbedCall("why(worry)")
    
    sequence = Sequence()
    sequence.add_expected_call(first_call)
    sequence.add_expected_call(second_call)
    
    sequence.add_actual_call(second_call)

def test_assertion_error_is_raised_when_we_have_an_expected_call():
    class StubbedCall(object):
        def __init__(self, name):
            self._name = name
        
        def __str__(self):
            return self._name
            
        def is_satisfied(self):
            return True
    
    first_call = StubbedCall("hand(in=hand)")
    second_call = StubbedCall("why(worry)")
    
    sequence = Sequence()
    sequence.add_expected_call(first_call)
    sequence.add_expected_call(second_call)
    
    sequence.add_actual_call(second_call)
    assert_raises_str(AssertionError,
                      'Invocation out of order. Expected no more calls in sequence, but got hand(in=hand).',
                      lambda: sequence.add_actual_call(first_call))
