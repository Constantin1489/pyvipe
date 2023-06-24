#!/usr/bin/env python
"""This module contains pyvipe program."""

import os
import subprocess
import sys
import tempfile
import argparse

def pyvipe():
    """Run pyvipe program."""

    parser = argparse.ArgumentParser(
            prog='pyvipe',
            description='edit pipe.',
            )
    parser.add_argument(
            '--suffix',
            action='store',
            dest='suffix',
            default=None,
            help='Add suffix to enable syntax highlighting in your editor.',
            )

    suffix = parser.parse_args(sys.argv[1:]).suffix
    if suffix:
        suffix = suffix if suffix.startswith('.') else f'.{suffix}'

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
        with tempfile.NamedTemporaryFile(suffix=suffix) as temporary_file:
            temporary_file.write(text.encode())
            temporary_file.flush()

            try:
                subprocess.check_call([editor, temporary_file.name])

            except subprocess.CalledProcessError:
                print(f'{editor} exited nonzero, aborting', file=sys.stderr)
                sys.exit(1)

            try:
                with open(temporary_file.name, 'r', encoding='utf-8') as edited_pipe:
                    print(edited_pipe.read(), end='')

            except PermissionError:
                print('cannot read tempfile', file=sys.stderr)
                sys.exit(1)

    except PermissionError:
        print('cannot create tempfile', file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    pyvipe()
