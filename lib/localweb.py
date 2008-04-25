# Project-specific webpage generation services.
# -*- mode: python; coding: utf-8 -*-
# Copyright © 2001, 2002, 2003, 2004, 2007 Translation Project.
# Copyright © 2000 Progiciels Bourbeau-Pinard inc.
# François Pinard <pinard@iro.umontreal.ca>, 2000.

import os, string, sys, glob
import config, htmlpage, registry, data

try:
    unicode
    have_unicode = 1
except NameError:
    have_unicode = 0

_extstats = None
def get_extstats():
    global _extstats
    if _extstats is None:
        _extstats = data.load_extstats()
    return _extstats

def generate_domain_page(domain):
    if domain == "index":
        file = "%s/index.html" % config.domain_path
        return produce_domain_index(file)
    sys.stderr.write("Generating domain page for %s...\n" % domain)
    file = "%s/%s.html" % (config.domain_path, domain)
    produce_domain_page(data.load_postats(), domain, file)

def generate_team_page(team):
    if team == "index":
        file = "%s/index.html" % config.team_path
        return produce_team_index(file)
    sys.stderr.write("Generating team page for %s...\n" % team)
    file = "%s/%s.html" % (config.team_path, team)
    produce_team_page(data.load_postats(), team, file)


# Generation of webpages describing domains.

def produce_domain_index(output=None):
    DomainIndex(output)

class DomainIndex(htmlpage.Htmlpage):

    def __init__(self, output):
        htmlpage.Htmlpage.__init__(self, None, output)
        write = self.writer
        if not write:
            return
        postats = data.load_postats()
        self.prologue("Textual domains", 'utf-8')
        write("<p>When looking for something to translate and wishing "
              "to reach the largest amount of users, one of the basic "
              "system tools is a good choice: grep, sed, tar, "
              "findutils, coreutils, and bash.  Then shared-mime-info, "
              "xdg-user-dirs, parts of libc and parts of util-linux-ng.  "
              "And then maybe aspell, dialog, diffutils, e2fsprogs, gawk, "
              "kbd, make, psmisc, wget, and xkeyboard-config.</p>")
        write('  <table align=center border=2>\n'
              '   <tr align=left>\n'
              '    <th>Domain</th>\n'
              '    <th>Current<br>version</th>\n'
              '    <th>Disclaimer<br>required</th>\n'
              '    <th>Reference</th>\n'
              '   </tr>\n')
        for domain in registry.domain_list():
            if domain.disclaim:
                hue = "#fff3f3"
                word = "Yes"
            else:
                hue = "#f3fff3"
                word = ""
            write('   <tr>\n'
                  '    <td bgcolor="%s"><a href="%s.html">%s</a></td>\n'
                  % (hue, domain.name, domain.name))
            if postats.potstats.has_key(domain.name):
                hints = registry.hints(postats.potstats[domain.name][0])
                write('    <td bgcolor="%s"><a href="%s">%s</a></td>\n'
                      % (hue, hints.template_url(), hints.version))
            else:
                write('    <td>-</td>\n')
                sys.stderr.write("  * No stats for '%s'\n" % domain.name)
            write('<td align="center" bgcolor="%s">%s</td>' % (hue, word))
            if domain.ref:
                write('    <td bgcolor="%s"><a href="%s">%s</a></td>\n'
                      % (hue, domain.ref[0][1], domain.ref[0][1]))
            elif domain.url:
                write('    <td bgcolor="%s"><a href="%s">%s</a></td>\n'
                      % (hue, domain.url[0], domain.url[0]))
            write('   </tr>\n')
        write('  </table>\n')
        self.epilogue()

def produce_domain_page(postats, name, output=None):
    DomainPage(postats, registry.domain(name), output)

