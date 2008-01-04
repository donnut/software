# Handling of the PO file Registry.
# -*- mode: python; coding: utf-8 -*-
# Copyright © 2001, 2002, 2003, 2004 Translation Project.
# Copyright © 1998, 1999, 2000 Progiciels Bourbeau-Pinard inc.
# François Pinard <pinard@iro.umontreal.ca>, 1998.

import os, re, string, sys, tempfile, types
import config

puburl = config.site_base
tempfile.tempdir = config.temp_path

# Emulate Python 1.5.
try:
    unicode
    have_unicode = 1
except NameError:
    def unicode(data, enc = None):
        return data
    have_unicode = 0

# Registry services (teams, translators, and domains).

# Teams contain translators, which handle domains.  There is no
# other containing relation, so there should not be cyclic references.

DOMAIN = ('iso_[0-9_]+|'
          '[a-z_-]+[a-z]|'
          'a2ps|e2fsprogs|libgphoto2_port|libgphoto2|gphoto2|m4')

VERSION = ('[.0-9]+-?b[0-9]+|'
           '[.0-9]+-?dev[0-9]+|'
           '[.0-9]+-?pre[0-9]+|'
           '[.0-9]+-?rc[0-9]+|'
           '[.0-9]+-?rel[0-9]+|'
           '[.0-9]+[a-z]?|'
           '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]')

TEAM = ('[a-z][a-z][a-z]?'
        '|[a-z][a-z]_[A-Z][A-Z]'
        '|[a-z][a-z]@[a-z]+')

def team(name, cache={}):
    team = cache.get(name)
    if team is None:
        cache[name] = team = Team(name)
    return team

class Team:

    def __init__(self, name):
        self.name = name
        info = registry.team_info(name)
        self.language = info.get('language')
        self.code = info.get('code')
        self.mailto = info.get('mailto')
        self.announceto = info.get('announceto')
        self.charset = info.get('charset')
        self.suppresspot = info.get('suppresspot')
        self.ref = info.get('ref')
        self.remark = info.get('remark')
        self.translator = {}
        for translator in info.get('translator', {}).keys():
            self.translator[translator] = Translator(self, translator)
        leader = info.get('leader')
        self.leader = leader and self.translator[leader]
        self.translators = info.get('translators')
        self.by_email = None

    def translator_for_domain(self, do):
        if type(do) is types.StringType:
            do = domain(do)
        result = []
        for t in self.translator.values():
            if t in result:
                continue
            if do in t.do:
                result.append(t)
        return result

    def translator_by_email(self, email):
        if self.by_email is None:
            self.by_email = {}
            for t in self.translators:
                t = translator(self, t)
                for e in t.mailto:
                    self.by_email[e] = t
        try:
            return self.by_email[email]
        except KeyError:
            raise KeyError, "Unknown translator `%s'" % email

    def announce_address(self):
        if self.announceto:
            return self.announceto
        return self.mailto[0]

    def encode(self, msg):
        if isinstance(msg, types.UnicodeType):
            try:
                return msg.encode(self.charset)
            except (UnicodeError, TypeError):
                # TypeError can occur when charset is None.
                return msg.encode("utf-8")
        return msg

    def __cmp__(self, other):
        return cmp(self.name, other.name)

    def __str__(self):
        return self.name

def translator(team, name, email=None, cache={}):
    if have_unicode and type(name) is types.UnicodeType:
        name = name.encode("utf-8")
    key = team.name, name
    translator = cache.get(key)
    if translator is None:
        try:
            cache[key] = translator = Translator(team, name)
        except KeyError:
            if email is None:raise
            cache[key] = translator = team.translator_by_email(email)
    return translator

class Translator:

    def __init__(self, team, name):
        info = registry.translator_info(team, name)
        self.name = info.get('name')
        self.mailto = info.get('mailto')
        self.showmail = info.get('showmail')
        self.url = info.get('url')
        self.disclaimer = info.get('disclaimer')
        self.autosend = info.get('autosend')
        self.do = []
        for do in info.get('do'):
            try:
                instance = domain(do)
            except KeyError:
                pass
            else:
                self.do.append(instance)
        self.remark = info.get('remark')

    def __cmp__(self, other):
        # Compare the full arrays of names.  It's simpler.
        return cmp(self.name, other.name)

    def uniname(self):
        return map(lambda n:unicode(n,"utf-8"), self.name)

    def can_show_mail(self):
        return self.showmail is None or self.showmail == "yes"


def domain(name, cache={}):
    domain = cache.get(name)
    if domain is None:
        cache[name] = domain = Domain(name)
    return domain

