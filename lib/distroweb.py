# Web generation services for distribution files.
# Copyright © 2000 Progiciels Bourbeau-Pinard inc.
# François Pinard <pinard@iro.umontreal.ca>, 2000.

import os, string, sys
import config, htmlpage

def _(text):
    return text

def display_file_list(output=None):
    DisplayFileList(output)

def display_file(input, raw=0, output=None):
    if os.path.isdir(input):
        DisplayFileList(output, subset=input)
    elif raw:
        if output:
            write = open(output, 'w').write
        else:
            write = sys.stdout.write
        write('Content-Type: text/plain\n\n')
        write(open(input).read())
    else:
        base = os.path.split(input)[1]
        extension = os.path.splitext(base)[1]
        if extension == '.cgi':
            language = 'python'
        else:
            language = None
        DisplayFile(input, output, language)

# Generation of a Web pages listing all existing folders.

class DisplayFileList(htmlpage.Htmlpage):

    def __init__(self, output, subset=None):
        htmlpage.Htmlpage.__init__(self, None, output)
        write = self.writer
        if not write:
            return
        files = []
        if subset:
            self.prologue("Files within %s" % subset)
            write("  <p>Here is a list of files. "
                  " Just click on the name of the file you want to see.</p>\n")
            os.path.walk(subset, self.walker, files)
        else:
            self.prologue("Distributed files for this project")
            write("  <p>Here is a list of those files which are likely going"
                  " to be included in the next packaged distribution for this"
                  " project. "
                  " Just click on the name of the file you want to see.</p>\n")
            os.path.walk('.', self.walker, files)
        write('  <ol>\n')
        previous = None
        for directories, base in files:
            if directories != previous:
                if directories is not None:
                    write('    <hr>\n')
                previous = directories
            name = string.join(directories + [base], '/')
            write('   <li><a href="%s/distro.cgi?file=%s">%s</a>\n'
                  % (config.cgi_base, name, name))
        write('  </ol>\n')
        self.epilogue()

    def walker(self, files, directory, bases):
        directories = string.split(directory, '/')
        bases.sort()
        for base in bases:
            if base[-1] != '~':
                if os.path.isfile(os.path.join(directory, base)):
                    if directories[0] == '.':
                        files.append((directories[1:], base))
                    else:
                        files.append((directories, base))

# Display a selected file.

class DisplayFile(htmlpage.Htmlpage):

    def __init__(self, input, output, language):
        htmlpage.Htmlpage.__init__(self, None, output)
        write = self.writer
        if not write:
            return
        self.name = input
        # Use `enscript' to produce highlighting HTML.
        lines = os.popen('enscript -p- -Whtml -G -E%s %s'
                         % (language or '', input)).readlines()
        start = 1
        while start <= len(lines) and lines[start-1] != '<PRE>\n':
            start = start + 1
        end = len(lines) - 1
        while end >= start and lines[end] != '</PRE>\n':
            end = end - 1
        # Nest lines[start:end] within our HTML layout.
        self.prologue(input)
        write('<pre>\n')
        while start < end:
            write(lines[start])
            start = start + 1
        write('</pre>\n')
        self.epilogue()

    def html_buttons(self):
        return ('  <p>Display a'
                ' <a href="%s/distro.cgi?file=%s&raw=1">raw copy</a>,'
                ' or go back to the'
                ' <a href="%s/distro.cgi">list of files</a>.</p>'
                % (config.cgi_base, self.name, config.cgi_base))
