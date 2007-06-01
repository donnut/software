#!/usr/bin/env python

import os, sys, stat, cStringIO, gzip, time, socket

sys.path.insert(0, sys.path[0]+'/../lib')
import config

starttime = time.time()
prefix = config.home_path
plen = len(prefix)

listing = []

def walker(arg, dir, files):
    newfiles = []
    for f in files:
        # Skip files that should not get mirrored
        if f == ".svn":
            continue
        if f[-1] == '~':
            continue
        if f[-3:] == "pyc":
            continue
        newfiles.append(f)
        p = os.path.join(dir, f)
        st = os.lstat(p)
        if stat.S_ISDIR(st[stat.ST_MODE]):
            continue
        if stat.S_ISLNK(st[stat.ST_MODE]):
            dest = os.readlink(p)
            listing.append((st[stat.ST_MTIME], 'link', p[plen+1:], dest))
            continue
        listing.append((st[stat.ST_MTIME], p[plen+1:]))
    files[:] = newfiles

# Program files:
os.path.walk(prefix+"/progs", walker, None)
# Cache:
os.path.walk(prefix+"/cache", walker, None)
# Data files:
os.path.walk(prefix+"/site", walker, None)

outfile=cStringIO.StringIO()
for entry in listing:
    if len(entry) == 2:
        outfile.write("%.8x %s\n" % entry)
    else:
        outfile.write("%.8x %s %s %s\n" % entry)
outfile.write("END")
data=outfile.getvalue()
outfile = open(prefix+"/mirror/INDEX","w")
outfile.write(data)
outfile.close()
os.chdir(prefix+"/mirror")
try:
    os.unlink("INDEX.gz")
except OSError:
    pass
f=gzip.open("INDEX.gz", "w")
f.write(open("INDEX").read())
try:
   f.close()
except:
   print >>sys.stderr, "Start time:", time.asctime(time.localtime(starttime))
   print >>sys.stderr, "Current time:", time.asctime(time.localtime(time.time()))
   print >>sys.stderr, "Directory contents", "\n".join(os.listdir("."))
   raise
os.unlink("INDEX")

