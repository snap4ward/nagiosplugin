# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

import mock
import nagiosplugin
import nagiosplugin.evaluator
import nagiosplugin.probe
import optparse
import re
import StringIO
import sys
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class ScriptTest(unittest.TestCase):

    def setUp(self):
        self.old_stdout = sys.stdout
        self.stdout = sys.stdout = StringIO.StringIO()

    def tearDown(self):
        sys.stdout = self.old_stdout

    @mock.patch('nagiosplugin.Controller')
    @mock.patch('sys.exit')
    def test_run(self, exit, controller_cls):
        controller = controller_cls.return_value
        controller.output = mock.Mock()
        probe = nagiosplugin.probe.Probe()
        evaluator = nagiosplugin.evaluator.Evaluator()
        nagiosplugin.run('FOO', probe, evaluator)
        controller.assert_called_once_with(None)
        controller_cls.assert_called_once_with('FOO', probe, evaluator, 0)
        exit.assert_called_once_with(controller.exitcode)

    @mock.patch('sys.exit')
    def test_standard_options(self, _exit):
        optp = optparse.OptionParser(prog='test', version='1.0')
        nagiosplugin.standard_options(
            optp, timeout=True, warning=True, critical=True, hostname=True,
            verbose=True, community=True, logname=True, port=True, url=True)
        _opts, _args = optp.parse_args(['--help'])
        self.maxDiff = None
        self.assertMultiLineEqual(self.stdout.getvalue(), """\
Usage: test [options]

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -t INTEGER, --timeout=INTEGER
                        seconds before plugin execution times out (default:
                        15)
  -w RANGE, --warning=RANGE
                        warning threshold range
  -c RANGE, --critical=RANGE
                        critical threshold range
  -H ADDRESS, --hostname=ADDRESS
                        host name or address to connect to
  -v, --verbose         show more details (specify up to three times to get
                        even more details)
  -C STRING, --community=STRING
                        SNMP read community (default: public)
  -l STRING, --logname=STRING
                        login name of user
  -p INTEGER, --port=INTEGER
                        port number to connect to
  -u STRING, --url=STRING
                        open this URL
""")

    @mock.patch('sys.exit')
    def test_standard_options_with_custom_help_text(self, _exit):
        optp = optparse.OptionParser(prog='test', version='1.0')
        nagiosplugin.standard_options(
            optp, timeout=u'custom help')
        _opts, _args = optp.parse_args(['--help'])
        self.assertRegexpMatches(
            self.stdout.getvalue(),
            re.compile(r'--timeout=INTEGER.*custom help', re.DOTALL))
