# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

from nagiosplugin.valueobj import ValueObject

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class SlotlessValue(ValueObject):

    pass


class MyVal(ValueObject):

    __slots__ = ['integer', 'string', 'l', '_private']


class ValueObjectTest(unittest.TestCase):

    def test_init_without_slots_should_fail(self):
        self.assertRaises(AssertionError, SlotlessValue)

    def test_disallow_attribute_modification(self):
        v = MyVal(attr=1)
        with self.assertRaises(AttributeError):
            v.attr = 2

    def test_disallow_attribute_deletion(self):
        v = MyVal(attr=1)
        with self.assertRaises(AttributeError):
            del v.attr

    def test_repr(self):
        v = MyVal(integer=1, string='hello')
        self.assertEqual(repr(v), "MyVal(integer=1, string='hello')")

    def test_eq(self):
        self.assertTrue(MyVal(integer=1) == MyVal(integer=1))
        self.assertFalse(MyVal(integer=1, l=[1]) == MyVal(integer=1, l=[2]))

    def test_ne(self):
        self.assertNotEqual(MyVal(integer=1), MyVal(integer=2))
        self.assertNotEqual(MyVal(integer=1), 1)

    def test_hash(self):
        v1 = MyVal(integer=1, string='foo')
        v2 = MyVal(integer=1, string='foo')
        self.assertEqual(hash(v1), hash(v2))
        self.assertEqual(v1, v2)

    def test_hash_with_unhashable_attribute(self):
        v1 = MyVal(integer=2, l=['foo', 'bar'])
        v2 = MyVal(integer=2, l=['foo', 'bar'])
        self.assertEqual(hash(v1), hash(v2))
        self.assertEqual(v1, v2)

    def test_replace_nothing(self):
        v1 = MyVal(integer=1, string='bar')
        v2 = v1.replace()
        self.assertEqual(v1, v2)

    def test_replace_attribute(self):
        v1 = MyVal(integer=1, string='foo')
        v2 = v1.replace(string='bar')
        self.assertEqual(v2, MyVal(integer=1, string='bar'))

    def test_replace_should_ignore_private_attributes(self):
        v1 = MyVal(integer=1, string='foo', _private=True)
        v2 = v1.replace(l=[1, 2, 3])
        self.assertEqual(v2, MyVal(integer=1, string='foo', l=[1, 2, 3]))
