# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

"""Overall plugin execution logic"""

import logging
import nagiosplugin
import nagiosplugin.state
import nagiosplugin.formatter
import operator
import signal
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO


class Controller(object):
    """Aid orchestration of various plugin components.

    A Controller takes several subordinate objects and "puts everything
    together":

        - plugin name
        - probe object
        - evaluator object
    """

    def __init__(self, name, probe, evaluator, verbosity=0,
                 initial=nagiosplugin.state.Ok()):
        """Create Controller object.

        `name` is the short plugin name that appears first in the
        output.
        `probe` is an object which supports the Probe protocol.
        `evaluator` is an object which supports the Evaluator protocol.
        `verbosity` is an integer which controls the amount of logging
        output to be included in the plugin's long outout.
        `initial` is the initial plugin state if the Evaluator does not
        specify something else.
        """
        self.name = name
        self.probe = probe
        self.evaluator = evaluator
        self._setup_logger(verbosity)
        self.state = initial
        self.initial = initial
        self.performance = None

    def __str__(self):
        """Complete plugin output as string."""
        return self.output()

    def __call__(self, timeout=None):
        """Perform plugin execution.

        Call both probe and evaluator in a controlled environment.
        After `timeout` seconds, abort execution and set an Unknown
        state. If any exceptions occurs, set an Unknown state with the
        exception message, too.
        """
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
        if verbosity > 2:
            handler.setLevel(logging.DEBUG)
        elif verbosity > 1:
            handler.setLevel(logging.INFO)
        elif verbosity > 0:
            handler.setLevel(logging.WARNING)
        else:
            handler.setLevel(logging.ERROR)
        handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
        self.logger.addHandler(handler)

    def _process(self, timeout=None):
        def handle_timeout(signum, stackframe):
            signal.alarm(0)
            raise RuntimeError(u'timeout {0} s exceeded'.format(timeout))
        signal.signal(signal.SIGALRM, handle_timeout)
        if timeout:
            signal.alarm(timeout)
        self.probe()
        signal.signal(signal.SIGALRM, signal.SIG_DFL)
        signal.alarm(0)
        self.evaluator(self.probe)
        self.state = reduce(operator.add, self.normalized_state, self.initial)
        self.performance = self.normalized_performance

    def output(self, file=None):
        """Create plugin output.

        Output generation is delegated to a Formatter object. The name
        attribute is used to define the uppercased plugin name in the
        first line. If `file` is given, the output is written to the
        specified file object. Otherwise, it is returned as string.
        """
        f = nagiosplugin.formatter.Formatter(self.name)
        f.addstate(self.state)
        if self.performance:
            f.addperformance(self.performance)
        if self.logoutput.getvalue():
            f.addlongoutput(self.logoutput.getvalue())
        if file:
            f.render(file)
        else:
            return f.renders()

    @property
    def normalized_state(self):
        """The evaluator's state property in normalized form.

        The state is forced to be a list and None elements are filtered
        out.
        """
        state = self.evaluator.state
        if isinstance(state, list):
            return [s for s in state if s]
        elif state:
            return [state]
        else:
            return None

    @property
    def normalized_performance(self):
        """The evaluator's performance property in normalized form.

        The performance is forced to be a dict. If it is a single
        Performance object, add a key with the check's name.
        """
        performance = self.evaluator.performance
        if isinstance(performance, dict):
            return performance
        elif performance:
            return {self.name.lower(): performance}
        else:
            return {}

    @property
    def exitcode(self):
        """Return Nagios exit code according to the plugin's state."""
        return self.state.code
