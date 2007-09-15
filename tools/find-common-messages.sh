#!/bin/bash
# Copyright © 2007 Translation Project.
# Benno Schulenberg <benno@vertaalt.nl>, 2007.

# Gather the messages that occur several times in the most recent POT files.

grep "<domain>" ~/progs/registry/registry.sgml  |
    sed -e 's/  <domain>//' -e '/Compendium/d'  |
    while read domain;
        do echo $(ls -1tr ~/site/POT-files/${domain}-[0-9]* | tail -1);
    done  >list-of-pots  &&

msgcomm  --no-location --no-wrap --more-than=4  -f list-of-pots  |
    msgfilter  --keep-header  sed -e d  |
    sed -e '/^#/d'  &&

rm list-of-pots

