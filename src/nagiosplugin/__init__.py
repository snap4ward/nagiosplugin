# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

import nagiosplugin.controller
import sys


def main(check):
    controller = nagiosplugin.controller.Controller(check)
    controller(sys.argv)
