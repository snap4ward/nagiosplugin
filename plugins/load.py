# Python 3

import io
import re


class LoadProbe:

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
        return load


class LoadEvaluator:

    def __init__(self, warn, crit, probe):
        self.warn = warn
        self.crit = crit
        self.probe = probe

    def __call__(self):
        self.load = self.probe()

    @property
    def status(self):
        if any(l >= self.crit for l in self.load):
            return Critical
        elif any(l >= self.warn for l in self.load):
            return Warning
        else:
            return Ok

    def get_message(self):
        return ''

    def get_performance(self):
        return PerformanceObjects


class Status(object):
    """Represents the logical outcome of checks.

    A Status has a numeric state code and a status word denoting the result. In
    addition a state carries one or more message lines. The first message line
    goes into Nagios' main status message and the remaining lines go into
    Nagios' long output (introduced with Nagios 3).
    """

    code = None
    word = None

    def __str__(self):
        """Textual status code."""
        if self.code is None or self.word is None:
            raise NotImplementedError
        return self.word

    def __int__(self):
        """Numeric status code."""
        if self.code is None or self.word is None:
            raise NotImplementedError
        return self.code

    def __cmp__(self, other):
        """Numerical status code comparision."""
        return self.code.__cmp__(other.code)


class Ok(Status):
    code = 0
    word = 'OK'

Ok = Ok()


class Warning(Status):
    code = 1
    word = 'WARNING'

Warning = Warning()


class Critical(Status):
    code = 2
    word = 'CRITICAL'

Critical = Critical()


class Unknown(Status):
    code = 3
    word = 'UNKNOWN'

Unknown = Unknown()
