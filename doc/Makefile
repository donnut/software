# Generating some web pages for the Translation Project.
# Copyright © 1999, 2000 Progiciels Bourbeau-Pinard inc.
# François Pinard <pinard@iro.umontreal.ca>, 1999.

htmldir = /home/benno/var/TP/html

ALL_FILES = maintainers.all leaders.all translators.all \
            files.all robot.all software.all
HTMA_FILES = $(ALL_FILES:.all=.html)
HTMH_FILES = index.html thanks.html whydisclaim.html


all: $(htmldir) $(addprefix $(htmldir)/,$(HTMA_FILES)) \
                $(addprefix $(htmldir)/,$(HTMH_FILES))

$(htmldir):
	mkdir -p $@

$(htmldir)/%.html: %.all
	../web/to-html -C $(htmldir) $<

$(htmldir)/%.html: %.html
	../web/to-html -C $(htmldir) $<

