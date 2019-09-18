"""
Command line interface for brainfuck programs.
"""

from __future__ import print_function
import sys
import os
import math
import argparse

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import brainfuck_fuck

def main(args=None):
    """Command-line brainfucking."""

    argp = argparse.ArgumentParser(description='Fuck the brain.')
    argp.add_argument('--stats', action='store_true',
                      help='Show stats after running')
    argp.add_argument('--dump', action='store_true',
                      help='Dump memory after running. Implies --stats')
    argp.add_argument('file', nargs='?', default=None,
                      help='Filename of Brainfuck program to run. Use - or '
                      'leave unspecified to read from stdin. Ignored if '
                      '-c is specified')
    argp.add_argument('-m', nargs='?', default=None,
                      help='Filename to read initial memory from. Data is '
                      'directly translated into memory')
    argp.add_argument('-c', nargs=argparse.REMAINDER, default=None,
                      help='Everything after this option is the Brainfuck '
                      'program to run')
    args = argp.parse_args(args)

    if args.c:
        prog = ' '.join(args.c)
    elif args.file != '-' and args.file:
        with open(args.file) as progfile:
            prog = progfile.read()
    elif args.file == '-':
        prog = sys.stdin.read()
    else:
        prog = input('Brainfuck program:\n')

    mem = b'\0'
    if args.m:
        with open(args.m, 'rb') as memfile:
            mem = memfile.read()

    mem, prog, tm = brainfuck_fuck.fuck(prog, mem)

    if args.stats or args.dump:
        print()
        print('Space used:', len(mem), 'cells')
        if args.dump:
            rlen = len(mem)
            s = ' '.join(i.rjust(2, ' ') for i in '0123456789ABCDEF'[:rlen])
            print('      | ' + s)
            print('-' * 6 + '+' + '-' * len(s))
            rows = math.ceil(rlen / 16)
            for i in range(rows):
                r = hex(i * 16)[2:-1].zfill(len(hex(rlen // 16 * 16)[2:]) - 1) + 'x'
                print(
                    r + ' ' * (6 - len(r)) + '| '
                    + ' '.join(
                        hex(mem[i*16+j])[2:].upper().zfill(2)
                        for j in range(16)
                        if i*16+j < rlen
                    )
                )
        print('Length of parsed program:', len(prog))
        print('Time used:', tm, 'seconds')

if __name__ == '__main__':
    main()
