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

    def __init__(self, pluginname, linelength=80):
        """Create new Formatter.

        `pluginname` as a preferably short uppercase string to identify the
        plugin in the output.
        `linelength` sets the maximum line length.
        """
        self.pluginname = pluginname.upper()
        self.linelength = linelength
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
        if isinstance(text, list):
            self.longoutput.extend([line.strip('\n') for line in text])
        else:
            self.longoutput.append(text.strip('\n'))

    def addperformance(self, performance):
        pass

    def render(self):
        """Return complete output as string (without trailing newline)."""
        out = StringIO.StringIO()
        out.write(u'{0} {1}'.format(self.pluginname, self.text))
        if self.longoutput:
            out.write('\n')
            out.write('\n'.join(self.longoutput))
        return out.getvalue()
