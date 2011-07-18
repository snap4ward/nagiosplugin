# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

import copy


class Range(object):
    """Represents a check range.

    The general format is `[@][start:][end]`. `start:` may be omitted if
    start==0. `~:` means that start is negative infinity. If `end` is omitted,
    infinity is assumed. To invert the match condition, prefix the range
    expression with `@`.

    See
    http://nagiosplug.sourceforge.net/developer-guidelines.html#THRESHOLDFORMAT
    for details.
    """

    def __init__(self, spec=None):
        """Create a Range object according to `spec`.

        `spec` may be either a string or another Range object.
        """
        self.invert = False
        self.start = 0
        self.end = None
        if isinstance(spec, Range):
            self.__dict__ = copy.copy(spec.__dict__)
        else:
            self._parse(spec)
        self.verify()

    def _parse(self, spec):
        spec = (spec or '')
        if spec.startswith('@'):
            self.invert = True
            spec = spec[1:]
        if spec.find(':') < 0:
            spec = ':' + spec
        (start, end) = spec.split(':')
        if start == '~':
            self.start = None
        elif start:
            if start.find('.') >= 0:
                self.start = float(start)
            else:
                self.start = int(start)
        if len(end):
            if end.find('.') >= 0:
                self.end = float(end)
            else:
                self.end = int(end)

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

    def __contains__(self, value):
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
        """Return a parseable range specification."""
        return 'Range(%r)' % str(self)

    def __eq__(self, other):
        """True if both objects represent the same value range."""
        if isinstance(other, Range):
            return self.__dict__ == other.__dict__
        return TypeError('cannot compare %r to %r' % (
            self.__class__, other.__class__))

    def __ne__(self, other):
        """True if the value ranges of both objects differ."""
        return not self.__eq__(other)
