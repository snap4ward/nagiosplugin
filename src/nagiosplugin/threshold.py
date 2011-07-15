# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

"""Define Threshold class."""

import nagiosplugin.state


class Threshold(object):
    """A Threshold object combines warning and critical ranges."""

    def __init__(self, warning=None, critical=None):
        """Create Threshold object with `warning` and `critical` ranges."""
        if not warning and not critical:
            raise ValueError(u'Threshold needs at least one of warning and '
                             u'critical')
        self.warning = warning
        self.critical = critical

    def __add__(self, performance):
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
