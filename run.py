#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Script zum einfachen Starten der Anwendung.
"""


import sys

import ddsw_chat.application


try:
    port = int(sys.argv[1])
except:
    port = 8080


ddsw_chat.application.app.start(port)