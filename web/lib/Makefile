# Python library files for the Translation Project.
# Copyright © 1999, 2000 Progiciels Bourbeau-Pinard inc.
# François Pinard <pinard@iro.umontreal.ca>, 1999.

IMPORTS = babylweb.py distroweb.py htmlpage.py rfc2047.py
PYTHONS = $(IMPORTS) data.py editor.py po.py registry.py run.py unpack.py

all: $(IMPORTS)
	@echo 'import compileall; compileall.compile_dir(".")' | python

%.py: $(HOME)/share/python/%.py
	install -m 444 $< $@

tags: TAGS
TAGS: $(PYTHONS)
	etags --lang=none --regex='/\(class\|def\)[ \t]+\([^ \t(]\)+/\1/' \
	  $(PYTHONS)
