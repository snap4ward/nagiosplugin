# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

import optparse
import unittest
import nagiosplugin.controller

from nagiosplugin.controller import Controller


class ControllerTest(unittest.TestCase):

    def test_init_should_fail_without_plugin_instance(self):
        self.assertRaises(ValueError, Controller, 'foo')

    def test_controller_calls_cmdline(self):
        class CmdlineCheck(nagiosplugin.Plugin):
            def cmdline(plugin, o):
                self.assertIsInstance(o, optparse.OptionParser)
                plugin.called = True
        plugin = CmdlineCheck()
        c = Controller(plugin)
        c()
        self.assert_(plugin.called)
