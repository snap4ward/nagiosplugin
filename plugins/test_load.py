import unittest
import load


class TestLoadProbe(unittest.TestCase):

    def test_probe_should_return_load(self):
        p = load.LoadProbe()
        values = p.probe()
        self.assertEqual(3, len(values))
        for (expected, actual) in zip(values, [1.24, 0.92, 0.80]):
            self.assertAlmostEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
