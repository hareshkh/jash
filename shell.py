import os
import sys
import shlex

SHELL_STATUS_RUN = 1
SHELL_STATUS_STOP = 0

def tokenize(string):
	return shlex.split(string)

def execute(cmd_tokens):
	pid = os.fork()

	if pid == 0:
	# Child process
		# Replace the child shell process with the program called with exec
		os.execvp(cmd_tokens[0], cmd_tokens)
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
		# string.split() not used due to problem with string type arguments like ' echo "Hello World" '
		cmd_tokens = tokenize(cmd)

		status = execute(cmd_tokens)

def main():
	shell_loop()

if __name__ == "__main__":
	main()