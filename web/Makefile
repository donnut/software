# Generating a Web site for the Translation Project.
# Copyright © 1999, 2000 Progiciels Bourbeau-Pinard inc.
# François Pinard <pinard@iro.umontreal.ca>, 1999.

#distdir = ../gettext/dist
htmldir = ../HTML
#HTML_FILES = domains.html gettext.html teams.html m17n99.html
HTML_FILES = domains.html teams.html
LAYOUT_DEPS = ../web/lib/config.py layout.html to-html
REGISTRY_DEPS = html-to-cgi ../data/postats ../data/registry

ifeq ($(SITE), iro.umontreal.ca)
cgidir = /home/www/usagers/gnutra/HTML
topdir = /home/www/usagers/gnutra/HTML
else
ifeq ($(SITE), sf.net)
cgidir = /home/groups/t/tr/translation/htdocs
topdir = /home/groups/t/tr/translation/htdocs
else
cgidir = /home/benno/www
htmldir = /home/benno/www/HTML
topdir = /home/benno/TP
endif
endif
libdir = $(topdir)/web/lib

CGI_FILES = babyl.cgi distro.cgi registry.cgi
DASH_X=-x

$(cgidir)/%.cgi: %.cgi.in
	sed 's,@topdir@,$(topdir),g;s,@libdir@,$(libdir),g' $< > $@-tmp
	chmod a+rx $@-tmp
	mv -f $@-tmp $@

all-iro: $(addprefix $(cgidir)/, $(CGI_FILES)) all-sf

all-sf: $(addprefix $(htmldir)/, $(HTML_FILES))
	$(MAKE) -C .. doc/matrix.texi DASH_X=${DASH_X}
	PYTHONPATH=$(libdir):$$PYTHONPATH \
	  ./to-html -C $(htmldir) ../doc $(distdir)

$(addprefix $(cgidir)/, $(CGI_FILES)): $(cgidir)
$(addprefix $(htmldir)/, $(HTML_FILES)): $(htmldir)
$(cgidir) $(htmldir):
	mkdir -p $@

$(htmldir)/po.html: $(LAYOUT_DEPS) $(distdir)/doc/po.texi
	 LANG=C LANGUAGE=C makeinfo --html \
	   --output=po.html -I$(distdir)/doc po.texi
	 PYTHONPATH=$(libdir):$$PYTHONPATH \
	   ./to-html -C $(htmldir) po.html
	 rm po.html

$(htmldir)/domains.html: $(REGISTRY_DEPS)
	PYTHONPATH=$(libdir):$$PYTHONPATH \
	  ./html-to-cgi -C $(htmldir) -D

$(htmldir)/gettext.html: $(LAYOUT_DEPS) $(distdir)/doc/gettext.texi
	 -LANG=C LANGUAGE=C makeinfo --html \
	   --force --output=gettext.html -I/u/loewisma/gettext-0.11.2/doc  gettext.texi
	 PYTHONPATH=$(libdir):$$PYTHONPATH \
	   ./to-html -C $(htmldir) gettext.html
	 rm gettext.html

$(htmldir)/teams.html: $(REGISTRY_DEPS)
	PYTHONPATH=$(libdir):$$PYTHONPATH \
	  ./html-to-cgi -C $(htmldir) -T

$(htmldir)/m17n99.html: $(LAYOUT_DEPS) m17n99-to-html m17n99.html \
 ../m17n99/mgp/slide-show
	PYTHONPATH=$(libdir):$$PYTHONPATH \
	  ./m17n99-to-html -C $(htmldir)

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