class DomainPage(htmlpage.Htmlpage):

    def __init__(self, postats, domain, output):
        htmlpage.Htmlpage.__init__(self, None, output)
        write = self.writer
        if not write:
            return
        self.prologue("The '%s' textual domain" % domain.name, 'utf-8')
        if not domain.ref:
            write('  <p>This page is about the translation of the messages'
                  ' for the <b><code>%s</code></b> textual domain.</p>\n'
                  % domain.name)
        else:
            write('  <p>This page is about the translation of the messages'
                  ' for the <b><code>%s</code></b> textual domain.  More'
                  ' information about the package can be found here:</p>\n'
                  '  <table align=center border=2>\n'
                  '   <tr align=center>\n'
                  '    <th>Topic</th>\n'
                  '    <th>URL</th>\n'
                  '   </tr>\n'
                  % domain.name)
            for ref in domain.ref:
                write('   <tr align=center>\n'
                      '    <td>%s</td>\n'
                      '    <td align=left><a href="%s">%s</a></td>\n'
                      '   </tr>\n'
                      % (ref[0], ref[1], ref[1]))
            write('  </table>\n')
        if domain.note:
            write('  <ul>\n')
            for note in domain.note:
                write('  <li>%s</li>' % note)
            write('  </ul>\n')
        if domain.disclaim:
            write('  <p>The maintainer of this package requires that'
                  ' disclaimers be filled out and sent to the'
                  ' Free Software Foundation before accepting PO files'
                  ' from the Translation Project.</p>\n')
        else:
            write('  <p>The maintainer does not require any special papers'
                  ' prior to accepting translations.</p>\n')
        if postats.potstats.has_key(domain.name):
            file = postats.potstats[domain.name][0]
            url = registry.hints(file).template_url()
            write('  <p>The current template for this domain is'
                  ' <a href="%s">%s</a>.\n' % (url, file))
        if domain.url:
            write('  <p>The following URL may help translators that need'
                  ' a finer context in order to make their translation. '
                  ' Be aware that the indicated package could be just'
                  ' a pre-release, and might not even compile:</p>\n')
            write('  <ul>\n')
            for url in domain.url:
                write('   <li><a href="%s">%s</a>\n' % (url, url))
            write('  </ul>\n')
        write('  <p>The following table lists (under <b>Version</b>) all the'
              ' PO files that are available for this domain:</p>\n'
              '  <table align=center border=2>\n'
              '   <tr>\n'
              '    <th>Language</th>\n'
              '    <th>Code</th>\n'
              '    <th>Package version</th>\n'
              '    <th>Last translator</th>\n'
              '    <th>Translated</th>\n'
              '   </tr>\n')
        for team in registry.team_list():
            if team.code in domain.ext:
                stats = get_extstats().get((domain.name, team.name))
                if stats:
                    trans = stats['translated']
                    total = trans + stats['untranslated'] + stats['fuzzy']
                    numbers = "%s / %s" % (trans, total)
                else:
                    numbers = "unknown"
                if os.path.isfile('%s/%s/%s.po'
                                  % (config.last_path, domain.name, team.name)):
                    color = "#f8d0f8"  # Magenta: external but file is present.
                else:
                    color = "#e8e8e8"  # Grey: plain external.
                write('<tr align=center>'
                      '<td><a href="../team/%s.html">%s</a></td>'
                      '<td>%s</td><td>--</td>'
                      '<td><i>external</i></td>'
                      '<td bgcolor="%s">%s</td></tr>\n'
                      % (team.code, team.language, team.code, color, numbers))
            else:
                build_language_cell(postats, write, team, domain)
        write('  </table>\n')
        self.epilogue()

def build_language_cell(postats, write, team, domain):
    table = []
    names = glob.glob("%s/%s/%s-[0-9]*.%s.po" %
                      (config.pos_path, team.name, domain.name, team.name))
    for filename in names:
        try:
            hints = registry.Hints(filename)
        except KeyError:
            sys.stderr.write("  * Nonexistent domain or team: %s\n" % filename)
            continue
        except ValueError:
            sys.stderr.write("  * No hints found for %s\n" % filename)
            continue
        if hints.domain != domain and hints.team != team:
            sys.stderr.write("  * Wrong domain or team in %s\n" % filename)
            continue
        if hints.version is None:
            sys.stderr.write("  * Missing version number in %s\n" % filename)
            continue
        key = hints.domain.name, hints.version.name, hints.team.name
        if not postats.has_key(key):
            sys.stderr.write("  * Not in stats database: %s\n" % filename)
            continue
        (translator, mailto, translated, total) = postats[key][:4]
        table.append((hints.version, translator, mailto, translated, total))
    if table:
        table.sort()
        for counter in range(len(table)):
            write('   <tr align=center>\n')
            if counter == 0:
                write('    <td rowspan=%d>'
                      '<a href="../team/%s.html">%s</a></td>\n'
                      '    <td rowspan=%d>%s</td>\n'
                      % (len(table), team.code, team.language,
                         len(table), team.code))
            version, translator, mailto, translated, total = table[counter]
            write('    <td><a href="../%s/%s/%s-%s.%s.po">%s</a></td>\n'
                  % (config.pos_dir, team.name, domain.name,
                     version.name, team.name, version.name))
            try:
                transinfo = registry.registry.translator_info
                email = transinfo(team, translator)['mailto'][0]
            except (IndexError, KeyError):
                email = mailto
            if email:
                write('    <td><a href="mailto:%s">%s</a></td>\n'
                      % (scramble(email), translator))
            else:
                write('    <td>%s</td>\n' % translator)
            write('    <td bgcolor="%s">%d / %d</td>\n'
                  % (colorize(translated, total), translated, total))
            write('   </tr>\n')


