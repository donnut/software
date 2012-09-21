#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright © 2002, 2003, 2007 Translation Project.
# Copyright © 2000, 2001 Progiciels Bourbeau-Pinard inc.
# François Pinard <pinard@iro.umontreal.ca>, 2000.

"""\
Configuration variables.
"""

import socket, string

host = string.split(socket.gethostname(), '.')[0]

if host in ('duik',):  # The machine at Vrijschrift.
    home_path = "/home/tp"
    site_base = "http://translationproject.org"
elif host in ('ordesa',):  # Benno's personal machine.
    home_path = "/home/ben/TP"
    site_base = "/home/ben/TP/site"
elif host in ('lidb-laptop',): # LI Daobing's personal machine
    home_path = '/home/lidb/workspace/TP'
    site_base = '/home/lidb/workspace/TP/site'
elif host in ('cassiopeia',):  # Erwin's personal machine.
    home_path = "/home/donnut/TP"
    site_base = "/home/donnut/TP/site"
elif host in ('dioganes',):  # Erwin's second personal machine.
    home_path = "/home/donnut/TP"
    site_base = "/home/donnut/TP/site"
else:
    raise RuntimeError("Not configured for host '%s' -- edit config.py file." % host)

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
feed_path = site_path + "/feeds"

domain_path = site_path + "/domain"
team_path = site_path + "/team"

environ = {
    'headline_color': '#d7ffd7',
    'caption_color': '#c7ffd7',
    'margin_color': 'white',
    'html_layout_file': '%s/webgen/layout.html.in' % progs_path,
    'site_base': '%s' % site_base
    }
