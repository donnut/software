# HTML related routines.
# -*- mode: python; coding: utf-8 -*-
# Copyright © 2007 Translation Project.
# Copyright © 2000 Progiciels Bourbeau-Pinard inc.
# François Pinard <pinard@iro.umontreal.ca>, 2000.

import commands, os, re, stat, string, sys


# Generic file transformations.

def transform_generic(input, html_dir=None):
    # If HTML_DIR is not given, results to standard output.
    if os.path.isdir(input):
        # When a directory, process the interesting files it contains.
        names = os.listdir(input)
        names.sort()
        for name in names:
            if name in ('NEWS', 'README', 'THANKS', 'TODO'):
                transform_generic('%s/%s' % (input, name), html_dir)
            else:
                base, extension = os.path.splitext(name)
                if extension in ('.all', '.html'):
                    transform_generic('%s/%s' % (input, name), html_dir)
        return
    directory, filename = os.path.split(input)
    if filename == 'AUTHORS':
        transform_authors(input, html_dir and '%s/authors.html' % html_dir,
                           'Who have signed a disclaimer')
    elif filename == 'NEWS':
        transform_verbatim(input, html_dir and '%s/news.html' % html_dir,
                           'NEWS - History of user-visible changes')
    elif filename == 'README':
        transform_allout(input, html_dir and '%s/readme.html' % html_dir,
                         'README - Introductory notes')
    elif filename == 'THANKS':
        transform_thanks(input, html_dir and '%s/thanks.html' % html_dir,
                         'THANKS - People who have contributed')
    elif filename == 'TODO':
        transform_verbatim(input, html_dir and '%s/todo.html' % html_dir,
                           'TODO - Things still to be done')
    else:
        base, extension = os.path.splitext(filename)
        output = html_dir and '%s/%s.html' % (html_dir, base)
        if extension == '.all':
            transform_allout(input, output, None)
        elif extension == '.html':
            transform_html(input, output, None)
        else:
            transform_verbatim(input, output,
                               'The %s file' % string.upper(filename))


# Configuration and layout of generated HTML pages.

class Htmlpage:

    def __init__(self, input, output):
        self.init_configuration()
        self.init_writer(input, output)
        self.init_layout()

    def init_configuration(self):
        self.configuration = {
            'page_title': '(Title not set)',
            'time_stamp': commands.getoutput('date "+%Y-%m-%d %H:%M %z"')}
        try:
            import config
            for key, value in config.environ.items():
                self.configuration[key] = value
        except ImportError:
            pass

    def init_writer(self, input, output):
        if not output:
            self.cgi = 1
            self.writer = sys.stdout.write
            return
        if input and os.path.exists(output):
            input_time = os.stat(input)[stat.ST_MTIME]
            output_time = os.stat(output)[stat.ST_MTIME]
            if input_time <= output_time:
                layout = self.configuration.get('html_layout_file')
                if layout:
                    layout_time = os.stat(layout)[stat.ST_MTIME]
                    if layout_time <= output_time:
                        self.writer = None
                        return
                else:
                    self.writer = None
                    return
        self.cgi = 0
        self.writer = open(output, 'w').write

    def init_layout(self):
        layout = self.configuration.get('html_layout_file')
        if layout:
            layout_text = open(layout).read()
        else:
            layout_text = self.default_layout()
        self.layout_start, self.layout_end = string.split(layout_text,
                                                          'INSERTION_POINT\n')

    def default_layout(self):
        return '''\
<!doctype HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html>
 <head><title>%(page_title)s</title></head>
 <body>
INSERTION_POINT
  <p><font size="-1">Last recomputed on %(time_stamp)s</font></p>
 </body>
</html>
'''

    def prologue(self, title, charset=None):
        write = self.writer
        if self.cgi:
            if charset:
                write('Content-Type: text/html; charset=%s\n\n' % charset)
            else:
                write('Content-Type: text/html\n\n')
        self.configuration['page_title'] = title % self.configuration
        text = self.layout_start % self.configuration
        if self.cgi or not charset:
            write(text)
        else:
            position = string.find(text, '<head')
            if position < 0:
                position = string.find(text, '<HEAD')
            assert position >= 0
            position = string.find(text, '>', position+5)
            assert position >= 0
            position = position + 1
            write(text[:position])
            write('\n  <meta http-equiv="Content-Type"'
                  ' content="text/html; charset=%s">'
                  % charset)
            write(text[position:])
        write('      <h1>%(page_title)s</h1>\n' % self.configuration)
        line = self.html_buttons()
        if line:
            write(line)
            write('      <hr>\n')

    def epilogue(self):
        write = self.writer
        line = self.html_buttons()
        if line:
            write('      <hr>\n')
            write(line)
        write(self.layout_end % self.configuration)

    def writelines(self, lines):
        write = self.writer
        for line in lines:
            if string.find(line, '%(') >= 0:
                try:
                    write(line % self.configuration)
                except KeyError:
                    write(line)
            else:
                write(line)

    def html_buttons(self):
        return None


