from unittest import TestCase

from frozen import freeze, FrozenException


class FrozenTest(TestCase):
    def test_frozen_list_is_immutable(self):
        collection = freeze([1, 2, 3])

        try:
            collection.append(4)
        except AttributeError:
            pass

        self.assertEqual(collection, (1, 2, 3))

    def test_frozen_dict_is_immutable(self):
        collection = freeze({'a': 1, 'b': 2, 'c': 3})

        try:
            collection.update({'d': 4})
        except AttributeError:
            pass

        self.assertEqual(collection, {'a': 1, 'b': 2, 'c': 3})

    def test_frozen_object_is_immutable(self):
        class Person:
            def __init__(self, name):
                self.name = name

            def __eq__(self, other):
                return self.name == other.name

            def set_name(self, name):
                self.name = name

        p = freeze(Person('Alice'))

        try:
            p.name = 'Bob'
        except FrozenException:
            pass

        p.set_name('Bob')

        self.assertEqual(p, Person('Alice'))
