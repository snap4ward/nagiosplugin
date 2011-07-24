# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

import logging
import nagiosplugin
import nagiosplugin.state
import nagiosplugin.formatter
import operator
import optparse
import signal


class Controller(object):

    def __init__(self, name, probe, evaluator, verbosity=0,
                 initial=nagiosplugin.state.Ok('')):
        self.name = name
        self.probe = probe
        self.evaluator = evaluator
        self.initial = initial
        self.state = None
        self.performance = None

    def __str__(self):
        return self.output

    def __call__(self, timeout=None):
        try:
            self._process(timeout)
        except StandardError as e:
            self.state = nagiosplugin.state.Unknown(str(e))

    def _process(self, timeout=None):
        def handle_timeout(signum, stackframe):
            raise RuntimeError(u'timeout {0} s exceeded'.format(timeout))
        signal.signal(signal.SIGALRM, handle_timeout)
        if timeout:
            signal.alarm(timeout)
        self.probe()
        signal.signal(signal.SIGALRM, signal.SIG_DFL)
        self.evaluator(self.probe)
        self.state = reduce(operator.add, self.normalized_state, self.initial)
        self.performance = self.evaluator.performance

    @property
    def normalized_state(self):
        if isinstance(self.evaluator.state, list):
            return self.evaluator.state
        else:
            return [self.evaluator.state]

    @property
    def output(self):
        f = nagiosplugin.formatter.Formatter(self.name)
        f.addstate(self.state)
        return f.render()

    @property
    def exitcode(self):
        return 0
