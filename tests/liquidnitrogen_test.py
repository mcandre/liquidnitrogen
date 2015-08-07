from unittest import TestCase
from collections import OrderedDict
from datetime import datetime
from pytz import utc

from liquidnitrogen import freeze, frozenmethod, LiquidNitrogenException


class LiquidNitrogenTest(TestCase):
    def test_can_freeze_native_immutables(self):
        self.assertEqual(freeze(0), 0)
        self.assertEqual(freeze(1.5), 1.5)
        self.assertEqual(freeze(complex(1, 1)), complex(1, 1))
        self.assertEqual(freeze('a'), 'a')
        self.assertEqual(freeze('a'.encode('utf-8')), 'a'.encode('utf-8'))
        self.assertEqual(freeze((1, 2, 3)), (1, 2, 3))
        self.assertEqual(freeze(frozenset({1, 2, 3})), frozenset({1, 2, 3}))

        add = lambda x, y: x + y

        self.assertEqual(freeze(add), add)

        t = datetime.now()
        t2 = freeze(t)
        t2.replace(tzinfo=utc)

        self.assertEqual(t2, t)

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

    def test_frozen_ordered_dict_is_immutable(self):
        collection = freeze(OrderedDict([('a', 1), ('b', 2), ('c', 3)]))

        try:
            collection.update(('d', 4))
        except AttributeError:
            pass

        self.assertEqual(collection, OrderedDict([('a', 1), ('b', 2), ('c', 3)]))

    def test_frozen_object_is_immutable(self):
        class Person:
            def __init__(self, name):
                self.name = name

            def __eq__(self, other):
                return self.name == other.name

            def __repr__(self):
                return 'Person({0})'.format(self.name)

            def set_name(self, name):
                self.name = name

        p = freeze(Person('Alice'))

        def try_to_set_name_attribute():
            p.name = 'Bob'

        self.assertRaises(
            LiquidNitrogenException,
            try_to_set_name_attribute
        )

        def try_to_use_name_set_method():
            p.set_name('Bob')

        self.assertRaises(
            LiquidNitrogenException,
            try_to_use_name_set_method
        )

        self.assertEqual(p, Person('Alice'))

    def test_frozen_method_is_immutable(self):
        class Pet:
            def __init__(self, breed, name):
                self.breed = breed
                self.name = name

            def __eq__(self, other):
                return self.breed == other.breed and self.name == other.name

            def __repr__(self):
                return 'Pet({0}, {1})'.format(self.breed, self.name)

            def set_breed(self, breed):
                self.breed = breed

            def set_name(self, name):
                self.name = name

        p = Pet('tabby', 'Cosmo')
        p.set_breed = frozenmethod(p, 'set_breed')

        def try_to_use_breed_set_method():
            p.set_breed('tiger')

        self.assertRaises(
            LiquidNitrogenException,
            try_to_use_breed_set_method
        )

        p.set_name('FizzBuzz')

        self.assertEqual(p, Pet('tabby', 'FizzBuzz'))
