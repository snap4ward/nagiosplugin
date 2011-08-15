# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

"""Define Performance class.

Performance objects are used to communicate performance data from the
Evaluator to the nagiosplugin Controller. They will be rendered into the
performance value sections of the plugin's output.
"""

import nagiosplugin
import nagiosplugin.valueobj


class Performance(nagiosplugin.valueobj.ValueObject):
    """Value object for performance data records.

    Performance objects contain a scalar value and a unit of measure.
    This value is augmented with contextual information like thresholds
    and value range.
    """
    # pylint: disable-msg=E1101

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
            kwargs = nagiosplugin.valueobj.s_vars(value)
            super(Performance, self).__init__(**kwargs)
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
