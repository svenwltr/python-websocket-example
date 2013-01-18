# -*- coding: utf-8 -*-
"""
    Prüft die Anforderungen an das System.
"""

import sys

try:
    import tornado
except ImportError:
    print >>sys.stderr, "Couldn't find package 'tornado'!"
    print >>sys.stderr, "(see http://pypi.python.org/pypi/tornado/)"
    sys.exit(1)
