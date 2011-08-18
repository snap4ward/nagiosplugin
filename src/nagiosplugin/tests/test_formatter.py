# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

from nagiosplugin.formatter import Formatter

import nagiosplugin
import StringIO
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class FormatterTest(unittest.TestCase):

    def test_capitalize_pluginname(self):
        f = Formatter(u'lowercase')
        f.addstate(nagiosplugin.Ok())
        self.assertEqual(u'LOWERCASE OK', f._render_firstline())

    def test_addstate(self):
        f = Formatter('')
        f.addstate(nagiosplugin.Critical([u'msg1', u'msg2', u'msg3']))
        self.assertEqual(f.text, u'CRITICAL - msg1')
        self.assertListEqual(f.longoutput, [u'msg2', u'msg3'])

    def test_addlongoutput_should_strip_newlines(self):
        f = Formatter('')
        f.addlongoutput([u'first line\n', u'second line\n'])
        self.assertListEqual(f.longoutput, [u'first line', u'second line'])

    def test_addlongout_add_multiline_string(self):
        f = Formatter('')
        f.addlongoutput(u'multi line\nstring\n')
        self.assertListEqual(f.longoutput, [u'multi line\nstring'])

    def test_render_firstline_text(self):
        f = Formatter(u'CHECK')
        f.addstate(nagiosplugin.Ok(u'status text'))
        self.assertEqual(f._render_firstline(), u'CHECK OK - status text')

    def test_perfdata_line_should_return_empty_string_if_none(self):
        f = Formatter()
        self.assertEqual(u'', f._perfdata_line())

    def test_perfdata_line_should_concat_perfdata_if_less_linelength(self):
        f = Formatter()
        f.addperformance([('performance1', nagiosplugin.Performance(1, u's')),
                          ('performance2', nagiosplugin.Performance(2, u's'))])
        self.assertEqual(f._perfdata_line(),
                         u'performance1=1s performance2=2s')

    def test_perfdata_line_should_split_perfdata_if_greater_linelength(self):
        f = Formatter()
        f.addperformance([('performance1', nagiosplugin.Performance(1, u's')),
                          ('performance2', nagiosplugin.Performance(2, u's'))])
        self.assertSetEqual(set([f._perfdata_line(20), f._perfdata_line(20)]),
                            set([u'performance1=1s', u'performance2=2s']))

    def test_perfdata_line_should_do_nothing_if_line_too_short(self):
        f = Formatter()
        f.addperformance([('performance1', nagiosplugin.Performance(1, u's')),
                          ('performance2', nagiosplugin.Performance(2, u's'))])
        self.assertEqual(f._perfdata_line(10), u'')

    def test_render_firstline_perfdata(self):
        f = Formatter()
        f.addstate(nagiosplugin.Ok())
        f.addperformance([('performance', nagiosplugin.Performance(1, u's'))])
        self.assertEqual(f._render_firstline(), u'OK | performance=1s')

    def test_render_tail_should_return_longoutput_if_no_perfdata(self):
        f = Formatter()
        f.addlongoutput([u'line1', u'line2'])
        self.assertListEqual(f._render_tail(), [u'line1', u'line2'])

    def test_render_tail_only_perfdata(self):
        f = Formatter()
        f.addperformance([('performance', nagiosplugin.Performance(1, u's'))])
        self.assertListEqual(f._render_tail(), [u'| performance=1s'])

    def test_render_tail_should_flow_perfdata(self):
        f = Formatter(maxlength=30)
        f.addlongoutput(u'0123456789')
        f.addperformance([('performance1', nagiosplugin.Performance(1, u's')),
                          ('performance2', nagiosplugin.Performance(2, u's'))])
        self.assertListEqual(f._render_tail(), [
            u'0123456789 | performance1=1s', u'performance2=2s'])

    def test_renders_minimal(self):
        f = Formatter()
        f.addstate(nagiosplugin.Ok())
        self.assertEqual(f.renders(), u'OK\n')

    def test_renders_maximal(self):
        f = Formatter(u'CHECK', 56)
        f.addstate(nagiosplugin.state.Critical([u'first status message',
                                                u'msg2']))
        f.addlongoutput(u'long debug output from logging')
        f.addperformance([
            ('performance1', nagiosplugin.Performance(1, 's')),
            ('performance2', nagiosplugin.Performance(2, 's')),
            ('performance3', nagiosplugin.Performance(3, 's')),
        ])
        self.assertMultiLineEqual(f.renders(), u"""\
CHECK CRITICAL - first status message | performance1=1s
msg2
long debug output from logging | performance2=2s
performance3=3s
""")

    def test_render(self):
        f = Formatter(u'CHECK')
        f.addstate(nagiosplugin.state.Warning('message'))
        f.addperformance([('performance', nagiosplugin.Performance(1, u's'))])
        f.addlongoutput(u'long output')
        io = StringIO.StringIO()
        f.render(io)
        self.assertMultiLineEqual(io.getvalue(), u"""\
CHECK WARNING - message | performance=1s
long output
""")
