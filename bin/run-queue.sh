#!/bin/sh
# Process the mail queue meant for the TP-robot.
# Copyright © 2007 Translation Project.
# Copyright © 1999 Progiciels Bourbeau-Pinard inc.
# François Pinard <pinard@iro.umontreal.ca>, 1999.

PYTHON=python

MAILDIR=~/Mail
progsdir=~/progs

TP_QUEUE=$MAILDIR/bot-queue
TP_QUEUE_LOCK=$MAILDIR/bot-queue.lock
TP_EXEC=$MAILDIR/bot-exec
TP_EXEC_LOCK=$MAILDIR/bot-exec.lock


# Don't handle mail when an admin is busy with
# things that modify the cache/postats file.
if ps ax | grep -q tp/progs/bin/[p]o-register; then
  exit 0
elif ps ax | grep -q tp/progs/bin/[c]alc-postats; then
  exit 0
fi

if [ ! -f $TP_EXEC ]; then
  lockfile $TP_EXEC_LOCK
    if [ -f $TP_QUEUE -a ! -f $TP_EXEC ]; then
      lockfile $TP_QUEUE_LOCK
	if [ -f $TP_QUEUE ]; then
	  mv $TP_QUEUE $TP_EXEC
	fi
      rm -f $TP_QUEUE_LOCK
    fi
  rm -f $TP_EXEC_LOCK
fi

if [ -f $TP_EXEC ]; then
  lockfile $TP_EXEC_LOCK
    if [ -f $TP_EXEC ]; then
      # Let the robot handle the arrived emails.
      formail -s $PYTHON $progsdir/bin/tp-robot <$TP_EXEC
      rm -f $TP_EXEC
    fi
  rm -f $TP_EXEC_LOCK
fi

exit 0
