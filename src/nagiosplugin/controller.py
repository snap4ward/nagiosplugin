# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

import nagiosplugin.plugin
import optparse


class Controller(object):

    def __init__(self, plugin_instance):
        if not isinstance(plugin_instance, nagiosplugin.plugin.Plugin):
            raise ValueError('%r is not a Plugin instance' % plugin_instance)
        self.plugin = plugin_instance

    def options(self, argv):
        """Set up and parse command line options."""
        self.optp = optparse.OptionParser(
            description=self.plugin.description, usage=self.plugin.usage,
            version=self.plugin.version)
        self.optp.add_option(
            '-t', '--timeout', metavar='SECONDS', dest='timeout',
            default=self.plugin.timeout,
            help='terminate plugin execution after SECONDS '
            '(default: %default)')
        self.plugin.cmdline(self.optp)
        options, arguments = self.optp.parse_args(argv)
        self.plugin.setup(options, arguments)

    def __call__(self, argv=None):
        """Main plugin life cycle."""
        self.options(argv)
