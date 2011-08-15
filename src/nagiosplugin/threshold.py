# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

"""Define Threshold class.

Thresholds bundle a pair of warning and critical ranges for convenient
use in Evaluator methods.
"""

import nagiosplugin
import nagiosplugin.valueobj


class Threshold(nagiosplugin.valueobj.ValueObject):
    """Convenience class to combine warning and critical ranges."""
    # pylint: disable-msg=E1101

    __slots__ = ['warning', 'critical']

    def __init__(self, warning=None, critical=None):
        """Create Threshold object with `warning` and `critical` ranges.

        `warning` and `critical` may be given either as strings or Range
        objects.
        """
        super(Threshold, self).__init__(warning=nagiosplugin.Range(warning),
                                        critical=nagiosplugin.Range(critical))

    def match(self, value, messages={}):
        """Return State object depending on value and ranges.

        Return State object (Ok, Warning, Critical) that depends on `value`
        matching the ranges associated with this Threshold object. The
        dict `messages` is used to pass optional messages strings for
        the resulting State object. Valid keys are:
            OK, WARNING, CRITICAL, UNKNOWN: message for the
                corresponding return state
            DEFAULT: fall-back message if one of the above keys is not
                present.
        If there is no matching key, the returned state has no message.
        """
        def message(word):
            return messages.get(word, messages.get('DEFAULT', None))
        try:
            if self.critical and not value in self.critical:
                return nagiosplugin.Critical(message('CRITICAL'))
            if self.warning and not value in self.warning:
                return nagiosplugin.Warning(message('WARNING'))
        except ValueError:
            return nagiosplugin.Unknown(message('UNKNOWN'))
        return nagiosplugin.Ok(message('OK'))
