# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

"""Overall plugin execution logic."""

# pylint: disable-msg=W0404
import functools
import logging
import nagiosplugin
import nagiosplugin.formatter
import nagiosplugin.state
import operator
import signal
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

LOG = logging.getLogger('nagiosplugin')


class Controller(object):
    """Aid orchestration of various plugin components.

    A Controller takes several subordinate objects and "puts everything
    together":

        - plugin name
        - evaluator object
    """

    def __new__(cls, identifier, *args, **kwargs):
        if isinstance(identifier, basestring):
            return object.__new__(Controller)
        else:
            import nagiosplugin.old.controller
            inst = object.__new__(nagiosplugin.old.controller.OldController)
            return inst

    def __init__(self, name, evaluator=None, verbosity=0):
        """Create Controller object.

        `name` is the short plugin name that appears first in the
        output.
        `evaluator` is an object which supports the Evaluator protocol.
        `verbosity` is an integer which controls the amount of logging
        output to be included in the plugin's long outout.
        """
        self.name = name
        self.evaluator = evaluator
        self.logoutput = StringIO.StringIO()
        self._setup_logger(verbosity)
        self.state = nagiosplugin.Ok()
        self.performance = None

    def __str__(self):
        """Complete plugin output as string."""
        return self.output()

    def __call__(self, timeout=None):
        """Perform plugin execution.

        Call evaluator in a controlled environment. After `timeout`
        seconds, abort execution and set an Unknown state. If any
        exceptions occurs, set an Unknown state with the exception
        message, too.
        """
        try:
            self._process(timeout)
        except StandardError as exc:
            self.state = nagiosplugin.state.Unknown(str(exc))
            LOG.exception(exc)

    def _setup_logger(self, verbosity):
        """Configure global logger for long output.

        Messages logged to the "nagiosplugin" logger will be included in
        the long output according to the `verbosity` level (0-3).
        """
        LOG.setLevel(logging.DEBUG)
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
        LOG.addHandler(handler)

    def _process(self, timeout=None):
        """Perform evaluator calls in controlled environment."""
        def handle_timeout(_signum, _stackframe):
            """Abort plugin evaluation."""
            signal.alarm(0)
            raise RuntimeError(u'timeout {0} s exceeded'.format(timeout))
        signal.signal(signal.SIGALRM, handle_timeout)
        if timeout:
            signal.alarm(timeout)
        self.evaluator.evaluate()
        signal.signal(signal.SIGALRM, signal.SIG_DFL)
        signal.alarm(0)
        self.state = self._normalized_state()
        self.performance = self._normalized_performance()

    def _normalized_state(self):
        """The evaluator's state property in normalized form.

        The state is forced to be a list and None elements are filtered
        out.
        """
        state = self.evaluator.state()
        if not state:
            return nagiosplugin.Ok()
        if isinstance(state, nagiosplugin.State):
            return state
        return functools.reduce(operator.add, (s for s in state if s),
                                nagiosplugin.Ok())

    def _normalized_performance(self):
        """The evaluator's performance property in normalized form.

        The performance is forced to be a list of `(key, performance)`
        pairs. If it is a single Performance object, add a key with the
        check's name. Null performance values are stripped.
        """
        performance = self.evaluator.performance()
        if not performance:
            return []
        try:
            normalized = list(performance.items())
        except AttributeError:
            if isinstance(performance, nagiosplugin.Performance):
                normalized = [(self.name.lower(), performance)]
            else:
                normalized = performance
        return [(key, perf) for key, perf in normalized if perf]

    def output(self, fileobj=None):
        """Create plugin output.

        Output generation is delegated to a Formatter object. The name
        attribute is used to define the uppercased plugin name in the
        first line. If `fileobj` is given, the output is written to the
        specified file object. Otherwise, it is returned as string.
        """
        fmt = nagiosplugin.formatter.Formatter(self.name)
        fmt.addstate(self.state)
        if self.performance:
            fmt.addperformance(self.performance)
        if self.logoutput.getvalue():
            fmt.addlongoutput(self.logoutput.getvalue())
        if fileobj:
            fmt.render(fileobj)
        else:
            return fmt.renders()

    @property
    def exitcode(self):
        """Return Nagios exit code according to the plugin's state."""
        return self.state.code
