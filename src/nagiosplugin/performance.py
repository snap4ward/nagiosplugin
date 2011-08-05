# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

"""Define Performance class."""

import nagiosplugin


class Performance(object):
    """Value object for performance data records.

    A Performance object contains a scalar values and a unit of measure. This
    value is augmented with contextual information like thresholds and value
    range.
    """

    def __init__(self, value, uom='', minimum=None, maximum=None,
                 warning=None, critical=None, threshold=None):
        """Initialize Performance object from scalars or other objects.

        `value` can either be a float, or a Performance object `uom`,
        `minimum`, and `maximum` specify the value's bounds.  `warning` and
        `critical` define the check ranges. Alternatively, a `threshold` value
        can be given instead of `warning` or `critical`.
        """
        if isinstance(value, Performance):
            self.__dict__.update(dict((k, v) for k, v in value.__dict__.items()
                                      if not k.startswith('_')))
            self._frozen = True
            return
        else:
            self.value = value
            self.uom = uom
            self.minimum = minimum
            self.maximum = maximum
        if threshold and (warning is not None or critical is not None):
            raise ValueError(u'cannot initialize with both warning/'
                             u'critical and threshold')
        elif threshold:
            self.warning = threshold.warning
            self.critical = threshold.critical
        else:
            self.warning = nagiosplugin.Range(warning)
            self.critical = nagiosplugin.Range(critical)
        self._check()
        self._frozen = True

    def __setattr__(self, name, value):
        """Inhibit attribute changes after object initialization."""
        if hasattr(self, '_frozen'):
            raise AttributeError(
                'cannot set {0!r} to {1!r} on frozen {2} instance'.format(
                    name, value, self.__class__.__name__))
        super(self.__class__, self).__setattr__(name, value)

    def with_threshold(self, warning=None, critical=None, threshold=None):
        """Return copy of myself with modified threshold values."""
        return self.__class__(self.value, self.uom, self.minimum, self.maximum,
                              warning, critical, threshold)

    def __eq__(self, other):
        """Return True if this objects's values matche `other`'s."""
        if isinstance(other, Performance):
            return self.__dict__ == other.__dict__
        return False

    def __neq__(self, other):
        """Return True if this object's values do not match `other`'s."""
        return not self.__eq__(other)

    def __hash__(self):
        """Return the same value for objects that are equal."""
        return (hash(self.value) ^ hash(self.uom) ^ hash(self.minimum) ^
                hash(self.maximum) ^ hash(self.warning) ^ hash(self.critical))

    def __repr__(self):
        """Return parseable string representation."""
        return '{0}({1})'.format(
            self.__class__.__name__,
            ', '.join(['{0}={1!r}'.format(k, v)
                       for k, v in self.__dict__.iteritems()
                       if not k.startswith('_')]))

    def __str__(self):
        """Return string representation conforming to the plugin API.

        The format is VALUE[OUM[;WARNING[;CRITICAL[;MIN[;MAX]]]]].
        """
        words = [(str(e) if e is not None else '') for e in [
                 self.uom, self.warning, self.critical,
                 self.minimum, self.maximum]]
        return '%s%s' % (self.value, ';'.join(words).rstrip(';'))

    def _check(self):
        """Check values for consistency."""
        if self.minimum is not None and self.value < self.minimum:
            raise ValueError(u'value %s is less than minimum %s' % (
                self.value, self.minimum))
        if self.maximum is not None and self.value > self.maximum:
            raise ValueError(u'values %s is greater than maximum %s' % (
                self.value, self.maximum))
