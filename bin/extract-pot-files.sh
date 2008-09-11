#!/bin/bash
echo=${2-true}

archive=$1
# [ -d $domain ] || { echo "wrong dir: $domain"; exit 1; }
suffix=${archive##*\.}
$echo $suffix
domain=${archive%%-[0-9]*}
$echo $domain

case $suffix in
    gz) tar xzf $archive ;;
    bz2) [ -d ${archive%.tar.$suffix} ] || tar xjf $archive ;;
esac

case ${domain} in
    aspell)
	$echo $domain
	oversion=${archive%.tar.$suffix}
	version=${oversion#$domain-}
	version=${version/-/-b}
	$echo $version
	cp -v $oversion/po/$domain.pot $domain-$version.pot
	;;
    binutils)
	$echo $domain
	oversion=${archive%.tar.$suffix}
	version=${oversion#$domain-}
	version=${version/-/-b}
	$echo $version
	cp -v $oversion/binutils/po/binutils.pot binutils-$version.pot
	cp -v $oversion/bfd/po/bfd.pot bfd-$version.pot
	cp -v $oversion/gas/po/gas.pot gas-$version.pot
	cp -v $oversion/opcodes/po/opcodes.pot opcodes-$version.pot
	cp -v $oversion/ld/po/ld.pot ld-$version.pot
	cp -v $oversion/gprof/po/gprof.pot gprof-$version.pot
	cp -v $oversion/gold/po/gold.pot gold-$version.pot
	;;
    bison)
	$echo $domain
	version=${archive%.tar.$suffix}
	version=${version#${domain}-}
	$echo $version
	cp -v $domain-$version/po/$domain.pot $domain-$version.pot
	cp -v $domain-$version/runtime-po/bison*.pot bison-runtime-$version.pot
	;;
    clisp)
	$echo $domain
	version=${archive%.tar.$suffix}
	version=${version#${domain}-}
	$echo $version
	cp -v $domain-$version/src/po/$domain.pot $domain-$version.pot
	;;
    gcc)
	$echo $domain
	version=${archive%.tar.$suffix}
	version=${version#${domain}-}
	$echo $version
	date=${version#*-}
	if [ $version = $date ]; then
	    tgcc=$domain-$version.pot
	    tcpp=cpplib-$version.pot
	else
	    ver=${version%-$date}
	    tgcc=$domain-$ver-b$date.pot
	    tcpp=cpplib-$ver-b$date.pot
	fi
	cp -v $domain-$version/gcc/po/$domain.pot $tgcc
	cp -v $domain-$version/libcpp/po/cpplib.pot $tcpp
	;;
    gettext)
	domain=gettext
	version=${archive%.tar.$suffix}
	version=${version#gettext-}
	$echo $version
	cp ${domain}-$version/gettext-tools/po/gettext-tools.pot \
		gettext-tools-$version.pot -v
	cp ${domain}-$version/gettext-tools/examples/po/gettext-examples.pot \
		gettext-examples-$version.pot -v
	cp ${domain}-$version/gettext-runtime/po/gettext-runtime.pot \
		gettext-runtime-$version.pot -v
	;;
    gsasl)
	domain=gsasl
	version=${archive%.tar.$suffix}
	version=${version#$domain-}
	$echo $version
	cp -v ${domain}-$version/po/$domain.pot $domain-$version.pot
	cp -v ${domain}-$version/lib/po/lib$domain.pot lib$domain-$version.pot
	;;
    hylafax)
	$echo domain
	version=${archive%.tar.$suffix}
	version=${version#$domain-}
	$echo $version
	cp -v ${domain}-$version/po/$domain.pot $domain-$version.pot
	;;
    iso-codes)
	$echo $domain
	version=${archive%.tar.$suffix}
	version=${version#$domain-}
	$echo $version
	pushd $domain-$version
	for d in iso_*; do
	    cp -v $d/$d.pot ../$d-$version.pot
	    if [ $d = iso_3166 ]; then
		pushd $d
		for dd in $d_*; do
		    [ -d $dd ] || continue
		    cp -v $dd/$dd.pot ../../$dd-$version.pot
		done
		popd
	    fi
	done
	popd
	;;
    keytouch)
	$echo domain
	version=${archive%.tar.$suffix}
	version=${version#$domain-}
	$echo $version
	cp -v keytouch-$version/keytouch-config/po/keytouch.pot \
		keytouch-$version.pot
	cp -v keytouch-$version/keytouch-keyboard/po/keytouch-keyboard-bin.pot \
		keytouch-keyboard-bin-$version.pot
	;;
    libgphoto2)
	$echo $domain
	version=${archive%.tar.$suffix}
	version=${version#$domain-}
	$echo $version
	cp -v ${domain}-$version/po/${domain}-2.pot \
		$domain-$version.pot
	cp -v ${domain}-$version/libgphoto2_port/po/${domain}_port-0.pot \
		${domain}_port-$version.pot
	;;
    lilypond)
	$echo $domain
	version=${archive%.tar.$suffix}
	version=${version#$domain-}
	$echo $version
	cp -v ${domain}-$version/po/${domain}.pot $domain-$version.pot
	;;
    man-db)
	$echo $domain
	version=${archive%.tar.$suffix}
	version=${version#$domain-}
	$echo $version
	cp -v ${domain}-$version/po/${domain}.pot $domain-$version.pot
	cp -v ${domain}-$version/man/po4a/po/man-db-manpages.pot \
		man-db-manpages-$version.pot
	;;
    solfege)
	$echo $domain
	version=${archive%.tar.$suffix}
	version=${version#$domain-}
	$echo $version
	cp -v ${domain}-$version/po/${domain}.pot \
		$domain-$version.pot
	cp -v ${domain}-$version/help/C/${domain}.pot \
		$domain-manual-$version.pot
	;;
esac

exit 0

