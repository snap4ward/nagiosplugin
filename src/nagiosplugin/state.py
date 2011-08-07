# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

"""State types that represent check outcomes

This module defines the four state types Ok, Warning, Critical, and
Unknown. These represent the possible check outcomes defined by the
Nagios plugin API.
"""

import nagiosplugin.valueobj


class State(nagiosplugin.valueobj.ValueObject):
    """Represents the logical outcome of checks.

    A State has a numeric state code and a status word denoting the
    result. In addition a state carries one or more message lines. The
    first message line goes into Nagios' main status message and the
    remaining lines go into Nagios' long output (introduced with Nagios
    3).
    """

    __slots__ = ['messages']

    code = None
    word = None

    def __init__(self, messages=None):
        """Initialize State value.

        `messages` can be given as single string or as list of strings.
        In the first case, the string defines a headline and no long
        output is defined. In the second case, the first string of the
        list is the headline and the subsequent strings are the long
        output.
        """
        if not messages:
            messages = []
        elif not isinstance(messages, list):
            messages = [messages]
        super(State, self).__init__(messages=messages)

    def __str__(self):
        """Numeric status code."""
        if self.code is None or self.word is None:
            raise NotImplementedError
        return self.word

    def __int__(self):
        """Textual status code."""
        if self.code is None or self.word is None:
            raise NotImplementedError
        return self.code

    def __cmp__(self, other):
        """Numerical code comparision.

        This comparision is only meaningful for states with different
        codes.
        """
        return self.code.__cmp__(other.code)

    def __add__(self, other):
        """Combine two states.

        The result has the type of the dominant state and the messages
        are concatenated both arguments are of the dominant state.
        Otherwise the non-dominant state is discarded and the dominant
        state remains.
        """
        if not isinstance(other, State):
            raise TypeError("cannot add '%s' and '%s' objects" % (
                            self.__class__, other.__class__))
        if type(self) == type(other):
            return self.__class__(self.messages + other.messages)
        elif self > other:
            return self
        return other

    @property
    def headline(self):
        """Main status message (the only one supported with Nagios 1 and 2)."""
        if self.messages:
            return self.messages[0]

    @property
    def longoutput(self):
        """Additional status messages."""
        return self.messages[1:]


class Ok(State):
    """Expresses that check result is inside all limits."""

    code = 0
    word = u'OK'


class Warning(State):
    """Expresses that check result is outside the warning range."""

    code = 1
    word = u'WARNING'


class Critical(State):
    """Expresses that check result is outside the critical range."""

    code = 2
    word = u'CRITICAL'


class Unknown(State):
    """Expresses that it was impossible to determine check outcome."""

    code = 3
    word = u'UNKNOWN'
