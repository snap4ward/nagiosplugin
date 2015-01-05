from nagiosplugin.metric import Metric
import warnings

try:
    import unittest2 as unittest
except ImportError:  # pragma: no cover
    import unittest


class MetricTest(unittest.TestCase):

    def test_valueunit_float(self):
        self.assertEqual('1.302s', Metric('time', 1.30234876, 's').valueunit)

    def test_valueunit_scientific(self):
        self.assertEqual('1.3e+04s', Metric('time', 13000., 's').valueunit)

    def test_valueunit_should_not_use_scientific_for_large_ints(self):
        self.assertEqual('13000s', Metric('time', 13000, 's').valueunit)

    def test_valueunit_nonfloat(self):
        self.assertEqual('text', Metric('text', 'text').valueunit)

    def test_evaluate_fails_if_no_context(self):
        with self.assertRaises(RuntimeError):
            Metric('time', 1, 's').evaluate()

    def test_performance_fails_if_no_context(self):
        with self.assertRaises(RuntimeError):
            Metric('time', 1, 's').performance()

    def test_description_should_issue_warning(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            Metric('time', 12800, 's').description
            self.assertEqual(1, len(w))
            self.assertIs(w[0].category, DeprecationWarning)
