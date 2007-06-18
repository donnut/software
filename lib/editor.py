# Editing and reconstruction of the PO file Registry.
# -*- mode: python; coding: utf-8 -*-
# Copyright © 1999, 2000 Progiciels Bourbeau-Pinard inc.
# François Pinard <pinard@iro.umontreal.ca>, 1999.

import registry
import os, string

def _(text):
    return text

def main():
    output_registry(os.popen('diff -u - ~/po/registry/registry.sgml', 'w'))

# Modification of the registry data file.

# domain DOMAIN
#   info
#   mailto EMAIL
#   #nomailto
#   [no]keep VERSION
#   keeps VERSION [, VERSION]...
#   [no]disclaim
#   [no]autosend
#   [no]url URL
#   urls URL [, URL]...
#   [no]remark TEXT
#   noremarks

def edit_domain(domain, command, args):
    if command == 'info':
        return 1, domain_description(domain['name'])
    if command == 'mailto':
        if len(args) != 1:
            return 0, _("Use exactly one argument with `mailto'")
        # FIXME: Validate args[0] as email.
        domain['mailto'] = args[0]
        return 1, None
    #if command == 'nomailto':
    #    if len(args) != 0:
    #        return 0, "Do not use arguments with `nomailto'"
    #    domain['mailto'] = None
    #    return 1, None
    if command == 'keep':
        if len(args) != 1:
            return 0, _("Use exactly one argument with `keep'")
        # FIXME: Validate args[0] as version.
        if args[0] in domain['keep']:
            return 1, _("Version `%s' is already present") % args[0]
        domain['keep'].append(args[0])
        # FIXME: Sort versions in domain['keep']
        return 1, None
    if command == 'nokeep':
        if len(args) != 1:
            return 0, _("Use exactly one argument with `nokeep'")
        # FIXME: Validate args[0] as version.
        if args[0] not in domain['keep']:
            return 1, _("Version `%s' was not there anyway") % args[0]
        domain['keep'].remove(args[0])
        return 1, None
    if command == 'keeps':
        if len(args) < 1:
            return 0, _("Use at least one argument with `keeps'")
        domain['keep'] = []
        lines = []
        for arg in args:
            # FIXME: Validate arg as version.
            if arg in domain['keep']:
                lines.append(_("Version `%s' duplicated") % arg)
            else:
                domain['keep'].append(arg)
        # FIXME: Sort versions in domain['keep']
        return 1, string.join(lines, '\n')
    if command == 'disclaim':
        if len(args) != 0:
            return 0, _("Do not use arguments with `disclaim'")
        domain['disclaim'] = 1
        return 1, None
    if command == 'nodisclaim':
        if len(args) != 0:
            return 0, _("Do not use arguments with `nodisclaim'")
        domain['disclaim'] = 0
        return 1, None
    if command == 'autosend':
        if len(args) != 0:
            return 0, _("Do not use arguments with `autosend'")
        domain['autosend'] = 1
        return 1, None
    if command == 'noautosend':
        if len(args) != 0:
            return 0, _("Do not use arguments with `noautosend'")
        domain['autosend'] = 0
        return 1, None
    if command == 'url':
        if len(args) != 1:
            return 0, _("Use exactly one argument with `url'")
        # FIXME: Validate args[0] as URL.
        if args[0] in domain['url']:
            return 1, _("URL `%s' is already present") % args[0]
        domain['url'].append(args[0])
        return 1, None
    if command == 'nourl':
        if len(args) != 1:
            return 0, _("Use exactly one argument with `nourl'")
        # FIXME: Validate args[0] as URL.
        if args[0] not in domain['url']:
            return 1, _("URL `%s' was not there anyway") % args[0]
        domain['url'].remove(args[0])
        return 1, None
    if command == 'urls':
        if len(args) < 1:
            return 0, _("Use at least one argument with `urls'")
        domain['url'] = []
        lines = []
        for arg in args:
            # FIXME: Validate arg as URL.
            if arg in domain['url']:
                lines.append["URL `%s' duplicated" % args[0]]
            else:
                domain['url'].append(arg)
        return 1, string.join(lines, '\n')
    if command == 'remark':
        if len(args) != 1:
            return 0, _("Use exactly one argument with `remark'")
        if args[0] in domain['remark']:
            return 1, _("Remark `%s' is already present") % args[0]
        domain['remark'].append(args[0])
        return 1, None
    if command == 'noremark':
        if len(args) != 1:
            return 0, _("Use exactly one argument with `noremark'")
        if args[0] not in domain['remark']:
            return 1, _("Remark `%s' was not there anyway") % args[0]
        domain['remark'].remove(args[0])
        return 1, None
    if command == 'noremarks':
        if len(args) != 0:
            return 0, _("Do not use arguments with `remarks'")
        domain['remark'] = []
        return 1, None

