# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

from __future__ import print_function

import logging
import nagiosplugin
import optparse
import sys
import time
import urllib2

logger = logging.getLogger('nagiosplugin')


class HTTPProbe(object):

    def __init__(self, hostname):
        self.hostname = hostname

    def __call__(self):
        self.url = 'http://{0}/'.format(self.hostname)
        logger.info('opening URL %s', self.url)
        self.fetch_url()
        logger.debug(u'start: %s, stop: %s', self.start, self.stop)
        logger.debug(self.response)

    def fetch_url(self):
        self.start = time.time()
        req = urllib2.urlopen(self.url)
        self.response = req.read()
        try:
            charset = [param for param in req.headers.getplist()
                       if param.startswith('charset=')][0]
            charset = charset.lstrip('charset=')
        except IndexError:
            charset = 'UTF-8'
        self.stop = time.time()
        self.responsetime = self.stop - self.start


class HTTPEvaluator(object):

    def __init__(self, warn, crit, stringmatch=None):
        self.threshold = nagiosplugin.Threshold(warn, crit)
        self.stringmatch = stringmatch

    def __call__(self, probe):
        self.probe = probe
        self.state = [self.check_string(), self.check_time()]
        self.performance = {'time': nagiosplugin.Performance(
            self.probe.responsetime, 's', 0, threshold=self.threshold))

    def check_string(self):
        if not self.stringmatch:
            return None
        if self.stringmatch.encode() in self.probe.response:
            return nagiosplugin.Ok('"{0}" found in response'.format(
                self.stringmatch))
        return nagiosplugin.Critical(
            '"{0}" not found in response'.format(self.stringmatch))

    def check_time(self):
        return self.threshold.match(
            self.probe.responsetime,
            default_msg=u'{0} Bytes in {1:.3g} s'.format(
                len(self.probe.response), self.probe.responsetime))


def main():
    op = optparse.OptionParser(
        description=u"Check a HTTP server's response time and output",
        usage=u'%prog -H HOSTNAME [options]',
        version=u'0.1')
    op.add_option('-t', '--timeout', metavar='SECONDS', dest='timeout',
                  type='int', default=120,
                  help=u'abort execution after SECONDS (default: %default)')
    op.add_option('-w', '--warning', metavar='SECONDS', dest='warning',
                  help=u'warning if response time is more than SECONDS')
    op.add_option('-c', '--critical', metavar='SECONDS', dest='critical',
                  help=u'critical if response time is more than SECONDS')
    op.add_option('-s', '--stringmatch', metavar='STRING',
                  dest='stringmatch', default=None,
                  help=u'HTTP response must contain STRING')
    op.add_option('-H', '--hostname', dest='hostname',
                  help=u'HTTP host to connect to')
    op.add_option('-v', '--verbose', dest='verbose', action='count', default=0,
                  help=u'increase verbosity')
    opts, args = op.parse_args()
    if not opts.hostname:
        op.error(u'need at least a hostname')
    if args:
        op.error(u'superfluous arguments: {0!r}'.format(args))
    probe = HTTPProbe(opts.hostname)
    evaluator = HTTPEvaluator(opts.warning, opts.critical, opts.stringmatch)
    nagiosplugin.run('HTTP', probe, evaluator, verbosity=opts.verbose,
                     timeout=opts.timeout)
