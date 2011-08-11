# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

"""Class library to help writing Nagios/Icinga plugins

nagiosplugin helps writing plugins that comply to the Nagios 3.0 API
specification. To do this, it defines various helper classes and a
Controller that directs the overall plugin execution.

A plugin generally consists of a Probe which queries the system for
information and an Evaluator which examines the probe object and
generates State and Performance objects.

Threshold objects bundle critical and warning Ranges which can be used
to check scalar values and return States.

To get started, read the documentation in the doc directory and see the
examples.
"""

# import commonly accessed classes into main namespace
# pylint: disable-msg=W0622
from nagiosplugin.controller import Controller
from nagiosplugin.performance import Performance
from nagiosplugin.range import Range
from nagiosplugin.state import State, Ok, Warning, Critical, Unknown
from nagiosplugin.threshold import Threshold

import sys


def run(checkname, probe, evaluator, verbosity=0, timeout=None):
    """Convenience method for common plugin execution steps.

    A Controller object is created with `checkname`, `probe`, and
    `evaluator`. The check is run with `timeout`. After that, the output
    is written to stdout and the program exits with the correct exit
    code.
    """
    controller = Controller(checkname, probe, evaluator, verbosity)
    controller(timeout)
    controller.output(sys.stdout)
    sys.exit(controller.exitcode)
