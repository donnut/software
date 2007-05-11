# Generating a Web site for the Translation Project.
# Copyright © 1999, 2000 Progiciels Bourbeau-Pinard inc.
# François Pinard <pinard@iro.umontreal.ca>, 1999.

package = po
htmldir = ../HTML
ALL_FILES = fr-traduc.all leaders.all maintainers.all software.all status.all translators.all
HTML_FILES = $(ALL_FILES:.all=.html)
LAYOUT_DEPS = ../web/lib/config.py layout.html to-html
REGISTRY_DEPS = html-to-cgi ../data/postats ../data/registry

ifeq ($(SITE), iro.umontreal.ca)
cgidir = /home/www2/usagers/gnutra/HTML/po
topdir = /home/www2/usagers/gnutra/HTML/po
else
ifeq ($(SITE), sf.net)
cgidir = /home/groups/t/tr/translation/htdocs
topdir = /home/groups/t/tr/translation/htdocs
else
cgidir = $(HOME)/CGI/$(package)
topdir = $(HOME)/$(package)
endif
endif
libdir = $(topdir)/web/lib

$(addprefix $(htmldir)/, $(HTML_FILES)): $(htmldir)
$(cgidir) $(htmldir):
	mkdir $@

all: $(HTML_FILES)

%.html: %.all
	 PYTHONPATH=$(libdir):$$PYTHONPATH \
	   ../web/to-html -C $(htmldir) $<

