# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

"""Test MeasuredPerformance and Performance classes."""

import nagiosplugin
import nagiosplugin.tests
import unittest

from nagiosplugin.performance import MeasuredPerformance, Performance


class MeasuredPerformanceTest(unittest.TestCase):

    def test_should_raise_if_greater_than_maximum(self):
        self.assertRaises(ValueError, MeasuredPerformance, 11, maximum=10)

    def test_should_raise_if_less_than_minimum(self):
        self.assertRaises(ValueError, MeasuredPerformance, -0.5, minimum=0)

    def test_repr(self):
        self.assertEqual("MeasuredPerformance(3, 'B', 0, None)",
                         repr(MeasuredPerformance(3, 'B', 0)))

    def test_eq(self):
        self.assertEqual(MeasuredPerformance(1, 's', 0, 100),
                         MeasuredPerformance(1, 's', 0, 100))
        self.assertNotEqual(MeasuredPerformance(1, 's', 0, 100),
                            MeasuredPerformance(1, 's'))


class PerformanceTest(nagiosplugin.tests.TestCase):

    def test_eq(self):
        self.assertEqual(Performance(10, 'B', 0, critical='1:'),
                         Performance(10, 'B', 0, critical='1:'))
        self.assertNotEqual(Performance(10, 'B', 0, critical='1:'),
                            Performance(11, 'B', 0, critical='1:'))

    def test_eq_measuredperformance(self):
        self.assertEqual(Performance(10, 'B', 0, 1024),
                         MeasuredPerformance(10, 'B', 0, 1024))
        self.assertNotEqual(Performance(-5, critical='1:'),
                            MeasuredPerformance(-5))

    def test_repr(self):
        self.assertEqual("Performance(3, 'B', 0, None, '1:3', '5')",
                         repr(Performance(3, 'B', 0, warning='1:3',
                              critical='5')))

    def test_init_should_accept_measuredperformance_object(self):
        mp = MeasuredPerformance(5, 's', -100, 100)
        p = Performance(mp)
        self.assertEqual(p.value, mp.value)
        self.assertEqual(p.uom, mp.uom)
        self.assertEqual(p.minimum, mp.minimum)
        self.assertEqual(p.maximum, mp.maximum)

    def test_init_should_accept_performance_object(self):
        p1 = Performance(100, minimum=0, critical='200')
        p2 = Performance(p1)
        self.assertEqual(p1, p2)

    def test_init_should_build_range_objects(self):
        p = Performance(0, warning='-5:5', critical='~:10')
        self.assertIsInstance(p.warning, nagiosplugin.Range)
        self.assertIsInstance(p.critical, nagiosplugin.Range)

    def test_init_should_accept_threshold_object(self):
        p = Performance(0, threshold=nagiosplugin.Threshold('5', '10'))
        self.assertEqual(p.warning, nagiosplugin.Range('5'))
        self.assertEqual(p.critical, nagiosplugin.Range('10'))

    def test_init_should_fail_if_both_threshold_and_warncrit_are_given(self):
        self.assertRaises(ValueError, Performance, 51,
                          warning='3', critical='23',
                          threshold=nagiosplugin.Threshold('45:', '5:'))
