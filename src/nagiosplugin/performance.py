# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

"""MeasuredPerformance and Performance classes."""


class MeasuredPerformance(object):
    """Scalar performance value without thresholds.

    A MeasuredPerformance object is a handy container for a scalar value (e.g.,
    time, size) and a unit of measure. The main difference from a Performance
    value is that it does not contain warning and critical thresholds.
    """

    def __init__(self, value, uom='', minimum=None, maximum=None):
        """Create MeasuredPerformance value object."""
        self.value = value
        self.uom = uom
        self.minimum = minimum
        self.maximum = maximum
        self.check()

    def check(self):
        """Check values for consistency."""
        if self.minimum is not None and self.value < self.minimum:
            raise ValueError('values %s is less than minimum %s' % (
                self.value, self.minimum))
        if self.maximum is not None and self.value > self.maximum:
            raise ValueError('values %s is greater than maximum %s' % (
                self.value, self.maximum))
