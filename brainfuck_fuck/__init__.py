"""
Brainfuck time!

This module contains a single function, "fuck", that does the work.
"""

import sys
import time

from .getch import getch

if sys.version_info.major < 3:
    CFA = unichr
else:
    CFA = chr

def fuck(raw_program):
    """Fuck the brain! :DDD"""
    prog = ''.join([c for c in raw_program if (c in [
        ',', '.', '[', ']', '<', '>', '+', '-',
        '=', '?', ':', '!', '@', '|', '^',
        ] or raw_program[raw_program.index(c)-1] in ['=', '@', '^'])])

    prog = ''.join(prog)
    cells = [0]
    cell = 0
    pos = 0
    cond = []
    lvl = 0
    funcs = {}
    func = False
    start = time.time()

    while pos < len(prog):
        if prog[pos] == '+':
            cells[cell] += 1
        elif prog[pos] == '-':
            cells[cell] -= 1
        elif prog[pos] == '>':
            cell += 1
            if len(cells) <= cell:
                cells.append(0)
        elif prog[pos] == '<':
            cell -= 1
        elif prog[pos] == '.':
            sys.stdout.write(CFA(cells[cell]))
            sys.stdout.flush()
        elif prog[pos] == ',':
            cells[cell] = ord(getch())
        elif prog[pos] == '[':
            if cells[cell] == 0:
                inc = 0
                pos += 1
                while prog[pos] != ']' or inc > 0:
                    if prog[pos] == '[':
                        inc += 1
                    if prog[pos] == ']':
                        inc -= 1
                    pos += 1
                pos -= 1
        elif prog[pos] == ']':
            if cells[cell] != 0:
                inc = 0
                pos -= 1
                while prog[pos] != '[' or inc > 0:
                    if prog[pos] == ']':
                        inc += 1
                    if prog[pos] == '[':
                        inc -= 1
                    pos -= 1
                pos -= 1
        elif prog[pos] == '=':
            pos += 1
            cells[cell] = ord(prog[pos])
        elif prog[pos] == '?':
            if cells[cell] == 0:
                inc = 0
                pos += 1
                while prog[pos] != ':' or inc > 0:
                    if prog[pos] == '?':
                        inc += 1
                    if prog[pos] == '!':
                        inc -= 1
                    pos += 1
                pos -= 1
            try:
                cond[lvl] = bool(cells[cell])
            except IndexError:
                cond.append(bool(cells[cell]))
            lvl += 1
        elif prog[pos] == ':':
            if cond[lvl-1]:
                inc = 0
                pos += 1
                while prog[pos] != '!' or inc > 0:
                    if prog[pos] == '?':
                        inc += 1
                    if prog[pos] == '!':
                        inc -= 1
                    pos += 1
                pos -= 1
            else:
                try:
                    cond[lvl] = False
                except IndexError:
                    cond.append(False)
        elif prog[pos] == '!':
            lvl -= 1
        elif prog[pos] == '@':
            pos += 1
            funcs[prog[pos]] = pos
            inc = 0
            pos += 1
            while prog[pos] != '|' or inc > 0:
                if prog[pos] == '@':
                    inc += 1
                if prog[pos] == '|':
                    inc -= 1
                pos += 1
            pos -= 1
        elif prog[pos] == '^':
            pos += 1
            prev = pos
            pos = funcs[prog[pos]]
            func = True
        elif prog[pos] == '|':
            if func:
                func = False
                pos = prev
        pos += 1

    end = time.time()
    return (cells, prog, end-start)
