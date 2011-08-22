# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

"""Immutable value objects

This module defines ValueObject, which is the base class for different
immutable value objects like State, Range, and others.
"""


def s_vars(obj):
    """Return dict of slots-based instance variables.

    This function resembles the built-in vars() function, but works also
    for objects with __slots__.
    """
    unknown = object()
    keyval = dict((attr, getattr(obj, attr))
                  for attr in obj.__slots__
                  if getattr(obj, attr, unknown) is not unknown and
                    not attr.startswith('_'))
    if hasattr(obj, '__dict__'):
        keyval.update(obj.__dict__)
    return keyval


class ValueObject(object):
    """Immutable object which acts mainly as container for it's values.

    ValueObjects are not allowed to modify any of their attributes after
    object initalization. This allows some methods to be sensibly
    predefined.

    Concrete classes are expected to override the __slots__
    class-variable with a list of expected attributes.
    """
    # pylint: disable-msg=E1101

    def __init__(self, **kwargs):
        """Create ValueObject instance.

        Concrete classes may overwrite this method, but must make sure
        that the constructor still accepts keyword arguments for all
        __slots__.
        """
        if not hasattr(self, '__slots__'):
            raise RuntimeError('__slots__ must be defined')
        for name, value in kwargs.iteritems():
            object.__setattr__(self, name, value)

    def __setattr__(self, name, value):
        """Inhibit attribute changes after object initialization."""
        raise AttributeError(
            'cannot set {0!r} to {1!r} on frozen {2} instance'.format(
                name, value, self.__class__.__name__))

    def __delattr__(self, name):
        """Inhibit attribute deletion after object initialization."""
        raise AttributeError(
            'cannot delete {0!r} on frozen {1} instance'.format(
                name, self.__class__.__name__))

    def __repr__(self):
        """Return parseable string representation."""
        attrs = ', '.join(('{0}={1!r}'.format(key, value)
                           for key, value in s_vars(self).iteritems()))
        return '{0}({1})'.format(self.__class__.__name__, attrs)

    def __eq__(self, other):
        """Return True if other has the same type and dict."""
        if not type(self) == type(other):
            return False
        return s_vars(self) == s_vars(other)

    def __ne__(self, other):
        """Return True if other is not equal to self."""
        return not self.__eq__(other)

    def __hash__(self):
        """Return the same value for objects that are equal."""
        hashval = hash(self.__class__.__name__)
        try:
            for attr in self.__slots__:
                hashval ^= hash(getattr(self, attr, None))
            return hashval
        except TypeError:
            # use slower string representation
            return hash(repr(self))

    def replace(self, **kwargs):
        """Return new instance with selectively overridden attributes."""
        # pylint: disable-msg=W0142
        newdict = s_vars(self)
        newdict.update(kwargs)
        return self.__class__(**newdict)