class Domain:

    def __init__(self, name):
        info = registry.domain_info(name)
        self.name = info.get('name')
        self.package = info.get('package')
        self.potcopyright = info.get('potcopyright')
        self.ref = info.get('ref')
        self.mailto = info.get('mailto')
        self.nomailto = info.get('nomailto')
        self.keep = info.get('keep')
        self.disclaim = info.get('disclaim')
        self.autosend = info.get('autosend')
        self.url = info.get('url')
        self.note = info.get('note', [])
        self.ext = info.get('ext')
        self.remark = info.get('remark')

    def __cmp__(self, other):
        return cmp(self.name, other.name)

    def __str__(self):
        return self.name

class Registry:
    """\
Consultation of the registry data file.
"""

    def __init__(self):
        self.domains = None             # dictionary of domains
        self.domain_names = None        # sorted domain names
        self.teams = None               # dictionary of teams
        self.team_names = None          # sorted team names

    def load_registry(self):
        import data
        domains, domain_names, teams, team_names = data.load_registry()
        self.domains = domains
        self.domain_names = domain_names
        self.teams = teams
        self.team_names = team_names

    def domain_list(self):
        if self.domains is None:
            self.load_registry()
        domains = []
        for name in self.domain_names:
            domains.append(domain(name))
        return domains

    def domain_info(self, name):
        if self.domains is None:
            self.load_registry()
        try:
            return self.domains[name]
        except KeyError:
            raise KeyError, "Unknown domain `%s'" % name

    def team_list(self):
        if self.domains is None:
            self.load_registry()
        teams = []
        for name in self.team_names:
            teams.append(team(name))
        return teams

    def team_info(self, name):
        if self.domains is None:
            self.load_registry()
        try:
            return self.teams[name]
        except KeyError:
            match = re.match('([a-z][a-z])[_\@]/:', name)
            if match:
                try:
                    return self.teams[match.group(1)]
                except KeyError:
                    pass
            raise KeyError, "Unknown team `%s'" % name

    def translator_info(self, team, name):
        try:
            return self.team_info(team.code)['translator'][name]
        except KeyError:
            raise KeyError, "Unknown translator `%s'" % name

registry = Registry()
domain_list = registry.domain_list
team_list = registry.team_list


# PO and POT name services (hints, versions, and charsets).

def hints(name=None):
    return Hints(name)

class Hints:
    """\
Splitting file names into components.
"""

    def __init__(self, name):
        self.pot = None                 # true if this is a template file
        self.domain = None              # textual domain of the file
        self.version = None             # version numbers of the domain
        self.team = None                # team code, including region or dialect
        self.charset = None             # None, or '.' plus translation charset
        self.gzipped = None             # None, or '.gz' if compressed
        if name:
            self.merge(name)

    def merge(self, name):
        match = re.search(r'(?P<dom>%s)-(?P<ver>%s)\.pot(?P<z>\.gz)?$'
                          % (DOMAIN, VERSION), name)
        if match:
            found_pot = 1
            found_domain = domain(match.group('dom'))
            found_version = version(match.group('ver'))
            found_team = None
            found_gzipped = match.group('z')
        else:
            match = re.search(r'(?P<dom>%s)-(?P<ver>%s)\.(?P<team>%s)'
                               '\.po(?P<z>\.gz)?$'
                              % (DOMAIN, VERSION, TEAM), name)
            if match:
                found_pot = 0
                found_domain = domain(match.group('dom'))
                found_version = version(match.group('ver'))
                found_team = team(match.group('team'))
                found_gzipped = match.group('z')
            else:
                raise ValueError, "No hints from '%s'" % name
        message = None
        if self.pot is None:
            self.pot = found_pot
        elif found_pot != self.pot:
            message = "POT hint from '%s' contradicts previous" % name
        if self.domain is None:
            self.domain = found_domain
        elif found_domain != self.domain:
            message = ("Domain hint from '%s' contradicts '%s'"
                       % (name, self.domain.name))
        if self.version is None:
            self.version = found_version
        elif found_version != self.version:
            message = ("Version hint from '%s' contradicts '%s'"
                       % (name, self.version.name))
        if self.team is None:
            self.team = found_team
        elif found_team != self.team:
            message = ("Team hint from '%s' contradicts '%s'"
                       % (name, self.team.name))
        self.gzipped = self.gzipped or found_gzipped
        if message:
            raise ValueError, message

    def __cmp__(self, other):
        return cmp((self.domain, self.version), (other.domain, other.version))

    def template_base(self):
        """Basename of a POT file."""
        return '%s-%s.pot' % (self.domain.name, self.version.name)

    def template_path(self):
        """Full path plus name of a POT file within the TP archive."""
        return '%s/%s' % (config.pots_path, self.template_base())

    def template_url(self):
        """URL of a POT file within the TP archive."""
        return '%s/%s/%s' % (puburl, config.pots_dir, self.template_base())

    def archive_base(self):
        """Basename of a PO file."""
        return ('%s-%s.%s.po' %
                (self.domain.name, self.version.name, self.team.name))

    def archive_path(self):
        """Full path plus name of a PO file within the TP archive."""
        return ('%s/%s/%s' %
                (config.pos_path, self.team.name, self.archive_base()))

    def archive_url(self):
        """URL of a PO file within the TP archive."""
        return ('%s/%s/%s/%s' %
                (puburl, config.pos_dir, self.team.name, self.archive_base()))

    def maintainer_path(self):
        """Maintainer's view of the full file name of a PO file."""
        return ('%s/%s/%s.po' %
                (config.last_path, self.domain.name, self.team.name))

    def maintainer_url(self):
        """Maintainer's view of the URL of a PO file."""
        return ('%s/%s/%s/%s.po' %
                (puburl, config.last_dir, self.domain.name, self.team.name))


