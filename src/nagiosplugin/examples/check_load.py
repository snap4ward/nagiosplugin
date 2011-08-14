# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

"""Example plugin modelled after the original check_load plugin"""

import optparse
import nagiosplugin
import logging

LOG = logging.getLogger('nagiosplugin')


class LoadProbe(object):

    """Determine system load averages from /proc/loadavg."""

    def __init__(self, percpu=False):
        """Create probe object.

        If percpu is true, load averages are normalized by the number of
        processors as indicated by /proc/cpuinfo.
        """
        self.percpu = percpu
        self.loadavg = '/proc/loadavg'
        self.cpuinfo = '/proc/cpuinfo'

    def __call__(self):
        """Determine load averages and save them as 3-tuple in self.load."""
        load = open(self.loadavg).readline().split(u' ')
        LOG.debug('read from %s: %r', self.loadavg, load)
        self.load = tuple(float(l) for l in load[0:3])
        LOG.info('probed load values: %r', self.load)


class LoadEvaluator(object):

    """Determine if probed load averages fall into ranges."""

    def __init__(self, warning, critical):
        """Create evaluator object with up to 3 ranges."""
        self.threshold = []
        if len(warning) < len(critical):
            warning += [None] * (len(critical) - len(warning))
        if len(critical) < len(warning):
            critical += [None] * (len(warning) - len(critical))
        for warn, crit in zip(warning, critical):
            self.threshold.append(nagiosplugin.Threshold(warn, crit))

    def evaluate(self, probe):
        LOG.info('thresholds set: %r', self.threshold)

    def state(self):
        """Return list of states for all load averages."""
        return []

    def performance(self):
        """Return dict of performance values for all load averages."""
        return {}


def main():
    optp = optparse.OptionParser(
        description=u'Check system load against thresholds.',
        usage=u'%prog [-r] [-w WARN1[,WARN5[,WARN15]]] '
              u'[-c CRIT1[,CRIT5[,CRIT15]]]',
        version=u'0.1')
    optp.add_option('-t', '--timeout', metavar='SECONDS', dest='timeout',
                    type='int', default=15,
                    help=u'abort execution after SECONDS (default: %default)')
    optp.add_option('-w', '--warning', metavar='LOADAVG', dest='warning',
                    default='',
                    help=u'Warning if load average is outside the range. Up '
                         u'to three comma separated ranges may be given')
    optp.add_option('-c', '--critical', metavar='LOADAVG', dest='critical',
                    default='',
                    help=u'Critical if load average is outside the range. Up '
                         u'to three comma separated ranges may be given')
    optp.add_option('-r', '--percpu', action='store_true', default=False,
                    help=u'Base thresholds on per-CPU load averages')
    optp.add_option('-v', '--verbose', dest='verbose', action='count',
                    default=0, help=u'increase verbosity')
    opts, args = optp.parse_args()
    warning = opts.warning.split(',')
    if len(warning) > 3:
        optp.error('use at most three warning ranges')
    critical = opts.critical.split(',')
    if len(critical) > 3:
        optp.error('use at most three critical ranges')
    nagiosplugin.run('LOAD', LoadProbe(opts.percpu),
                     LoadEvaluator(warning, critical), verbosity=opts.verbose,
                     timeout=opts.timeout)
