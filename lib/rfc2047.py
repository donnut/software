# Handling of RFC 2047 (previously RFC 1522) headers.
# Copyright © 1998, 1999, 2000 Progiciels Bourbeau-Pinard inc.
# François Pinard <pinard@iro.umontreal.ca>, 1998.

import re, string

def from_latin1(text):
    # FIXME!
    return text

def to_latin1(text):
    return _sub_f(r'=\?ISO-8859-1\?Q\?([^?]*)\?=', re.I, _replace1, text)

def _replace1(match):
    return _sub_f('=([0-9A-F][0-9A-F])', re.I, _replace2,
                  re.sub('_', ' ', match.group(1)))

def _replace2(match):
    return chr(string.atoi(match.group(1), 16))

def _sub_f(pattern, flags, function, text):
    matcher = re.compile(pattern, flags).search
    position = 0
    results = []
    while 1:
        match = matcher(text, position)
        if not match:
            results.append(text[position:])
            return string.joinfields(results, '')
        results.append(text[position:match.start(0)])
        position = match.end(0)
        results.append(function(match))
