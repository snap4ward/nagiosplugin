# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

"""Range objects that define scalar matching rules"""

import nagiosplugin.valueobj


class Range(nagiosplugin.valueobj.ValueObject):
    """Represents a check range.

    The general format is `[@][start:][end]`. `start:` may be omitted if
    start==0. `~:` means that start is negative infinity. If `end` is
    omitted, infinity is assumed. To invert the match condition, prefix
    the range expression with `@`.

    See
    http://nagiosplug.sourceforge.net/developer-guidelines.html#THRESHOLDFORMAT
    for details.
    """

    __slots__ = ['start', 'end', 'invert']

    @classmethod
    def _parse(cls, spec):
        """Crack up string representation into start, end, invert."""
        spec = (spec or '')
        start = 0
        end = None
        invert = False
        if spec.startswith('@'):
            invert = True
            spec = spec[1:]
        if not ':' in spec:
            spec = ':' + spec
        (str_start, str_end) = spec.split(':')
        if str_start == '~':
            start = None
        elif str_start:
            if str_start.find('.') >= 0:
                start = float(str_start)
            else:
                start = int(str_start)
        if len(str_end):
            if str_end.find('.') >= 0:
                end = float(str_end)
            else:
                end = int(str_end)
        return start, end, invert

    def __init__(self, spec=None):
        """Create a Range object according to `spec`.

        `spec` may be either a string or another Range object.
        """
        if isinstance(spec, Range):
            start = spec.start
            end = spec.end
            invert = spec.invert
        else:
            start, end, invert = self._parse(spec)
        super(Range, self).__init__(start=start, end=end, invert=invert)
        self.verify()

    def __contains__(self, value):
        """Alias for `match`."""
        return self.match(value)

    def __str__(self):
        """Return a human-readable range specification."""
        result = []
        if self.invert:
            result.append('@')
        if self.start is None:
            result.append('~:')
        elif self.start != 0:
            result.append(('%s:' % self.start))
        if self.end is not None:
            result.append(('%s' % self.end))
        return ''.join(result)

    def __repr__(self):
        """Return a parseable string representation."""
        return '{0}({1!r})'.format(self.__class__.__name__, str(self))

    def verify(self):
        """Throw ValueError if the range is not consistent."""
        if (self.start is not None and self.end is not None and
            self.start > self.end):
            raise ValueError('start %f must not be greater than end %f' % (
                             self.start, self.end))

    def match(self, value):
        """Return True if `value` is inside the bounds (~ inversion)."""
        if self.start is not None and value < self.start:
            return False ^ self.invert
        if self.end is not None and value > self.end:
            return False ^ self.invert
        return True ^ self.invert