# Generation of webpages describing national teams.

def produce_team_index(output=None):
    TeamIndex(output)

class TeamIndex(htmlpage.Htmlpage):

    def __init__(self, output):
        htmlpage.Htmlpage.__init__(self, None, output)
        write = self.writer
        if not write:
            return
        self.prologue("Translation teams", 'utf-8')
        write('  <table align=center border=2>\n'
              '   <tr align=center>\n'
              '    <th>Language</th>\n'
              '    <th>Code</th>\n'
              '    <th>Team address</th>\n'
              '   </tr>\n')
        for team in registry.team_list():
            write('   <tr align=center>\n'
                  '    <td><a href="%s.html">%s</a></td>\n'
                  '    <td>%s</td>\n'
                  % (team.code, team.language, team.code))
            if team.mailto:
                write('    <td><a href="mailto:%s">%s</a></td>\n'
                      % (team.mailto[0], team.mailto[0]))
            else:
                write('    <td></td>\n')
            write('   </tr>\n')
        write('  </table>\n')
        self.epilogue()

def produce_team_page(postats, name, output=None):
    TeamPage(postats, registry.team(name), output)

class TeamPage(htmlpage.Htmlpage):

    def __init__(self, postats, team, output):
        htmlpage.Htmlpage.__init__(self, None, output)
        write = self.writer
        if not write:
            return
        self.prologue("Translation team for %s" % team.language, 'utf-8')
        assigned_domains = {}
        seen_translators = []
        write('  <p>The %s translation team uses <b><code>%s</code></b> as'
              ' its language code.  This code is part of the %s PO file'
              ' names.  It is also sometimes used as a short identification'
              ' for the team.</p>\n'
              % (team.language, team.code, team.language))

        write('  <p>\n')
        if team.mailto:
            write('   The team uses <a href="mailto:%s">%s</a> as official'
                  ' email address, which reaches either a mailing list or'
                  ' someone who broadcasts information to all other team'
                  ' members.\n'
                  % (team.mailto[0], team.mailto[0]))
        if team.leader and team.leader.mailto:
            name = uni2html(team.leader.uniname()[0],'utf-8')
            if team.leader.can_show_mail():
                write('   <a href="mailto:%s">%s</a>'
                      ' currently acts as the team leader,'
                      % (team.leader.mailto[0], name))
            elif team.leader.url:
                write('   <a href="%s">%s</a>'
                      ' currently acts as the team leader,'
                      % (team.leader.url[0], name))
            else:
                write('   %s currently acts as the team leader,' % name)
            write(' and you may write to him or her for all matters related'
                  ' to team coordination.\n')
        elif team.mailto:
            write('   The team does not seem to have appointed a leader, so'
                  ' for any questions you may write to the above team address.'
                  ' To get a package assigned, you can write directly to a'
                  ' <a href="mailto:coordinator@translationproject.org">'
                  'TP coordinator</a> while CC\'ing the team list.\n')
        else:
            write('   The team does not seem to have appointed a leader, so'
                  ' for any questions or to get a package assigned, you may'
                  ' write directly to a'
                  ' <a href="mailto:coordinator@translationproject.org">'
                  'TP coordinator</a>.\n')

        if team.charset:
            write('   Team members expressed a preference towards using the'
                  ' <code>%s</code> charset. '
                  ' You may want to consider using it whenever you send email'
                  ' to the team list or members, or if you produce any'
                  ' translation file meant for this team.\n'
                  % team.charset)
        write('  </p>\n')

        if team.ref:
            write('  <p>You can get more information about the'
                  ' %s effort here:</p>\n'
                  '  <table align=center border=2>\n'
                  '   <tr align=center>\n'
                  '    <th>Topic</th>\n'
                  '    <th>URL</th>\n'
                  '   </tr>\n'
                  % team.language)
            for ref in team.ref:
                write('   <tr align=center>\n'
                      '    <td>%s</td>\n'
                      '    <td align=left><a href="%s">%s</a></td>\n'
                      '   </tr>\n'
                      % (ref[0], ref[1], ref[1]))
            write('  </table>\n')
        write('  <p>The %s team currently consists of'
              ' the following translators:</p>\n'
              '  <table align=center border=2>\n'
              '   <tr align=center>\n'
              '    <th>Translator</th>\n'
              '    <th>Assignments</th>\n'
              '    <th>Disclaimed</th>\n'
              '    <th>Autosend</th>\n'
              '    <th>Personal website</th>\n'
              '   </tr>\n'
              % team.language)
        # Construct the table of translators.
        for name in team.translators:
            translator = registry.translator(team, name)
            domain_count = 0
            if translator.name[0] in seen_translators:
                continue
            seen_translators.append(translator.name[0])
            for domain in translator.do:
                if assigned_domains.has_key(domain.name):
                    sys.stderr.write("  * Domain multiply assigned: %s.%s\n"
                                     % (domain.name, team.name))
                assigned_domains[domain.name] = translator
                domain_count = domain_count + 1
            write('   <tr align=center>\n'
                  '    <td align=left>%s</td>\n'
                  % translator_best_href(translator))
            if domain_count:
                write('    <td>%d</td>\n' % domain_count)
            else:
                write('    <td></td>\n')
            if translator.disclaimer:
                write('    <td>yes</td>\n')
            else:
                write('    <td></td>\n')
            if translator.autosend == "compress":
                write('    <td>compress</td>\n')
            elif translator.autosend:
                write('    <td>plain</td>\n')
            else:
                write('    <td>-</td>\n')
            if translator.url:
                write('    <td><a href="%s">yes</a></td>\n'
                      % translator.url[0])
            else:
                write('    <td></td>\n')
            write('   </tr>\n')
        write('  </table>\n')
        write('  <p>The Autosend column is for translators who want the PO'
              ' file sent to them when a new POT file is added to the project'
              ' -- they don\'t want to fetch the PO file themselves, but'
              ' wish to receive it together with the notice. '
              ' <a href="mailto:coordinator@translationproject.org">'
              'Just ask</a> if you want this service for yourself.</p>\n')
        write('  <p>Here is the current list of assignments of textual domains'
              ' to translators, as known to the Translation Project registry. '
              ' The robot relies on this information for directly accepting'
              ' submissions from translators. '
              ' The domains with a pinkish background'
              ' require that the translator has filled out a disclaimer;'
              ' those with a greenish background are freely translatable.'
              ' If no <b>Current package version</b> is listed in the table,'
              ' the information is identical to the  most recent submission'
              ' (under <b>Last-submitted PO version</b>). '
              ' If you find an error or omission, please write')
        if team.leader and team.leader.mailto and team.leader.can_show_mail():
            write(' to <a href="mailto:%s">%s</a> to get it corrected.</p>\n'
                  % (team.leader.mailto[0],
                     uni2html(team.leader.uniname()[0],'utf-8')))
        elif team.leader and team.leader.url:
            write(' to <a href="%s">%s</a> to get it corrected.</p>\n'
                  % (team.leader.url[0],
                     uni2html(team.leader.uniname()[0],'utf-8')))
        else:
            write(' to a <a href="mailto:coordinator@translationproject.org">'
                  'TP coordinator</a> to get it corrected.</p>\n')
        write('  <table align=center border=2>\n'
              '   <tr align=center>\n'
              '    <th>Domain</th>\n'
              '    <th>Assigned translator</th>\n'
              '    <th>Last-submitted PO version</th>\n'
              '    <th>Translated</th>\n'
              '    <th>Current package version</th>\n'
              '    <th>Translated</th>\n'
              '   </tr>\n')
        # Construct the table of packages.
        for domain in registry.domain_list():
            if domain.disclaim:
                hue = "#fff3f3"
            else:
                hue = "#f3fff3"
            write('   <tr align=center>\n'
                  '    <td align=left bgcolor="%s">'
                  '<a href="../domain/%s.html">%s</a></td>\n'
                  % (hue, domain.name, domain.name))
            extstats = None
            if assigned_domains.has_key(domain.name):
                write('    <td align=left>%s</td>\n'
                      % translator_best_href(assigned_domains[domain.name]))
            elif team.code in domain.ext:
                write('    <td bgcolor="#e8e8e8"><i>external</i></td>\n')
                extstats = get_extstats().get((domain.name, team.code))
            else:
                write('    <td></td>\n')
            current = None
            file = '%s/%s/%s.po' % (config.last_path, domain.name, team.name)
            # Show current version not for absent files nor for externals.
            if os.path.isfile(file) and (not team.code in domain.ext):
                hints = registry.hints(os.readlink(file))
                key = hints.domain.name, hints.version.name, hints.team.name
                if postats.has_key(key):
                    (translated, total) = postats[key][2:4]
                    current = hints.version
                    write('    <td><a href="../%s/%s/%s-%s.%s.po">%s</a></td>\n'
                          % (config.pos_dir, team.name, domain.name,
                             current.name, team.name, current.name))
                    write('    <td bgcolor="%s">%d / %d</td>\n'
                          % (colorize(translated, total), translated, total))
                    try:
                        current.set_sort_key()
                    except AssertionError:
                        current = None
            else:
                write('    <td colspan=2></td>\n')
            try:
                template, tally = postats.potstats[domain.name]
                version = registry.hints(template).version
            except KeyError:
                version = None
            if version and (not current or current != version):
                key = domain.name, version.name, team.name
                if team.code in domain.ext:
                    reference = '%s' % version
                    if os.path.isfile(file):
                        color = "#f8d0f8"  # Magenta: external but file present.
                    else:
                        color = "#e8e8e8"  # Grey: external.
                    if extstats:
                        numbers = ("%d / %d" % (extstats['translated'], tally))
                    else:
                        numbers = "unknown"
                elif postats.has_key(key):
                    reference = ('<a href="../%s/%s/%s-%s.%s.po">%s</a>'
                                 % (config.pos_dir, team.name,
                                    domain.name, version, team.name, version))
                    translated = postats[key][2]
                    numbers = "%d / %d" % (translated, tally)
                    color = colorize(translated, tally)
                else:
                    reference = ('<a href="../%s/%s-%s.pot">%s</a>'
                                 % (config.pots_dir, domain.name, version,
                                    version))
                    color = "#d0f0f8"  # Blue: fully untranslated.
                    numbers = "%d / %d" % (0, tally)
                write('    <td>%s</td>\n'
                      '    <td bgcolor="%s">%s</td>\n'
                      % (reference, color, numbers))
            write('   </tr>\n')
        write('  </table>\n')
        self.epilogue()


