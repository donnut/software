# Babyl specific Web generation services.
# Copyright © 2000 Progiciels Bourbeau-Pinard inc.
# François Pinard <pinard@iro.umontreal.ca>, 2000.

import mimify, os, string, sys
import config, htmlpage

def _(text):
    return text

# Generation of a Web pages listing all existing folders.

def display_folders(directories, output=None):
    DisplayFolders(directories, output)

class DisplayFolders(htmlpage.Htmlpage):

    def __init__(self, directories, output):
        htmlpage.Htmlpage.__init__(self, None, output)
        write = self.writer
        if not write:
            return
        self.prologue("Existing folders for this project")
        write("  <p>Here is a comprehensive list of nearly all administrative"
              " folders which are kept with this project.  You may click\n"
              " on the folder line for which you want more details.\n"
              " Messages are saved according to the needs of the project\n"
              " maintainer.  This is no kind of mailing list archive, as\n"
              " messages may be deleted, edited or sorted at any time.</p>\n")
        folders = []
        for directory in directories:
            os.path.walk(directory, self.walker, folders)
        write('  <ol>\n')
        previous = None
        for directories, base in folders:
            if directories != previous:
                if directories is not None:
                    write('    <hr>\n')
                previous = directories
            name = '%s/%s' % (string.join(directories, '/'), base)
            write('   <li><a href="%s/babyl.cgi?folder=%s">%s</a>\n'
                  % (config.cgi_base, name, name))
        write('  </ol>\n')
        self.epilogue()

    def walker(self, folders, directory, bases):
        directories = string.split(directory, '/')
        all = 'rmail' in directories
        bases.sort()
        for base in bases:
            if base[-1] != '~' and (all or string.find(base, 'RMAIL') >= 0):
                name = os.path.join(directory, base)
                if os.path.isfile(name):
                    if directories[0] == '.':
                        folders.append((directories[1:], base))
                    else:
                        folders.append((directories, base))

# Study of a single Babyl folder and generation of a message summary.

def display_summary(folder, output=None):
    DisplaySummary(folder, output)

class DisplaySummary(htmlpage.Htmlpage):

    def __init__(self, folder, output):
        htmlpage.Htmlpage.__init__(self, None, output)
        write = self.writer
        if not write:
            return
        self.folder = folder
        messages = babyl_split(folder)
        if messages:
            self.first = 1
            self.last = len(messages)
        else:
            self.first = self.last = None
        self.prologue("%s (index)" % folder)
        write('  <p>\n'
              "   Here is a summary of the contents of the <code>%s</code>\n"
              "   folder.  Click on any subject to see the full message.\n"
              '  </p>\n'
              % folder)
        counter = 0
        write('  <table align=center border=2>\n'
              '   <tr align=left>\n'
              '    <th align=center>No.</th>\n'
              '    <th align=center>From</th>\n'
              '    <th align=center>Subject</th>\n'
              '   </tr>\n')
        for message in messages:
            counter = counter + 1
            name, email = message.getaddr('From')
            if name:
                name = mimify.mime_decode_header(name)
            else:
                name = email
            subject = message.getheader('Subject')
            if subject:
                subject = mimify.mime_decode_header(subject)
            else:
                subject = '(Subject not given)'
            write('   <tr>\n'
                  '    <td align=center>%d</td>\n'
                  '    <td><a href="mailto:%s">%s</a></td>\n'
                  '    <td><a href="%s/babyl.cgi?folder=%s&ordinal=%d/%d">%s</a></td>\n'
                  '   </tr>\n'
                  % (counter, email, name[:20],
                     config.cgi_base, folder, counter, len(messages), subject))
        write('  </table>\n')
        self.epilogue()

    def html_buttons(self):
        fragments = []
        write = fragments.append
        write("  <p>Go to")
        listed = 0
        if self.first:
            write(' <a href="%s/babyl.cgi?folder=%s&ordinal=%d/%d">first</a>'
                  " message"
                  % (config.cgi_base, self.folder, self.first, self.last))
            listed = 1
        if self.last:
            if listed:
                write(',')
            write(' <a href="%s/babyl.cgi?folder=%s&ordinal=%d/%d">last</a>'
                  " message"
                  % (config.cgi_base, self.folder, self.last, self.last))
            listed = 1
        if listed:
            write (' or')
        write(' list of <a href="%s/babyl.cgi">folders.</a></p>\n'
              % config.cgi_base)
        return string.join(fragments, '')

# Display a selected message from within a folder.

def display_message(folder, ordinal, maximum=None, output=None):
    DisplayMessage(folder, ordinal, maximum, output)

