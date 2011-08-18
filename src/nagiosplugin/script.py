# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

"""Top-level script functions.

This module contains functions which help writing the console scripts.
They are imported into the main nagiosplugin namespace.
"""

import nagiosplugin.controller
import sys


def run(checkname, evaluator, verbosity=0, timeout=None):
    """Convenience method for common plugin execution steps.

    A Controller object is created with `checkname` and `evaluator`. The
    check is run with `timeout`. After that, the output is written to
    stdout and the program exits with the correct exit code.
    """
    controller = nagiosplugin.Controller(checkname, evaluator, verbosity)
    controller(timeout)
    controller.output(sys.stdout)
    sys.exit(controller.exitcode)


def standard_options(optionparser, default_timeout=15, **kw):
    """Quick add standard Plugin API options to OptionParser object.

    The Nagios Plugin API defines some standard options which are
    reserved and should not be used for other purposes. See
    http://nagiosplug.sourceforge.net/developer-guidelines.html for
    details.

    Each option is defined via a keyword argument. For example,
    `verbose=True' means "add --verbose option with the standard help
    text", while `verbose=u'my help text'` means "add --verbose option,
    but display custom help text". Each argument defines both the long
    and a corresponding short option.

    The following keyword arguments are recognized (option in
    parentheses):
        timeout (--timeout / -t)
        warning (--warning / -w)
        critical (--critical / -c)
        hostname (--hostname / -H)
        verbose (--verbose / -v)
        community (--community / -C)
        logname (--logname / -l)
        port (--port / -p)
        password (--password / -p)
        url (--url / -u)
        username (--username / -u)

    Arguments with conflicting short option names may not be specified
    in conjunction.
    """

    def _add(option, shortopt, default_help, default_val='',
             **add_option_kw):
        """Helper to avoid option adding code repetition."""
        if option not in kw:
            return
        if kw[option] is True:
            helptext = default_help
        else:
            helptext = kw[option]
        optionparser.add_option(
            shortopt, '--'+option, help=helptext, default=default_val,
            **add_option_kw)

    _add('timeout', '-t', u'seconds before plugin execution times out '
         u'(default: %default)', default_timeout, metavar='INTEGER',
         type='int')
    _add('warning', '-w', u'warning threshold range', metavar='RANGE')
    _add('critical', '-c', u'critical threshold range', metavar='RANGE')
    _add('hostname', '-H', u'host name or address to connect to',
         metavar='ADDRESS')
    _add('verbose', '-v', u'show more details (specify up to three times to '
         u'get even more details)', 0, action='count')
    _add('community', '-C', u'SNMP read community (default: %default)',
         'public', metavar='STRING')
    _add('logname', '-l', u'login name of user', metavar='STRING')
    _add('port', '-p', u'port number to connect to', default_val=0, type='int',
         metavar='INTEGER')
    _add('password', '-p', u'authentication password (caution: possible '
         u'security issue)', metavar='STRING')
    _add('url', '-u', u'open this URL', metavar='STRING')
    _add('username', '-u', u'authentication username', metavar='STRING')
