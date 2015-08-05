from frozen.FrozenException import FrozenException

class Frozen:
    IMMUTABLE_TYPES = frozenset({
        int,
        float,
        complex,
        str,
        bytes,
        tuple,
        frozenset
    })

    def __init__(self, value):
        self._value = value

    def __getattribute__(self, name):
        if name == '_value':
            return super(Frozen, self).__getattribute__(name)

        v = getattr(self._value, name)

        if v.__class__ in Frozen.IMMUTABLE_TYPES:
            return v
        else:
            return Frozen(v)

    def __setattribute__(self, name, value):
        if name == '_value':
            super(Frozen, self).__setattr__(name, value)
        else:
            raise FrozenException('Cannot modify frozen object {0}'.format(self._value))
