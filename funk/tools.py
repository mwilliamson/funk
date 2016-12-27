class ValueObject(object):
    def __init__(self, attributes):
        self._keys = attributes.keys()
        for key in attributes:
            setattr(self, key, attributes[key])

    def __str__(self):
        attributes = {}
        for key in self._keys:
            attributes[key] = getattr(self, key)
        return "<value_object: %s>" % attributes
    
    def __repr__(self):
        return str(self)

def value_object(**kwargs):
    return ValueObject(kwargs)
