# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

"""Define Formatter class to render plugin output."""

from __future__ import print_function

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO


class Formatter(object):

    def __init__(self, pluginname, linelength=80):
        self.pluginname = pluginname
        self.linelength = linelength
        self.text = ''
        self.longoutput = []
        self.perfdata = []

    def addstate(self, state):
        self.text = u'{0} {1} - {2}'.format(
            self.pluginname, str(state), state.messages[0].strip(u'\n'))
        return self

    def addlongoutput(self, text):
        pass

    def addperformance(self, performance):
        pass

    def render(self):
        out = StringIO.StringIO()
        out.write(self.text)
        return out.getvalue()
