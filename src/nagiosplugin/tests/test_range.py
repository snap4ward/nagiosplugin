# Copyright (c) 2010 gocept gmbh & co. kg
# See also LICENSE.txt

import unittest
from nagiosplugin.range import Range


class RangeParseTest(unittest.TestCase):

    def test_empty_range_is_zero_to_infinity(self):
        r = Range('')
        self.assertFalse(r.invert)
        self.assertEqual(r.start, 0)
        self.assertIsNone(r.end)

    def test_null_range(self):
        self.assertEqual(Range(), Range(''))
        self.assertEqual(Range(), Range(None))

    def test_explicit_start_end(self):
        r = Range('0.5:4')
        self.assertFalse(r.invert)
        self.assertEqual(r.start, 0.5)
        self.assertEqual(r.end, 4)

    def test_fail_if_start_gt_end(self):
        self.assertRaises(ValueError, Range, '4:3')

    def test_omit_start(self):
        r = Range('5')
        self.assertFalse(r.invert)
        self.assertEqual(r.start, 0)
        self.assertEqual(r.end, 5)

    def test_omit_end(self):
        r = Range('7.7:')
        self.assertFalse(r.invert)
        self.assertEqual(r.start, 7.7)
        self.assertIsNone(r.end)

    def test_start_is_neg_infinity(self):
        r = Range('~:5.5')
        self.assertFalse(r.invert)
        self.assertIsNone(r.start)
        self.assertEqual(r.end, 5.5)

    def test_invert(self):
        r = Range('@-9.1:2.6')
        self.assertTrue(r.invert)
        self.assertEqual(r.start, -9.1)
        self.assertEqual(r.end, 2.6)

    def test_range_from_range(self):
        orig = Range('@3:5')
        copy = Range(orig)
        self.assertEqual(copy, orig)

    def test_contains(self):
        r = Range('1.7:2.5')
        self.assertFalse(1.6 in r)
        self.assertTrue(1.7 in r)
        self.assertTrue(2.5 in r)
        self.assertFalse(2.6 in r)


class RangeStrTest(unittest.TestCase):

    def test_empty(self):
        self.assertEqual('', str(Range()))

    def test_explicit_start_stop(self):
        self.assertEqual('1.5:5', str(Range('1.5:5')))

    def test_omit_start(self):
        self.assertEqual('6.7', str('6.7'))

    def test_omit_end(self):
        self.assertEqual('-6.5:', str('-6.5:'))

    def test_neg_infinity(self):
        self.assertEqual('~:-3.0', str(Range('~:-3.0')))

    def test_invert(self):
        self.assertEqual('@3:7', str(Range('@3:7')))

    def test_large_number(self):
        self.assertEqual('2800000000', str(Range('2800000000')))