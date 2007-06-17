#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# Copyright © 2002, 2003, 2007 Translation Project.
# Copyright © 2000, 2001 Progiciels Bourbeau-Pinard inc.
# François Pinard <pinard@iro.umontreal.ca>, 2000.

"""\
Configuration variables.
"""

import socket, string

host = string.split(socket.gethostname(), '.')[0]

if host in ('neoduik',):  # The machine at Vrijschrift.
    home_path = "/home/tp"
    site_base = "http://tp.vrijschrift.org"
elif host in ('ordesa',):  # Benno's personal machine.
    home_path = "/home/ben/TP"
    site_base = "http://tp.vrijschrift.org"
else:
    raise "Not configured for host '%s' -- edit config.py file." % host

progs_path = home_path + "/progs"
cache_path = home_path + "/cache"
site_path = home_path + "/site"
temp_path = home_path + "/tmp"

pots_dir = "POT-files"
pos_dir = "PO-files"
last_dir = "latest"

pots_path = site_path + "/" + pots_dir
pos_path = site_path + "/" + pos_dir
last_path = site_path + "/"  + last_dir

cgi_base = site_base
pass_base = site_base + "/pass"

environ = {
    'margin_color': 'white',
    'caption_color': 'cyan',
    'html_layout_file': '%s/web/layout.html' % progs_path,
    }
