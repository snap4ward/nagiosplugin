# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

"""Class library to help writing Nagios/Icinga plugins.

nagiosplugin helps writing plugins that comply to the Nagios 3.0 API
specification. To do this, it defines various helper classes and a
Controller that directs the overall plugin execution.

A plugin queries the system for information and generates State and
Performance objects.

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
from nagiosplugin.script import run, standard_options
from nagiosplugin.state import State, Ok, Warning, Critical, Unknown
from nagiosplugin.threshold import Threshold

# deprecated modules
from nagiosplugin.old.check import Check
from nagiosplugin.old.measure import Measure
