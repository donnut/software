# Validate the SGML in the registry.
# Copyright (C) 1996, 1997, 1998, 1999, 2000, 2002, 2003 Free Software Foundation, Inc.
# François Pinard <pinard@iro.umontreal.ca>, 1996.

PATH:=/u/gnutra/bin:$(PATH)

all:
	$(MAKE) -C .. data/registry
	$(MAKE) $(HOME)/.mailrc-i18n

$(HOME)/.mailrc-i18n: ../data/registry
	../bin/i18n-aliases -TDf > $@-tmp
	mv $@-tmp $@

fromremote:
	umask 002;\
	cvs update;\
	$(MAKE) all
	-chmod 664 registry.sgml

remote:
	ssh frontal "(cd /u/gnutra/po/registry;make fromremote)"

validate v:
	SP_CHARSET_FIXED=YES SP_ENCODING=utf-8 nsgmls -s registry.sgml
