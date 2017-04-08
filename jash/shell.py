import os
import shlex
import signal
import subprocess
import sys
from jash.constants import *
from jash.inbuilt import *

# Stores built in commands
commands = {}

# Stores I/O redirection status
# normal - 0
# >      - 1
# <      - 2
REDIR = 0


def tokenize(string):
    return shlex.split(string)


def handler_kill(signum, frame):
    raise OSError("Killed!")


def execute(tokens, cmd, REDIR):
    cmd_name = tokens[0]
    cmd_args = tokens[1:]

    # If the command is a built-in command, invoke its function with arguments
    if cmd_name in commands:
        return commands[cmd_name](cmd_args)

    signal.signal(signal.SIGINT, handler_kill)
    # Spawn a child process
    p = subprocess.Popen(tokens)
    # Parent process read data from child process
    # and wait for child process to exit
    p.communicate()

    return SHELL_STATUS_RUN


def shell_loop():
    status = SHELL_STATUS_RUN

    while status == SHELL_STATUS_RUN:
        sys.stdout.write('> ')
        sys.stdout.flush()

        cmd = sys.stdin.readline()

        # Tokenize the command input
        # string.split() not used due to problem with string type arguments
        # like ' echo "Hello World" '
        tokens = tokenize(cmd)

        if ">" in tokens:
            REDIR = 1
        elif "<" in tokens:
            REDIR = 2
        else:
            REDIR = 0

        status = execute(tokens, cmd, REDIR)


def register_command(name, func):
    commands[name] = func


def init():
    register_command("cd", cd)
    register_command("exit", exit)


def main():
    init()
    shell_loop()


if __name__ == "__main__":
    main()
