# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

"""Define Threshold class."""

import nagiosplugin.state
import nagiosplugin


class Threshold(object):
    """A Threshold object combines warning and critical ranges."""

    def __init__(self, warning=None, critical=None):
        """Create Threshold object with `warning` and `critical` ranges."""
        if warning is None and critical is None:
            raise ValueError(u'Threshold needs at least one of warning and '
                             u'critical')
        self.warning = nagiosplugin.Range(warning)
        self.critical = nagiosplugin.Range(critical)

    def __add__(self, measuredperformance):
        """Combine this with a MeasuredPerformance to a Performance."""
        pass

    def match(self, value, crit_msg=None, warn_msg=None, ok_msg=None):
        """Return State object depending on value and ranges.

        If `value` is outside the critical or warning ranges, the returned
        state object is optionally constructed with the respective message
        string.
        """
        if self.critical and not self.critical.match(value):
            return nagiosplugin.state.Critical()
        if self.warning and not self.warning.match(value):
            return nagiosplugin.state.Warning()
        return nagiosplugin.state.Ok()
