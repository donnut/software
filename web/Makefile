# Generating a website for the Translation Project.
# Copyright © 1999, 2000 Progiciels Bourbeau-Pinard inc.
# François Pinard <pinard@iro.umontreal.ca>, 1999.

cgidir = /home/benno/var/TP/cgi-bin
htmldir = /home/benno/var/TP/html
progsdir = /home/benno/TP
cachedir= /home/benno/var/TP/cache
libdir = $(progsdir)/lib

CGI_FILES = registry.cgi
HTML_FILES = domains.html teams.html

LAYOUT_DEPS = ../web/lib/config.py layout.html to-html
REGISTRY_DEPS = html-to-cgi $(cachedir)/postats $(cachedir)/registry


all: cgi html

cgi: $(addprefix $(cgidir)/,$(CGI_FILES))

html: $(addprefix $(htmldir)/,$(HTML_FILES))
	PYTHONPATH=$(libdir):$$PYTHONPATH \
	  ./to-html -C $(htmldir) ../doc $(distdir)

$(addprefix $(cgidir)/,$(CGI_FILES)): $(cgidir)
$(addprefix $(htmldir)/,$(HTML_FILES)): $(htmldir)
$(cgidir) $(htmldir):
	mkdir -p $@

$(cgidir)/%.cgi: %.cgi.in
	sed 's,@topdir@,$(progsdir),g;s,@libdir@,$(libdir),g' $< > $@-tmp
	chmod a+rx $@-tmp
	mv -f $@-tmp $@

$(htmldir)/domains.html: $(REGISTRY_DEPS)
	PYTHONPATH=$(libdir):$$PYTHONPATH \
	  ./html-to-cgi -C $(htmldir) -D

$(htmldir)/teams.html: $(REGISTRY_DEPS)
	PYTHONPATH=$(libdir):$$PYTHONPATH \
	  ./html-to-cgi -C $(htmldir) -T

lint: all
	find $(htmldir) -name '*.html' | while read file; do \
	  case $$file in \
	    *po*) nsgmls -s $$file 2>&1 | egrep -v '"P"|"SMALL"' ;; \
	    *gettext*) nsgmls -s $$file 2>&1 | egrep -v '"P"|"SMALL"' ;; \
	    *) nsgmls -s $$file ;; \
	  esac; \
	done
	-weblint -x Netscape $(htmldir) \
	| egrep -v 'cyan|empty container element <P>|'
