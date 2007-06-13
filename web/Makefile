# Generating a website for the Translation Project.
# Copyright © 1999, 2000 Progiciels Bourbeau-Pinard inc.
# François Pinard <pinard@iro.umontreal.ca>, 1999.

homedir = /home/tp
sitedir = $(homedir)/site

cgidir = $(sitedir)
htmldir = $(sitedir)
passdir = $(sitedir)/pass
cachedir= $(homedir)/cache
progsdir = $(homedir)/progs

CGI_FILES = registry.cgi
PASS_FILES = domains.html teams.html

LAYOUT_DEPS = ../lib/config.py layout.html html-to-cgi to-html


all: cgi pass html

cgi: $(cgidir) $(addprefix $(cgidir)/,$(CGI_FILES))

pass: $(passdir) $(addprefix $(passdir)/,$(PASS_FILES))

html:
	$(MAKE) -C ../doc

$(cgidir) $(passdir):
	mkdir -p $@

$(cgidir)/%.cgi: %.cgi.in
	sed 's,@progsdir@,$(progsdir),g' $< > $@-tmp
	chmod a+rx $@-tmp
	mv -f $@-tmp $@

domains $(passdir)/domains.html: $(LAYOUT_DEPS)
	./html-to-cgi -C $(passdir) -D

teams $(passdir)/teams.html: $(LAYOUT_DEPS)
	./html-to-cgi -C $(passdir) -T

lint: all
	find $(htmldir) $(passdir) -name '*.html' | while read file; do \
	  case $$file in \
	    *po*) nsgmls -s $$file 2>&1 | egrep -v '"P"|"SMALL"' ;; \
	    *gettext*) nsgmls -s $$file 2>&1 | egrep -v '"P"|"SMALL"' ;; \
	    *) nsgmls -s $$file ;; \
	  esac; \
	done
	-weblint -x Netscape $(htmldir) \
	| egrep -v 'cyan|empty container element <P>|'
