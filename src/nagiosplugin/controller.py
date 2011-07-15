# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

import nagiosplugin.plugin
import optparse
import signal


class Controller(object):

    def __init__(self, plugin_instance):
        if not isinstance(plugin_instance, nagiosplugin.plugin.Plugin):
            raise ValueError('%r is not a Plugin instance' % plugin_instance)
        self.plugin = plugin_instance

    def default_options(self):
        """Set up command line options required by the plugin API."""
        self.optp = optparse.OptionParser(
            description=self.plugin.description, usage=self.plugin.usage,
            version=self.plugin.version)
        # --help and --version come for free
        self.optp.add_option(
            '-t', '--timeout', metavar='SECONDS', dest='timeout',
            default=self.plugin.timeout, type='int',
            help='terminate plugin execution after SECONDS '
            '(default: %default)')

    def probe_with_timeout(self):
        def handle_timeout(signum, stackframe):
            raise RuntimeError('timeout %is exceeded' % self.options.timeout)
        signal.signal(signal.SIGALRM, handle_timeout)
        signal.alarm(self.options.timeout)
        self.plugin.probe()
        signal.signal(signal.SIGALRM, signal.SIG_DFL)

    def __call__(self, argv=None):
        """Main plugin life cycle."""
        self.default_options()
        self.plugin.commandline(self.optp)
        self.options, self.arguments = self.optp.parse_args(argv)
        self.plugin.setup(self.options, self.arguments)
        self.probe_with_timeout()
        self.plugin.evaluator(self.plugin.probe)
