from inspect import isfunction
from datetime import datetime
from collections import OrderedDict

from frozendict import frozendict
from frozenordereddict import FrozenOrderedDict
from copy import deepcopy

from liquidnitrogen.exceptions import LiquidNitrogenException

IMMUTABLE_TYPES = frozenset({
    int,
    float,
    complex,
    str,
    bytes,
    tuple,
    frozenset,
    datetime,
    frozendict,
    FrozenOrderedDict
})


def isimmutable(thing):
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
            raise LiquidNitrogenException(
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
            raise LiquidNitrogenException(
                'frozenmethod call {0} with arguments {1} {2} would mutate {3}'
                .format(method_name, args, kwargs, obj)
            )

    return protected_method

def freeze(thing):
    '''
        Given a Python value, return an immutable version of the value.

        Natively immutable values such as tuples, frozensets, and frozendicts are simply returned as-is.

        Methods and objects are wrapped to raise LiquidNitrogenExceptions on attempts to set attributes or call methods that would mutate the objects.

        Warning: `freezemethod` and `freezeobject` perform a `deepcopy` of the object's attributes upon each method call in order to test whether the method call would modify the object. The attribute copy  may use a significant amount of memory. To save memory, model data with structures designed to be immutable, such as tuples, frozensets, frozendicts, etc.

        :param value: a Python value (an object or primitive)
        :return a frozen version of the value
    '''

    if isimmutable(thing):
        return thing
    elif isinstance(thing, list):
        return tuple(thing)
    elif isinstance(thing, set):
        return frozenset(thing)
    elif isinstance(thing, OrderedDict):
        return FrozenOrderedDict(thing)
    elif isinstance(thing, dict):
        return frozendict(thing)
    else:
        return frozenobject(thing)
