# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

"""Define Cookie class to store persistent data."""

import fcntl
import os.path


class Cookie(object):
    """Store persistent state between consecutive plugin runs.

    A Cookie allow to store unstructured data or dict/list structures in a
    human-readable file. This file can be loaded by the next plugin run. This
    is used for example by a log file reader to remeber the last file position
    seen.

    During usage, the cookie file is locked.
    """
    def __init__(self, filename, defaultdir=None):
        """Initialize Cookie object.

        `filename` sets the file where the persistent state should be stored.
        `defaultdir` provides a default directory in case `filename` is a
        relative path.
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

    def _open(self):
        """Open and lock the file."""
        if self.fileobj:
            raise(RuntimeError,
                  'should not re-open already locked cookie file', self.path)
        self.fileobj = open(self.path, 'a+')
        fcntl.lockf(self.fileobj, fcntl.LOCK_EX)

    def get(self):
        """Return the cookie's content at the time of object creation."""
        return self.old_content

    def set(self, content):
        """Update the cookie's content to `content`.

        Writing the new content to disk is deferred until Cookie.close()
        is called.
        """
        self.new_content = content

    def close(self):
        """Sync cookie's content to disk if changed."""
        if not os.path.exists(self.path):
            self._open()
        self.fileobj.seek(0)
        self.fileobj.truncate()
        self.fileobj.write(self.new_content)
        self.fileobj.close()
        self.fileobj = None
