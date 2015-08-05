from frozendict import frozendict
from copy import deepcopy

from frozen.FrozenException import FrozenException

IMMUTABLE_TYPES = frozenset({
    int,
    float,
    complex,
    str,
    bytes,
    tuple,
    frozenset,
    frozendict
})


class frozenobject(object):
    def __init__(self, value):
        self._value = value

    def __getattribute__(self, name):
        if name == '_value':
            return super(frozenobject, self).__getattribute__('_value')

        v = getattr(self._value, name)

        if callable(v):
            return getattr(deepcopy(self._value), name)
        else:
            return freeze(v)

    def __setattribute__(self, name, value):
        raise FrozenException('Cannot alter attribute {0} of frozenobject {1}'.format(name, self._value))

    def __call__(self, *args, **kwargs):
        return self._value.__call__(*args, **kwargs)

    def __len__(self):
        return self._value.__len__()

    def __getitem__(self, index):
        if name == '_value':
            return super(Frozen, self).__getitem__(index)

        v = self._value[index]

        if v.__class__ in Frozen.IMMUTABLE_TYPES:
            return v
        else:
            return Frozen(v)

    def __setitem__(self, index, value):
        raise FrozenException('Cannot alter frozen object {0}'.format(self._value))

    def __delitem__(self, index):
        raise FrozenException('Cannot alter frozen object {0}'.format(self._value))

def immutable(thing):
    return (
        any([
            isinstance(thing, t)
            for t in IMMUTABLE_TYPES.union(frozenset({frozenobject}))
        ]) or
        callable(thing)
        )


def freeze(thing):
    if immutable(thing):
        return thing
    elif isinstance(thing, list):
        return tuple(thing)
    elif isinstance(thing, set):
        return frozenset(thing)
    elif isinstance(thing, dict):
        return frozendict(thing)
    else:
        return frozenobject(thing)
