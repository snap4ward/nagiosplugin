# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

import functools
import logging
import nagiosplugin
import nagiosplugin.old.pluginoptparse
import operator
import warnings


class AdapterEvaluator(object):

    def __init__(self, check_cls, argv):
        warnings.warn(u'Old nagiosplugin API detected. '
                      u'Port your check to the new API.', DeprecationWarning)
        self.optparser = nagiosplugin.old.pluginoptparse.PluginOptionParser()
        self.optparser.add_option('-V', '--version', action='version',
                help=u'print version and exit')
        self.optparser.add_option('-v', '--verbose', action='count',
                default=0, help=u'increase output verbosity (up to 3 times)')
        self.optparser.add_option('-t', '--timeout', metavar='TIMEOUT',
                default=15, type='int',
                help=u'abort execution after TIMEOUT seconds '
                     u'(default: %default)')
        self.logger = logging.getLogger('nagiosplugin')
        self.check = check_cls(self.optparser, self.logger)
        self.stderr = u''
        self.exitcode = None
        self.states = []
        self.performances = []
        self.dominant_state = nagiosplugin.state.Unknown()
        (self.opts, self.args) = self.optparser.parse_args(argv)
        self.loglevel = max((40 - self.opts.verbose * 10, 10))

    def evaluate(self):
        """Run, but interrupt check if it takes longer than the timeout."""
        self.states = []
        self.performances = []
        self.run_inner()
        try:
            self.dominant_state = functools.reduce(
                operator.add, self.states, nagiosplugin.Ok())
        except TypeError:
            pass
        self.exitcode = self.dominant_state.code

    def run_inner(self):
        """Perform check action."""
        msg = self.check.process_args(self.opts, self.args)
        if msg:
            raise RuntimeError(msg)
        self.check.obtain_data()
        self.states = self.check.states()
        self.performances = self.check.performances()
        if self.check.default_message():
            self.states.append(nagiosplugin.Ok(
                self.check.default_message()))

    def state(self):
        return self.dominant_state

    def performance(self):
        return self.performances
