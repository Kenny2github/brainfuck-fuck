import sys
class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

getch = _Getch()

CELLS = [0]
if len(sys.argv) > 1:
    if sys.argv[1] == '-c':
        PRGM = sys.argv[2].strip('"')
    elif sys.argv[1] == '-v':
        PRGM = raw_input('Brainfuck program: ')
    else:
        with open(sys.argv[1]) as f:
            PRGM = f.read()
else:
    PRGM = raw_input('Brainfuck program: ')
CELL = 0
POS = 0
COND = []
LVL = 0
_VERBOSE = '-v' in sys.argv
if len(sys.argv) > 3:
    if sys.argv[3] == '--timeit':
        import time
        print time.time()

while POS < len(PRGM):
    if PRGM[POS] == '+':
        CELLS[CELL] += 1
        if _VERBOSE: print '|'.join([unichr(i) for i in CELLS])
    elif PRGM[POS] == '-':
        CELLS[CELL] -= 1
        if _VERBOSE: print '|'.join([unichr(i) for i in CELLS])
    elif PRGM[POS] == '>':
        CELL += 1
        if len(CELLS) <= CELL:
            CELLS.append(0)
    elif PRGM[POS] == '<':
        CELL -= 1
    elif PRGM[POS] == '.':
        sys.stdout.write(unichr(CELLS[CELL]))
    elif PRGM[POS] == ',':
        try: CELLS[CELL] = ord(getch())
        except IndexError: CELLS[CELL] = 0
        if _VERBOSE: print '|'.join([unichr(i) for i in CELLS])
    elif PRGM[POS] == '[':
        if CELLS[CELL] == 0:
            INC = 0
            POS += 1
            while PRGM[POS] != ']' or INC > 0:
                if PRGM[POS] == '[':
                    INC += 1
                if PRGM[POS] == ']':
                    INC -= 1
                POS += 1
            POS -= 1
    elif PRGM[POS] == ']':
        if CELLS[CELL] != 0:
            INC = 0
            POS -= 1
            while PRGM[POS] != '[' or INC > 0:
                if PRGM[POS] == ']':
                    INC += 1
                if PRGM[POS] == '[':
                    INC -= 1
                POS -= 1
            POS -= 1
    elif PRGM[POS] == '=':
        POS += 1
        CELLS[CELL] = ord(PRGM[POS])
        if _VERBOSE: print '|'.join([unichr(i) for i in CELLS])
    elif PRGM[POS] == '?':
        if CELLS[CELL] == 0:
            INC = 0
            POS += 1
            while PRGM[POS] != ':' or INC > 0:
                if PRGM[POS] == '?':
                    INC += 1
                if PRGM[POS] == '!':
                    INC -= 1
                POS += 1
            POS -= 1
        try: COND[LVL] = bool(CELLS[CELL])
        except IndexError: COND.append(bool(CELLS[CELL]))
        LVL += 1
    elif PRGM[POS] == ':':
        if COND[LVL-1]:
            INC = 0
            POS += 1
            while PRGM[POS] != '!' or INC > 0:
                if PRGM[POS] == '?':
                    INC += 1
                if PRGM[POS] == '!':
                    INC -= 1
                POS += 1
            POS -= 1
        else:
            try: COND[LVL] = False
            except IndexError: COND.append(False)
    elif PRGM[POS] == '!':
        LVL -= 1
    POS += 1
if len(sys.argv) > 3:
    if sys.argv[3] == '--timeit':
        print '\n' + str(time.time())
