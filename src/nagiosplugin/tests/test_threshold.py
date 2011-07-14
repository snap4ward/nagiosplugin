# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

"""Define tests for Threshold objects."""

import nagiosplugin
import nagiosplugin.state
import nagiosplugin.tests

from nagiosplugin.threshold import Threshold


class ThresholdTests(nagiosplugin.tests.TestCase):

    def test_init_should_fail_if_neither_range_given(self):
        self.assertRaises(ValueError, Threshold)

    def test_in_both_ranges_should_return_ok(self):
        t = Threshold(nagiosplugin.Range('5'), nagiosplugin.Range('6'))
        self.assertIsInstance(t.match(3), nagiosplugin.state.Ok)

    def test_in_crit_range_should_return_warning(self):
        t = Threshold(nagiosplugin.Range('1'), nagiosplugin.Range('3'))
        self.assertIsInstance(t.match(2), nagiosplugin.state.Warning)

    def test_outside_both_ranges_should_return_critical(self):
        t = Threshold(nagiosplugin.Range('1'), nagiosplugin.Range('2'))
        self.assertIsInstance(t.match(3), nagiosplugin.state.Critical)

    def test_omit_warning(self):
        t = Threshold(critical=nagiosplugin.Range('1:3'))
        self.assertIsInstance(t.match(2), nagiosplugin.state.Ok)

    def test_omit_critical(self):
        t = Threshold(warning=nagiosplugin.Range('1:3'))
        self.assertIsInstance(t.match(2), nagiosplugin.state.Ok)
