import os
import sys
import shlex
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


def execute(tokens, REDIR):
    cmd_name = tokens[0]
    cmd_args = tokens[1:]

    # If the command is a built-in command, invoke its function with arguments
    if cmd_name in commands:
        return commands[cmd_name](cmd_args)

    pid = os.fork()

    if pid == 0:
        # Child process
        # Replace the child shell process with the program called with exec
        os.execvp(tokens[0], tokens)
    elif pid > 0:
        # Parent process
        while True:
            # Wait response status from its child process (identified with pid)
            wpid, status = os.waitpid(pid, 0)

            # Finish waiting if its child process exits normally
            # or is terminated by a signal
            if os.WIFEXITED(status) or os.WIFSIGNALED(status):
                break

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

        status = execute(tokens, REDIR)


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
