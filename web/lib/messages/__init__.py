import gettext
import os
import textwrap
import sys

catalogs = {}
dir = os.path.dirname(__file__)

sys.path.append(os.path.normpath(os.path.join(dir, "../../../python")))
try:
    import cjkcodecs.aliases
except ImportError:
    pass

for f in os.listdir(dir):
    base, ext = os.path.splitext(f)
    if ext == '.mo':
        catalogs[base] = gettext.GNUTranslations(open(os.path.join(dir, f)))

languages = catalogs.keys()

def fill_paras(text):
    res = []
    cur_para = []
    for l in text.splitlines():
        l1 = l.rstrip()
        if l1.startswith('>'):
            res.append(textwrap.fill("".join(cur_para)))
            res.append(l1 + "\n")
        elif l1 == "":
            res.append(textwrap.fill("".join(cur_para)))
            cur_para = []
            res.append("\n\n")
        else:
            cur_para.append(l+"\n")
    res.append(textwrap.fill("".join(cur_para)))
    return "".join(res)

def _get_param(p, L = None):
    if isinstance(p, MultiString):
        return p.get(L)
    return p
    
class MultiString:
    def __init__(self, data = None):
        self.trans = {}
        if data is not None:
            self.data = data
            for k,v in catalogs.items():
                self.trans[k] = v.ugettext(data)

    def __str__(self):
        return self.data

    def __repr__(self):
        return repr(self.data)

    def __add__(self, m):
        if isinstance(m, MultiString):
            res = MultiString()
            res.data = self.data + m.data
            for L in languages:
                res.trans[L] = self.get(L) + m.get(L)
            return res
        return self + MultiString(m)

    def __radd__(self, m):
        return MultiString(m)+self

    def __mod__(self, params):
        res = MultiString()
        try:
            res.data = self.data % utf8tuple(params)
        except Exception, e:
            if len(e.args) == 1:
                raise e.__class__, e.args[0] + repr(self.data)+repr(utf8tuple(params))
            raise
        for L in languages:
            if isinstance(params, tuple):
                p1 = tuple([_get_param(p, L) for p in params])
            else:
                p1 = _get_param(params, L)
            try:
                res.trans[L] = self.get(L) % p1
            except UnicodeError, e:
                raise UnicodeError("%s [%s,%s,%s]" % (str(e), L, repr(self.get(L)), p1))
        return res

    def join(self, items):
        res = MultiString()
        res.data = self.data.join([_get_param(x) for x in items])
        for L in languages:
            try:
                res.trans[L] = self.get(L).join([_get_param(x, L) for x in items])
            except UnicodeError:
		# Not joinable in L, just rely on .data instead
		pass
        return res

    def get(self, L = None):
        if L is None: return self.data
        return self.trans.get(L, self.data)

    def translate(self, lang, encoding = None, do_Q=False):
        if lang == 'en':
            return self.data
        res = self.get(lang)
        if isinstance(res, unicode):
            if encoding is None:
                import registry
                try:
                    encoding = registry.team(lang).charset
                except KeyError:
                    encoding = 'utf-8'
                if encoding is None:
                    encoding = 'iso-8859-1'
            try:
                res = res.encode(encoding)
            except (KeyError, UnicodeError):
                encoding="utf-8"
                res = res.encode('utf-8')
        if do_Q and encoding:
            # Do quoted printable encoding.
            from email.Charset import Charset
            charset = Charset(encoding)
            lines = res.split('\n')
            for i in range(len(lines)):
                l = lines[i]
                try:
                    l.decode("us-ascii")
                except UnicodeError:
                    pass
                else:
                    continue
                f,b = l.split(": ",1) # RFC822 field and body
                lines[i] = f+": "+charset.header_encode(b)
            res = "\n".join(lines)
        return res

    def refill(self):
        res = MultiString()
        res.data = fill_paras(self.data)
        for k, v in self.trans.items():
            res.trans[k] = fill_paras(v)
        return res

def translate(txt, lang, encoding = None, do_Q=False):
    if isinstance(txt, MultiString):
        return txt.translate(lang, encoding, do_Q)
    return txt

def refill(text):
    if isinstance(text, MultiString):
        return text.refill()
    return fill_paras(text)

def utf8tuple(l):
    if not isinstance(l, tuple): l = (l,)
    r = []
    for x in l:
        if isinstance(x, MultiString):
            r.append(x.data)
        elif isinstance(x, unicode):
            r.append(x.encode('utf-8'))
        else:
            r.append(x)
    return tuple(r)
