import os
import subprocess
import sys
import tempfile

EDITOR = 'vi'
if os.access('/usr/bin/editor', os.X_OK):
    EDITOR = '/usr/bin/editor'

if 'EDITOR' in os.environ:
    EDITOR = os.environ['EDITOR']

if 'VISUAL' in os.environ:
    EDITOR = os.environ['VISUAL']

text = ''
if sys.stdin.isatty() is False:
    text = sys.stdin.read()

initial_message = text.encode()

stdin_fd = os.open('/dev/tty', os.O_RDONLY)
os.dup2(stdin_fd, 0)
os.close(stdin_fd)

with tempfile.NamedTemporaryFile() as tf:
    tf.write(initial_message)
    tf.flush()

    subprocess.check_call([EDITOR, tf.name])
    print(open(tf.name).read(), end='')