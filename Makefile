# Conveniently process the PO directory hierarchy.
# Copyright © 2004, 2007 Translation Project.
# Copyright © 1996, 1997, 1998, 1999, 2000, 2001 Free Software Foundation, Inc.
# François Pinard <pinard@iro.umontreal.ca>, 1996.

VERSION=1.93

extra_dir=../site/extra


all: registry site

check: all
	@find ../site/latest -type l | while read file; do \
	  echo; \
	  echo "Verifying \``ls -l $$file | sed 's,.*-> ../../,,'`'"; \
	  msgfmt --statistics -c -v -o /dev/null $$file; \
	done

expire:
	bin/po-expire

tags: tags-recursive
	etags -i bin/TAGS -i lib/TAGS

tags-recursive:
	$(MAKE) -C bin tags
	$(MAKE) -C lib tags

registry: ../cache/registry
../cache/registry: registry/registry.sgml
	$(MAKE) -C registry all

indexes:
	$(MAKE) -C registry indexes

mailrc:
	$(MAKE) -C registry mailrc

procmailrc:
	$(MAKE) -C registry procmailrc

site:
	$(MAKE) -C webgen all

.PRECIOUS: postats
postats: ../cache/postats
../cache/postats: FORCE
	VERSION_CONTROL=numbered cp -fb ../cache/postats ../cache/postats
	bin/calc-postats -u -v
FORCE:

matrix: $(extra_dir)/matrix.texi
$(extra_dir)/matrix.texi: ../site/PO-files/*
	bin/po-matrix
	mv tmp-matrix.html $(extra_dir)/matrix.html
	mv tmp-matrix.texi $(extra_dir)/matrix.texi
	mv tmp-matrix.xml $(extra_dir)/matrix.xml

.PHONY:	pot
pot:
	# Extract translatable strings from relevant files:
	xgettext -o po/tp-robot.pot -kt_ -L Python \
	    bin/{tp-robot,po-register} lib/{po,run,unpack}.py
	# Add the list of language teams:
	python lib/registry.py >>po/tp-robot.pot

dist:
	tar -cz -f ../site/bundles/tp-robot-${VERSION}.tgz \
	    --transform='s:^\./:tp-robot-${VERSION}/:' \
	    --exclude=.svn  .
