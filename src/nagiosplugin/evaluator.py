# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

"""Define the Evaluator interface."""


class Evaluator(object):
    """Evalute measured facts into status and performance values.

    An evalutor is called with the probe after the latter has been executed. The
    evaluator should read interesting facts from the probe object and decide if
    they are OK. It is responsible for generating Status and Performance
    objects.

    Properties:
        `status` -- a list of Status objects computed from the probe's contents
        `performance` -- a list of Performance objects computed from the probe's
            contents

    Custom evaluator classes don't need to be necessarily descendands of this
    class as long as they define the same interface.
    """

    status = []
    performance = []

    def __init__(self, *args, **kwargs):
        """Configure the evaluator with criteria to evaluate the probe."""
        pass

    def __call__(self, probe):
        """Process probe and update status and performance."""
