#!/usr/bin/python2.7

import nagiosplugin.probe
import nagiosplugin.evaluator
import nagiosplugin.status
import nagiosplugin.performance
import optparse
import urllib.request
import time


class HTTPProbe(nagiosplugin.probe.Probe):

    def __init__(self, hostname):
        self.hostname = hostname

    def __call__(self):
        start = time.time()
        req = urllib.request.urlopen('http://{}/'.format(self.hostname))
        self.response = req.read()
        stop = time.time()
        self.responsetime = stop - start

    @property
    def performance(self):
        return performance.MeasuredPerformance(
            'time', self.responsetime, 's', 0)


class HTTPEvaluator(nagiosplugin.evaluator.Evaluator):

    def __init__(self, probe, options):
        self.probe = probe
        self.threshold = nagiosplugin.threshold.Threshold(
            options.warn, options.crit)
        self.stringmatch = options.stringmatch

    def __call__(self, probe):
        self.probe = probe
        string_status = self.check_string()
        time_status = self.check_time()

    @property
    def status(self):
        return [string_status, time_status]

    def check_string(self):
        if self.stringmatch.encode() in self.probe.response:
            return status.Ok('{} found in response'.format(self.stringmatch))
        return status.Critical(
            '{} not found in response'.format(self.stringmatch))

    def check_time(self):
        return self.probe.responsetime in self.threshold

    @property
    def performance(self):
        return [self.probe.performance[0] + self.threshold]


class HTTPCheck(nagiosplugin.check.Check):

    def cmdline_options(self, o, default_opts):
        o.description = 'test http server for response time and output'
        o.add_option('-s', '--string', dest='stringmatch',
                     help='string to expect in the content')
        o.add_option('-C', '--certificate', type='float', default=None,
                     help='minimum number of days a certificate has to be valid')
        return default_opts

    def setup(self, options, arguments):
        if options.certificate is not None:
            self.probe = CertificateProbe(options.hostname)
            self.evaluator = CertificateEvaluator(
                self.probe, options.certificate)
        else:
            self.probe = HTTPProbe(options.hostname)
            self.evaluator = HTTPEvaluator(self.probe, options)

    def __call__(self):
        self.evaluator()
        self.status = self.evaluator.status
        self.performance = self.evaluator.performance

if __name__ == '__main__':
    nagiosplugin.main()
