# Generating some web pages for the Translation Project.
# Copyright © 1999, 2000 Progiciels Bourbeau-Pinard inc.
# François Pinard <pinard@iro.umontreal.ca>, 1999.

htmldir = /home/benno/www/HTML
topdir = /home/benno/TP
libdir = $(topdir)/web/lib

ALL_FILES = maintainers.all leaders.all translators.all software.all status.all
HTML_FILES = $(ALL_FILES:.all=.html)


all: $(htmldir) $(HTML_FILES) ../web/to-html

$(htmldir):
	mkdir -p $@

%.html: %.all
	PYTHONPATH=$(libdir):$$PYTHONPATH \
	    ../web/to-html -C $(htmldir) $<

