from inspect import isfunction

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


def immutable(thing):
    return (
        any([
            isinstance(thing, t)
            for t in IMMUTABLE_TYPES.union(frozenset({frozenobject}))
        ]) or
        isfunction(thing)
    )


class frozenobject(object):
    def __init__(self, value):
        self._value = value

    def __getattribute__(self, name):
        if name == '_value':
            return super(frozenobject, self).__getattribute__('_value')

        attribute = getattr(self._value, name)

        # protect methods from mutation
        if callable(attribute) and not isfunction(attribute):
            return frozenmethod(self._value, name)
        # protect non-method attributes from mutation
        else:
            return freeze(attribute)

    def __setattr__(self, name, value):
        if name == '_value':
            super(frozenobject, self).__setattr__('_value', value)
        else:
            raise FrozenException(
                'Cannot alter attribute {0} of frozenobject {1}'
                .format(name, self)
            )

    def __call__(self, *args, **kwargs):
        return self._value.__call__(*args, **kwargs)

    def __repr__(self):
        return self._value.__repr__()


def frozenmethod(obj, method_name):
    obj_copy = deepcopy(obj)
    method_copy = getattr(obj_copy, method_name)

    def protected_method(*args, **kwargs):
        result = method_copy(*args, **kwargs)

        # Has the copy mutated compared to the original?
        if obj_copy == obj:
            return result
        else:
            raise FrozenException(
                'frozenmethod call {0} with arguments {1} {2} would mutate {3}'
                .format(method_name, args, kwargs, obj)
            )

    return protected_method

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
