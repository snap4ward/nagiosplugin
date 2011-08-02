# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

import logging
import mock
import nagiosplugin.evaluator
import nagiosplugin.probe
import optparse
import os
import signal
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from nagiosplugin import Controller


class ControllerTest(unittest.TestCase):

    def setUp(self):
        self.probe = nagiosplugin.probe.Probe()
        self.evaluator = nagiosplugin.evaluator.Evaluator()

    def test_str_before_invocation(self):
        c = Controller(u'PLUGIN', self.probe, self.evaluator)
        self.assertEqual(str(c), u'PLUGIN OK\n')

    @mock.patch('nagiosplugin.probe.Probe')
    def test_controller_calls_probe(self, probe_cls):
        mock_probe = probe_cls.return_value
        c = Controller(u'TEST', mock_probe, self.evaluator)
        c()
        mock_probe.assert_called_with()

    @mock.patch('nagiosplugin.evaluator.Evaluator')
    def test_controller_calls_evaluator(self, evaluator_cls):
        mock_evaluator = evaluator_cls.return_value
        c = Controller(u'TEST', self.probe, mock_evaluator)
        c()
        mock_evaluator.assert_called_with(self.probe)

    def test_timeout_should_raise_exception(self):
        class TimeoutProbe(nagiosplugin.probe.Probe):
            def __call__(self):
                os.kill(os.getpid(), signal.SIGALRM)
        c = Controller(u'TEST', TimeoutProbe(), self.evaluator)
        self.assertRaises(RuntimeError, c._process, 5)

    def test_call_should_catch_exceptions(self):
        class FaultyProbe(nagiosplugin.probe.Probe):
            def __call__(self):
                raise RuntimeError(u'exception message')
        c = Controller(u'TEST', FaultyProbe(), self.evaluator)
        c()
        self.assertEqual(
            c.state, nagiosplugin.state.Unknown(u'exception message'))

    def test_call_should_log_catched_exceptions(self):
        class FaultyProbe(nagiosplugin.probe.Probe):
            def __call__(self):
                raise RuntimeError(u'exception msg')
        c = Controller(u'TEST', FaultyProbe(), self.evaluator)
        c()
        self.assertRegexpMatches(c.output(), r'Traceback')
        self.assertRegexpMatches(c.output(), r'RuntimeError: exception msg')

    def test_normalize_scalar_state(self):
        self.evaluator.state = nagiosplugin.state.Ok(u'looks good')
        c = Controller(u'TEST', self.probe, self.evaluator)
        c._process()
        self.assertListEqual(c.normalized_state,
                             [nagiosplugin.state.Ok(u'looks good')])

    def test_processe_valuator_state_list(self):
        self.evaluator.state = [
            nagiosplugin.state.Ok(u's1'), nagiosplugin.state.Ok(u's2')]
        c = Controller(u'TEST', self.probe, self.evaluator)
        c._process()
        self.assertListEqual(c.normalized_state, [
            nagiosplugin.state.Ok(u's1'), nagiosplugin.state.Ok(u's2')])

    def test_normalize_state_should_filter_none(self):
        self.evaluator.state = [nagiosplugin.Ok(), None]
        c = Controller(u'TEST', self.probe, self.evaluator)
        self.assertListEqual(c.normalized_state, [nagiosplugin.Ok()])

    def test_exitcode(self):
        self.evaluator.state = nagiosplugin.state.Critical()
        c = Controller(u'TEST', self.probe, self.evaluator)
        c()
        self.assertEqual(c.exitcode, self.evaluator.state.code)

    def test_add_logoutput(self):
        class LoggingEvaluator(nagiosplugin.evaluator.Evaluator):
            def __call__(self, probe):
                log = logging.getLogger('nagiosplugin')
                log.info('log message')
        c = Controller(u'TEST', self.probe, LoggingEvaluator(), 3)
        c()
        self.assertTrue(u'log message' in c.output(),
                        u'log message not found in {0}'.format(c.output()))

    def test_normalized_performance_should_convert_to_dict(self):
        self.evaluator.performance = nagiosplugin.Performance(1, u's')
        c = Controller(u'TEST', self.probe, self.evaluator)
        c()
        self.assertDictEqual(c.normalized_performance,
                             {u'test': nagiosplugin.Performance(1, u's')})

    def test_process_should_add_performance(self):
        self.evaluator.performance = {'p1': nagiosplugin.Performance(1, u's')}
        c = Controller(u'TEST', self.probe, self.evaluator)
        c()
        self.assertRegexpMatches(c.output(), r'p1=1s')
