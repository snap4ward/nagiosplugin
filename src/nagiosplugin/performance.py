# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

"""Define Performance class"""

import nagiosplugin
import nagiosplugin.valueobj


class Performance(nagiosplugin.valueobj.ValueObject):
    """Value object for performance data records.

    A Performance object contains a scalar values and a unit of measure.
    This value is augmented with contextual information like thresholds
    and value range.
    """

    __slots__ = ['value', 'uom', 'minimum', 'maximum', 'warning', 'critical']

    def __init__(self, value, uom='', minimum=None, maximum=None,
                 warning=None, critical=None, threshold=None):
        """Initialize Performance object from scalars or other objects.

        `value` can either be a float, or a Performance object `uom`,
        `minimum`, and `maximum` specify the value's bounds.  `warning`
        and `critical` define the check ranges. Alternatively, a
        `threshold` value can be given instead of `warning` or
        `critical`.
        """
        if isinstance(value, Performance):
            super(Performance, self).__init__(**value._dict)
            return
        if threshold and (warning or critical):
            raise ValueError(u'cannot initialize with both warning/'
                             u'critical and threshold')
        elif threshold:
            warning = threshold.warning
            critical = threshold.critical
        if warning:
            warning = nagiosplugin.Range(warning)
        if critical:
            critical = nagiosplugin.Range(critical)
        super(Performance, self).__init__(
            value=value, uom=uom, minimum=minimum, maximum=maximum,
            warning=warning, critical=critical)
        self._check()

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
