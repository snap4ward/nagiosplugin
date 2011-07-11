# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

import nagiosplugin.controller
import sys

# import commonly accessed classes into main namespace
from nagiosplugin.plugin import Plugin


def main(check):
    controller = nagiosplugin.controller.Controller(check)
    controller(sys.argv)
