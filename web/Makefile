# Generating a website for the Translation Project.
# Copyright © 1999, 2000 Progiciels Bourbeau-Pinard inc.
# François Pinard <pinard@iro.umontreal.ca>, 1999.

homedir = /home/tp
sitedir = $(homedir)/site

cgidir = $(sitedir)/cgi
htmldir = $(sitedir)/html
cachedir= $(homedir)/cache
progsdir = $(homedir)/progs

CGI_FILES = registry.cgi domains.html teams.html

LAYOUT_DEPS = ../lib/config.py layout.html html-to-cgi to-html


all: cgi html

cgi: $(cgidir) $(addprefix $(cgidir)/,$(CGI_FILES))

html:
	cp stepinto.html.in $(sitedir)/index.html
	cp ../doc/disclaim.txt $(sitedir)
	$(MAKE) -C ../doc

$(cgidir):
	mkdir -p $@

$(cgidir)/%.cgi: %.cgi.in
	sed 's,@progsdir@,$(progsdir),g' $< > $@-tmp
	chmod a+rx $@-tmp
	mv -f $@-tmp $@

domains $(cgidir)/domains.html: $(LAYOUT_DEPS)
	./html-to-cgi -C $(cgidir) -D

teams $(cgidir)/teams.html: $(LAYOUT_DEPS)
	./html-to-cgi -C $(cgidir) -T

lint: all
	find $(htmldir) $(cgidir) -name '*.html' | while read file; do \
	  case $$file in \
	    *po*) nsgmls -s $$file 2>&1 | egrep -v '"P"|"SMALL"' ;; \
	    *gettext*) nsgmls -s $$file 2>&1 | egrep -v '"P"|"SMALL"' ;; \
	    *) nsgmls -s $$file ;; \
	  esac; \
	done
	-weblint -x Netscape $(htmldir) \
	| egrep -v 'cyan|empty container element <P>|'
