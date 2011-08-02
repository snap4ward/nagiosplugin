# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

"""Define Threshold class."""

import nagiosplugin


class Threshold(object):
    """A Threshold object combines warning and critical ranges."""

    def __init__(self, warning=None, critical=None):
        """Create Threshold object with `warning` and `critical` ranges."""
        self.warning = nagiosplugin.range.Range(warning)
        self.critical = nagiosplugin.range.Range(critical)

    def __add__(self, measuredperformance):
        """Combine this with `measuredperformance` to a Performance object."""
        return measuredperformance.__add__(self)

    def match(self, value, default_msg=None, critical_msg=None,
              warning_msg=None, ok_msg=None):
        """Return State object depending on value and ranges.

        If `value` is outside the critical or warning ranges, the returned
        state object is optionally constructed with the respective message
        string. If there is no specific message for the computed state given,
        `default_msg` is used as fallback message.
        """
        if self.critical and not value in self.critical:
            return nagiosplugin.Critical(critical_msg or default_msg)
        if self.warning and not value in self.warning:
            return nagiosplugin.Warning(warning_msg or default_msg)
        return nagiosplugin.Ok(ok_msg or default_msg)
