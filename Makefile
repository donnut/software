# Conveniently process the PO directory hierarchy.
# Copyright © 2004, 2007 Translation Project.
# Copyright © 1996, 1997, 1998, 1999, 2000, 2001 Free Software Foundation, Inc.
# François Pinard <pinard@iro.umontreal.ca>, 1996.

VERSION=1.93

# define default locations for some directories if you want to change
# these, the best way to avoid conflicts with version control is to
# create a file called Makefile.local and set the variables in there
sitedir  = /home/tp/site
htmldir  = $(sitedir)/html
extradir = $(sitedir)/extra
cachedir = $(sitedir)/cache

# load user defined values, if any
-include Makefile.local

# export variables for recursive calls of make
export sitedir
export htmldir
export extradir
export cachedir

all: registry site

check: all
	@find $(sitedir)/latest -type l | while read file; do \
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

registry: $(cachedir)/registry
$(cachedir)/registry: registry/registry.sgml
	mkdir -p $(cachedir)
	$(MAKE) -C registry all

indexes:
	$(MAKE) -C registry indexes

mailrc:
	$(MAKE) -C registry mailrc

procmailrc:
	$(MAKE) -C registry procmailrc

normal normalize:
	$(MAKE) -C registry normalize

remote:
	$(MAKE) -C registry remote

site:
	$(MAKE) -C webgen all

domains:
	$(MAKE) -C webgen domains

teams:
	$(MAKE) -C webgen teams

.PRECIOUS: postats
postats: $(cachedir)/postats
$(cachedir)/postats: FORCE
	-VERSION_CONTROL=numbered cp -fb $(cachedir)/postats $(cachedir)/postats
	bin/calc-postats -u -v
FORCE:

matrix: $(extradir)/matrix.texi
$(extradir)/matrix.texi: $(sitedir)/PO-files/*
	bin/po-matrix
	mv tmp-matrix.html $(extradir)/matrix.html
	mv tmp-matrix.texi $(extradir)/matrix.texi
	mv tmp-matrix.xml $(extradir)/matrix.xml

install-test-system:
	if [ -s registry/registry.sgml ] ; then \
	  echo "registry/registry.sgml already exists. not doing anything"; \
	else \
	  echo "generating a dummy install for testing purposes only"; \
	  cp registry/registry.sgml_example registry/registry.sgml;\
	  cp registry/AUTHORS_example registry/AUTHORS;\
	  mkdir -p $(sitedir)/cache;\
	  mkdir -p $(sitedir)/tmp;\
	  mkdir -p $(sitedir)/POT-files;\
	  mkdir -p $(sitedir)/PO-files;\
	  mkdir -p $(sitedir)/PO-files/{de,fi,fr,ga,hu,nl,pa,ru,vi,wa,zh_CN,zh_TW};\
	  mkdir -p $(sitedir)/domain;\
	  mkdir -p $(sitedir)/team;\
	  for j in lib/messages/*po; do\
	    i=`basename $$j`;\
	    cp $$j $(sitedir)/PO-files/$${i%.po}/tp-robot-1.0.$$i;\
	  done;\
	  echo "...generated files";\
	  bin/calc-postats -i;\
	  bin/registry-data -e;\
	  bin/generate-static-pages -i;\
	  bin/generate-static-pages -d;\
	  bin/generate-static-pages -t;\
	  echo "...generated webpages";\
	fi

.PHONY:	pot
pot:
	# Extract translatable strings from relevant files:
	xgettext -o po/tp-robot.pot -kt_ -L Python \
	    bin/{tp-robot,po-register} lib/{po,run,unpack}.py
	# Add the list of language teams:
	python lib/registry.py >>po/tp-robot.pot

dist:
	mkdir -p $(sitedir)/bundle
	tar -cz -f  $(sitedir)/bundles/tp-robot-${VERSION}.tgz \
	    --transform='s:^\./:tp-robot-${VERSION}/:' \
	    --exclude=.git  .
