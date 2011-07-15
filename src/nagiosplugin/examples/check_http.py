# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

import nagiosplugin.performance
import nagiosplugin.plugin
import nagiosplugin
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
        return nagiosplugin.MeasuredPerformance(
            self.responsetime, 's', 0)


class HTTPEvaluator(object):

    def __init__(self, warn, crit, stringmatch=False):
        self.threshold = nagiosplugin.Threshold(warn, crit)
        self.stringmatch = stringmatch

    def __call__(self, probe):
        self.probe = probe
        self.state = [self.check_string(), self.check_time()]
        self.performance = [self.probe.performance + self.threshold]

    def check_string(self):
        if self.stringmatch and (
            self.stringmatch.encode() in self.probe.response):
            return nagiosplugin.state.Ok('%s found in response' %
                                         self.stringmatch)
        return nagiosplugin.state.Critical(
            '%s not found in response' % self.stringmatch)

    def check_time(self):
        return self.threshold.match(self.probe.responsetime)


class HTTPCheck(nagiosplugin.Plugin):

    name = u'HTTP'
    description = u"Check a HTTP server's response time and output"
    usage = u'%prog -H HOSTNAME [options]'
    version = u'0.1'
    timeout = 60

    def commandline(self, o):
        o.add_option('-w', '--warning', metavar='SECONDS', dest='warning',
                     help=u'warning if response time is more than SECONDS')
        o.add_option('-c', '--critical', metavar='SECONDS', dest='critical',
                     help=u'critical if response time is more than SECONDS')
        o.add_option('-s', '--stringmatch', metavar='STRING',
                     dest='stringmatch', default='',
                     help=u'HTTP response must contain STRING')
        o.add_option('-H', '--hostname', dest='hostname',
                     help=u'HTTP host to connect to')

    def setup(self, opts, args):
        if not opts.hostname:
            raise RuntimeError(u'need at least a hostname')
        self.probe = HTTPProbe(opts.hostname)
        self.evaluator = HTTPEvaluator(opts.warning, opts.critical,
                                       opts.stringmatch)


def main():
    nagiosplugin.main(HTTPCheck())
