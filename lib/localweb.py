# Project-specific webpage generation services.
# -*- mode: python; coding: utf-8 -*-
# Copyright © 2001, 2002, 2003, 2004, 2007 Translation Project.
# Copyright © 2000 Progiciels Bourbeau-Pinard inc.
# François Pinard <pinard@iro.umontreal.ca>, 2000.

import os, string, sys
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
        self.prologue("Textual domains for translations", 'utf-8')
        write('  <table align=center border=2>\n'
              '   <tr align=left>\n'
              '    <th>Domain</th>\n'
              '    <th align=center>Reference</th>\n'
              '   </tr>\n')
        for domain in registry.domain_list():
            write('   <tr>\n'
                  '    <td><a href="../domain/%s.html">%s</a></td>\n'
                  % (domain.name, domain.name))
            if domain.url:
                write('    <td><a href="%s">%s</a></td>\n'
                      % (domain.url[0], domain.url[0]))
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
        self.prologue("The '%s' textual domain" % domain.name,'utf-8')
        if domain.ref:
            write('  <p>This page is about the translation of messages for'
                  ' the <code>%s</code> textual domain.  More information'
                  ' about this package can be found here:</p>\n'
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
            url = registry.hints(file).template_urls()[0]
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
              '    <th>Code</th>\n'
              '    <th>Language</th>\n'
              '    <th>Version</th>\n'
              '    <th>Last translator</th>\n'
              '    <th>Translated</th>\n'
              '   </tr>\n')
        for team in registry.team_list():
            if team.code in domain.ext:
                st = get_extstats().get((domain.name, team.name))
                if st:
                    version = st['version']
                    trans = st['translated']
                    total = trans + st['untranslated'] + st['fuzzy']
                    stats = "%s / %s" % (trans, total)
                else:
                    version = stats = "unknown"
                write('<tr align=center><td>%s</td>'
                      '<td><a href="../team/%s.html">%s</a></td>'
                      '<td>%s</td>'
                      '<td><i>external</i></td><td>%s</td></tr>\n'
                      % (team.code, team.code, team.language, version, stats))
            os.path.walk('%s/%s' % (config.pos_path, team.name),
                         domain_page_walker, (postats, write, team, domain))
        write('  </table>\n')
        self.epilogue()

