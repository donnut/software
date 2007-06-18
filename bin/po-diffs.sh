#!/bin/sh
# Unidiffs of a PO file and its canonical form.
# Copyright © 1998 Progiciels Bourbeau-Pinard inc.
# François Pinard <pinard@iro.umontreal.ca>, 1998.

for file in $*; do
  base=`echo $file | sed 's,.*/,,'`
  po-normalize $file | diff -u -L $base~ -L $base $file -
done

exit 0
