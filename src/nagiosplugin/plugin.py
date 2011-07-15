# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

"""Defines Plugin, the base class for custom plugins."""

import nagiosplugin.probe
import nagiosplugin.evaluator
import operator


class Plugin(object):
    """Abstract base class that defines the life cycle of plugins.

    Custom plugin should subclass this class and override the appropriate
    life cycle methods to implement the desired functionality.

    Attributes:
        name - Plugin short name
        description - One paragraph about what this plugin does
        version - Plugin version
        timeout - maximal execution time if nothing else is specified
    """

    name = ''
    description = ''
    version = '0.0'
    timeout = 15

    def __init__(self):
        """Create plugin instance.

        This methods should not require any arguments. Command line arguments
        are passed in the setup phase.
        """
        pass

    def cmdline(self, optparse):
        """Define command line parameters for this plugin.

        An standard optparse.OptionParser object is passed and should be
        customized using add_option and friends. Please note that the standard
        options -h/--help, -t/--timeout, and -V/--version are already defined.
        """
        pass

    def setup(self, options, arguments):
        """Command line argument setup phase.

        The result from the option parser invocation is fed into this method.
        Custom plugins should evaluate the options and generate the probe and
        evaluator objects according to the argument passed in here.
        """
        self.probe = nagiosplugin.probe.Probe()
        self.evaluator = nagiosplugin.evaluator.Evaluator()

    def message(self, states, performances=None):
        """Synthesize status messages into main message.

        If there are several status objects returned, this method can be used
        to provide a more helpful textual output. The default implementation
        concats the message lines from all state objects passed. The return
        value should be a list of strings.
        """
        return reduce(operator.add, states).messages
