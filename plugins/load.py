# Python 3

import io


class LoadProbe(object):

    def __init__(self, percpu=False):
        pass

    def probe(self):
        return map(float, io.open('/proc/loadavg').read().split()[:3])


class LoadEvaluator(object):

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

