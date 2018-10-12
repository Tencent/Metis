#!/usr/bin/env python
import os
import sys
import signal
import errno


def wait_child(signum, frame):
    print('receive SIGCHLD')
    try:
        while True:
            cpid, status = os.waitpid(-1, os.WNOHANG)
            if cpid == 0:
                print('no child process was immediately available')
                break
            exitcode = status >> 8
            print('child process %s exit with exitcode %s', cpid, exitcode)
    except OSError as e:
        if e.errno == errno.ECHILD:
            print ('current process has no existing unwaited-for child processes.')
        else:
            raise
    print('handle SIGCHLD end')

if __name__ == "__main__":
    signal.signal(signal.SIGCHLD, wait_child)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
