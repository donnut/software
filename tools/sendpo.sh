#!/bin/bash

# Script that sends the given file to the TP robot.

USERLANG=""    # Default language code, when absent in filename.

[ -n "$USERLANG" ] || { echo "Edit script first and set USERLANG."; exit 1; }

file="$1"

[ -n "$file" ] || { echo "Usage:  $0 POFILE
POFILE can be <package_name>-<version>.<lang>.po
           or <package_name>-<version>.po\
"; exit 1; }

[ -f "$file" ] || { echo "No such file: $file"; exit 1; }

msgfmt --check $file || { echo "Fix errors first."; exit 1; }

name=${file##*/}
base=${name%\.po}
bare=${base%\.[[:alpha:]_]*}
lang=${base##*\.}

# Fill in the default language code when filename does not contain it.
[ "$bare" == "$base" ] && { lang=$USERLANG; name=$bare.$lang.po; }

# Compare Project-Id-Version with filename.
project=$(sed -n -e '/^\"Project-Id-Version:/{
s/.*: *\([Gg][Nn][Uu] \)*\(.*\)\\n\"/\2/
s/ /-/g
p;q;}' $file)
[ "$name" == "$project.$lang.po" ] || {
    echo "Project-Id-Version '${project/-/ }' does not match filename."
    exit 1;
}

# Send compressed PO file to TP robot.
gzip <$file | uuencode $name.gz |
    mail -s "TP-robot $name" robot@translationproject.org