# team TEAM
#   info
#   mailto EMAIL
#   #nomailto
#   charset CHARSET
#   nocharset
#   leader NAME
#   #noleader
#   [no]ref TAG, URL
#   refs TAG, URL [, TAG, URL]...
#   [no]remark TEXT
#   noremarks
#   [no]translator NAME

def edit_team(team, command, args):
    if command == 'info':
        return 1, team_description(team['code'])
    if command == 'mailto':
        if len(args) != 1:
            return 0, _("Use exactly one argument with `mailto'")
        # FIXME: Validate args[0] as email.
        team['mailto'] = args[0]
        return 1, None
    #if command == 'nomailto':
    #    if len(args) != 0:
    #        return 0, "Do not use arguments with `nomailto'"
    #    team['mailto'] = None
    #    return 1, None
    if command == 'charset':
        if len(args) != 1:
            return 0, _("Use exactly one argument with `charset'")
        # FIXME: Validate args[0] as charset.
        team['charset'] = args[0]
        return 1, None
    if command == 'nocharset':
        if len(args) != 0:
            return 0, _("Do not use arguments with `nocharset'")
        team['charset'] = None
        return 1, None
    if command == 'leader':
        if len(args) != 1:
            return 0, _("Use exactly one argument with `leader'")
        # FIXME: Validate args[0] as leader.
        team['leader'] = args[0]
        return 1, None
    #if command == 'noleader':
    #    if len(args) != 0:
    #        return 0, "Do not use arguments with `noleader'"
    #    team['leader'] = None
    #    return 1, None
    if command == 'ref':
        if len(args) != 2:
            return 0, _("Use exactly two arguments with `ref'")
        # FIXME: Validate args[1] as URL.
        pair = args[0], args[1]
        if pair in team['ref']:
            return 1, _("Reference `%s, %s' is already present") % pair
        team['ref'].append(pair)
        return 1, None
    if command == 'noref':
        if len(args) != 2:
            return 0, _("Use exactly two arguments with `noref'")
        # FIXME: Validate args[1] as URL.
        pair = args[0], args[1]
        if pair not in team['ref']:
            return 1, _("Reference `%s, %s' was not there anyway") % pair
        team['ref'].remove(pair)
        return 1, None
    if command == 'refs':
        if len(args) < 2 or len(args) % 2 != 0:
            return 0, _("Use a pair number of arguments with `refs'")
        team['ref'] = []
        lines = []
        counter = 0
        while counter < len(args):
            # FIXME: Validate args[counter+1] as URL.
            pair = args[counter], args[counter+1]
            counter = counter + 2
            if pair in team['ref']:
                lines.append(_("Reference `%s, %s' duplicated") % pair)
            else:
                team['ref'].append(pair)
        # FIXME: Sort versions in team['ref']
        return 1, string.join(lines, '\n')
    if command == 'remark':
        if len(args) != 1:
            return 0, _("Use exactly one argument with `remark'")
        if args[0] in team['remark']:
            return 1, _("Remark `%s' is already present") % args[0]
        team['remark'].append(args[0])
        return 1, None
    if command == 'noremark':
        if len(args) != 1:
            return 0, _("Use exactly one argument with `noremark'")
        if args[0] not in team['remark']:
            return 1, _("Remark `%s' was not there anyway") % args[0]
        team['remark'].remove(args[0])
        return 1, None
    if command == 'noremarks':
        if len(args) != 0:
            return 0, _("Do not use arguments with `remarks'")
        team['remark'] = []
        return 1, None
    if command == 'translator':
        if len(args) != 1:
            return 0, _("Use exactly one argument with `translator'")
        if team['translator'].has_key(args[0]):
            return 1, _("Translator `%s' is already present") % args[0]
        trans = {'name': args[0],
                 'mailto': None,
                 'alias': [],
                 'http': None,
                 'disclaimer': None,
                 'autosend': 0,
                 'do': [],
                 'remark': [],
                 }
        team['translator'][args[0]] = trans
        items = map(registry.latin1_presort, info['translator'].keys())
        items.sort()
        info['translators'] = map(registry.latin1_postsort, items)
        return 1, None
    if command == 'notranslator':
        if len(args) != 1:
            return 0, _("Use exactly one argument with `notranslator'")
        if not team['translator'].has_key(args[0]):
            return 1, _("Translator `%s' is not know anyway")
        translator = team['translator'][args[0]]
        if translator['disclaimer']:
            return 0, _("Should keep `%s' because of disclaimer") % args[0]
        del team['translator'][args[0]]
        team['translators'].remove(args[0])
        return 1, None

