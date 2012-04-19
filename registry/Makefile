# Make a digest from or validate the SGML in registry.sgml.
# Copyright © 2007 Translation Project.
# Copyright © 1996, 1997, 1998, 1999, 2000, 2002, 2003 Free Software Foundation, Inc.
# François Pinard <pinard@iro.umontreal.ca>, 1996.

DECODED = decoded-cached-registry


all: registry indexes procmailrc

remote:
	ssh tp@translationproject.org "(cd progs/registry; make fromremote)"

fromremote:
	umask 0002;
	git pull;
	$(MAKE) all
	-chmod 664 registry.sgml

registry: ../../cache/registry
../../cache/registry: registry.sgml
	VERSION_CONTROL=numbered
	    cp -fb ../../cache/registry ../../cache/registry
	-../bin/registry-data -de >registry.tmp && \
	    diff -u registry.tmp registry.sgml
	rm registry.tmp

indexes: ../../cache/registry
	../bin/generate-static-pages -i

mailrc: $(HOME)/.mailrc-tp
$(HOME)/.mailrc-tp: ../../cache/registry ../bin/create-mail-aliases
	../bin/create-mail-aliases -mTDf >$@-tmp
	mv $@-tmp $@

procmailrc: maintainers leaders teams
maintainers: $(HOME)/.procmailrc-maintainers
leaders: $(HOME)/.procmailrc-leaders
teams: $(HOME)/.procmailrc-teams

$(HOME)/.procmailrc-maintainers: ../../cache/registry ../bin/create-mail-aliases
	../bin/create-mail-aliases -pDf >$@-tmp
	mv $@-tmp $@

$(HOME)/.procmailrc-leaders: ../../cache/registry ../bin/create-mail-aliases
	../bin/create-mail-aliases -pTf >$@-tmp
	mv $@-tmp $@

$(HOME)/.procmailrc-teams: ../../cache/registry ../bin/create-mail-aliases
	../bin/create-mail-aliases -ptf >$@-tmp
	mv $@-tmp $@

normalize: validate
	# Use this to standardize whitespace in registry.sgml
	# after adding or deleting <do> tags.
	../bin/registry-data -e
	../bin/registry-data -d >$(DECODED)
	mv $(DECODED) registry.sgml

validate val:
	SP_CHARSET_FIXED=YES SP_ENCODING=utf-8 nsgmls -s registry.sgml

