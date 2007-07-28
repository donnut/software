# Python library files for the Translation Project.
# Copyright © 1999, 2000 Progiciels Bourbeau-Pinard inc.
# François Pinard <pinard@iro.umontreal.ca>, 1999.

IMPORTS = htmlpage.py data.py po.py registry.py
PYTHONS = $(IMPORTS) editor.py run.py unpack.py

all: $(IMPORTS)
	@echo 'import compileall; compileall.compile_dir(".")' | python

tags: TAGS
TAGS: $(PYTHONS)
	etags --lang=none --regex='/\(class\|def\)[ \t]+\([^ \t(]\)+/\1/' \
	  $(PYTHONS)
