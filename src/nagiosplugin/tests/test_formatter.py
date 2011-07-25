# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

import nagiosplugin
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from nagiosplugin.formatter import Formatter


class FormatterTest(unittest.TestCase):

    def test_capitalize_pluginname(self):
        f = Formatter(u'lowercase')
        self.assertEqual(u'LOWERCASE', f.pluginname)

    def test_addstate(self):
        f = Formatter('')
        f.addstate(nagiosplugin.Critical([u'msg1', u'msg2', u'msg3']))
        self.assertEqual(f.text, u'CRITICAL - msg1')
        self.assertListEqual(f.longoutput, [u'msg2', u'msg3'])

    def test_addstate_should_handle_null_message_gracefully(self):
        f = Formatter(u'PLUGIN')
        f.addstate(nagiosplugin.state.Ok())
        self.assertEqual(f.render(), u'PLUGIN OK')

    def test_addlongoutput_should_strip_newlines(self):
        f = Formatter('')
        f.addlongoutput([u'first line\n', u'second line\n'])
        self.assertListEqual(f.longoutput, [u'first line', u'second line'])

    def test_addlongout_add_multiline_string(self):
        f = Formatter('')
        f.addlongoutput(u'multi line\nstring\n')
        self.assertListEqual(f.longoutput, [u'multi line\nstring'])

    def test_render(self):
        f = Formatter('PLUGIN')
        f.addstate(nagiosplugin.Ok([u'msg1', u'msg2']))
        self.assertMultiLineEqual(f.render(), u"""\
PLUGIN OK - msg1
msg2""")
