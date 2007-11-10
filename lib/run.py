# Emailing for the Translation Project robot.
# -*- mode: python; coding: utf-8 -*-
# Copyright © 2001, 2002, 2003, 2004 Translation Project.
# Copyright © 1999, 2000 Progiciels Bourbeau-Pinard inc.
# François Pinard <pinard@iro.umontreal.ca>, 1999.

import os, sys, re, tempfile, types
import messages

def _(text):
##  return messages.MultiString(text)
    return text

# Execution variables.

dry = 0                                 # don't send mail, don't modify things
rejected = 0                            # a serious error was diagnosed

subject = _('Report from TP-Robot')     # best known subject for messages
translator_name = None                  # translator name when known
translator_address = None               # translator address when known
header_lines = []                       # header of submission message
body_lines = []                         # body of submission message
po_charset = None                       # charset in PO file

hints = None                            # domain, version, team and charset


# Mailing reports.

class Reporter:

    def __init__(self):
        self.delay = 1
        self.delayed = []
        self.lang = 'en'
        self.encoding = 'utf-8'

    def mime_header(self):
        return "MIME-Version: 1.0\n" + \
               "Content-Type: text/plain; charset=%s\n" % self.encoding + \
               "Content-Transfer-Encoding: 8bit\n"

    def prune_hibit(self, line):
        pruned = []
        for char in line:
            if ord(char) > 127:
                pruned.append("[]")
            else:
                pruned.append(char)
        return "".join(pruned)

    def prepare(self, force=0):
        if self.delay:
            reply_header = self.reply_header(force)
            if reply_header:
                if not dry:
                    self.file = os.popen('sendmail -i -t', 'w')
                else:
                    self.file = sys.stdout
                self.file.write(messages.translate(reply_header, self.lang))
                for line in self.delayed:
                    try:
                        self.file.write(messages.translate(line, self.lang,
                                                           self.encoding))
                    except UnicodeEncodeError:
                        # XXX Chapuza, to finally get to see what goes wrong.
                        self.file.write(self.prune_hibit(line))
                self.delay = 0
                self.delayed = []

    def complete(self):
        if self.delayed:
            self.prepare(force=1)
            if self.delayed:
                sys.stderr.write(
                    '================================================\n'
                    'Unable to send report.  Dumping it here instead.\n'
                    '================================================\n')
                sys.stderr.writelines(self.delayed)
        if not self.delay and not dry:
            self.file.close()

    def write_nofill(self, text):
        if self.delay:
            self.delayed.append('\n')
            self.delayed.append(text)
            self.delayed.append('\n')
        else:
            self.file.write('\n')
            try:
                self.file.write(messages.translate(text, self.lang,
                                                   self.encoding))
            except UnicodeEncodeError:
                self.file.write(self.prune_hibit(text))
            self.file.write('\n')

    def write(self, text):
        self.write_nofill(messages.refill(text))


class Coordinator(Reporter):

    def reply_header(self, force=0):
        global subject
        try:
            if hints.team:
                if hints.team.leader:
                    mailto = hints.team.leader.mailto[0]
                    subject = shorten(subject)
                else:
                    mailto = '<report@translationproject.org>'
                    subject = 'Team %s is without leader' % hints.team.name
            else:
                mailto = '<report@translationproject.org>'
                subject = 'No team determined'
        except (KeyError, TypeError, AttributeError),e:
            if not force:
                return None
            mailto = '<report@translationproject.org>'
            subject = 'reply_header(): %s' % e.__class__.__name__
        return _("""\
From: Translation Project Robot <robot@translationproject.org>
To: %s
Subject: XXX: %s
%s"""
                 % (mailto, subject, self.mime_header()))

    def complete(self):
        if rejected and not dry:
            self.prepare(force=1)
            self.file.write("\nThe rejected PO file was submitted by:\n")
            self.file.write('-' * 70 + '>\n')
            self.file.writelines(header_lines)
            self.file.write('\n')
            # The body lines may be very many, so they aren't included.
            self.file.write("[Body lines suppressed]\n")
            self.file.write('-' * 70 + '<\n')
            self.file.write(
"\nIf necessary, please help the translator to get the error fixed\n"
"and assist her to submit the fixed file again.\n"
"\nIf anything needs changing, please write to:\n"
" <coordinator@translationproject.org>\n\n")
        Reporter.complete(self)

    def write_nofill(self, text):
        Reporter.write_nofill(self, text)


