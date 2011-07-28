# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

from __future__ import print_function

# import commonly accessed classes into main namespace
from nagiosplugin.controller import Controller
from nagiosplugin.performance import Performance
from nagiosplugin.range import Range
from nagiosplugin.state import State, Ok, Warning, Critical, Unknown
from nagiosplugin.threshold import Threshold

import sys


def run(checkname, probe, evaluator, verbosity=0, timeout=None):
    """Convenience method for common plugin execution steps."""
    controller = Controller(checkname, probe, evaluator, verbosity)
    controller(timeout)
    print(controller)
    sys.exit(controller)
