# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

import nagiosplugin.controller
import nagiosplugin.old.evaluator
import sys


class OldController(nagiosplugin.controller.Controller):

    def __init__(self, check_cls, argv=None):
        adapter = nagiosplugin.old.evaluator.AdapterEvaluator(check_cls, argv)
        super(OldController, self).__init__(
            adapter.check.shortname, adapter, adapter.loglevel)

    def __call__(self):
        timeout = self.evaluator.opts.timeout
        super(OldController, self).__call__(timeout)
        self.output(sys.stdout)
        sys.exit(self.exitcode)
