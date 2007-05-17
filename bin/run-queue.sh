#!/bin/sh
# Run the queue meant for the translation project robot.
# Copyright © 1999 Progiciels Bourbeau-Pinard inc.
# François Pinard <pinard@iro.umontreal.ca>, 1999.

export PATH=/usr/local/bin:/usr/ucb:/usr/bin:/bin
#export LD_LIBRARY_PATH=/usr/local/lib:/usr/lib

maildir=/mail/gnutra
podir=/home/www/usagers/gnutra/HTML

tp_queue_lock=$maildir/tpr-queue-lock
tp_queue=$maildir/tpr-queue
tp_exec_lock=$maildir/tpr-exec-lock
tp_exec=$maildir/tpr-exec

PYTHON=python

/usr/kerberos/bin/kinit gnutra < /u/gnutra/.pass >/dev/null

if [ ! -f $tp_exec ]; then
  lockfile $tp_exec_lock
    if [ -f $tp_queue -a ! -f $tp_exec ]; then
      lockfile $tp_queue_lock
	if [ -f $tp_queue ]; then
	  mv $tp_queue $tp_exec
	fi
      rm -f $tp_queue_lock
    fi
  rm -f $tp_exec_lock
fi

if [ -f $tp_exec ]; then
  lockfile $tp_exec_lock
    if [ -f $tp_exec ]; then
      formail -s $PYTHON $podir/bin/tp-robot -r < $tp_exec
      rm -f $tp_exec
    fi
  rm -f $tp_exec_lock
fi

exit 0
