"""
Brainfuck time!

This module contains a single function, "fuck", that does the work.
"""
from __future__ import print_function

__all__ = ['fuck', 'BF_CHARS', 'BF_ARGCHARS']

import sys
import time

from .getch import getch

BF_CHARS = '+-<>[].,=?:!@|^'
BF_ARGCHARS = '=@^'

if sys.version_info.major < 3:
    CFA = unichr
else:
    CFA = chr

def fuck(raw_program, starting_memory=b'\0'):
    """Fuck the brain! :DDD

    Arguments:
    ``raw_program`` - the brainfuck program in question
    ``starting_memory`` - bytes to load as initial memory
    """
    prog = ''.join(
        c for i, c in enumerate(raw_program)
        if (c in BF_CHARS)
        or raw_program[i-1] in BF_ARGCHARS
    )
    cells = bytearray(starting_memory or b'\0')
    cell = 0
    pos = 0
    cond = []
    lvl = 0
    funcs = {}
    func = False
    start = time.time()

    while pos < len(prog):
        if prog[pos] == '+':
            try:
                cells[cell] += 1
            except ValueError:
                cells[cell] = 0
        elif prog[pos] == '-':
            try:
                cells[cell] -= 1
            except ValueError:
                cells[cell] = 255
        elif prog[pos] == '>':
            cell += 1
            if cell >= len(cells):
                cells.append(0)
        elif prog[pos] == '<':
            cell -= 1
            if cell < 0:
                cell += 1
                cells.insert(0, 0)
        elif prog[pos] == '.':
            print(CFA(cells[cell]), end='')
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
