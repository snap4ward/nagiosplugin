# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

"""Define Threshold class.

Thresholds bundle a pair of warning and critical ranges for convenient
use in Evaluator methods.
"""

# pylint: disable-msg=W0402
# pylint: disable-msg=W0404
import nagiosplugin
import nagiosplugin.valueobj
import string


def fill_list(lst, min_len, filler_if_empty=None):
    """Replicate last item until `lst` it has at least `min_len` elements.

    If the list is empty, `filler_if_empty` is used to extend the list.
    """
    if len(lst) >= min_len:
        return lst
    try:
        filler = lst[-1]
    except IndexError:
        filler = filler_if_empty
    return lst + [filler] * (min_len - len(lst))


class Threshold(nagiosplugin.valueobj.ValueObject):
    """Convenience class to combine warning and critical ranges."""
    # pylint: disable-msg=E1101

    __slots__ = ['warning', 'critical']

    @classmethod
    def create_multi(cls, warnings, criticals, min_len=0):
        """Create multiple Threshold objects from warning/critical lists.

        This convenience method supports the creation of multiple
        Treshold values. Parameters are the minimum number of items to
        be created, a list of warning range specifications, and a list
        of critical range specifications.

        It returns a list of at least `min_len` Threshold objects. If
        one of the `warnings` or `criticals` list contains more items,
        the resulting list is made that long. Missing list items are
        filled up with the last element from the respective list or None
        if the list has no elements.
        """
        warnings = fill_list(warnings, max(len(warnings), len(criticals)))
        criticals = fill_list(criticals, max(len(warnings), len(criticals)))
        result = [Threshold(w, c) for w, c in zip(warnings, criticals)]
        return fill_list(result, min_len, Threshold())

    def __init__(self, warning=None, critical=None):
        """Create Threshold object with `warning` and `critical` ranges.

        `warning` and `critical` may be given either as strings or Range
        objects.
        """
        super(Threshold, self).__init__(warning=nagiosplugin.Range(warning),
                                        critical=nagiosplugin.Range(critical))

    def match(self, value, messages=None):
        """Return State object depending on value and ranges.

        Return State object (Ok, Warning, Critical) that depends on
        `value` matching the ranges associated with this Threshold
        object. The dict `messages` is used to pass optional messages
        strings for the resulting State object. Valid keys are:

            OK, WARNING, CRITICAL, UNKNOWN: message for the
                corresponding return state
            DEFAULT: fall-back message if one of the above keys is not
                present.

        If there is no matching key, the returned state has no message.

        Message strings may contain special tokens which are substituted
        with their corresponding values:

            $value - measured value (`value` parameter)
            $range - range which caused the returned state (warning or
                critical)
        """

        def msg(word, active_range=None):
            """Helper to pick the right message from `messages`."""
            try:
                template = string.Template(messages.get(word, messages.get(
                    'DEFAULT', '')))
                return template.substitute(
                    value=value, range=active_range)
            except (TypeError, AttributeError):
                return None

        try:
            if self.critical and not value in self.critical:
                return nagiosplugin.Critical(msg('CRITICAL', self.critical))
            if self.warning and not value in self.warning:
                return nagiosplugin.Warning(msg('WARNING', self.warning))
        except ValueError:
            return nagiosplugin.Unknown(msg('UNKNOWN'))
        return nagiosplugin.Ok(msg('OK'))