# Transform a page, taken almost verbatim, into HTML.

def transform_verbatim(input, output=None, title=None):
    Verbatim(input, output, title)

class Verbatim(Htmlpage):

    def __init__(self, input, output, title):
        Htmlpage.__init__(self, input, output)
        write = self.writer
        if not write:
            return
        lines = open(input).readlines()
        self.prologue(title or self.find_title(lines), charset="utf-8")
        write('<pre>\n')
        for line in lines:
            write(enhance(line, 1))
        write('</pre>\n')
        self.epilogue()

    def find_title(self, lines):
        title = Allout.find_title(self, lines)
        if not title and lines and lines[0]:
            title = string.strip(lines[0])
        return title


# Transform the AUTHORS file into a simple HTML table.

def transform_authors(input, output=None, title=None):
    Authors(input, output, title)

class Authors(Htmlpage):

    def __init__(self, input, output, title):
        Htmlpage.__init__(self, input, output)
        write = self.writer
        if not write:
            return
        lines = open(input).readlines()
        self.prologue(title, charset="utf-8")
        write('<table>\n')
        write('<b><th align="left">Author<th>Signed<th>Language</b>\n')
        tack = False
        for line in lines:
            if line[:12] == "TRANSLATIONS":
                name = " ".join(line.split()[1:-1])
                date = line.split()[-1]
                write('<tr><td>%s<td>%s' % (name, date))
                tack = True
            elif tack:
                tack = False
                if name == "Ingenieurburo":
                    write('<td></tr>\n')
                    continue
                team = line.split("[")[1].split("]")[0]
                write('<td align="center">%s</tr>\n' % team)
        write('</table>\n')
        self.epilogue()


# Transform an `allout' outline file into HTML.

def transform_allout(input, output=None, title=None):
    Allout(input, output, title)

