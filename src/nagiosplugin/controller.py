# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

import logging
import nagiosplugin
import nagiosplugin.state
import nagiosplugin.formatter
import operator
import optparse
import signal
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO


class Controller(object):

    def __init__(self, name, probe, evaluator, verbosity=0,
                 initial=nagiosplugin.state.Ok()):
        self.name = name
        self.probe = probe
        self.evaluator = evaluator
        self.initial = initial
        self._setup_logger(verbosity)
        self.state = None
        self.performance = None

    def __str__(self):
        return self.output

    def __call__(self, timeout=None):
        try:
            self._process(timeout)
        except StandardError as e:
            self.state = nagiosplugin.state.Unknown(str(e))
            self.logger.exception(e)

    def _setup_logger(self, verbosity):
        self.logoutput = StringIO.StringIO()
        self.logger = logging.getLogger('nagiosplugin')
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(self.logoutput)
        if verbosity >= 2:
            handler.setLevel(logging.DEBUG)
        elif verbosity >= 1:
            handler.setLevel(logging.INFO)
        elif verbosity > 0:
            handler.setLevel(logging.WARNING)
        else:
            handler.setLevel(logging.ERROR)
        handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
        self.logger.addHandler(handler)

    def _process(self, timeout=None):
        def handle_timeout(signum, stackframe):
            raise RuntimeError(u'timeout {0} s exceeded'.format(timeout))
        signal.signal(signal.SIGALRM, handle_timeout)
        if timeout:
            signal.alarm(timeout)
        self.probe()
        signal.signal(signal.SIGALRM, signal.SIG_DFL)
        signal.alarm(0)
        self.evaluator(self.probe)
        self.state = reduce(operator.add, self.normalized_state, self.initial)
        self.performance = self.evaluator.performance

    @property
    def normalized_state(self):
        # XXX filter none
        if isinstance(self.evaluator.state, list):
            return self.evaluator.state
        else:
            return [self.evaluator.state]

    @property
    def output(self):
        f = nagiosplugin.formatter.Formatter(self.name)
        f.addstate(self.state)
        f.addlongoutput(self.logoutput.getvalue())
        return f.render()

    @property
    def exitcode(self):
        return self.state.code