def translator_best_href(translator):
    name = uni2html(translator.uniname()[0], 'utf-8')
    if translator.url:
        return name
    if translator.mailto and translator.can_show_mail():
        return ('<a href="mailto:%s">%s</a>'
                % (scramble(translator.mailto[0]), name))
    else:
        return name

_entities = {}
def _uni2html(char):
    if not _entities:
        for i in range(32,128):
            _entities[unichr(i)] = chr(i)
        import htmlentitydefs
        for k,v in htmlentitydefs.entitydefs.items():
            if len(v) == 1:
                v = unicode(v,"latin-1")
            else:
                v = unichr(int(v[2:-1]))
            _entities[v] = '&'+k+';'
    try:
        return _entities[char]
    except KeyError:
        return '&#%d;' % ord(char)

if have_unicode:
    def uni2html(str, code = None):
        if code:
            try:
                return str.encode(code)
            except UnicodeError:
                pass
        return string.join(map(_uni2html, str), "")
else:
    def uni2html(str, code = None):
        assert string.lower(code)=="utf-8"
        return str

def scramble(email):
    email = string.replace(email, "@", " (at) ")
    email = string.replace(email, ".", " (dot) ")
    return email

palette = ['#ff7777', '#f7bf77', '#efdf77', '#efef8f',
                      '#dfef77', '#bff777', '#77ff77']
def colorize(translated, total):
    if total == 0:
        return "#d7d7d7"
    if translated > total:
        return "#00f8f8"
    return palette[6 * translated / total]
