# Generating a website for the Translation Project.
# Copyright © 1999, 2000 Progiciels Bourbeau-Pinard inc.
# François Pinard <pinard@iro.umontreal.ca>, 1999.

cgidir = /home/benno/www
htmldir = /home/benno/www/HTML
topdir = /home/benno/TP
libdir = $(topdir)/web/lib

CGI_FILES = babyl.cgi distro.cgi registry.cgi
HTML_FILES = domains.html teams.html

LAYOUT_DEPS = ../web/lib/config.py layout.html to-html
REGISTRY_DEPS = html-to-cgi ../data/postats ../data/registry


$(cgidir)/%.cgi: %.cgi.in
	sed 's,@topdir@,$(topdir),g;s,@libdir@,$(libdir),g' $< > $@-tmp
	chmod a+rx $@-tmp
	mv -f $@-tmp $@

all-iro: $(addprefix $(cgidir)/,$(CGI_FILES)) all-sf

all-sf: $(addprefix $(htmldir)/,$(HTML_FILES))
	$(MAKE) -C .. doc/matrix.texi DASH_X=-x
	PYTHONPATH=$(libdir):$$PYTHONPATH \
	  ./to-html -C $(htmldir) ../doc $(distdir)

$(addprefix $(cgidir)/,$(CGI_FILES)): $(cgidir)
$(addprefix $(htmldir)/,$(HTML_FILES)): $(htmldir)
$(cgidir) $(htmldir):
	mkdir -p $@

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
