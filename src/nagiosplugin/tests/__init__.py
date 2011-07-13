# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

"""Provide compatibility enhancements.

We need some additional methods to help the tests run on all supported Python
version.
"""

import unittest


class TestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        """Monkey-patch methods missing in Python 2.6."""
        super(TestCase, self).__init__(*args, **kwargs)
        try:
            self.assertIsInstance
        except AttributeError:
            self.assertIsInstance = self._assertIsInstance
        try:
            self.assertListEqual
        except AttributeError:
            self.assertListEqual = self._assertListEqual

    def _assertIsInstance(self, obj, cls, message=None):
        """Test that obj is (or is not) an instance of cls."""
        self.assert_(isinstance(obj, cls),
                     message or '%r is not an instance of %r' % (
                         obj, cls))

    def _assertListEqual(self, list1, list2, message=None):
        """Tests that two lists are equal."""
        self.assertEqual(list1, list2, message)
