import os
import sys
from jash.constants import *


def history(number):
    with open(HISTORY_PATH, 'r') as history:
        lines = history.readlines()

        if len(number) > 0:
            to_be_printed = int(number[0])
        else:
            to_be_printed = len(lines)

        start = len(lines) - to_be_printed

        for i in range(start, len(lines)):
            sys.stdout.write(lines[i])
        sys.stdout.flush()

    return SHELL_STATUS_RUN
