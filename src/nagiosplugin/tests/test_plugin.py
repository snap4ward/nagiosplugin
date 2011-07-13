# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

"""Test the default plugin implementation."""

import nagiosplugin
import nagiosplugin.plugin
import nagiosplugin.tests
import nagiosplugin.state

from nagiosplugin import Plugin


class PluginTest(nagiosplugin.tests.TestCase):

    def test_setup_creates_probe_and_evaluator(self):
        p = Plugin()
        p.setup({}, [])
        self.assertIsInstance(p.probe, nagiosplugin.Probe)
        self.assertIsInstance(p.evaluator, nagiosplugin.Evaluator)

    def test_status_combines_status_messages(self):
        p = Plugin()
        s1 = nagiosplugin.state.Ok('first msg')
        s2 = nagiosplugin.state.Ok('second msg')
        self.assertListEqual(
            ['first msg', 'second msg'], p.message([s1, s2]))
