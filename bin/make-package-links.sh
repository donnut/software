#!/bin/sh
# Create for each package a series of symlinks to its corresponding files in
# the PO-files/ subdirectory.  With the goal of making domain walking easy.

export LC_ALL=POSIX

cd /home/tp/site/latest/ &&
rm -r ../packages &&  # Clean out existing links.
mkdir ../packages &&  # Recreate the subdirectory.

for pack in *; do
    mkdir ../packages/${pack} &&
    cd ../PO-files/ &&
    echo "Making links for ${pack}..." &&
    for lang in *; do
        if ! $(ls -1 ${lang} | grep -q "${pack}"); then
            ##echo "No ${lang} translations for ${pack}"
	    continue
        fi
        for file in ${lang}/${pack}*; do
	    ##echo "ln -s ../../PO-files/$file ../packages/${pack}/"
	    ln -nsf ../../PO-files/$file ../packages/${pack}/
	done
    done
done

cd ..
