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
        """Create HTTPProbe that connects to `hostname`."""
        self.hostname = hostname
        self.start = None
        self.stop = None
        self.response = None
        self.url = 'http://{0}/'.format(self.hostname)

    def __call__(self):
        """Trigger probe execution."""
        LOG.info('opening URL %s', self.url)
        self.fetch_url()
        LOG.debug(u'start: %s, stop: %s', self.start, self.stop)
        LOG.debug(self.response)

    def fetch_url(self):
        """Retrieve HTTP object and measure time."""
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


class HTTPEvaluator(object):
    """Evalute if HTTP matches given criteria."""

    def __init__(self, probe, options):
        """Create HTTPEvaluator object with match criteria.

        `warn` is the warning time range
        `crit` is the critical time range
        `stringmatch` is a string which must be present in the HTTP
            response body
        """
        self.probe = probe
        self.threshold = nagiosplugin.Threshold(options.warning,
                                                options.critical)
        self.stringmatch = options.stringmatch
        self.response = None
        self.responsetime = None

    def evaluate(self):
        """Retrieve measured values from `probe`."""
        self.probe()
        self.response = self.probe.response
        self.responsetime = self.probe.stop - self.probe.start

    def state(self):
        """Return check states for time and content."""
        return [self.check_time(), self.check_string()]

    def check_string(self):
        """Decide if stringmatch is present in the response."""
        if not self.stringmatch:
            return None
        if self.stringmatch.encode() in self.response:
            return nagiosplugin.Ok('{0!r} found in response'.format(
                self.stringmatch))
        LOG.warning('stringmatch {0!r} failed'.format(
            self.stringmatch))
        return nagiosplugin.Critical(
            '{0!r} not found in response'.format(self.stringmatch))

    def check_time(self):
        """Decide if the answer time is inside the given range."""
        return self.threshold.match(
            self.responsetime, {
                'DEFAULT': u'{0} Bytes in {1:.3g} s'.format(
                    len(self.response), self.responsetime)})

    def performance(self):
        """Return response time as Performance object."""
        return {'time': nagiosplugin.Performance(
            self.responsetime, 's', 0, threshold=self.threshold)}


def main():
    """Console script for HTTP check."""
    optp = optparse.OptionParser(
        description=u"Check a HTTP server's response time and output",
        usage=u'%prog -H HOSTNAME [options]',
        version=u'0.1')
    nagiosplugin.standard_options(
        optp, timeout=True, default_timeout=60, verbose=True, hostname=True,
        warning=u'response time outside RANGE results in warning state',
        critical=u'response time outside RANGE results in critical state')
    optp.add_option('-s', '--stringmatch', metavar='STRING',
                    dest='stringmatch', default=None,
                    help=u'HTTP response must contain STRING')
    opts, args = optp.parse_args()
    if not opts.hostname:
        optp.error(u'need at least a hostname')
    if args:
        optp.error(u'superfluous arguments: {0!r}'.format(args))
    evaluator = HTTPEvaluator(HTTPProbe(opts.hostname), opts)
    nagiosplugin.run('HTTP', evaluator, verbosity=opts.verbose,
                     timeout=opts.timeout)