# translator TEAM NAME
#   info
#   see NAME
#   mailto EMAIL
#   nomailto
#   [no]alias EMAIL
#   aliases EMAIL [, EMAIL]...
#   http URL
#   nohttp
#   [no]autosend
#   [no]do DOMAIN
#   dos DOMAIN [, DOMAIN]...
#   [no]remark TEXT
#   noremarks

def edit_translator(team, translator, command, args):
    if command == 'info':
        return 1, team_description(team['code'], translator['name'])
    # FIXME: `see' processing to wholly rewrite
#   see NAME
    # FIXME: mailto should also be one of the aliases.
    if command == 'mailto':
        if len(args) != 1:
            return 0, _("Use exactly one argument with `mailto'")
        # FIXME: Validate args[0] as email.
        translator['mailto'] = args[0]
        return 1, None
    #if command == 'nomailto':
    #    if len(args) != 0:
    #        return 0, "Do not use arguments with `nomailto'"
    #    translator['mailto'] = None
    #    return 1, None
    if command == 'alias':
        if len(args) != 1:
            return 0, _("Use exactly one argument with `alias'")
        # FIXME: Validate args[0] as email.
        if args[0] in translator['aliases']:
            return 1, _("Version `%s' is already present") % args[0]
        translator['alias'].append(args[0])
        return 1, None
    if command == 'noalias':
        if len(args) != 0:
            return 0, _("Do not use arguments with `noalias'")
        # FIXME: Validate args[0] as email.
        if args[0] not in translator['alias']:
            return 1, _("Alias `%s' was not there anyway") % args[0]
        translator['alias'].remove(args[0])
        return 1, None
    if command == 'aliases':
        if len(args) < 1:
            return 0, _("Use at least one argument with `aliases'")
        translator['alias'] = []
        lines = []
        for arg in args:
            # FIXME: Validate arg as email.
            if arg in translator['alias']:
                lines.append(_("Alias `%s' duplicated") % arg)
            else:
                translator['alias'].append(arg)
        # FIXME: Sort aliases in translator['alias']
        return 1, string.join(lines, '\n')
    if command == 'http':
        if len(args) != 1:
            return 0, _("Use exactly one argument with `http'")
        # FIXME: Validate args[0] as URL.
        translator['http'] = args[0]
        return 1, None
    if command == 'nohttp':
        if len(args) != 0:
            return 0, _("Do not use arguments with `nohttp'")
        translator['http'] = None
        return 1, None
    if command == 'autosend':
        if len(args) != 0:
            return 0, _("Do not use arguments with `autosend'")
        translator['autosend'] = 1
        return 1, None
    if command == 'noautosend':
        if len(args) != 0:
            return 0, _("Do not use arguments with `noautosend'")
        translator['autosend'] = 0
        return 1, None
    if command == 'do':
        if len(args) != 1:
            return 0, _("Use exactly one argument with `do'")
        if args[0] in translator['do']:
            return 1, _("Remark `%s' is already present") % args[0]
        translator['do'].append(args[0])
        return 1, None
    if command == 'nodo':
        if len(args) != 1:
            return 0, _("Use exactly one argument with `nodo'")
        if args[0] not in translator['do']:
            return 1, _("Remark `%s' was not there anyway") % args[0]
        translator['do'].remove(args[0])
        return 1, None
    if command == 'dos':
        if len(args) < 1:
            return 0, _("Use at least one argument with `dos'")
        translator['do'] = []
        lines = []
        for arg in args:
            # FIXME: Validate arg as translator.
            if arg in translator['do']:
                lines.append(_("Do `%s' duplicated") % arg)
            else:
                translator['do'].append(arg)
        # FIXME: Sort dos in translator['do']
        return 1, string.join(lines, '\n')
    if command == 'remark':
        if len(args) != 1:
            return 0, _("Use exactly one argument with `remark'")
        if args[0] in translator['remark']:
            return 1, _("Remark `%s' is already present") % args[0]
        translator['remark'].append(args[0])
        return 1, None
    if command == 'noremark':
        if len(args) != 1:
            return 0, _("Use exactly one argument with `noremark'")
        if args[0] not in translator['remark']:
            return 1, _("Remark `%s' was not there anyway") % args[0]
        translator['remark'].remove(args[0])
        return 1, None
    if command == 'noremarks':
        if len(args) != 0:
            return 0, _("Do not use arguments with `remarks'")
        translator['remark'] = []
        return 1, None

if __name__ == '__main__':
    reload(registry)
    #import sys
    #for team in registry.team_list():
    #    sys.stdout.write("\n")
    #    sys.stdout.write(team_description(team))
    main()
