import os
import getpass
import shlex
import signal
import socket
import subprocess
import sys
from jash.constants import *
from jash.inbuilt import *
from jash.helpers import *

# Stores built in commands
commands = {}

# Stores I/O redirection status
REDIR = 0

# Sets the color
c = color()


def ignore_signals():
    # Ignore Ctrl-Z stop signal
    signal.signal(signal.SIGTSTP, signal.SIG_IGN)
    # Ignore Ctrl-C interrupt signal
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def convert_env_var(tokens):
    processed_token = []
    for token in tokens:
        # Convert $-prefixed token to value of an environment variable
        if token.startswith('$'):
            processed_token.append(os.getenv(token[1:]))
        else:
            processed_token.append(token)
    return processed_token


def tokenize(string):
    return shlex.split(string)


def handler_kill(signum, frame):
    raise OSError("Killed!")


def display_prompt():
    # Get user and hostname
    user = getpass.getuser()
    hostname = socket.gethostname()

    # Get base directory (last part of the curent working directory path)
    cwd = os.getcwd()
    base_dir = os.path.basename(cwd)

    # Use ~ instead if a user is at his/her home directory
    home_dir = os.path.expanduser('~')
    if cwd == home_dir:
        base_dir = '~'

    # Print out to console
    c.setc("green", True)
    sys.stdout.write("[%s@%s %s]$ " % (user, hostname, base_dir))
    sys.stdout.flush()
    c.setc("default", False)


def execute(tokens, cmd, REDIR):
    cmd_name = tokens[0]
    cmd_args = tokens[1:]

    # If the command is a built-in command, invoke its function with arguments
    if cmd_name in commands:
        return commands[cmd_name](cmd_args)

    signal.signal(signal.SIGINT, handler_kill)
    # Spawn a child process
    if REDIR == 0:
        p = subprocess.Popen(tokens)
    else:
        p = subprocess.Popen(cmd, shell=True)
    # Parent process read data from child process
    # and wait for child process to exit
    p.communicate()

    return SHELL_STATUS_RUN


def shell_loop():
    status = SHELL_STATUS_RUN

    while status == SHELL_STATUS_RUN:
        display_prompt()
        ignore_signals()

        cmd = sys.stdin.readline()

        # Tokenize the command input
        # string.split() not used due to problem with string type arguments
        # like ' echo "Hello World" '
        tokens = tokenize(cmd)

        if ">" in tokens:
            REDIR = 1
        elif ">>" in tokens:
            REDIR = 2
        elif "<" in tokens:
            REDIR = 3
        elif "<<" in tokens:
            REDIR = 4
        elif "|" in tokens:
            REDIR = 5
        else:
            REDIR = 0

        tokens = convert_env_var(tokens)
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
