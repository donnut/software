#!/usr/bin/env python

import sys, os, urllib, gzip, stat, errno, string, time

urlprefix = "http://www.translationproject.org/self/"

def mkdir(p):
    try:
        os.mkdir(p)
    except OSError, e:
        if e.errno == errno.EEXIST:
            return
        if e.errno == errno.ENOENT:
            d, f = os.path.split(p)
            mkdir(d)
            os.mkdir(p)
            return
        raise

if len(sys.argv) != 2:
    print "Usage: mirror_tp.py destdir"
    raise SystemExit

prefix = sys.argv[1]
os.chdir(prefix)

mkdir("mail")
mkdir("tmp")

mkdir("mirror")
for i in range(5):
    sock = urllib.urlretrieve(urlprefix + "mirror/INDEX.gz","mirror/INDEX.gz")
    try:
        data = string.split(gzip.GzipFile("mirror/INDEX.gz").read(), '\n')
        if data[-1]=="END":
            del data[-1]
            break
    except IOError:
        pass
    time.sleep(10)
else:
    # otherwise, it is an incomplete file
    raise SystemExit

for line in data:
    time, name = string.split(line, ' ', 1)
    type = 'file'
    time = string.atoi(time, 16)
    if name[:5] == 'link ':
        try:
            type, name, dest = string.split(name, ' ')
        except ValueError:
            # file name with spaces, ignore
            print 'Splitting',name,'failed'
            continue
    try:
        st = os.lstat(name)
    except OSError:
        pass
    else:
        if st[stat.ST_MTIME] == time:
            continue
    dir, file = os.path.split(name)
    if dir:
        mkdir(dir)
    if type == 'link':
        try:
            os.remove(name)
        except OSError:
            os.symlink(dest, name)
        continue
    print "retrieving %s" % (name)
    urllib.urlretrieve(urlprefix+name, name)
    os.utime(name, (time,time))

