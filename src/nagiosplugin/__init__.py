# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

import nagiosplugin.controller
import sys

# import commonly accessed classes into main namespace
from nagiosplugin.controller import Controller
from nagiosplugin.performance import Performance, MeasuredPerformance
from nagiosplugin.range import Range
from nagiosplugin.state import State, Ok, Warning, Critical, Unknown
from nagiosplugin.threshold import Threshold


def main(check):
    controller = nagiosplugin.controller.Controller(check)
    controller(sys.argv)
