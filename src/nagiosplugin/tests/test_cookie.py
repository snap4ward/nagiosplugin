# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

from __future__ import print_function
from nagiosplugin.cookie import Cookie
import os
import os.path
import tempfile
import time
import shutil
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class CookieTest(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.mkdtemp(prefix='cookie')
        self.fname = os.path.join(self.tempdir, 'cookie')

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def test_absolute_path(self):
        c = Cookie('/absolute/path')
        self.assertEqual('/absolute/path', c.path)

    def test_relative_path(self):
        c = Cookie('relative/path')
        self.assertEqual('relative/path', c.path)

    def test_defaultdir(self):
        c = Cookie('relative/path', '/prefix')
        self.assertEqual('/prefix/relative/path', c.path)

    def test_init_should_open_existing_file(self):
        open(self.fname, 'w').close()
        c = Cookie(self.fname)
        self.assertIsInstance(c.fileobj, file)

    def test_get_should_return_none_if_cookie_missing(self):
        c = Cookie('newcookie', self.tempdir)
        self.assertIsNone(c.get())

    def test_get_existing_content(self):
        with open(self.fname, 'w') as f:
            print('content', file=f)
        c = Cookie(self.fname)
        self.assertEqual('content\n', c.get())

    def test_set_should_not_modify_file(self):
        with open(self.fname, 'w') as f:
            print('content1', file=f)
        c = Cookie(self.fname)
        c.set('content2\n')
        self.assertEqual('content1\n', open(self.fname).read())

    def test_set_close_should_write_file(self):
        with open(self.fname, 'w') as f:
            print('content1', file=f)
        c = Cookie(self.fname)
        c.set('content2\n')
        c.close()
        self.assertEqual('content2\n', open(self.fname).read())

    def test_close_should_create_file(self):
        c = Cookie(self.fname)
        c.set('content\n')
        c.close()
        self.assertTrue(os.path.exists(self.fname))

    def test_close_should_not_touch_file_if_content_unchanged(self):
        with open(self.fname, 'w') as f:
            print('content', file=f)
        mtime = time.time() - 1
        os.utime(self.fname, (mtime, mtime))
        # re-read mtime to avoid rounding issues
        mtime = os.stat(self.fname).st_mtime
        c = Cookie(self.fname)
        c.set('content\n')
        c.close()
        self.assertNotAlmostEqual(os.stat(self.fname).st_mtime, mtime)

    def test_getstruct_should_return_none_if_cookie_missing(self):
        c = Cookie(self.fname)
        self.assertIsNone(c.getstruct())

    def test_getstruct_deserialize_json(self):
        c = Cookie(self.fname)
        c.old_content = '{"key1":2, "key2": [1, 2, 3]}\n'
        self.assertDictEqual(c.getstruct(), {"key1": 2, "key2": [1, 2, 3]})

    def test_getstruct_should_raise_on_invalid_content(self):
        c = Cookie(self.fname)
        c.old_content = '["array started"\n'
        self.assertRaises(ValueError, c.getstruct)

    def test_setstruct_should_serialize(self):
        c = Cookie(self.fname)
        c.setstruct({'key2': 'value', 'key1': 'value', 'key3': 'value'})
        self.assertMultiLineEqual(c.new_content, """\
{
  "key1": "value",\x20
  "key2": "value",\x20
  "key3": "value"
}
""")

    def test_contextmanager(self):
        with Cookie(self.fname) as cookie:
            cookie.set('content')
        self.assertEqual(open(self.fname).read(), 'content')
