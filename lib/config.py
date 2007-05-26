#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# Copyright © 2002, 2003, 2007 Translation Project.
# Copyright © 2000, 2001 Progiciels Bourbeau-Pinard inc.
# François Pinard <pinard@iro.umontreal.ca>, 2000.

"""\
Configuration variables for this project.
"""

import socket, string

host = string.split(socket.gethostname(), '.')[0]

if host in ('neoduik',): # The machine of Vrijschrift
    progs_path = "/home/benno/progs"
    site_path = "/home/benno/site"
    pots_dir = "POT-files"
    pos_dir = "PO-files"
    last_dir = "latest-POs"
    pots_path = site_path+"/"+pots_dir
    pos_path = site_path+"/"+pos_dir
    last_path = site_path+"/"+last_dir
    cgi_base = 'http://tp.vrijschrift.org'
    pass_base = 'http://tp.vrijschrift.org/pass'
    site_base = 'http://tp.vrijschrift.org'
else:
    raise "Not configured for host '%s' -- edit config.py file." % host
    
environ = {
    'long_package_name': 'Translation Project',
    'package_name': 'gettext',
    'stable_version': '0.11',
    'current_version': '0.11',
    'margin_color': 'white',
    'caption_color': 'cyan',
    'html_layout_file': '%s/web/layout.html' % progs_path,
    'cgi_base': cgi_base,
    'pass_base': pass_base,
    'site_base': site_base,
    }
