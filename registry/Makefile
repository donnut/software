# Make a digest from or validate the SGML in registry.sgml.
# Copyright © 2007 Translation Project.
# Copyright © 1996, 1997, 1998, 1999, 2000, 2002, 2003 Free Software Foundation, Inc.
# François Pinard <pinard@iro.umontreal.ca>, 1996.

all: registry procmailrc

registry: ../../cache/registry
../../cache/registry: registry.sgml
	VERSION_CONTROL=numbered
	    cp -fb ../../cache/registry ../../cache/registry
	-../bin/registry-data -de >registry.tmp && \
	    diff -u registry.tmp registry.sgml
	rm registry.tmp

mailrc: $(HOME)/.mailrc-tp
$(HOME)/.mailrc-tp: ../../cache/registry
	../bin/i18n-aliases -mTDf >$@-tmp
	mv $@-tmp $@

procmailrc: leaders maintainers
leaders: $(HOME)/.procmailrc-leaders
maintainers: $(HOME)/.procmailrc-maintainers

$(HOME)/.procmailrc-leaders: ../../cache/registry
	../bin/i18n-aliases -pTf >$@-tmp
	mv $@-tmp $@

$(HOME)/.procmailrc-maintainers: ../../cache/registry
	../bin/i18n-aliases -pDf >$@-tmp
	mv $@-tmp $@

validate val:
	SP_CHARSET_FIXED=YES SP_ENCODING=utf-8 nsgmls -s registry.sgml
