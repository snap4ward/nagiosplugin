# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

import unittest
import nagiosplugin.state

from nagiosplugin.state import State, Ok, Warning, Critical, Unknown


class StateTest(unittest.TestCase):

    def test_messages_is_list_on_empty_params(self):
        self.assertEqual([], Unknown().messages)

    def test_str(self):
        self.assertEqual(u'OK', str(Ok()))

    def test_int(self):
        self.assertEqual(0, int(Ok()))

    def test_cmp_less(self):
        self.assertEqual(-1, cmp(Warning(), Critical()))

    def test_cmp_equal(self):
        self.assertEqual(0, cmp(Unknown(), Unknown()))

    def test_cmp_greater(self):
        self.assertEqual(1, cmp(Warning(), Ok()))

    def test_firstline(self):
        s = Ok([u'first line', u'more lines 1', u'more lines 2'])
        self.assertEqual(u'first line', s.headline())

    def test_longoutput(self):
        s = Ok([u'first line', u'more lines 1', u'more lines 2'])
        self.assertEqual([u'more lines 1', u'more lines 2'],
                         s.longoutput())

    def test_add_should_discard_minor_status(self):
        s_crit = Critical(u'problem')
        s_ok = Ok(u'no problem')
        self.assertEqual(s_crit, s_crit + s_ok)

    def test_add_should_not_concant_messages_of_minor_state(self):
        s1 = Warning([u'msg 1', u'msg 2'])
        s2 = Unknown([u'msg 3', u'msg 4'])
        self.assertEqual([u'msg 3', u'msg 4'], (s1 + s2).messages)

    def test_add_should_concat_messages_of_equal_states(self):
        s1 = Warning([u'msg 1', u'msg 2'])
        s2 = Warning([u'msg 3', u'msg 4'])
        self.assertEqual([u'msg 1', u'msg 2', u'msg 3', u'msg 4'],
                         (s1 + s2).messages)
