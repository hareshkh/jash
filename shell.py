import os
import sys

work = True
input_cmd = ""
while work:
	sys.stdout.write("> ")
	sys.stdout.flush()
	input_cmd = raw_input()
	if (input_cmd == "exit"):
		work = False
	else:
		os.system(input_cmd)