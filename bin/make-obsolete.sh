#!/bin/sh
#   Move the files of an obsolete domain out of the way;
#   also delete its statistics and symlinks.
# -*- mode: sh; coding: utf-8 -*-
# Copyright © 2007 Translation Project.
# Benno Schulenberg <benno@vertaalt.nl>, 2007.

if [ -z "$1" -o -n "$2" ]; then
    echo "Supply one argument.";
    exit 2
fi &&

cd /home/tp/site/ &&
if [ ! -d latest/$1 ]; then
    echo "No such domain.";
    exit 2
fi &&

domain=$1 &&
mkdir obsolete/${domain} &&

mv -v POT-files/${domain}* obsolete/${domain}/ &&
mv -v PO-files/*/${domain}-[0-9]* obsolete/${domain}/ &&

calc-postats -dv &&

rm -rv latest/$domain

