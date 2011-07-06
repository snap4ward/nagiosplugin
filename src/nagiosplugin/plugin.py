# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

"""Defines Plugin, the base class for custom plugins."""

import nagiosplugin.probe
import nagiosplugin.evaluator


class Plugin(object):
    """Abstract base class that defines the life cycle of plugins.

    Custom plugin should subclass this class and override the appropriate
    life cycle methods to implement the desired functionality.

    Attributes:
        name - Plugin short name
        description - One paragraph about what this plugin does
        version - Plugin version
        default_timeout - maximal execution time if nothing else is specified
    """

    name = ''
    description = ''
    version = '0.0'
    default_timeout = 15

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
