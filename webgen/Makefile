# Generating the documenting web pages for the Translation Project.
# Copyright © 2007 Translation Project.
# Copyright © 1999, 2000 Progiciels Bourbeau-Pinard inc.
# François Pinard <pinard@iro.umontreal.ca>, 1999.

homedir = /home/tp
sitedir = $(homedir)/site
htmldir = $(sitedir)/html

ALLOUT_FILES = maintainers.all leaders.all translators.all \
               changes.all files.all robot.all software.all
HTMA_FILES = $(ALLOUT_FILES:.all=.html)
HTMH_FILES = welcome.html thanks.html whydisclaim.html

LAYOUT_DEPS = ../lib/config.py ../lib/htmlpage.py layout.html.in to-html.py


all: alloutfiles htmlfiles $(sitedir)/disclaim.txt

$(htmldir):
	mkdir -p $@


alloutfiles: $(htmldir) $(addprefix $(htmldir)/,$(HTMA_FILES))

htmlfiles: $(htmldir) $(addprefix $(htmldir)/,$(HTMH_FILES)) 

$(htmldir)/%.html: %.all $(LAYOUT_DEPS)
	./to-html.py -C $(htmldir) $<

$(htmldir)/%.html: %.html $(LAYOUT_DEPS)
	./to-html.py -C $(htmldir) $<

$(sitedir)/disclaim.txt: disclaim.txt
	cp disclaim.txt $(sitedir)/disclaim.txt

domains:
	../bin/generate-static-pages -d

teams:
	../bin/generate-static-pages -t


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
