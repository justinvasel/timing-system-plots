import sys

# /////////////////////////////////////////////////////////////////////////////
def progressBar(value, endvalue, bar_length = 40):
    percent = float(value) / endvalue
    arrow = '=' * int(round(percent * bar_length) - 1) + '>'
    spaces = ' ' * (bar_length - len(arrow))

    sys.stdout.write("\rProgress: [\033[01;32m{0}\033[00m] {1}/{2} ({3}%)".format(arrow + spaces, value, endvalue, int(round(percent * 100))))
    sys.stdout.flush()
