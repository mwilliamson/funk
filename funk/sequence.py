class Sequence(object):
    def __init__(self):
        self._expected_calls = []
    
    def add_expected_call(self, call):
        self._expected_calls.append(call)
        
    def add_actual_call(self, call):
        if call is not self._expected_calls[0]:
            raise AssertionError("Invocation out of order. Expected %s, but got %s." % (self._expected_calls[0], call))

