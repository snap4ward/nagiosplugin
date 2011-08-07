# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

"""Partial re-implementation of check_http.

This examples illustrates basic nagiosplugin API features via a partial
re-implemetation of the original check_http plugin.
"""

from __future__ import print_function

import logging
import nagiosplugin
import optparse
import time
import urllib2

LOG = logging.getLogger('nagiosplugin')


class HTTPProbe(object):
    """Retrieve a HTTP object and examine it."""

    def __init__(self, hostname):
        self.hostname = hostname
        self.start = None
        self.stop = None
        self.response = None
        self.url = 'http://{0}/'.format(self.hostname)

    def __call__(self):
        LOG.info('opening URL %s', self.url)
        self.fetch_url()
        LOG.debug(u'start: %s, stop: %s', self.start, self.stop)
        LOG.debug(self.response)

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

    @property
    def responsetime(self):
        return self.stop - self.start


class HTTPEvaluator(object):

    def __init__(self, warn, crit, stringmatch=None):
        self.threshold = nagiosplugin.Threshold(warn, crit)
        self.stringmatch = stringmatch
        self.state = None
        self.performance = None

    def __call__(self, probe):
        self.state = [self.check_time(probe), self.check_string(probe)]
        self.performance = {'time': nagiosplugin.Performance(
            probe.responsetime, 's', 0, threshold=self.threshold)}

    def check_string(self, probe):
        if not self.stringmatch:
            return None
        if self.stringmatch.encode() in probe.response:
            return nagiosplugin.Ok('{0!r} found in response'.format(
                self.stringmatch))
        LOG.warning('stringmatch {0!r} failed'.format(
            self.stringmatch))
        return nagiosplugin.Critical(
            '{0!r} not found in response'.format(self.stringmatch))

    def check_time(self, probe):
        return self.threshold.match(
            probe.responsetime,
            default_msg=u'{0} Bytes in {1:.3g} s'.format(
                len(probe.response), probe.responsetime))


def main():
    optp = optparse.OptionParser(
        description=u"Check a HTTP server's response time and output",
        usage=u'%prog -H HOSTNAME [options]',
        version=u'0.1')
    optp.add_option('-t', '--timeout', metavar='SECONDS', dest='timeout',
                    type='int', default=120,
                    help=u'abort execution after SECONDS (default: %default)')
    optp.add_option('-w', '--warning', metavar='SECONDS', dest='warning',
                    help=u'warning if response time is more than SECONDS')
    optp.add_option('-c', '--critical', metavar='SECONDS', dest='critical',
                    help=u'critical if response time is more than SECONDS')
    optp.add_option('-s', '--stringmatch', metavar='STRING',
                    dest='stringmatch', default=None,
                    help=u'HTTP response must contain STRING')
    optp.add_option('-H', '--hostname', dest='hostname',
                    help=u'HTTP host to connect to')
    optp.add_option('-v', '--verbose', dest='verbose', action='count',
                    default=0, help=u'increase verbosity')
    opts, args = optp.parse_args()
    if not opts.hostname:
        optp.error(u'need at least a hostname')
    if args:
        optp.error(u'superfluous arguments: {0!r}'.format(args))
    probe = HTTPProbe(opts.hostname)
    evaluator = HTTPEvaluator(opts.warning, opts.critical, opts.stringmatch)
    nagiosplugin.run('HTTP', probe, evaluator, verbosity=opts.verbose,
                     timeout=opts.timeout)