class Submitter(Reporter):

    def reply_header(self, force=0):
        if header_lines:
            work = tempfile.mktemp()
            file = os.popen('formail -t -r '
'-a "From: Translation Project Robot <robot@translationproject.org>" '
'-a "BCC: robot-mail@benno.vertaalt.nl" '
'-I "Subject: %s" >%s'
                            % (subject, work), 'w')
            file.writelines(header_lines)
            file.close()
            file = open(work)
            header = file.read()
            file.close()
            header = header.splitlines()
            while header[-1] == "":
                del header[-1]
            header = "\n".join(header) + "\n" + self.mime_header() + "\n"
            os.remove(work)
        elif translator_address:
            header = (_("""\
From: Translation Project Robot <robot@translationproject.org>
To: "%s" <%s>
BCC: robot-mail@benno.vertaalt.nl
Subject: Re: %s
%s
""") % (translator_name, translator_address, subject, self.mime_header()))
        else:
            header = None

        if header:
            if hints.domain and hints.version and hints.team:
                announce = (_("""\
Hi!  I am the service robot at the Translation Project,
and was awakened by your submission of '%s'.
""") % hints.archive_base())
            else:
                announce = _("""\
Hi!  I am the service robot at the Translation Project,
and was awakened by one of your submissions.
""")
            return '%s\n%s' % (header, announce)
        return None

    def complete(self):
        if hints and hints.team:
            self.lang = hints.team.code
            if hints.team.charset:
                self.encoding = hints.team.charset
        if rejected:
            self.prepare(force=1)
            self.write(_("""\
Some error reported above (marked with "***>") prevents me from
accepting your PO file.  Sorry!  But do not hesitate to resubmit your
PO file, once you think the problem has been fixed.  As a robot I am
incredibly patient at these things!
"""))
        self.write_nofill(_("""\
                                The Translation Project robot, in the
                                name of your kind translation coordinator.
                                <coordinator@translationproject.org>
"""))
        Reporter.complete(self)


coordinator = Coordinator()
submitter = Submitter()

def reject_nofill(text, reason = ""):
    global rejected, subject

    if not rejected:
        subject = 'TP: %s [REJECTED]: %s' % (shorten(subject), reason[1:-1])
    rejected = 1
    if not dry:
        coordinator.write_nofill(text)
    submitter.write_nofill('***> %s' % text)

def reject(text, reason = ""):
    global rejected, subject

    if not rejected:
        subject = 'TP: %s [REJECTED]: %s' % (shorten(subject), reason[1:-1])
    rejected = 1
    if not dry:
        coordinator.write(text)
    submitter.write('***> %s' % text)

def shorten(subject):
    match = re.match('( *)([Tt][Pp][-_ ][Rr]obot)( *)(.*)', subject)
    if match:
        return match.group(4)
    else:
        return subject

def refill(text):
    work = tempfile.mktemp()
    file = os.popen('fmt >%s' % work, 'w')
    try:
        file.write(text)
    except UnicodeError:
        file.write(text.encode("utf-8"))
    file.close()
    file = open(work)
    text = file.read()
    file.close()
    os.remove(work)
    return text

def encode(msg):
    if hints and hints.team:
        return hints.team.encode(msg)
    if isinstance(msg, types.UnicodeType):
        return msg.encode("utf-8")
    return msg
