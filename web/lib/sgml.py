# Encode textual description into a more efficient database.
# -*- coding: iso-8859-1 -*-
# Copyright © 2001, 2002, 2003, 2004 Free Translation Project.
# Copyright © 1998, 1999, 2000 Progiciels Bourbeau-Pinard inc.
# François Pinard <pinard@iro.umontreal.ca>, 1998.

import os,sys,string
import config,data

dir = "/u/loewisma/bin"
if os.path.isfile("%s/nsgmls" % dir):
    os.environ['PATH'] = '%s:%s' % (dir, os.environ['PATH'])

def _(text):
    return text

def quote(text):
    if '&' in text:
        text = text.replace('&', '&amp;')
    return text

def encode_database():
    sgml = read_sgml_file(config.top_directory + '/registry/registry.sgml')
    # Convert all domains and build a dictionary.
    domains = {}
    for domain in sgml[1][1:]:
        name = domain[1]
        info = {'name':  name,
                'potcopyright': None,
                'ref': [],
                'mailto': [],
                'nomailto': [],
                'keep': [],
                'disclaim': 0,
                'autosend': 0,
                'note': [],
                'url': [],
                'ext': [],
                'remark': [],
                }
        for item in domain[2:]:
            tag = item[0]
            if tag == 'ref':
                info[tag].append((item[1], item[2][1]))
            elif tag in ('keep', 'mailto', 'nomailto', 'remark', 'url', 'ext', 'note'):
                info[tag].append(item[1])
            elif tag == 'autosend':
                if len(item) == 3:
                    info[tag] = item[1]['option']
                else:
                    info[tag] = 1
            elif tag == 'potcopyright':
                info[tag] = item[1]
            else:
                info[tag] = 1
        domains[name] = info
    # Prepare a list of domains.
    domain_list = domains.keys()
    domain_list.sort()
    # Convert all teams and build a dictionary.
    teams = {}
    for team in sgml[2][1:]:
        code = team[2][1]
        info = {'language': team[1],
                'code': code,
                'mailto': [],
                'announceto': None,
                'charset': None,
                'leader': None,
                'ref': [],
                'remark': [],
                'translator': {},
                'translators': None, # sorted keys of translator
                'suppresspot': 0,
                }
        for item in team[3:]:
            tag = item[0]
            if tag == 'ref':
                info[tag].append((item[1], item[2][1]))
            elif tag in ('mailto', 'remark'):
                info[tag].append(item[1])
            elif tag == 'translator':
                # Convert one translator in that team.
                trans = {'name': [item[1]],
                         'mailto': [],
                         'url': [],
                         'disclaimer': None,
                         'autosend': 0,
                         'do': [],
                         'remark': [],
                         }
                info['translator'][item[1]] = trans
                for item in item[2:]:
                    tag = item[0]
                    if tag == 'alias':
                        trans['name'].append(item[1])
                        info['translator'][item[1]] = trans
                    elif tag in ('do', 'remark', 'url'):
                        if tag == 'do':
                            e = domains[item[1]]['ext']
                            if info['code'] in e:
                                raise "External assignment",(item[1],info['code'])
                        trans[tag].append(item[1])
                    elif tag == 'disclaimer':
                        if len(item) > 1:
                            trans[tag] = item[1] or '*'
                        else:
                            trans[tag] = '*'
                    elif tag == 'mailto':
                        if len(item) == 3:
                            trans[tag].append(item[2])
                            trans['showmail'] = item[1]['show']
                        else:
                            trans[tag].append(item[1])
                    elif tag == 'autosend':
                        if len(item) == 3:
                            trans[tag] = item[1]['option']
                        else:
                            trans[tag] = 1
                    else:
                        trans[tag] = 1
            elif tag == "suppresspot":
                info[tag] = 1
            else:
                info[tag] = item[1]
        # Prepare a list of translators in that team (aliases included).
        items = info['translator'].keys()
        items.sort()
        info['translators'] = items
        teams[code] = info
    # Prepare a list of teams.
    items = map(team_presort, teams.values())
    items.sort()
    team_list = map(team_postsort, items)
    data.save_registry((domains, domain_list, teams, team_list))

