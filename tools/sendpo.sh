#!/bin/bash
# sendpo.sh

po_in="$1"
[ -n "$po_in" ] || { echo "\
usage: $0 POFILE
POFILE must be in the \"<project_name>-<version>.<lang>.po\" format\
"; exit 1; }
[ -f "$po_in" ] || { echo "$0: $po_in not found"; exit 1; }
msgfmt --check $po_in || { echo "Fix errors first"; exit 1; }

po=${po_in##*/}
lang=${po%\.po}
lang=${lang##*\.}

# compare Project-Id-Version with file name
project=$(sed -n -e '/^\"Project-Id-Version:/{
s/.*: *\([Gg][Nn][Uu] \)*\(.*\)\\n\"/\2/
s/ /-/g
p;q;}' $po_in)
[ "$po" == "$project.$lang.po" ] || {
  echo "File name ./. version number does not match:"
  echo "  Project ID (Project-Id-Version): ${project/-/ }"
  echo "  File name of PO file           : $po"
  echo "Adjust Project-Id-Version of file \"$po_in\""
  exit 1;
}

gzip < $po_in | uuencode $po.gz \
  | mail -s "TP-Robot $po" translation@iro.umontreal.ca

# eof sendpo.sh
