# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

"""Define tests for Threshold objects."""

import nagiosplugin
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from nagiosplugin.threshold import Threshold


class ThresholdTests(unittest.TestCase):

    def test_threshold_should_build_range_objects(self):
        t = Threshold('0', '20')
        self.assertIsInstance(t.warning, nagiosplugin.Range)
        self.assertIsInstance(t.critical, nagiosplugin.Range)

    def test_in_both_ranges_should_return_ok(self):
        t = Threshold(nagiosplugin.Range('5'), nagiosplugin.Range('6'))
        self.assertIsInstance(t.match(3), nagiosplugin.Ok)

    def test_in_crit_range_should_return_warning(self):
        t = Threshold(nagiosplugin.Range('1'), nagiosplugin.Range('3'))
        self.assertIsInstance(t.match(2), nagiosplugin.Warning)

    def test_outside_both_ranges_should_return_critical(self):
        t = Threshold(nagiosplugin.Range('1'), nagiosplugin.Range('2'))
        self.assertIsInstance(t.match(3), nagiosplugin.Critical)

    def test_omit_warning(self):
        t = Threshold(critical=nagiosplugin.Range('1:3'))
        self.assertIsInstance(t.match(2), nagiosplugin.Ok)

    def test_omit_critical(self):
        t = Threshold(warning=nagiosplugin.Range('1:3'))
        self.assertIsInstance(t.match(2), nagiosplugin.Ok)

    def test_match_should_return_unknown_on_invalid_value(self):
        t = Threshold(critical=nagiosplugin.Range('3'))
        self.assertIsInstance(t.match(None), nagiosplugin.Unknown)

    def test_specific_message(self):
        t = Threshold(warning='1:5')
        state = t.match(6, {'WARNING': 'warning message'})
        self.assertEqual(['warning message'], state.messages)

    def test_default_message(self):
        t = Threshold(critical='3')
        state = t.match(-1, {'DEFAULT': 'default message'})
        self.assertEqual(['default message'], state.messages)

    def test_create_multi_should_create_min_empty_thresholds(self):
        self.assertListEqual([Threshold(), Threshold(), Threshold()],
                             Threshold.create_multi([], [], min_len=3))

    def test_create_multi_should_zip_ranges(self):
        self.assertListEqual([Threshold('2', '4'), Threshold('3', '5')],
                             Threshold.create_multi(['2', '3'], ['4', '5']))

    def test_create_multi_should_fill_missing_elements(self):
        self.assertListEqual([Threshold('1', '3'), Threshold('2', '3')],
                             Threshold.create_multi(['1', '2'], ['3']))

    def test_create_multi_should_fill_with_none_on_empty_list(self):
        self.assertListEqual([Threshold('1'), Threshold('2'), Threshold()],
                             Threshold.create_multi(['1', '2'], [], 3))

    def test_match_should_replace_value(self):
        self.assertEqual(Threshold().match(
            4.5, {'DEFAULT': 'value is $value'}).headline,
            'value is 4.5')

    def test_match_should_replace_range(self):
        self.assertEqual(Threshold('2:3', '1:4').match(
            4.5, {'DEFAULT': 'range is $range'}).headline,
            'range is 1:4')

    def test_match_should_tolerate_none(self):
        self.assertEqual(Threshold().match(
            4.5, {'DEFAULT': None}).headline,
            None)
