# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

"""Define state types that represent the check outcomes defined by Nagios."""


class State(object):
    """Represents the logical outcome of checks.

    A State has a numeric state code and a status word denoting the result. In
    addition a state carries one or more message lines. The first message line
    goes into Nagios' main status message and the remaining lines go into
    Nagios' long output (introduced with Nagios 3).
    """

    code = None
    word = None

    def __init__(self, messages=None):
        if not messages:
            self.messages = []
        elif not isinstance(messages, list):
            self.messages = [messages]
        else:
            self.messages = messages

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

    def __eq__(self, other):
        """Compare for equality."""
        if not hasattr(other, 'code') or not hasattr(other, 'messages'):
            return False
        return self.code == other.code and self.messages == other.messages

    def __ne__(self, other):
        """Compare for non-equality."""
        return not self.__eq__(other)

    def __cmp__(self, other):
        """Numerical code comparision.

        This comparision is only meaningful for states with different codes.
        """
        return self.code.__cmp__(other.code) 

    def headline(self):
        """Main status message (the only one supported with Nagios 1 and 2)."""
        if self.messages:
            return self.messages[0]

    def longoutput(self):
        """Additional status messages."""
        return self.messages[1:]

    def __repr__(self):
        return u'%s(%r)' % (self.__class__.__name__, self.messages)

    def __add__(self, other):
        """Combine two states.

        The result has the type of the dominant state and the messages are
        concatenated both arguments are of the dominant state. Otherwise the
        non-dominant state is discarded and the dominant state remains.
        """
        if not isinstance(other, State):
            raise TypeError("cannot add '%s' and '%s' objects" % (
                            self.__class__, other.__class__))
        if type(self) == type(other):
            return self.__class__(self.messages + other.messages)
        elif self > other:
            return self
        return other


class Ok(State):
    code = 0
    word = u'OK'


class Warning(State):
    code = 1
    word = u'WARNING'


class Critical(State):
    code = 2
    word = u'CRITICAL'


class Unknown(State):
    code = 3
    word = u'UNKNOWN'
