#!/usr/bin/env python
"""This module contains pyvipe program."""

import os
import subprocess
import sys
import tempfile
import argparse

VERSION_HELP = """pyvipe - 0.1.3
Copyright (C) 2023 Constantin Hong
License GPLv2: GNU GPL version 2 <https://gnu.org/licenses/gpl.html>.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law."""

def pyvipe():
    """Run pyvipe program."""

    parser = argparse.ArgumentParser(
            prog='pyvipe',
            description='edit pipe.',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            )
    parser.add_argument(
            '--suffix',
            action='store',
            dest='suffix',
            default=None,
            help='Add suffix to enable syntax highlighting in your editor.',
            )
    parser.add_argument(
            '-V', '--version',
            action='version',
            version=VERSION_HELP,
            help='Print a version number and a license of pyvipe.',
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

    out = os.dup(1)

    stdout_fd = os.open('/dev/tty', os.O_WRONLY)
    os.dup2(stdout_fd, 1)
    os.close(stdout_fd)

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
                with open(temporary_file.name, 'rb') as edited_pipe:
                    os.write(out, edited_pipe.read())

            except PermissionError:
                print('cannot read tempfile', file=sys.stderr)
                sys.exit(1)

    except PermissionError:
        print('cannot create tempfile', file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    pyvipe()
