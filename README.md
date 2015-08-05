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
```

# CREDITS

* `freeze(dict)` uses the [frozendict](https://pypi.python.org/pypi/frozendict) library
* `freeze(object)` based on Andreas Nilsson's [ActiveState recipe](http://code.activestate.com/recipes/576527-freeze-make-any-object-immutable/).
