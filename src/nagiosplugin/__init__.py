# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

import nagiosplugin.controller
import sys

# import commonly accessed classes into main namespace
from nagiosplugin.evaluator import Evaluator
from nagiosplugin.plugin import Plugin
from nagiosplugin.probe import Probe


def main(check):
    controller = nagiosplugin.controller.Controller(check)
    controller(sys.argv)
