#!/usr/bin/python3

import io
import re
import optparse
import sys
import collections


class LoadProbe:

    names = ['load1', 'load5', 'load15']

    def __init__(self, percpu=False):
        self.percpu = percpu

    def count_cpus(self):
        r_processor = re.compile(r'^processor\s*:\s*\d')
        cpus = 0
        for line in io.open('/proc/cpuinfo'):
            if r_processor.match(line):
                cpus += 1
        return cpus

    def __call__(self):
        load = map(float, io.open('/proc/loadavg').read().split()[:3])
        if self.percpu:
            cpus = self.count_cpus()
            load = [l/cpus for l in load]
        return collections.OrderedDict(zip(self.names, load))


class LoadEvaluator:

    def __init__(self, warn, crit, probe):
        self.warn = warn
        self.crit = crit
        self.probe = probe

    def __call__(self):
        self.load = self.probe()

    @property
    def status(self):
        if self.crit:
            overthreshold = [(k, v) for (k, v) in self.load.items()
                             if v >= self.crit]
            if overthreshold:
                return Critical(
                    '{} exceeds critical threshold {}'.format(
                        overthreshold[0][0], overthreshold[0][1]))
        if self.warn:
            overthreshold = [(k, v) for (k, v) in self.load.items()
                             if v >= self.warn]
            if overthreshold:
                return Warning(
                    '{} exceeds warning threshold {}'.format(
                        overthreshold[0][0], overthreshold[0][1]))
        return Ok('load averages ' + ', '.join(map(str, self.load.values())))


class Status(object):
    """Represents the logical outcome of checks.

    A Status has a numeric state code and a status word denoting the result. In
    addition a state carries one or more message lines. The first message line
    goes into Nagios' main status message and the remaining lines go into
    Nagios' long output (introduced with Nagios 3).
    """

    code = None
    word = None

    def __init__(self, message):
        self.message = message

    def __str__(self):
        """Textual status code."""
        return '{} - {}'.format(self.word, self.message)

    def __int__(self):
        """Numeric status code."""
        return self.code

    def __cmp__(self, other):
        """Numerical status code comparision."""
        return self.code.__cmp__(other.code)


class Ok(Status):
    code = 0
    word = 'OK'


class Warning(Status):
    code = 1
    word = 'WARNING'


class Critical(Status):
    code = 2
    word = 'CRITICAL'


class Unknown(Status):
    code = 3
    word = 'UNKNOWN'


#------------------------------------------------------------------------

class RawPerformance():

    def __init__(self, label, value, uom=None, min=None, max=None):
        pass


class Performance():

    def __init__(self, rawperformance, warn, crit):
        pass


#------------------------------------------------------------------------


class Check():

    def __init__(self, options):
        p = LoadProbe(options.percpu)
        self.e = LoadEvaluator(options.warn, options.crit, p)

    def __call__(self):
        self.e()
        self.status = self.e.status


#------------------------------------------------------------------------


def main():
    o = optparse.OptionParser(prog='check_load',
                              description='check load average')
    o.add_option('-w', '--warning', dest='warn', type='float',
                 help='warning threshold')
    o.add_option('-c', '--critical', dest='crit', type='float',
                 help='critical threshold')
    o.add_option('-r', '--percpu', dest='percpu', action='store_true', 
                 default=False,
                 help='divide the load averages by the number of CPUs')
    options, arguments = o.parse_args()
    check = Check(options)
    try:
        check()
    except RuntimeError as e:
        print('LOAD UNKNOWN - ' + str(e))
        sys.exit(Unkown.code)
    print('LOAD ' + str(check.status))
    sys.exit(int(check.status))


if __name__ == '__main__':
    main()
