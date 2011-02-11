#!/usr/bin/python3

import io
import unittest
import load


class TestLoadProbe(unittest.TestCase):

    def setUp(self):
        def mock_open(fn, *args, **kw):
            if fn == '/proc/loadavg':
                return io.StringIO('1.24 0.92 0.80 1/296 2554\n')
            elif fn == '/proc/cpuinfo':
                return io.StringIO("""\
processor	: 0
vendor_id	: GenuineIntel
cpu family	: 6
model		: 23
model name	: Intel(R) Core(TM)2 Duo CPU     E8400  @ 3.00GHz
stepping	: 10
cpu MHz		: 2000.000

processor	: 1
vendor_id	: GenuineIntel
cpu family	: 6
model		: 23
model name	: Intel(R) Core(TM)2 Duo CPU     E8400  @ 3.00GHz
stepping	: 10
cpu MHz		: 2000.000

""")
            return NotImplementedError
        io.open = mock_open

    def test_probe_should_return_load(self):
        p = load.LoadProbe()
        values = list(p())
        self.assertEqual(3, len(values))
        for (expected, actual) in zip(values, [1.24, 0.92, 0.80]):
            self.assertAlmostEqual(expected, actual)

    def test_probe_should_return_normalized_load(self):
        p = load.LoadProbe(True)
        values = list(p())
        for (expected, actual) in zip(values, [0.62, 0.46, 0.40]):
            self.assertAlmostEqual(expected, actual)


class FakeLoadProbe(load.LoadProbe):

    def __call__(self):
        return [0.5, 0.729, 1.256]


class TestLoadEvaluator(unittest.TestCase):

    def test_load_should_give_ok(self):
        e = load.LoadEvaluator(2, 3, FakeLoadProbe())
        e()
        self.assertEqual(load.Ok, e.status)

    def test_load_should_give_warning(self):
        e = load.LoadEvaluator(1, 3, FakeLoadProbe())
        e()
        self.assertEqual(load.Warning, e.status)

    def test_load_should_give_critical(self):
        e = load.LoadEvaluator(1.0, 1.2, FakeLoadProbe())
        e()
        self.assertEqual(load.Critical, e.status)


if __name__ == '__main__':
    unittest.main()