class Allout(Htmlpage):

    def __init__(self, input, output, title):
        Htmlpage.__init__(self, input, output)
        write = self.writer
        if not write:
            return
        lines = open(input).readlines()
        if lines and lines[0] and lines[0][0] != '*':
            abort('* line expected')
        self.prologue(title or self.find_title(lines), charset="utf-8")
        self.element = None
        self.level = -1
        self.margin = '  '
        counter = 1
        while counter < len(lines):
            line = lines[counter]
            #warning('%d<%s>%s' % (level, margin, line))
            if line[0] == '*':
                abort('Title unexpected')
            match = re.match(r'\.( *)[-*+:.,@] (.+)', line)
            if match:
                self.maybe_stop('p')
                self.maybe_stop('pre')
                self.header(len(match.group(1)), match.group(2))
                counter = counter + 1
                continue
            if line == '\n':
                self.maybe_stop('p')
                write(line)
                counter = counter + 1
                continue
            if string.find(line, '\t') >= 0:
                self.maybe_start('pre')
                if line[:1] == '\t':
                    line = line[1:]
                write(enhance(line))
                counter = counter + 1
                continue
            if line[:len(self.margin)] == self.margin:
                #warning('<%s>%d:%s' % (margin, match.end(), line))
                line = line[len(self.margin):]
            if line[-5:] == '----\n':
                counter = counter + 1
                continue
            if string.find(line, '   ') >= 0:
                self.maybe_start('pre')
            else:
                self.maybe_start('p')
            write(enhance(line))
            counter = counter + 1
        self.maybe_stop('p')
        self.maybe_stop('pre')
        while self.level >= 0:
            self.level = self.level - 1
            self.margin = ' ' * (self.level+3)
            write('%s</ol>\n' % self.margin)
        self.epilogue()

    def find_title(self, lines):
        if lines and lines[0]:
            match = re.match(r'\* (.*)', lines[0])
            if match:
                title = match.group(1)
                title = re.sub(r'-\*- .* -\*-', '', title, 1)
                title = re.sub(r'[ \t]allout', '', title, 1)
                return string.strip(title)
        return None

    def header(self, goal, title):
        write = self.writer
        while self.level < goal:
            write('%s<ol>\n' % self.margin)
            self.level = self.level + 1
            self.margin = ' ' * (self.level+3)
        while self.level > goal:
            self.level = self.level - 1
            self.margin = ' ' * (self.level+3)
            write('%s</ol>' % self.margin)
        write('%s<li><h%d>%s</h%d>'
              % (self.margin, self.level+2, enhance(title), self.level+2))

    def maybe_start(self, tag):
        write = self.writer
        if tag != self.element:
            if self.element:
                write('</%s>\n' % self.element)
            write('%s<%s>\n' % (self.margin, tag))
            self.element = tag

    def maybe_stop(self, tag):
        write = self.writer
        if tag == self.element:
            write('</%s>\n' % self.element)
            self.element = None


# Transform an HTML file into another.

def transform_html(input, output=None, title=None):
    Html(input, output, title)

class Html(Htmlpage):

    def __init__(self, input, output, title):
        Htmlpage.__init__(self, input, output)
        write = self.writer
        if not write:
            return
        lines = open(input).readlines()
        self.prologue(title or self.find_title(lines), charset="utf-8")
        start = 0
        while start < len(lines):
            line = lines[start]
            start = start + 1
            if string.find(line, '<body>') >= 0:
                break
            if string.find(line, '<BODY>') >= 0:
                break
        end = len(lines)
        while end > start:
            end = end - 1
            line = lines[end]
            if string.find(line, '</body>') >= 0:
                break
            if string.find(line, '</BODY>') >= 0:
                break
        self.writelines(lines[start:end])
        self.epilogue()

    def find_title(self, lines):
        title = None
        for line in lines:
            if string.find(line, '<body>') >= 0:
                break
            if string.find(line, '<BODY>') >= 0:
                break
            position = string.find(line, '<title>')
            if position >= 0:
                title = line[position+7:]
                line = ''
            position = string.find(line, '<TITLE>')
            if position >= 0:
                title = line[position+7:]
                line = ''
            if title:
                title = title + line
                position = string.find(title, '</title>')
                if position >= 0:
                    title = title[:position]
                    break
                position = string.find(title, '</TITLE>')
                if position >= 0:
                    title = title[:position]
                    break
        if title:
            return string.strip(title)
        return None


# Transform a `THANKS' file into HTML.

def transform_thanks(input, output=None, title=None):
    Thanks(input, output, title)