def team_presort(team):
    return team['language'], team['code']
def team_postsort((language, code)):
    return code

def read_sgml_file(name):
    stack = []
    current = []
    attrs = {}
    # Avoid docbk30, which raises some unanalysed interference.
    # Also request UTF-8 processing
    for line in os.popen('SGML_CATALOG_FILES= SP_ENCODING=UTF-8 SP_CHARSET_FIXED=YES nsgmls %s' % name).readlines():
        if line[0] == '(':
            stack.append(current)
            current = [string.lower(line[1:-1])]
            if attrs:
                current.append(attrs)
                attrs = {}
            continue
        if line[0] == ')':
            element = tuple(current)
            current = stack[-1]
            del stack[-1]
            current.append(element)
            continue
        if line[0] == '-':
            line = line[1:-1]
            line = string.replace(line, '\\n', '\n')
            line = string.replace(line, '\\011', '\t')
            line = string.rstrip(line)
            current.append(line)
            continue
        if line[0] == 'A':
            attr = line[1:].split()
            if attr[1] == "IMPLIED":
                continue
            if attr[1] == "TOKEN":
                attrs[attr[0].lower()] = attr[2].lower()
                continue
            raise ValueError,_("Unsupported attribute %s") % `attr`
            continue
        if line[0] == 'C':
            return current[0]
    raise ValueError,_("SGML in `%s' is not conformant.\n") % name


### Decode the database to produce clear text.

def decode_database():
    import registry
    write = sys.stdout.write
    write("""\
<!-- Registry data for use in the Translation Project. -*- coding: utf-8 -*-
     Copyright Â© 2001, 2002 Translation Project.
     Copyright Â© 1996, 1997, 1998, 1999, 2000 Progiciels Bourbeau-Pinard inc.
     FranÃ§ois Pinard `pinard@iro.umontreal.ca', 1996.
-->

<!DOCTYPE registry SYSTEM "registry.dtd">
<registry>

 <domains>
""")
    for domain in registry.domain_list():
        write('\n')
        write(domain_description(domain))
    write("""\

 </domains>

 <teams>
""")
    for team in registry.team_list():
        write('\n')
        write(team_description(team))
    write("""\

 </teams>
</registry>

<!--
Local variables:
xxml-highlight-tag-alist: (("domains" . secondary-selection)
			   ("teams" . secondary-selection))
xxml-highlight-initial-alist: (("alias" . font-lock-type-face)
			       ("charset" . xxml-header-4-face)
			       ("code" . xxml-header-1-face)
			       ("disclaimer" . font-lock-comment-face)
			       ("do" . italic)
			       ("domain" . xxml-header-3-face)
			       ("http" . font-lock-string-face)
			       ("leader" . xxml-header-4-face)
			       ("mailto" . font-lock-string-face)
			       ("nomailto" . font-lock-string-face)
			       ("ref" . font-lock-builtin-face)
			       ("remark" . font-lock-comment-face)
			       ("see" . font-lock-type-face)
			       ("team" . xxml-header-1-face)
			       ("translator" . font-lock-type-face))
sgml-validate-command: "SP_CHARSET_FIXED=YES SP_ENCODING=utf-8 nsgmls -s %s %s"
sgml-omittag:t
sgml-shorttag:nil
sgml-omit-transparent:t
sgml-namecase-general:t
sgml-general-insert-case:lower
sgml-minimize-attributes:nil
sgml-always-quote-attributes:nil
sgml-indent-step:1
sgml-indent-data:nil
sgml-parent-document:nil
sgml-exposed-tags:nil
sgml-local-catalogs:nil
sgml-local-ecat-files:nil
End:
-->
""")