def version(name):
    return Version(name)

class Version:

    def __init__(self, name):
        self.name = name
        self.sort_key = None

    def __cmp__(self, other):
        if self.sort_key is None:
            self.set_sort_key()
        if other.sort_key is None:
            other.set_sort_key()
        return cmp(self.sort_key, other.sort_key)

    def set_sort_key(self):
        match = re.match(
            r'([0-9]+)\.?([0-9]*)\.?([0-9]*)\.([0-9]{6,8})$', self.name)
        if match:
            major = int(match.group(1))
            minor = pretest = patch = 0
            if match.group(2):
                minor = int(match.group(2))
            if match.group(3):
                patch = int(match.group(3))
            pretest = int(match.group(4))
            self.sort_key = major, minor, patch, 1, pretest
            return self.sort_key
        match = re.match(
            r'([0-9]+)\.?([0-9]*)\.?([0-9]*)([a-z]?)$', self.name)
        if match:
            major = int(match.group(1))
            minor = pretest = 0
            if match.group(2):
                minor = int(match.group(2))
            if match.group(4):
                pretest = ord(match.group(4)) - ord('a') + 1
            if match.group(3):
                patch = int(match.group(3))
            else:
                patch = 0
            self.sort_key = major, minor, patch, 0, pretest
            return self.sort_key
        match = re.match(
            r'([0-9]+)\.?([0-9]*)\.?([0-9]*)[-.]?rel([0-9]+)$', self.name)
        if match:
            major = int(match.group(1))
            minor = patch = pretest = 0
            if match.group(2):
                minor = int(match.group(2))
            if match.group(3):
                patch = int(match.group(3))
            if match.group(4):
                pretest = int(match.group(4))
            self.sort_key = major, minor, patch, 1, pretest
            return self.sort_key
        match = re.match(
            r'([0-9]+)\.?([0-9]*)\.?([0-9]*)[-.]?(b|dev|pre|rc)([0-9]+)$',
            self.name)
        if match:
            major = int(match.group(1))
            minor = patch = pretest = 0
            if match.group(2):
                minor = int(match.group(2))
            if match.group(3):
                patch = int(match.group(3))
            if match.group(4) in ['pre','rc']:
                pre_val = -1
            else:
                pre_val = -2
            if match.group(4):
                pretest = int(match.group(5))
            self.sort_key = major, minor, patch, pre_val, pretest
            return self.sort_key
        match = re.match(
            r'([0-9]+)\.([0-9]+)\.([0-9]+)\.([0-9.]+)$', self.name)
        if match:
            major = int(match.group(1))
            minor = int(match.group(2))
            patch = int(match.group(3))
            pretest = map(int, match.group(4).split("."))
            self.sort_key = major, minor, patch, 0, pretest
            return self.sort_key
        match = re.match(
            r'([0-9]{4})-([0-9]{2})-([0-9]{2})$', self.name)
        if match:  # Fake something
            major = int(match.group(1))
            minor = int(match.group(2))
            patch = int(match.group(3))
            self.sort_key = major, minor, patch, 0, 0
            return self.sort_key
        assert 0, 'Unrecognised version: %s' % repr(self.name)

    def __str__(self):
        return self.name


def charset(name):
    if name:
        return Charset(name)
    return None

class Charset:

    def __init__(self, name):
        self.name = name

    def __cmp__(self, other):
        return cmp(self.name, other.name)

def archive_path(d, v, t):
    h = Hints(None)
    h.domain = domain(d)
    h.team = team(t)
    h.version = version(v)
    return h.archive_path()

def compare_files(file1, file2):
    if os.path.isfile(file1) and os.path.isfile(file2):
        return open(file1).read() == open(file2).read()
    return 0


if __name__ == '__main__':
    langs = {}
    for t in team_list():
        print
        print 'msgid "%s"' % t.language
        print 'msgstr ""'
        langs[t.language] = 1
