#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# Copyright © 2002,2003 Translation Project.
# Copyright © 2000, 2001 Progiciels Bourbeau-Pinard inc.
# François Pinard <pinard@iro.umontreal.ca>, 2000.

"""\
Configuration variables for this project.
"""

import socket, string

package = 'po'
host = string.split(socket.gethostname(), '.')[0]

if host in ('frontal', 'frontal01', 'frontal02', 'frontal03', 'frontal04', 'frontal05', 'webby', 'anex', 'vor', 'bor', 'callisto', 'trex', 'grange'):
    top_directory = '/home/www/usagers/gnutra/HTML'
    cgi_base = 'http://www.iro.umontreal.ca/translation'
    home_base = 'http://www.iro.umontreal.ca/translation'
    html_base = 'http://www.iro.umontreal.ca/translation' 
elif host in ('mira', 'tux'):
    import os
    top_directory = os.path.expanduser('~/%s' % package)
    cgi_base = 'http://www.iro.umontreal.ca/translation'
    home_base = 'http://www.iro.umontreal.ca/translation'
    html_base = 'http://www.iro.umontreal.ca/translation'
elif string.find(host, "pr-web") != -1 or string.find(host, "pr-shell") != -1:
    # translation.sourceforge.net
    top_directory = "/home/groups/t/tr/translation/htdocs"
    cgi_base = "http://translation.sf.net/cgi-bin"
    home_base = "http://translation.sf.net/"
    html_base = "http://translation.sf.net/"
elif host in ('galadriel',): # Personnal machine of Martin Quinson
    top_directory = "/home/mquinson/L10N/TP/po"
    cgi_base = "http://%s/cgi-bin" % host
    home_base = "http://%s/" % host
    html_base = "http://%s/" % host
elif host in ('neoduik',): # The machine of Vrijschrift
    top_directory = "/home/benno/TP"
    cgi_base = 'http://www.vrijschrift.org/~benno/'
    home_base = 'http://www.vrijschrift.org/~benno/'
    html_base = 'http://www.vrijschrift.org/~benno/'
else:
    raise "Sorry, I was not configured for the host %s. Please help me" % host
    
environ = {
    'long_package_name': 'Translation Project',
    'package_name': 'gettext',
    'stable_version': '0.11',
    'current_version': '0.11',
    'margin_color': 'white',
    'caption_color': 'cyan',
    'html_layout_file': '%s/web/layout.html' % top_directory,
    'cgi_base': cgi_base,
    'home_base': home_base,
    'html_base': html_base,
    }