class Thanks(Htmlpage):

    def __init__(self, input, output, title):
        Htmlpage.__init__(self, input, output)
        write = self.writer
        if not write:
            return
        lines = open(input).readlines()
        self.prologue(title, charset="utf-8")
        # Transform the introductory paragraphs.
        within_p = 0
        counter = 0
        while counter < len(lines):
            line = lines[counter]
            if line == '\n':
                if within_p:
                    write('  </p>\n')
                    within_p = 0
                counter = counter + 1
                continue
            if re.search('\t|   ', line):
                if within_p:
                    write('  </p>\n')
                break
            if not within_p:
                write('  <p>\n')
                within_p = 1
            write('   %s' % enhance(line))
            counter = counter + 1
        # Make a table with the remainder of the file.
        if counter < len(lines):
            write('  <p> </p>\n'
                  '  <table align=center>\n'
                  '   <tr>\n'
                  '    <th>Contributor</th>\n'
                  '    <th>Email address</th>\n'
                  '   </tr>\n')
            while counter < len(lines):
                line = lines[counter]
                match = re.match('([^ \t\n][^\t\n]*)$', line)
                if match:
                    name, mailto = match.group(1), None
                else:
                    match = re.match('([^ \t\n][^\t\n]*)\t+([^ \t\n]+)$', line)
                    if match:
                        name, mailto = match.group(1, 2)
                    else:
                        warning(line)
                        counter = counter + 1
                        continue
                counter = counter + 1
                if counter == len(lines):
                    self.produce_row(name, mailto, None)
                    break
                line = lines[counter]
                match = line and re.match('[ \t]+(http:\/\/.*[^ \t\n])$', line)
                if match:
                    self.produce_row(name, mailto, match.group(1))
                    counter = counter + 1
                    continue
                self.produce_row(name, mailto, None)
            write('  </table>\n')
        self.epilogue()

    def produce_row(self, name, mailto, url):
        write = self.writer
        write('   <tr>\n')
        if url:
            write('    <td><a href="%s">%s</a></td>\n'
                  '    <td>%s</td>\n' % (url, name, mailto or ''))
        else:
            write('    <td>%s</td>\n' % name)
            if mailto:
                write('    <td><a href="mailto:%s">%s</a></td>\n'
                      % (mailto, mailto))
            else:
                write('    <td></td>\n')
        write('   </tr>\n')


# Services.

def enhance(text, verbatim=0):
    text = string.replace(text, '&', '&amp;')
    text = string.replace(text, '<', '&lt;')
    text = string.replace(text, '>', '&gt;')
    text = string.replace(text, '\f', '')
    if verbatim:
        text = re.sub(
            r'((mailto:|http://|ftp://)[-_.@~/a-zA-Z0-9]*[~/a-zA-Z0-9])',
            r'<a href="\1">\1</a>', text)
    else:
        text = re.sub(
            r'((mailto:|http://|ftp://)([-_.@~/a-zA-Z0-9]*[~/a-zA-Z0-9]))',
            r'<a href="\1">\3</a>', text)
    text = re.sub(
        (r'(^|[^-_%+./a-zA-Z0-9:])'
         r'([-_%+./a-zA-Z0-9]+@[-a-zA-Z0-9]+\.[-.a-zA-Z0-9]*[a-zA-Z0-9])'),
        r'\1<a href="mailto:\2">\2</a>', text)
    if verbatim:
        text = re.sub(
            r'_([-_@./a-zA-Z0-9]*[/a-zA-Z0-9])_', r'_<i>\1</i>_', text)
        text = re.sub(
            r'\*([-_@./a-zA-Z0-9]*[/a-zA-Z0-9])\*', r'*<b>\1</b>*', text)
        text = re.sub(
            r"`([-_@./a-zA-Z0-9]*[/a-zA-Z0-9])'", r"`<tt><b>\1</b></tt>'",
            text)
    else:
        text = re.sub(
            r'_([-_@./a-zA-Z0-9]*[/a-zA-Z0-9])_', r'<i>\1</i>', text)
        text = re.sub(
            r'\*([-_@./a-zA-Z0-9]*[/a-zA-Z0-9])\*', r'<b>\1</b>', text)
        text = re.sub(
            r"`([-_@./a-zA-Z0-9]*[/a-zA-Z0-9])'", r'<tt><b>\1</b></tt>', text)
    return text

def abort(message):
    warning(message)
    sys.exit(1)

def warning(message):
    sys.stderr.write('** %s' % message)
    if message[-1] != '\n':
        sys.stderr.write('\n')
