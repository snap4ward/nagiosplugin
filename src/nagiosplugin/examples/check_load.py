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
        self.load = (None, None, None)

    def __call__(self):
        """Determine load averages and save them as 3-tuple in self.load."""
        line = open(self.loadavg).readline()
        LOG.debug('read from %s: %r', self.loadavg, line)
        self.load = tuple(float(l) for l in line.split(u' ')[0:3])
        LOG.info('probed load values: %r', self.load)


class LoadEvaluator(object):

    """Determine if probed load averages fall into ranges."""

    def __init__(self, warning, critical):
        """Create evaluator object with up to 3 ranges."""
        self.name = [u'load1', u'load5', u'load15']
        self.threshold = []
        self.load = []
        if len(warning) < len(critical):
            warning += [None] * (len(critical) - len(warning))
        elif len(critical) < len(warning):
            critical += [None] * (len(warning) - len(critical))
        for warn, crit in zip(warning, critical):
            self.threshold.append(nagiosplugin.Threshold(warn, crit))

    def evaluate(self, probe):
        """Retrieve load information from probe."""
        LOG.info('thresholds set: %r', self.threshold)
        self.load = probe.load

    def state(self):
        """Return list of states for all load averages."""
        states = [t.match(l, messages={
            'OK': None,
            'DEFAULT': '{0} %val is outside %range'.format(n),
        }) for n, l, t in zip(self.name, self.load, self.threshold)]
        return (states +
                [nagiosplugin.Ok(' '.join([str(l) for l in self.load]))])

    def performance(self):
        """Return dict of performance values for all load averages."""
        perf = []
        for i in range(3):
            try:
                perf.append(nagiosplugin.Performance(
                    self.load[i], minimum=0, threshold=self.threshold[i]))
            except IndexError:
                perf.append(nagiosplugin.Performance(self.load[i], minimum=0))
        return dict((n, p) for n, p in zip(self.name, perf))


def main():
    """Console script for load check."""
    optp = optparse.OptionParser(
        description=u'Check system load against thresholds.',
        usage=u'%prog [-r] [-w WARN1[,WARN5[,WARN15]]] '
              u'[-c CRIT1[,CRIT5[,CRIT15]]]',
        version=u'0.1')
    nagiosplugin.standard_options(
        optp, timeout=True, verbose=True,
        warning=u'load average outside RANGE results in warning',
        critical=u'load average outside RANGE results in critical')
    optp.add_option('-r', '--percpu', action='store_true', default=False,
                    help=u'Base thresholds on per-CPU load averages')
    opts, args = optp.parse_args()
    if len(args):
        optp.error(u'superfluous arguments')
    warning = opts.warning.split(',')
    if not len(warning):
        warning = [None, None, None]
    elif len(warning) > 3:
        optp.error('use at most three warning ranges')
    else:
        warning += [warning[-1]] * (3 - len(warning))
    critical = opts.critical.split(',')
    if not len(critical):
        critical = [None, None, None]
    elif len(critical) > 3:
        optp.error('use at most three critical ranges')
    else:
        critical += [critical[-1]] * (3 - len(critical))
    nagiosplugin.run('LOAD', LoadProbe(opts.percpu),
                     LoadEvaluator(warning, critical), verbosity=opts.verbose,
                     timeout=opts.timeout)
