# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

"""Test MeasuredPerformance and Performance classes."""

import unittest

from nagiosplugin.performance import MeasuredPerformance


class TestMeasuredPerformance(unittest.TestCase):

    def test_init(self):
        mp = MeasuredPerformance(5, 's')
        self.assertEqual(mp.value, 5)
        self.assertEqual(mp.uom, 's')

    def test_should_raise_if_greater_than_maximum(self):
        self.assertRaises(ValueError, MeasuredPerformance, 11, maximum=10)

    def test_should_raise_if_less_than_minimum(self):
        self.assertRaises(ValueError, MeasuredPerformance, -0.5, minimum=0)
