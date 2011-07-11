# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

import nagiosplugin.performance
import nagiosplugin.plugin
import optparse
import urllib2
import time


class HTTPProbe(object):

    def __init__(self, hostname):
        self.hostname = hostname

    def __call__(self):
        start = time.time()
        req = urllib2.urlopen('http://%s/' % self.hostname)
        self.response = req.read()
        stop = time.time()
        self.responsetime = stop - start

    @property
    def performance(self):
        return performance.MeasuredPerformance(
            'time', self.responsetime, 's', 0)


class HTTPEvaluator(object):

    def __init__(self, warn, crit, stringmatch=False):
        self.threshold = nagiosplugin.threshold.Threshold(warn, crit)
        self.stringmatch = stringmatch

    def __call__(self, probe):
        self.probe = probe
        self.status = [self.check_string(), self.check_time()]
        self.performance = [self.probe.performance[0] + self.threshold]

    def check_string(self):
        if self.stringmatch and (
            self.stringmatch.encode() in self.probe.response):
            return status.Ok('%s found in response' % self.stringmatch)
        return status.Critical(
            '%s not found in response' % self.stringmatch)

    def check_time(self):
        return self.threshold.match(self.probe.responsetime)


class HTTPCheck(nagiosplugin.Plugin):

    name = 'HTTP'
    description = "Check a HTTP server's response time and output"
    version = '0.1'
    default_timeout = 60

    def cmdline(self, o):
        o.add_option('-w', '--warning', metavar='SECONDS', dest='warning',
                     help='warning if response time more than SECONDS')
        o.add_option('-c', '--critical', metavar='SECONDS', dest='critical',
                     help='warning if response time more than SECONDS')
        o.add_option('-s', '--string', dest='stringmatch', default='',
                     help='string to expect in the content')
        o.add_option('-H', '--hostname', dest='hostname',
                     help='HTTP host to connect to')

    def setup(self, opts, args):
        self.probe = HTTPProbe(opts.hostname)
        self.evaluator = HTTPEvaluator(opts.warning, opts.critical,
                                       opts.stringmatch)

    def __call__(self):
        self.evaluator()
        self.status = self.evaluator.status
        self.performance = self.evaluator.performance


def main():
    nagiosplugin.main(HTTPCheck())
