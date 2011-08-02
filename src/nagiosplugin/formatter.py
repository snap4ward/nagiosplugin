# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

"""Render plugin output."""

from __future__ import print_function

import collections
import operator
import logging

LOG = logging.getLogger(__name__)


class Formatter(object):
    """Class responsible for Nagios plugin API compliant output formatting.

    State objects, Performance objects, and lists of long output strings
    can be fed into the Formatter. After that, call renders() to get a
    complete output.
    """

    def __init__(self, pluginname=None, maxlength=80):
        """Create new Formatter.

        `pluginname` as a preferably short uppercase string to identify
        the plugin in the output.
        `maxlength` sets the maximum line length.
        """
        self.pluginname = pluginname
        self.maxlength = maxlength
        self.text = ''
        self.longoutput = []
        self.perfdata = collections.deque()

    def addstate(self, state):
        """Set State object that defines the first line.

        Note that this method should be called only once. Subsequent
        invocations overwrite the state set in a previous invocation.
        """
        LOG.debug('addstate({0!r})'.format(state))
        if state.headline:
            self.text = u'{0} - {1}'.format(
                str(state), state.headline.strip(u'\n'))
        else:
            self.text = str(state)
        self.addlongoutput(state.longoutput)
        return self

    def addlongoutput(self, text):
        """Add lines of long output.

        `text` may be given either as single string or has list of
        strings in case of multi-line output to be added.
        """
        LOG.debug('addlongoutput({0!r})'.format(text))
        if isinstance(text, list):
            self.longoutput.extend([line.strip('\n') for line in text])
        else:
            self.longoutput.append(text.strip('\n'))

    def addperformance(self, performance):
        """Add performance values.

        `performance` must be a dict of `{string: Performance}` items.
        The key determines the performance value's name.
        """
        LOG.debug('addperformance({0!r})'.format(performance))
        for name, perf in sorted(performance.items()):
            self.perfdata.append(u'{0}={1}'.format(name, perf))

    def _perfdata_line(self, maxlength=80):
        """Pick performance data atoms for at most maxlength characters."""
        line = []
        while self.perfdata:
            perf = self.perfdata.popleft()
            line.append(perf)
            if reduce(operator.add, [len(e) + 1 for e in line],
                      0) > maxlength:
                self.perfdata.appendleft(line.pop())
                break
        return u' '.join(line)

    def _render_firstline(self):
        """Return first output line (status, message, performance)."""
        line = self.text
        if self.pluginname:
            line = self.pluginname.upper() + u' ' + line
        if len(line) >= self.maxlength:
            return line
        perf = self._perfdata_line(self.maxlength - len(line) - 3)
        if perf:
            line += u' | ' + perf
        return line

    def _render_tail(self):
        """Return remaining lines (longoutput, longperformance).

        The remaining output is returned as list of strings without newlines.
        """
        if not self.perfdata:
            return self.longoutput
        if self.longoutput:
            lines = self.longoutput
            lines[-1] = (
                lines[-1] + ' | ' +
                self._perfdata_line(self.maxlength - len(lines[-1]) - 3))
        else:
            lines = ['| ' + self._perfdata_line(self.maxlength - 2)]
        while self.perfdata:
            perf = self._perfdata_line(self.maxlength)
            if not perf:
                lines.append(self.perfdata.popleft())
            else:
                lines.append(perf)
        return lines

    def renders(self):
        """Return complete output as multi-line string.

        The string has a trailing newline. To write output directly into
        a stream, see the `render` method.
        """
        return (u'\n'.join([self._render_firstline()] + self._render_tail()) +
                u'\n')

    def render(self, fileobj):
        """Write complete output into file object.

        To get a string output, see the `renders` method.
        """
        print(self._render_firstline(), file=fileobj)
        for line in self._render_tail():
            print(line, file=fileobj)
