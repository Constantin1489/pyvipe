#!/usr/bin/env python
"""This module contains pyvipe program."""

import os
import subprocess
import sys
import tempfile
import argparse

VERSION_HELP = """pyvipe - 0.2.2
Copyright (C) 2023 Constantin Hong
License GPLv2: GNU GPL version 2 <https://gnu.org/licenses/gpl.html>.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law."""
WINDOWS_LINE_ENDING = b'\r\n'
UNIX_LINE_ENDING = b'\n'

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
            '--universal-newline',
            action='store_true',
            dest='universal_newline',
            help='Print stdout with a universal newline.',
            )
    parser.add_argument(
            '-V', '--version',
            action='version',
            version=VERSION_HELP,
            help='Print a version number and a license of pyvipe.',
            )

    parsed_arg = parser.parse_args(sys.argv[1:])

    suffix = parsed_arg.suffix
    if suffix:
        suffix = suffix if suffix.startswith('.') else f'.{suffix}'

    editor = 'vi'
    if os.access('/usr/bin/editor', os.X_OK):
        editor = '/usr/bin/editor'

    if 'EDITOR' in os.environ:
        editor = os.environ['EDITOR']

    if 'VISUAL' in os.environ:
        editor = os.environ['VISUAL']


    # if there is no PIPE, then open an empty file.
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
                subprocess.check_call([*editor.split(), temporary_file.name])

            except subprocess.CalledProcessError:
                print(f'{editor} exited nonzero, aborting', file=sys.stderr)
                sys.exit(1)

            try:
                with open(temporary_file.name, 'rb') as edited_pipe:
                    binary_edited_pipe = edited_pipe.read()

                    # if option is true, then read CRLF PIPE and return LF(\n) stdout.
                    if parsed_arg.universal_newline:
                        # prevent pyvipe to change encoding.
                        binary_edited_pipe = binary_edited_pipe.replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)

                    os.write(out, binary_edited_pipe)

            except PermissionError:
                print('cannot read tempfile', file=sys.stderr)
                sys.exit(1)

    except PermissionError:
        print('cannot create tempfile', file=sys.stderr)
        sys.exit(1)

    os.close(out)

if __name__ == "__main__":
    pyvipe()
