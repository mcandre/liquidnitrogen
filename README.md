# frozen - freeze arbitrary Python things as immutables

# EXAMPLES

```
$ python
>>> from frozen import freeze
>>> collection = freeze([1, 2, 3])
>>> collection.append(4)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'tuple' object has no attribute 'append'
>>> collection
(1, 2, 3)

>>> collection = freeze({'a': 1, 'b': 2, 'c': 3})
>>> collection.update({'d': 4})
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'frozendict' object has no attribute 'update'
>>> collection
<frozendict {'b': 2, 'c': 3, 'a': 1}>

>>> class Person:
    def __init__(self, name):
        self.name = name
    def __eq__(self, other):
        return self.name == other.name
    def set_name(self, name):
        self.name = name

>>> class Person:
...     def __init__(self, name):
...         self.name = name
...     def set_name(self, name):
...         self.name = name
...     def __eq__(self, other):
...         return self.name == other.name
...     def __repr__(self):
...         return 'Person({0})'.format(self.name)
...
>>> p = freeze(Person('Alice'))
>>> p.name = 'Bob'
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/andrew.pennebaker/Desktop/src/frozen/frozen/freeze.py", line 53, in __setattr__
    .format(name, self)
frozen.FrozenException.FrozenException: Cannot alter attribute name of frozenobject Person(Alice)
>>> p.set_name('Bob')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/andrew.pennebaker/Desktop/src/frozen/frozen/freeze.py", line 76, in protected_method
    .format(method_name, obj)
frozen.FrozenException.FrozenException: Call would mutate frozenmethod set_name on Person(Alice)
>>> p
Person(Alice)
```

# CREDITS

* `freeze(dict)` uses the [frozendict](https://pypi.python.org/pypi/frozendict) library
* `freeze(object)` based on Andreas Nilsson's [ActiveState recipe](http://code.activestate.com/recipes/576527-freeze-make-any-object-immutable/).
