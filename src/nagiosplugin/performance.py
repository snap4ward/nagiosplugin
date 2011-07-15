# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

"""MeasuredPerformance and Performance classes."""

import copy
import nagiosplugin.range


class MeasuredPerformance(object):
    """Scalar performance value without thresholds.

    A MeasuredPerformance object is a handy container for a scalar value (e.g.,
    time, size) and a unit of measure. The main difference from a Performance
    value is that it does not contain warning and critical thresholds.
    """

    def __init__(self, value, uom='', minimum=None, maximum=None):
        """Create MeasuredPerformance value object.

        `value` is the scalar value. `uom` is the unit of measure expressed as
        an string abbreviation. `minimum` and `maximum` specify the value's
        bounds.
        """
        self.value = value
        self.uom = uom
        self.minimum = minimum
        self.maximum = maximum
        self.check()

    def __eq__(self, other):
        """Return True if this object's values equal `other`'s values."""
        if isinstance(other, MeasuredPerformance):
            return self.__dict__ == other.__dict__
        raise TypeError('cannot compare %r to %r' % (
            self.__class__, other.__class__))

    def __neq__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        """Return parseable string representation."""
        return '%s(%g, %r, %r, %r)' % (
            self.__class__.__name__, self.value, self.uom, self.minimum,
            self.maximum)

    def __add__(self, threshold):
        """Combine this object with `threshold` to a Performance object."""
        return Performance(self, threshold=threshold)

    def check(self):
        """Check values for consistency."""
        if self.minimum is not None and self.value < self.minimum:
            raise ValueError(u'values %s is less than minimum %s' % (
                self.value, self.minimum))
        if self.maximum is not None and self.value > self.maximum:
            raise ValueError(u'values %s is greater than maximum %s' % (
                self.value, self.maximum))


class Performance(MeasuredPerformance):
    """MeasuredPerformance with thresholds.

    A Performance contains warning and critical ranges in addition to all
    attributes of a MeasuredPerformance object. Performance objects
    represent performance data as required by the Nagios plugin API.
    """

    def __init__(self, value, uom='', minimum=None, maximum=None,
                 warning=None, critical=None, threshold=None):
        """Initialize Performance object from scalars or other objects.

        `value` can either be a float, or a Performance object, or a
        MeasuredPerformance object. `uom`, `minimum`, and `maximum` have the
        same meaning as in `MeasuredPerformance()`. `warning` and `critical`
        define the check ranges. Alternatively, a `threshold` value can be
        given instead of `warning` or `critical`.
        """
        if isinstance(value, Performance):
            self.__dict__ = copy.copy(value.__dict__)
            return
        elif isinstance(value, MeasuredPerformance):
            super(Performance, self).__init__(
                value.value, value.uom, value.minimum, value.maximum)
        else:
            super(Performance, self).__init__(value, uom, minimum, maximum)
        if threshold and (warning is not None or critical is not None):
            raise ValueError(u'cannot initialize %s with both warning/'
                             u'critical and threshold' % self.__class__)
        elif threshold:
            self.warning = threshold.warning
            self.critical = threshold.critical
        else:
            self.warning = nagiosplugin.range.Range(warning)
            self.critical = nagiosplugin.range.Range(critical)

    def __eq__(self, other):
        """Return True if this objects's values matche `other`'s.

        `other` may also be a MeasuredPerformance object. In this case,
        `__eq__` returns only True if this object has no warning or critical
        ranges."""
        if isinstance(other, Performance):
            return self.__dict__ == other.__dict__
        if isinstance(other, MeasuredPerformance):
            return self == Performance(other)
        raise TypeError('cannot compare %r to %r' % (
            self.__class__, other.__class__))

    def __neq__(self, other):
        """Return True if this object's values do not match `other`'s."""
        return not self.__eq__(other)

    def __repr__(self):
        """Return parseable string representation."""
        return "%s(%g, %r, %r, %r, '%s', '%s')" % (
            self.__class__.__name__, self.value, self.uom, self.minimum,
            self.maximum, self.warning, self.critical)
