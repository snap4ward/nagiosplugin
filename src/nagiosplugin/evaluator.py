# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

"""Define the Evaluator interface."""


class Evaluator(object):
    """Evalute measured facts into status and performance values.

    The evaluate() method should gather interesting system information
    decide if it lies within the thresholds. The state() and performance()
    methods return State and Performance objects corresponding to the system
    state.

    Custom evaluator classes don't need to be necessarily descendands of
    this class as long as they define the same interface.
    """

    def __init__(self):
        """Create and configure the Evaluator."""
        self._state = []
        self._performance = []

    def evaluate(self):
        """Get interesting information."""
        pass

    def state(self):
        """Return list of states."""
        return self._state

    def performance(self):
        """Return performance data as dict or list of (key, value) pairs.

        When the performance data is returned as list of pairs, the
        ordering is preserved.
        """
        return self._performance