def domain_page_walker((postats, write, team, domain), dirname, bases):
    table = []
    for base in bases:
        try:
            hints = registry.Hints(base)
        except KeyError:
            sys.stderr.write("  * Nonexistent domain or team: %s\n" % base)
            continue
        except ValueError:
            sys.stderr.write("  * No hints found for %s\n" % base)
            continue
        if hints.domain == domain and hints.team == team:
            if hints.version is None:
                sys.stderr.write("  * Missing version: %s\n" % base)
                continue
            key = hints.domain.name, hints.version.name, hints.team.name
            if not postats.has_key(key):
                sys.stderr.write("  * Not in stats database: %s\n" % base)
                continue
            (translator, mailto, translated, total) = postats[key][:4]
            table.append(
                (hints.version, translator, mailto, translated, total))
    if table:
        code = team.code
        language = team.language
        table.sort()
        for counter in range(len(table)):
            write('   <tr align=center>\n')
            if counter == 0:
                if len(table) > 1:
                    write('    <td rowspan=%d>%s</td>\n'
                          '    <td rowspan=%d>'
                          '<a href="../team/%s.html">%s</a></td>\n'
                          % (len(table), code, len(table), code, language))
                else:
                    write('    <td>%s</td>\n'
                          '    <td><a href="../team/%s.html">%s</a></td>\n'
                          % (code, code, language))
            version, translator, mailto, translated, total = table[counter]
            write('    <td><a href="%s/%s/%s/%s-%s.%s.po">%s</a></td>\n'
                  % (config.site_base, config.pos_dir, team.name, domain.name,
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
            write('    <td bgcolor="%s">%d / %d</td>\n' %
	          (colorize(translated, total), translated, total))
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
        self.prologue("National translation teams", 'utf-8')
        write('  <table align=center border=2>\n'
              '   <tr align=center>\n'
              '    <th>Code</th>\n'
              '    <th>Language</th>\n'
              '    <th>Team address</th>\n'
              '   </tr>\n')
        for team in registry.team_list():
            write('   <tr align=center>\n'
                  '    <td>%s</td>\n'
                  '    <td><a href="../team/%s.html">%s</a></td>\n'
                  % (team.code, team.code, team.language))
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
                      ' and you may write to him or her for all matters'
                      ' related to team coordination.\n'
                      % (team.leader.mailto[0], name))
            elif team.leader.url:
                write('   <a href="%s">%s</a>'
                      ' currently acts as the team leader.\n'
                      % (team.leader.url[0], name))
            else:
                write('   %s currently acts as the team leader.\n' % (name))
        if team.charset:
            write('   Team members expressed a preference towards using the'
                  ' <code>%s</code> charset. '
                  ' You may want to consider using it whenever you send email'
                  ' to the team list or members, or if you produce any'
                  ' translation file meant for this team.\n'
                  % team.charset)
        write('  </p>\n')

        if team.ref:
            write('  <p>You may get more information about the'
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
              '    <th>Website</th>\n'
              '    <th>Disclaimer</th>\n'
              '    <th>Autosend</th>\n'
              '    <th>Count</th>\n'
              '   </tr>\n'
              % team.language)
        names = team.translator.keys()
        names.sort()
        for name in names:
            translator = registry.translator(team, name)
            domain_count = 0
            if translator.name[0] in seen_translators:
                continue
            seen_translators.append(translator.name[0])
            for domain in translator.do:
                if assigned_domains.has_key(domain.name):
                    sys.stderr.write(
                        "  * Domain assigned more than once: %s.%s\n"
                        % (domain.name, team.name))
                assigned_domains[domain.name] = translator
                domain_count = domain_count + 1
            # Displaying URLs in all cases allows to configure translators
            # who don't like their email addresses displayed.
            write('   <tr align=center>\n'
                  '    <td align=left>%s</td>\n'
                  % translator_best_href(translator,prefer_mail = 0,
                                         charset = 'utf-8'))
            if translator.url:
                write('    <td><a href="%s">Yes</a></td>\n'
                      % translator.url[0])
            else:
                write('    <td></td>\n')
            if translator.disclaimer:
                write('    <td>Yes</td>\n')
            else:
                write('    <td></td>\n')
            if translator.autosend:
                write('    <td>Yes</td>\n')
            else:
                write('    <td></td>\n')
            if domain_count:
                write('    <td>%d</td>\n' % domain_count)
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
              ' submissions from translators.  If no <b>Current version</b>'
              ' is listed in the table, the information is identical to the'
              ' most recent submission (under <b>Version</b>). '
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
            write(' directly to the'
                  ' <a href="mailto:coordinator@translationproject.org">'
                  'coordinator of the Translation Project</a>'
                  ' to get it corrected, as the team does not seem to have'
                  ' appointed its own coordinator yet.</p>\n')
        write('  <table align=center border=2>\n'
              '   <tr align=center>\n'
              '    <th>Domain</th>\n'
              '    <th>Assigned translator</th>\n'
              '    <th>Version</th>\n'
              '    <th>Translated</th>\n'
              '    <th>Current version</th>\n'
              '    <th>Translated</th>\n'
              '   </tr>\n')
        for domain in registry.domain_list():
            write('   <tr align=center>\n'
                  '    <td align=left><a href="../domain/%s.html">%s</a></td>\n'
                  % (domain.name, domain.name))
            extstats = None
            if assigned_domains.has_key(domain.name):
                write('    <td align=left>%s</td>\n'
                      % translator_best_href(assigned_domains[domain.name],
                                             charset = 'utf-8'))
            elif team.code in domain.ext:
                write('   <td><i>external</i></td>\n')
                extstats = get_extstats().get((domain.name, team.code))
            else:
                write('   <td></td>\n')
            file = '%s/%s/%s.po' % (config.last_path, domain.name, team.name)
            have_stats = 0
            if os.path.isfile(file):
                hints = registry.Hints(os.readlink(file))
                key = hints.domain.name, hints.version.name, hints.team.name
                if postats.has_key(key):
                    (translated, total) = postats[key][2:4]
                    have_stats = 1
                    current = hints.version
            elif extstats:
                    translated = extstats['translated']
                    total = translated + extstats['untranslated'] + extstats['fuzzy']
                    current = registry.version(extstats['version'])
                    have_stats = 1
            if have_stats:
                color = colorize(translated, total)
                write('    <td align="center">%s</td>\n'
                      '   <td align="center" bgcolor="%s">%d / %d</td>\n'
                      % (current.name, color, translated, total))
                try:
                    current.set_sort_key()
                except AssertionError:
                    current = None
                    have_stats = 0
            else:
                write('  <td colspan=2>\n')
            try:
                templ_file, templ_msgs = postats.potstats[domain.name]
                templ_hints = registry.hints(templ_file)
            except KeyError:
                templ_hints = None
            if templ_hints and (not have_stats or current!=templ_hints.version):
                cur_key = domain.name, templ_hints.version.name, team.name
                if postats.has_key(cur_key):
                    (translated, total) = postats[cur_key][2:4]
                    color = colorize(translated, total)
                elif extstats:
                    if templ_msgs:
                        color = colorize(translated, templ_msgs)
                    else:
                        color = '#f8d0f8'  # Magenta; seems to never occur.
                    total = templ_msgs
                else:
                    if templ_msgs:
                        color = '#00d0f8'  # Blue: fully untranslated.
                    else:
                        color = '#f8d0f8'  # Magenta; seems to never occur.
                    translated = 0
                    total = templ_msgs
                write('    <td align="center">%s</td>\n'
                      '   <td align="center" bgcolor="%s">%d / %d</td>\n'
                      % (templ_hints.version.name, color, translated, total))
            write('   </tr>\n')
        write('  </table>\n')
        language = string.split(team.language)[0]
        self.epilogue()


def translator_best_href(translator, prefer_mail = 0, charset = None):
    url = mail = None
    name = uni2html(translator.uniname()[0],charset)
    if translator.url and translator.showmail != 'no':
        url = '<a href="%s">%s</a>' % (translator.url[0], name)
    if translator.mailto and translator.can_show_mail():
        mail = '<a href="mailto:%s">%s</a>' % (scramble(translator.mailto[0]), name)
    if mail and prefer_mail: return mail
    if url: return url
    if mail: return mail
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

palette = ['#ff0000', '#f8c040', '#f0e070', '#f0f090',
                      '#e0f070', '#c0f840', '#00ff00']
def colorize(translated, total):
    if total == 0:
        return "#d7d7d7"
    if translated > total:
        return "#00f8f8"
    return palette[6 * translated / total]
