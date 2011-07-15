# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

import nagiosplugin.controller
import nagiosplugin.tests
import optparse
import os
import signal

from nagiosplugin.controller import Controller


class ControllerTest(nagiosplugin.tests.TestCase):

    def test_init_should_fail_without_plugin_instance(self):
        self.assertRaises(ValueError, Controller, 'foo')

    def test_controller_calls_commandline(self):
        class CmdlineCheck(nagiosplugin.Plugin):
            def commandline(plugin, o):
                self.assertIsInstance(o, optparse.OptionParser)
                plugin.called = True
        plugin = CmdlineCheck()
        c = Controller(plugin)
        c()
        self.assert_(plugin.called)

    def test_controller_calls_setup(self):
        class SetupCheck(nagiosplugin.Plugin):
            def setup(plugin, opts, args):
                super(SetupCheck, plugin).setup(opts, args)
                plugin.called = True
        plugin = SetupCheck()
        c = Controller(plugin)
        c()
        self.assert_(plugin.called)

    def test_controller_calls_probe(self):
        class ProbeCheck(nagiosplugin.Plugin):
            def probe(plugin):
                plugin.called = True
        plugin = ProbeCheck()
        c = Controller(plugin)
        c()
        self.assert_(plugin.called)

    def test_controller_calls_evaluator(self):
        class EvaluatorCheck(nagiosplugin.Plugin):
            def evaluator(plugin, probe):
                plugin.called = True
        plugin = EvaluatorCheck()
        c = Controller(plugin)
        c()
        self.assert_(plugin.called)

    def test_timeout_should_raise_exception(self):
        class TimeoutCheck(nagiosplugin.Plugin):
            def probe(self):
                os.kill(os.getpid(), signal.SIGALRM)
        c = Controller(TimeoutCheck())
        self.assertRaises(RuntimeError, c)
