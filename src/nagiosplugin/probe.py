# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

"""Define the Probe interface."""


class Probe(object):
    """A probe object queries the system for specific facts.

    Probes interact with the system and store measured facts into attributes.
    After a probe has been run, it is passed to an evaluator object which
    queries the probe object for information of interest.

    Custom probe classes don't need to be necessarily descendands of this
    class as long as they define the same interface.
    """

    def __init__(self, *args, **kwargs):
        """Configure the probe so that it has all information to proceed."""
        pass

    def __call__(self):
        """Query the system.

        __call__ is invoked in a controlled environment. All exceptions raised
        here are converted to UNKNOWN Nagios status codes. There is also a
        timeout in effect: if the __call__ method does not return within the
        specified time, the framwork also emits an UNKNOWN status code.
        """
        pass
