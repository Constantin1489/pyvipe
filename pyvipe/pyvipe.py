#!/usr/bin/env python

"""This module contains pyvipe program."""
import os
import subprocess
import sys
import tempfile

def pyvipe():
    """Run pyvipe program."""

    editor = 'vi'
    if os.access('/usr/bin/editor', os.X_OK):
        editor = '/usr/bin/editor'

    if 'EDITOR' in os.environ:
        editor = os.environ['EDITOR']

    if 'VISUAL' in os.environ:
        editor = os.environ['VISUAL']

    text = ''
    if sys.stdin.isatty() is False:
        text = sys.stdin.read()

    stdin_fd = os.open('/dev/tty', os.O_RDONLY)
    os.dup2(stdin_fd, 0)
    os.close(stdin_fd)

    try:
        with tempfile.NamedTemporaryFile() as temporary_file:
            temporary_file.write(text.encode())
            temporary_file.flush()

            try:
                subprocess.check_call([editor, temporary_file.name])

            except subprocess.CalledProcessError:
                print(f'{editor} exited nonzero, aborting', file=sys.stderr)
                sys.exit(1)

            with open(temporary_file.name, 'r', encoding='utf-8') as edited_pipe:
                print(edited_pipe.read(), end='')

    except PermissionError:
        print('cannot create tempfile', file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    pyvipe()
