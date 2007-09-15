#!/usr/bin/env python
# Copyright © 2007 Translation Project.
# Benno Schulenberg <benno@vertaalt.nl>, 2007.

# Digest translation disclaimers and output these in sorted order.

import sys

try:
    file = open(sys.argv[2], 'r')
    text = file.readlines()
    file.close()
except:
    print "Usage:  process-disclaimers  -r|-s  filename"
    sys.exit(1)

if sys.argv[1] == "-r":
    way = "recreate"
else:
    way = "sortbyteam"


def nextline():
    global index, line
    index += 1
    line = text[index -1 ]

def addperson():
    name = " ".join(line.split()[1:-1])
    date = line.split()[-1]
    nextline()
    if not "[" in line:
        print "Bad team spec:", line
        return
    if not "]" in line:
        print "Very bad team spec:", line
        return
    claim = line.split(".")[0]
    team = line.split("[")[1].split("]")[0]
    nextline()
    if line != "\n":
        try:
       	    email = " ".join(line.split())
        except IndexError:
            print "FAULT:", name
        nextline()
    else:
        email = "<>"
    if line != "\n":
        note = " ".join(line.split())
	nextline()
    else:
        note = "xx"
    if way == "sortbyteam":
        translators.append([team, date, name, email])
    else:
        translators.append([date, name, claim, team, email, note])


translators = []
index = 0

# Read in the disclaimer elements.
while index < len(text):
    nextline()
    if line[:12] == "TRANSLATIONS":
        addperson()
    if line != "\n":
        print line[:-1] 

translators.sort()

if way == "recreate":
    # Recreate the read file in a nearly identical way.
    for person in translators:
        print "TRANSLATIONS\t" + person[1] + "\t" + person[0]
        print person[2] + ".  [" + person[3] + "]"
        if person[4] != "<>":
            print person[4]
        if person[5] != "xx":
            print person[5]
        print
else:
    # Sort the translators by team and year.
    for person in translators:
        print person[0], "\t", person[1][0:4], "\t", person[2]

