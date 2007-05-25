# Generating some web pages for the Translation Project.
# Copyright © 1999, 2000 Progiciels Bourbeau-Pinard inc.
# François Pinard <pinard@iro.umontreal.ca>, 1999.

htmldir = /home/benno/var/TP/html

ALL_FILES = maintainers.all leaders.all translators.all \
            files.all robot.all software.all
HTMLA_FILES = $(ALL_FILES:.all=.html)

HTM_FILES = index.htm thanks.htm whydisclaim.htm
HTMLH_FILES = $(HTM_FILES:.htm=.html)


all: $(htmldir) $(addprefix $(htmldir)/,$(HTMLA_FILES)) \
                $(addprefix $(htmldir)/,$(HTMLH_FILES))

$(htmldir):
	mkdir -p $@

$(htmldir)/%.html: %.all
	../web/to-html -C $(htmldir) $<

$(htmldir)/%.html: %.htm
	../web/to-html -C $(htmldir) $<

