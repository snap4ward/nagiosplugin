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
            description=self.plugin.description, version=self.plugin.version)
        self.optp.add_option(
            '-t', '--timeout', metavar='T', dest='timeout',
            default=self.plugin.timeout,
            help='terminate plugin execution after T seconds')
        self.plugin.cmdline(self.optp)
        self.options, self.arguments = self.optp.parse_args(argv)

    def __call__(self, argv=None):
        """Main plugin life cycle."""
        self.options(argv)
