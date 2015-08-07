# liquidnitrogen - freeze arbitrary Python things as immutables

# HOMEPAGE

https://github.com/mcandre/liquidnitrogen

# PyPi

https://pypi.python.org/pypi/liquidnitrogen

# EXAMPLES

## freeze(list)

```
$ python
>>> from liquidnitrogen import freeze
>>> collection = freeze([1, 2, 3])
>>> collection.append(4)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'tuple' object has no attribute 'append'
>>> collection
(1, 2, 3)
```

## freeze(dict)

```
>>> collection = freeze({'a': 1, 'b': 2, 'c': 3})
>>> collection.update({'d': 4})
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'frozendict' object has no attribute 'update'
>>> collection
<frozendict {'b': 2, 'c': 3, 'a': 1}>
```

## freezemethod(obj, method_name)

Warning: `freezemethod` and `freezeobject` perform a `deepcopy` of the object's attributes upon each method call in order to test whether the method call would modify the object. The attribute copy  may use a significant amount of memory. To save memory, model data with structures designed to be immutable, such as tuples, frozensets, frozendicts, etc.

```
>>> from liquidnitrogen import frozenmethod
>>> class Pet:
    def __init__(self, breed, name):
        self.breed = breed
        self.name = name
    def set_breed(self, breed):
        self.breed = breed
    def set_name(self, name):
        self.name = name
    def __eq__(self, other):
        return self.breed == other.breed and self.name == other.name
    def __repr__(self):
        return 'Pet({0}, {1})'.format(self.breed, self.name)
>>> p = Pet('tabby', 'Cosmo')
>>> p.set_breed = frozenmethod(p, 'set_breed')
>>> p.set_breed('tiger')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/andrew/Desktop/src/liquidnitrogen/liquidnitrogen/liquidnitrogen.py", line 76, in protected_method
    .format(method_name, args, kwargs, obj)
liquidnitrogen.LiquidNitrogenException: frozenmethod call set_breed with arguments ('tiger',) {} would mutate Pet(tabby, Cosmo)
>>> p.set_name('FizzBuzz')
>>> p
Pet(tabby, FizzBuzz)
```

## freeze(obj)

```
>>> class Person:
    def __init__(self, name):
        self.name = name
    def set_name(self, name):
        self.name = name
    def __eq__(self, other):
        return self.name == other.name
    def __repr__(self):
        return 'Person({0})'.format(self.name)
>>> p = freeze(Person('Alice'))
>>> p.name = 'Bob'
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/andrew/Desktop/src/liquidnitrogen/liquidnitrogen/freeze.py", line 53, in __setattr__
    .format(name, self)
liquidnitrogen.LiquidNitrogenException: Cannot alter attribute name of frozenobject Person(Alice)
>>> p.set_name('Bob')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/andrew/Desktop/src/liquidnitrogen/liquidnitrogen/liquidnitrogen.py", line 76, in protected_method
    .format(method_name, obj)
liquidnitrogen.LiquidNitrogenException: frozenmethod call set_name with arguments ('Bob',) {} would mutate Person(Alice)
>>> p
Person(Alice)
```

# CREDITS

* `freeze(dict)` uses the [frozendict](https://pypi.python.org/pypi/frozendict) library
* `freeze(OrderedDict)` uses the [frozenordereddict](https://pypi.python.org/pypi/frozenordereddict) library
* `freeze(object)` based on Andreas Nilsson's [ActiveState recipe](http://code.activestate.com/recipes/576527-freeze-make-any-object-immutable/).

# LICENSE

FreeBSD
