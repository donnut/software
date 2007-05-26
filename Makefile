# Conveniently process the PO directory hierarchy.
# Copyright (C) 2004, 2007 Translation Project.
# Copyright (C) 1996, 1997, 1998, 1999, 2000, 2001 Free Software Foundation, Inc.
# François Pinard <pinard@iro.umontreal.ca>, 1996.

VERSION=1.2

PATH:=/home/benno/progs/bin:$(PATH)
DASH_X:=-x


all: data/registry doc/matrix.texi
	po-expire

check: all
	@find maint -type l | while read file; do \
	  echo; \
	  echo "Verifying \``ls -l $$file | sed 's,.*-> ../../,,'`'"; \
	  msgfmt --statistics -c -v -o /dev/null $$file; \
	done

tags: tags-recursive
	etags -i bin/TAGS -i lib/TAGS

tags-recursive:
	$(MAKE) -C bin tags
	$(MAKE) -C lib tags

data/registry: registry/registry.sgml
	VERSION_CONTROL=numbered cp -fb data/registry data/registry
	-bin/registry-data -de >registry.tmp && \
	    diff -u registry.tmp registry/registry.sgml
	rm registry.tmp

.PRECIOUS: data/postats
data/postats: FORCE
	VERSION_CONTROL=numbered cp -fb data/postats data/postats
	bin/postats-data -v -i -u
FORCE:

ifeq ($(SITE), iro.umontreal.ca)
doc/matrix.texi: teams/PO/*
	bin/po-matrix
	mv tmp-matrix.html doc/matrix.html
	@if cmp -s tmp-matrix.texi doc/matrix.texi; then \
	  set ${DASH_X}; \
	  rm tmp-matrix.texi; \
	else \
	  set ${DASH_X}; \
	  mv tmp-matrix.texi doc/matrix.texi; \
	  mail -s "New PO file matrix" sv@li.org < doc/matrix.texi; \
	fi
	@if cmp -s tmp-matrix.xml doc/matrix.xml; then \
	  set ${DASH_X}; rm tmp-matrix.xml; \
	else \
	  set ${DASH_X}; \
	  mv tmp-matrix.xml doc/matrix.xml; \
	  mail -s "New PO file matrix" haible@ilog.fr < doc/matrix.xml; \
	fi
else
doc/matrix.texi:
	:
endif

mailrc-i18n: $(HOME)/.mailrc-i18n
$(HOME)/.mailrc-i18n: data/registry
	bin/i18n-aliases -TDf >$@-tmp
	mv $@-tmp $@

.PHONY:	pot
pot:
	xgettext -o po/tp-robot.pot -kt_ -L Python bin/[a-z]* lib/*.py
	# Add the list of language teams:
	python lib/registry.py >>po/tp-robot.pot

dist:
	tar -czv -f $(HOME)/translationproject-${VERSION}.tgz \
	    --exclude=.svn  ../$(pwd)
