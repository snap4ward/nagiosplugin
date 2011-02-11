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

    def probe(self):
        load = map(float, io.open('/proc/loadavg').read().split()[:3])
        if self.percpu:
            cpus = self.count_cpus()
            load = [l/cpus for l in load]
        return load


class LoadEvaluator:

    def __init__(self, warn, crit, probe):
        pass

    def run(self):
        pass

    def get_status(self):
        return StatusObject

    def get_message(self):
        return ''

    def get_performance(self):
        return PerformanceObjects

