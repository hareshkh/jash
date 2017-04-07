import os
from jash.constants import *

def cd(args):
	os.chdir(args[0])
	return SHELL_STATUS_RUN