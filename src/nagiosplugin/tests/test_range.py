# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

import unittest

from nagiosplugin.range import Range


class RangeParseTest(unittest.TestCase):

    def test_empty_range_is_zero_to_infinity(self):
        r = Range('')
        self.failIf(r.match(-0.1))
        self.failUnless(r.match(0))
        self.failUnless(r.match(1000000))

    def test_none_range(self):
        self.assertEqual(Range(None), Range(''))

    def test_explicit_start_end(self):
        r = Range('0.5:4')
        self.failIf(r.match(0.4))
        self.failUnless(r.match(0.5))
        self.failUnless(r.match(4))
        self.failIf(r.match(5))

    def test_fail_if_start_gt_end(self):
        self.assertRaises(ValueError, Range, '4:3')

    def test_omit_start(self):
        r = Range('5')
        self.failIf(r.match(-0.1))
        self.failUnless(r.match(0))
        self.failUnless(r.match(5))
        self.failIf(r.match(5.1))

    def test_omit_end(self):
        r = Range('7.7:')
        self.failIf(r.match(7.6))
        self.failUnless(r.match(7.7))
        self.failUnless(r.match(1000000))

    def test_start_is_neg_infinity(self):
        r = Range('~:5.5')
        self.failUnless(r.match(-1000000))
        self.failUnless(r.match(5.5))
        self.failIf(r.match(5.6))

    def test_invert(self):
        r = Range('@-9.1:2.6')
        self.failUnless(r.match(-9.2))
        self.failIf(r.match(-9.1))
        self.failIf(r.match(2.6))
        self.failUnless(r.match(2.7))

    def test_compare_invert(self):
        (a, b) = ('', '@')
        self.failIf(Range(a) == Range(b))
        self.failUnless(Range(a) != Range(b))

    def test_compare_start(self):
        (a, b) = ('2.2:', '4:')
        self.failIf(Range(a) == Range(b))
        self.failUnless(Range(a) != Range(b))

    def test_compare_end(self):
        (a, b) = ('9.7', '4.2')
        self.failIf(Range(a) == Range(b))
        self.failUnless(Range(a) != Range(b))

    def test_range_from_range(self):
        orig = Range('@3:5')
        copy = Range(orig)
        self.assertEqual(copy, orig)
        self.assertNotEqual(hash(copy), hash(orig))


class RangeStrTest(unittest.TestCase):

    def setUp(self):
        self.r = Range()

    def test_empty(self):
        self.assertEqual('', str(self.r))

    def test_explicit_start_stop(self):
        (self.r.start, self.r.end) = (1.5, 5)
        self.assertEqual('1.5:5', str(self.r))

    def test_omit_start(self):
        self.r.end = 6.7
        self.assertEqual('6.7', str(self.r))

    def test_omit_end(self):
        self.r.start = -6.5
        self.assertEqual('-6.5:', str(self.r))

    def test_neg_infinity(self):
        (self.r.start, self.r.end) = (None, -3.0)
        self.assertEqual('~:-3.0', str(self.r))

    def test_invert(self):
        (self.r.invert, self.r.start, self.r.end) = (True, 3, 7)
        self.assertEqual('@3:7', str(self.r))

    def test_large_number(self):
        self.r.end = 2800000000
        self.assertEqual('2800000000', str(self.r))
