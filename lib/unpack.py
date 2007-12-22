# Unpacking messages sent to the Translation Project.
# -*- mode: python; coding: utf-8 -*-
# Copyright © 2003, 2007 Translation Project
# Copyright © 1999, 2000 Progiciels Bourbeau-Pinard inc.
# François Pinard <pinard@iro.umontreal.ca>, 1998.

import mimetools, multifile, os, re, string, tempfile
import quopri, base64, cStringIO, gzip, popen2, binascii

def _(text):
    return text

def unpack_file(name):
    import run
    unpacked = UnpackedFile(name, run.submitter.write_nofill, run.reject)
    return unpacked.parts

def base64_decode(input, output):
    """Decode a file."""
    # binascii of Python 2.2.2 has a bug which causes an empty crlf
    # line to decode as content. Work around this by duplicating
    # base64.decode.
    while 1:
        line = input.readline().rstrip() # added rstrip
        if not line: break
        s = binascii.a2b_base64(line)
        output.write(s)

class UnpackedFile:

    def __init__(self, name, write_warning, write_fatal):
        self.parts = []
        self.write_warning = write_warning
        self.write_fatal = write_fatal
        if type(name) is type(''):
            self.simple_unpack(open(name), name, ())
        else:
            self.mime_unpack(multifile.MultiFile(name), ())

    def simple_unpack(self, input, name, stack):
        lines = input.readlines()
        # Replace any DOS end-of-line.
        for start in range(len(lines)):
            if lines[start][-2:] == '\r\n':
                lines[start] = lines[start][:-2] + '\n'
        # Remove prefix and suffix white lines.  If nothing remains,
        # we have an empty part.
        while lines and string.strip(lines[-1]) == '':
            del lines[-1]
        while lines and string.strip(lines[0]) == '':
            del lines[0]
        if not lines:
            self.parts.append(MessagePart(None, None, stack))
            return
        # Prepare to recognise uuencoded data.
        uu_pattern = re.compile('begin(-base64)? [0-7]+ [^ ]*?([^ /\n]+)$')
        terminator = None
        # Find where the data starts.
        start = 0
        while start < len(lines):
            match = uu_pattern.match(lines[start])
            if match:
                if match.group(1):
                    terminator = '====\n'
                else:
                    terminator = 'end\n'
                break
            if lines[start][:6] == 'msgid ':
                while start > 0 and lines[start-1][0] in '#\n':
                    start = start - 1
                while lines[start][0] == '\n':
                    start = start + 1
                break
            start = start + 1
        # Find where the data ends.
        end = len(lines)
        while end > start:
            if lines[end-1] == terminator:
                break
            if lines[end-1][:6] == 'msgstr':
                while end < len(lines) and lines[end][0] in '"#\n':
                    end = end + 1
                while lines[end-1][0] == '\n':
                    end = end - 1
                break
            end = end - 1
        # Diagnose spurious lines.  If contents erroneous or empty,
        # we still have an empty part.
#        if start > 0:
#            self.write_warning(_("""\
#I'm ignoring the following leading lines within your message:
#
#--------------------------------------------------------------->
#%s
#---------------------------------------------------------------<
#""")
#                                  % string.join(lines[:start], ''))
#        if end < len(lines):
#            self.write_warning(_("""\
#I'm ignoring the following final lines within your message:
#
#--------------------------------------------------------------->
#%s
#---------------------------------------------------------------<
#""")
#                                  % string.join(lines[end:], ''))
        if terminator and lines[end-1] != terminator:
            self.write_fatal(_("""\
Your message seems to use the 'uuencode' format, yet no proper terminator
was found to end the encoded region.
"""))
            self.parts.append(MessagePart(None, None, stack))
            return
        if start == end:
            self.parts.append(MessagePart(None, None, stack))
            return
        # Prepare a work file that will uudecode to the proper location.
        work = tempfile.mktemp()
        if match:
            # FIXME: match.group(2) should be validated against `name',
            # or maybe used to provide more hints.
            name = match.group(2)
            output = os.popen('uudecode', 'w')
            output.write('begin%s 600 %s\n' % (match.group(1) or '', work))
            start = start + 1
        else:
            output = open(work, 'w')
        output.writelines(lines[start:end])
        output.close()
        self.parts.append(MessagePart(name, work, stack))

    def mime_unpack(self, input, stack):
        entity = mimetools.Message(input)
        stack = (entity,) + stack
        if entity.getmaintype() == 'multipart':
            self.parts.append(MessagePart(None, None, stack))
            boundary = entity.getparam('boundary')
            if boundary:
                input.push(boundary)
                while input.next():
                    self.mime_unpack(input, stack)
                input.pop()
        elif entity.gettype() == 'message/rfc822':
            self.parts.append(MessagePart(None, None, stack))
            self.mime_unpack(input, stack)
        else:
            name = get_filename(entity)
            work = tempfile.mktemp()
            cte = entity.getencoding()
            if cte == 'quoted-printable':
                output = cStringIO.StringIO()
                quopri.decode(input, output)
            elif cte == 'base64':
                output = cStringIO.StringIO()
                base64_decode(input, output)
            else:
                output = None
            if output:
                output.reset()
                if entity.gettype() == "application/x-gzip" or \
                       (name and name.endswith(".gz")):
                    work2 = tempfile.mktemp()
                    tmp2 = open(work2+".gz", "w")
                    tmp2.write(output.read())
                    tmp2.close()
                    inst = popen2.Popen4("gunzip %s.gz" % work2)
                    data = inst.fromchild.read()
                    if inst.wait() != 0:
                        self.write_fatal(_("Uncompressing your submission with gzip has failed. gzip said:\n%s\n") % data)
                        try:
                            os.unlink(work2+".gz")
                        except OSError:
                            pass
                        return
                    output=open(work2)
                    os.unlink(work2)
                    if name and name.endswith(".gz"):
                        name=name[:-3]
                tmp = open(work,"w")
                tmp.write(output.read())
                tmp.close()
                del output
                self.simple_unpack(open(work), name, stack)
                os.remove(work)
            else:
                self.simple_unpack(input, name, stack)

def get_filename(entity):
    text = entity.getheader('content-disposition')
    if text:
        match = re.search('filename=([^ \t\n]+)', text)
        if match:
            import rfc822
            return rfc822.unquote(match.group(1))
    return entity.getparam('name')

class MessagePart:

    def __init__(self, name, work, stack):
        if name and name[-3:] == '.gz':
            self.name = name[:-3]
            self.work = tempfile.mktemp()
            os.system('gzip -dc %s > %s' % (work, self.work))
            os.remove(work)
        else:
            self.name = name
            self.work = work
        self.stack = stack

    def __del__(self):
        if self.work:
            try:
                os.remove(self.work)
            except os.error:
                pass

    def __str__(self):
        return 'MessagePart(%s, %s, %s)' % (self.name, self.work, self.stack)

    def value(self, header):
        for level in self.stack:
            if level.has_key(header):
                return level[header]

    def size(self):
        if self.work:
            try:
                return os.path.getsize(self.work)
            except:
                # `os.path.getsize' does not exist for Python 1.5.1.
                import stat
                return os.stat(self.work)[stat.ST_SIZE]
        return 0

def test():
    global unpacker
    try:
        del unpacker
    except:
        pass
    unpacker = unpack_file(open('/tmp/message2'))
