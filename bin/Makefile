# Main binaries for the Translation Project.
# Copyright © 2000 Progiciels Bourbeau-Pinard inc.
# François Pinard <pinard@iro.umontreal.ca>, 2000.

PERLS = po-expire po-tidy-links
PYTHONS = fetch-pot msg-to-po po-count po-empty po-matrix po-normalize \
po-register po-to-scm scm-to-po tp-robot
SHELLS = po-diffs run-queue

all:
	@echo 'import compileall; compileall.compile_dir(".")' | python

tags: TAGS
TAGS: $(PYTHONS)
	etags --lang=none --regex='/\(class\|def\)[ \t]+\([^ \t(]\)+/\1/' \
	  $(PYTHONS)
