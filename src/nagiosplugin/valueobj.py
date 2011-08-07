# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

"""Immutable value objects

This module defines ValueObject, which is the base class for different
immutable value objects like State, Range, and others.
"""


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
        assert hasattr(self, '__slots__'), '__slots__ must be defined'
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
                           for key, value in self.publicitems()))
        return '{0}({1})'.format(self.__class__.__name__, attrs)

    def __eq__(self, other):
        """Return True if other has the same type and dict."""
        if not type(self) == type(other):
            return False
        return dict(self.publicitems()) == dict(other.publicitems())

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

    def publicitems(self):
        """Iterate over (key, value) pairs of public attributes."""
        unknown = object()
        return ((attr, getattr(self, attr)) for attr in self.__slots__
                if getattr(self, attr, unknown) is not unknown
                and not attr.startswith('_'))

    def replace(self, **kwargs):
        """Return new instance with selectively overridden attributes."""
        newdict = dict(self.publicitems())
        newdict.update(kwargs)
        return self.__class__(**newdict)
