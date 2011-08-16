# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

"""Define the Evaluator interface."""


class Evaluator(object):
    """Evalute measured facts into status and performance values.

    An evalutor is called with the probe after the latter has been executed.
    The evaluator should read interesting facts from the probe object and
    decide if they are OK. It is responsible for generating Status and
    Performance objects.

    Custom evaluator classes don't need to be necessarily descendands of this
    class as long as they define the same interface.
    """

    def __init__(self):
        """Configure the evaluator with criteria to evaluate the probe."""
        self._state = []
        self._performance = {}

    def evaluate(self, probe):
        """Get interesting information out or `probe` for evaluation."""
        pass

    def state(self):
        """Return list of states."""
        return self._state

    def performance(self):
        """Return dict of performance values."""
        return self._performance
