# Project-specific webpage generation services.
# -*- mode: python; coding: utf-8 -*-
# Copyright © 2011, Translation Project.
# Mikel Olasagasti Uranga <mikel@olasagasti.info>, 2011.
# Erwin Poeze <erwin.poeze@gmail.com>, 2011.

import datetime
import PyRSS2Gen
import feedparser
import config

MAX_ITEMS = 50

def generate_po_rss(translator, pofile, domain, code):
	items = []
	
	"""Generate the first item from data"""
	items.append(PyRSS2Gen.RSSItem(
		title = pofile,
        link = "http://translationproject.org/PO-files/"+code+"/"+pofile,
        description = pofile+" has been updated by "+translator,
        guid = PyRSS2Gen.Guid("http://translationproject.org/domain/"+domain+".html"),
        pubDate = datetime.datetime.utcnow()))

	"""Try to open current RSS file"""
	d = feedparser.parse('%s/tp_po.xml' % config.feed_path)
	if len(d['entries']) < MAX_ITEMS - 1:
		MAX = len(d['entries'])
	else:
		MAX = MAX_ITEMS - 1

	"""Generate MAX items from current RSS file and append to current item"""
	for i in range (0, MAX ):
		items.append(PyRSS2Gen.RSSItem(
			title = d['entries'][i]['title'],
			link = d['entries'][i]['link'],
			description = d['entries'][i]['description'],
			guid = d['entries'][i]['guid'],
			pubDate = d['entries'][i]['date']
		))
	"""Generate RSS file"""
        rss = PyRSS2Gen.RSS2(
                title = "Translation Project RSS for PO files",
                link = "http://www.translationproject.org",
                description = "Latest translated domains",
                lastBuildDate = datetime.datetime.utcnow(),
                items = items)

        rss.write_xml(open('%s/tp_po.xml' % config.feed_path, 'w'), encoding = "utf-8")
	
