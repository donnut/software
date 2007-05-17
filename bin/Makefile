# Main binaries for the Translation Project.
# Copyright © 2000 Progiciels Bourbeau-Pinard inc.
# François Pinard <pinard@iro.umontreal.ca>, 2000.

PYTHONS = fetch-pot msg-to-po po-count po-empty po-expire po-matrix \
          po-normalize po-register po-tidy-links po-to-scm scm-to-po \
          tp-robot
SHELLS = extract-pot-files.sh po-diffs.sh run-queue.sh

all:
	@echo 'import compileall; compileall.compile_dir(".")' | python

tags: TAGS
TAGS: $(PYTHONS)
	etags --lang=none --regex='/\(class\|def\)[ \t]+\([^ \t(]\)+/\1/' \
	  $(PYTHONS)
