# Copyright (c) gocept gmbh & co. kg
# See also LICENSE.txt

"""Platform-specific services."""

import os

platform = __import__('nagiosplugin.platform.{0}'.format(os.name),
                      fromlist=['with_timeout', 'flock_exclusive'])

with_timeout = platform.with_timeout
flock_exclusive = platform.flock_exclusive
