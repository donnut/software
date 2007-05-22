#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# Copyright © 2002,2003 Translation Project.
# Copyright © 2000, 2001 Progiciels Bourbeau-Pinard inc.
# François Pinard <pinard@iro.umontreal.ca>, 2000.

"""\
Configuration variables for this project.
"""

import socket, string

host = string.split(socket.gethostname(), '.')[0]

if host in ('neoduik',): # The machine of Vrijschrift
    scripts_dir = "/home/benno/opt/TP"
    data_dir = "/home/benno/var/TP"
    cgi_base = 'http://tp.vrijschrift.org/cgi-bin'
    html_base = 'http://www.vrijschrift.org/~benno'
    data_base = 'http://www.vrijschrift.org/~benno/..'
else:
    raise "Not configured for host '%s' -- edit config.py file." % host
    
environ = {
    'long_package_name': 'Translation Project',
    'package_name': 'gettext',
    'stable_version': '0.11',
    'current_version': '0.11',
    'margin_color': 'white',
    'caption_color': 'cyan',
    'html_layout_file': '%s/web/layout.html' % scripts_dir,
    'cgi_base': cgi_base,
    'html_base': html_base,
    'data_base': data_base,
    }
