# Generating the web pages for the Translation Project.
# Copyright (C) 2007 Translation Project.
# Copyright © 1999, 2000 Progiciels Bourbeau-Pinard inc.
# François Pinard <pinard@iro.umontreal.ca>, 1999.

htmldir = /home/tp/site/html

ALL_FILES = maintainers.all leaders.all translators.all \
            files.all robot.all software.all
HTMA_FILES = $(ALL_FILES:.all=.html)
HTMH_FILES = welcome.html thanks.html whydisclaim.html

LAYOUT_DEPS = ../lib/config.py ../web/layout.html.in


all: allfiles htmlfiles

allfiles: $(htmldir) $(addprefix $(htmldir)/,$(HTMA_FILES))

htmlfiles: $(htmldir) $(addprefix $(htmldir)/,$(HTMH_FILES)) 

$(htmldir):
	mkdir -p $@

$(htmldir)/%.html: %.all $(LAYOUT_DEPS)
	../web/to-html -C $(htmldir) $<

$(htmldir)/%.html: %.html $(LAYOUT_DEPS)
	../web/to-html -C $(htmldir) $<

