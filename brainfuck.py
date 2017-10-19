import sys
CELLS = [0]
if len(sys.argv) > 1:
    if sys.argv[1] == '-c':
        PRGM = sys.argv[2].strip('"')
    else:
        with open(sys.argv[1]) as f:
            PRGM = f.read()
else:
    PRGM = raw_input('Brainfuck program: ')
CELL = 0
POS = 0
if len(sys.argv) > 3:
    if sys.argv[3] == '--timeit':
        import time
        print time.time()

while POS < len(PRGM):
    if PRGM[POS] == '+':
        CELLS[CELL] += 1
    elif PRGM[POS] == '-':
        CELLS[CELL] -= 1
    elif PRGM[POS] == '>':
        CELL += 1
        if len(CELLS) <= CELL:
            CELLS.append(0)
    elif PRGM[POS] == '<':
        CELL -= 1
    elif PRGM[POS] == '.':
        sys.stdout.write(unichr(CELLS[CELL]))
    elif PRGM[POS] == ',':
        CELLS[CELL] = ord(raw_input()[0])
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
    POS += 1
if len(sys.argv) > 3:
    if sys.argv[3] == '--timeit':
        print '\n' + str(time.time())
