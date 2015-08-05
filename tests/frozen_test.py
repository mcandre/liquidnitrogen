from unittest import TestCase

from frozen import Frozen, FrozenException

class FrozenTest(TestCase):
    def test_frozen_object_is_immutable():
        items = Frozen([1, 2, 3])

        try:
            items.append(4)
        except FrozenException as e:
            pass

        self.assertEqual(len(items), 3)
