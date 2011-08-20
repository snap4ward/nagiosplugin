# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

"""Example plugin modelled after the original check_load plugin"""

import optparse
import nagiosplugin
import logging

LOG = logging.getLogger('nagiosplugin')


class LoadProbe(object):

    """Determine system load averages from /proc/loadavg."""

    def __init__(self):
        """Create probe object."""
        self.procloadavg = '/proc/loadavg'
        self.proccpuinfo = '/proc/cpuinfo'

    def loadavg(self):
        """Determine load averages and return them as 3-tuple."""
        line = open(self.procloadavg).readline()
        LOG.debug('read from %s: %r', self.procloadavg, line)
        return tuple(float(l) for l in line.split(u' ')[0:3])

    def cpucount(self):
        """Determine the number of processors."""
        cpus = 0
        for line in open(self.proccpuinfo):
            fields = [field.strip() for field in line.split(':')]
            if fields[0] == 'processor':
                LOG.debug('found processor line in %s: "%s"', self.proccpuinfo,
                          line.strip())
                cpus += 1
        if cpus > 1 and cpus % 2:
            LOG.warning('odd number of cpus: %s', cpus)
        return cpus


class LoadEvaluator(object):

    """Determine if probed load averages fall into ranges."""

    def __init__(self, probe, thresholds, percpu):
        """Create evaluator object.

        `probe` is a Probe instance configured according to the local system.
        `thresholds` is a list of up to three threshold values.
        `percpu` is a flag which indicates if the load values should be
        normalized.
        """
        self.probe = probe
        self.thresholds = thresholds
        self.percpu = percpu
        self.names = [u'load1', u'load5', u'load15']
        self.load = []

    def evaluate(self):
        """Retrieve load information from probe."""
        LOG.debug('thresholds set: %r', self.thresholds)
        self.load = self.probe.loadavg()
        LOG.info('probed load values: %r', self.load)
        if self.percpu:
            self.normalize()

    def normalize(self):
        """Divide load through number of CPUs."""
        cpus = self.probe.cpucount()
        LOG.info('cpus counted: %s', cpus)
        self.load = [load / cpus for load in self.load]

    def state(self):
        """Return list of states for all load averages."""
        states = [threshold.match(load, messages={
            'OK': None,
            'DEFAULT': '{0} $value is outside range $range'.format(name),
        }) for name, load, threshold in zip(
            self.names, self.load, self.thresholds)]
        return (states +
                [nagiosplugin.Ok(' '.join([str(l) for l in self.load]))])

    def performance(self):
        """Return dict of performance values for all load averages."""
        perf = []
        for i in range(3):
            try:
                perf.append(nagiosplugin.Performance(
                    self.load[i], minimum=0, threshold=self.thresholds[i]))
            except IndexError:
                perf.append(nagiosplugin.Performance(self.load[i], minimum=0))
        return zip(self.names, perf)


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
    if len(opts.warning) > 3 or len(opts.critical) > 3:
        optp.error('use at most three ranges')
    thresholds = nagiosplugin.Threshold.create_multi(
        opts.warning.split(','), opts.critical.split(','), 3)
    probe = LoadProbe()
    evaluator = LoadEvaluator(probe, thresholds, opts.percpu)
    nagiosplugin.run('LOAD', evaluator, verbosity=opts.verbose,
                     timeout=opts.timeout)
