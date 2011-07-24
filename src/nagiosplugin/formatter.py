# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

"""Define Formatter class to render plugin output."""

from __future__ import print_function

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO


class Formatter(object):
    """Class responsible for Nagios plugin API compliant output formatting."""

    def __init__(self, pluginname, maxlength=80):
        """Create new Formatter which identifies itself with `pluginname`."""
        self.pluginname = pluginname.upper()
        self.maxlength = maxlength
        self.text = ''
        self.longoutput = []
        self.perfdata = []

    def addstate(self, state):
        """Add textual contents of `state` to output."""
        if state.headline:
            self.text = u'{0} - {1}'.format(
                str(state), state.headline.strip(u'\n'))
        else:
            self.text = str(state)
        self.addlongoutput(state.longoutput)
        return self

    def addlongoutput(self, text):
        if isinstance(text, str) or isinstance(text, unicode):
            self.addlongoutput(text.strip(u'\n').split(u'\n'))
        else:
            self.longoutput.extend([l.strip(u'\n') for l in text])

    def addperformance(self, performance):
        pass

    def render(self):
        """Return complete output as string (without trailing newline)."""
        out = StringIO.StringIO()
        out.write(u'{0} {1}'.format(self.pluginname, self.text))
        if self.longoutput:
            out.write(u'\n')
            out.write(u'\n'.join(self.longoutput))
        return out.getvalue()
