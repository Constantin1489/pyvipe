import os
import subprocess
import sys
import tempfile

if os.access('/usr/bin/editor', os.X_OK):
    EDITOR = '/usr/bin/editor'

if 'EDITOR' in os.environ:
    EDITOR = os.environ['EDITOR']

if 'VISUAL' in os.environ:
    EDITOR = os.environ['VISUAL']

text = sys.stdin.read()
initial_message = text.encode()

with tempfile.NamedTemporaryFile(suffix=".tmp") as tf: 
    tf.write(initial_message)
    tf.flush()

    stdin_fd = os.open('/dev/tty', os.O_RDONLY)
    os.dup2(stdin_fd, 0)
    os.close(stdin_fd)

#    stdout_fd = os.open('/dev/tty', os.O_WRONLY)
#    os.dup2(stdout_fd, 0)
#    os.close(stdout_fd)

    subprocess.check_call([EDITOR, tf.name])
    print(open(tf.name).read(), end='')
