# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

"""Define Cookie class to store persistent data.

A Cookie allow to store unstructured data or dict/list structures in a
human-readable file. This file can be loaded by the next plugin run.
This is used for example by a log file reader to remeber the last file
position seen.
"""

import fcntl
import json
import os.path


class Cookie(object):
    """Store persistent state between consecutive plugin runs.

    Cookie objects have both get()/set() methods for unstructured data
    and getstruct()/setstruct() for structured data which is dumped as
    JSON. After setting data, a call to Cookie.close() commits it to
    disk. Alternatively, Cookies can be used as context manager.
    During usage, the cookie file is locked.
    """
    def __init__(self, filename, defaultdir=None):
        """Initialize Cookie object.

        `filename` sets the file where the persistent state should be
        stored. `defaultdir` provides a default directory in case
        `filename` is a relative path.
        """
        self.path = filename
        self.fileobj = None
        self.old_content = None
        self.new_content = None
        if defaultdir and not os.path.isabs(filename):
            self.path = os.path.normpath(os.path.join(defaultdir, filename))
        if os.path.exists(self.path):
            self._open()
            self.fileobj.seek(0)
            self.old_content = self.fileobj.read()

    def __enter__(self):
        """Provide Cookie as context.

        Use it like a file "with" clause::

            with Cookie('filename') as cookie:
                cookie.get(...)
                cookie.set(...)
        """
        return self

    def __exit__(self, _exc_type, _exc_val, _exc_tb):
        """Save cookie context to disk."""
        self.close()
        return False

    def _open(self):
        """Open and lock the file."""
        if self.fileobj:
            raise RuntimeError('should not re-open already locked cookie file',
                               self.path)
        self.fileobj = open(self.path, 'a+')
        fcntl.lockf(self.fileobj, fcntl.LOCK_EX)

    def close(self):
        """Sync cookie's content to disk if changed."""
        if not os.path.exists(self.path):
            self._open()
        self.fileobj.seek(0)
        self.fileobj.truncate()
        self.fileobj.write(self.new_content)
        self.fileobj.close()
        self.fileobj = None

    def get(self):
        """Return the cookie's content at the time of object creation."""
        return self.old_content

    def set(self, content):
        """Update the cookie's content to `content`.

        Writing the new content to disk is deferred until Cookie.close()
        is called.
        """
        self.new_content = content

    def setstruct(self, struct):
        """Write structured data into Cookie.

        `struct` may be anything that is serializable by the json
        module. This includes str, unicode, int, long, float, bool,
        None, list, tuple, dict.
        """
        encoder = json.JSONEncoder(sort_keys=True, indent=2)
        self.new_content = encoder.encode(struct) + u'\n'

    def getstruct(self):
        """Return the Cookie's content as structured data.

        The Cookie is assumed to contain a json dump. If this is not the
        case, a ValueError is raised.
        """
        if not self.old_content:
            return None
        return json.loads(self.old_content)