def domain_description(domain):
    import registry
    lines = []
    write = lines.append
    write('  <domain>%s\n' % domain.name)
    if domain.potcopyright:
        write('   <potcopyright>%s\n' % domain.potcopyright)
    for ref in domain.ref:
        write('   <ref>%s<url>%s\n' % (ref[0],quote(ref[1])))
    for mailto in domain.mailto:
        write('   <mailto>%s\n' % mailto)
    if domain.nomailto:
        for nomailto in domain.nomailto:
            write('   <nomailto>%s\n' % nomailto)
    if domain.keep:
        write('   <keep>%s\n' % string.join(domain.keep, '<keep>'))
    if domain.disclaim:
        disclaim = '<disclaim>'
    else:
        disclaim = ''
    if domain.autosend:
        if domain.autosend == 'compress':
            autosend = "<autosend compress>"
        else:
            autosend = '<autosend>'
    else:
        autosend = ''
    if disclaim or autosend:
        write('   %s%s\n' % (disclaim, autosend))
    for url in domain.url:
        write('   <url>%s\n' % url)
    for note in domain.note:
        write('   <note>%s\n' % note)
    if domain.ext:
        write("<ext>".join(['   ']+domain.ext)+"\n")
    for remark in domain.remark:
        write('   <remark>%s\n' % remark)
    return string.join(lines, '')

def team_description(team):
    import registry
    lines = []
    write = lines.append
    write('  <team>%s<code>%s\n' % (team.language, team.code))
    for mailto in team.mailto:
        write('   <mailto>%s\n' % mailto)
    if team.announceto:
        write('   <announceto>%s\n' % team.announceto)
    if team.charset:
        write('   <charset>%s\n' % team.charset)
    if team.suppresspot:
        write('   <suppresspot>\n')
    if team.leader:
        write('   <leader>%s\n' % team.leader.name[0])
    for ref in team.ref:
        write('   <ref>%s<url>%s\n' % (ref[0],quote(ref[1])))
    for remark in team.remark:
        write('   <remark>%s\n' % remark)
    for name in team.translators:
        translator = registry.Translator(team, name)
        if translator.name[0] == name:
            write('\n')
            write(translator_description(translator))
    return string.join(lines, '')

def translator_description(translator):
    import registry
    lines = []
    write = lines.append
    write('   <translator>%s\n' % translator.name[0])
    for alias in translator.name[1:]:
        write('    <alias>%s\n' % alias)
    for url in translator.mailto:
        # XXX transitional
        if not hasattr(translator, 'showmail'):
            translator.showmail = None
        if translator.showmail is None:
            show = ''
        else:
            show = ' show='+translator.showmail
        write('    <mailto%s>%s\n' % (show, url))
    for url in translator.url:
        write('    <url>%s\n' % url)
    if translator.disclaimer:
        if translator.disclaimer == '*':
            disclaimer = '<disclaimer>'
        else:
            disclaimer = '<disclaimer>' + translator.disclaimer
    else:
        disclaimer = ''
    if translator.autosend:
        if translator.autosend == 'compress':
            autosend = "<autosend compress>"
        else:
            autosend = '<autosend>'
    else:
        autosend = ''
    if disclaimer or autosend:
        write('    %s%s\n' % (disclaimer, autosend))
    if translator.do:
        line = '    '
        for do in translator.do:
            if len(line) + 4 + len(do.name) > 76:
                write(line + '\n')
                line = '    '
            line = '%s<do>%s' % (line, do.name)
        write(line + '\n')
    for remark in translator.remark:
        write('    <remark>%s\n' % remark)
    return string.join(lines, '')

# Unused routines.

def write_sgml_file(name, element):
    write_sgml_file_rec(open(name, 'w').write, 0, element)

def write_sgml_file_rec(write, depth, element, spacing='  '):
    if type(element) is type(''):
        write('%s%s\n' % (spacing * depth,
                          string.replace(element, '\n', '\\n')))
    else:
        tag = element[0]
        write('%s<%s>\n' % (spacing * depth, tag))
        for sub_element in element[1:]:
            write_sgml_file_rec(write, depth + 1, sub_element, spacing)
        write('%s</%s>\n' % (spacing * depth, tag))