class DisplayMessage(htmlpage.Htmlpage):

    def __init__(self, folder, ordinal, maximum, output):
        htmlpage.Htmlpage.__init__(self, None, output)
        write = self.writer
        if not write:
            return
        self.folder = folder
        self.maximum = maximum
        if ordinal == 1:
            self.previous = None
        else:
            self.previous = ordinal - 1
        if maximum:
            message = babyl_split(folder, [ordinal])[0]
            if ordinal == maximum:
                self.next = None
            else:
                self.next = ordinal + 1
            self.prologue('%s (%d/%d)' % (folder, ordinal, maximum))
        else:
            messages = babyl_split(folder, [ordinal, ordinal+1])
            message = messages[0]
            if len(messages) == 1:
                self.next = None
            else:
                self.next = ordinal + 1
            self.prologue('%s (%d)' % (folder, ordinal))
        write('  <table align=center border=0>\n')
        for field in 'Date', 'From', 'Subject', 'To', 'Cc':
            value = message.getheader(field)
            if value:
                write('   <tr>\n'
                      '    <td><strong>%s: </strong></td>\n'
                      '    <td>%s</td>\n'
                      '   </tr>\n'
                      % (htmlpage.enhance(field),
                         htmlpage.enhance(mimify.mime_decode_header(value))))
        write('  </table>\n'
              '  <hr>\n'
              '<pre>\n')
        write(htmlpage.enhance(message.fp.read(), 1))
        write('</pre>\n')
        self.epilogue()

    def html_buttons(self):
        fragments = []
        write = fragments.append
        write("  <p>Go to")
        listed = 0
        if self.next:
            if self.maximum:
                write(' <a href="%s/babyl.cgi?folder=%s&ordinal=%d/%d">next</a>'
                      " message"
                      % (config.cgi_base, self.folder, self.next,
                         self.maximum))
            else:
                write(' <a href="%s/babyl.cgi?folder=%s&ordinal=%d">next</a>'
                      " message"
                      % (config.cgi_base, self.folder, self.next))
            listed = 1
        if self.previous:
            if listed:
                write(',')
            if self.maximum:
                write(' <a href="%s/babyl.cgi?folder=%s&ordinal=%d/%d">previous</a>'
                      " message"
                      % (config.cgi_base, self.folder, self.previous,
                         self.maximum))
            else:
                write(' <a href="%s/babyl.cgi?folder=%s&ordinal=%d">previous</a>'
                      " message"
                      % (config.cgi_base, self.folder, self.previous))
            listed = 1
        if listed:
            write(',')
        write(' this folder <a href="%s/babyl.cgi?folder=%s">summary</a>'
              % (config.cgi_base, self.folder))
        write(' or list of <a href="%s/babyl.cgi">all folders.</a></p>\n'
              % config.cgi_base)
        return string.join(fragments, '')

# Web-indepedent Babyl file processing.

def babyl_split(folder, selection=None):
    """\
Read in a Babyl file and return a list of message buffers.
If SELECTION is None, all messages are read.  Otherwise, SELECTION is
a list of message ordinals (counting from one), and only those are read.
If an ordinal refers to an unexisting message, it is ignored.
"""
    import rfc822
    buffer = open(folder).read()
    assert string_begins(buffer, 'BABYL OPTIONS:')
    assert string_ends(buffer, '\037')
    messages = []
    end = string.find(buffer, '\037\014')
    if end < 0:
        loop = 0
    elif selection is None:
        loop = 1
    else:
        selection = selection[:]
        loop = len(selection) > 0
    counter = 0
    while loop:
        counter = counter + 1
        start = end + 2
        end = string.find(buffer, '\037\014', start)
        if end < 0:
            end = len(buffer)-1
            loop = 0
        if selection is not None:
            if counter in selection:
                selection.remove(counter)
                if len(selection) == 0:
                    loop = 0
            else:
                continue
        eooh = string.find(buffer, '*** EOOH ***\n', start, end)
        messages.append(rfc822.Message(MessageBuffer(
            buffer, eooh+len('*** EOOH ***\n'), end)))
    return messages

class MessageBuffer:

    def __init__(self, buffer, start, limit):
        self.buffer = buffer
        self.start = start
        self.limit = limit
        self.position = start

    def size(self):
        return self.limit - self.start

    def rewind(self):
        self.position = self.start

    def tell(self):
        return self.position

    def seek(self, position, relative=0):
        if relative == 0:
            self.position = position
        elif relative == 1:
            self.position = self.position + position
        elif relative == 2:
            self.position = self.limit + position

    def read(self):
        buffer = self.buffer[self.position:self.limit]
        self.position = self.limit
        return buffer

    def readline(self):
        position = string.find(self.buffer, '\n', self.position, self.limit)
        if position >= 0:
            line = self.buffer[self.position:position+1]
            self.position = position+1
            return line
        return self.read()

    def readlines(self):
        lines = []
        line = self.readline()
        while line:
            lines.append(line)
            line = self.readline()
        return lines

def string_begins(buffer, text):
    return buffer[:len(text)] == text

def string_ends(buffer, text):
    return buffer[-len(text):] == text
