import sys


class color:

    default = '\033[39;0m'
    default_bold = '\033[39;1m'
    red = '\033[31;0m'
    red_bold = '\033[31;1m'
    green = '\033[32;0m'
    green_bold = '\033[32;1m'
    yellow = '\033[33;0m'
    yellow_bold = '\033[33;1m'
    blue = '\033[34;0m'
    blue_bold = '\033[34;1m'

    def setc(self, clr, bold):
        clr = clr.lower()
        if bold:
            if clr == "default":
                sys.stdout.write(self.default_bold)
            elif clr == "red":
                sys.stdout.write(self.red_bold)
            elif clr == "green":
                sys.stdout.write(self.green_bold)
            elif clr == "yellow":
                sys.stdout.write(self.yellow_bold)
            elif clr == "blue":
                sys.stdout.write(self.blue_bold)
        else:
            if clr == "default":
                sys.stdout.write(self.default)
            elif clr == "red":
                sys.stdout.write(self.red)
            elif clr == "green":
                sys.stdout.write(self.green)
            elif clr == "yellow":
                sys.stdout.write(self.yellow)
            elif clr == "blue":
                sys.stdout.write(self.blue)
        sys.stdout.flush()
