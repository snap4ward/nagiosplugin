# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

from nagiosplugin.performance import Performance

import nagiosplugin
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class PerformanceTest(unittest.TestCase):

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

    def test_should_raise_if_less_than_minimum(self):
        self.assertRaises(ValueError, Performance,
                          -0.5, minimum=0)

    def test_should_raise_if_greater_than_maximum(self):
        self.assertRaises(ValueError, Performance, 11,
                          maximum=10)

    def test_str_naked_value(self):
        self.assertEqual('26', str(Performance(26)))

    def test_str_value_uom_warn_crit(self):
        self.assertEqual(
            '42bps;10:100;500',
            str(Performance(42, 'bps', warning='10:100', critical='500')))

    def test_str_value_minimum(self):
        self.assertEqual('-35;;;;0', str(Performance(-35, maximum=0)))

    def test_replace_warning_critical(self):
        p = Performance(3, 's', 0, 100)
        self.assertEqual(p.replace(warning='1:3', critical='~:5'),
                         Performance(3, 's', 0, 100, '1:3', '~:5'))

    def test_replace_threshold(self):
        p = Performance(3, 's', 0, 100)
        self.assertEqual(p.replace(threshold=nagiosplugin.Threshold('3', '5')),
                         Performance(3, 's', 0, 100, '3', '5'))
