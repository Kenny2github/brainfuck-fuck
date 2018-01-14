"""
Command line interface for brainfuck programs.
"""

from __future__ import print_function
import sys
import brainfuck_fuck

def main(args=None):
    """Command-line brainfucking."""
    if args is None:
        args = sys.argv[1:]

    if '--stats' in args:
        args.remove('--stats')
        args.append('--stats')
    if len(args) > 1:
        if args[0] == '-c':
            prog = args[1].strip('"')
        else:
            with open(args[0], 'rb') as progfile:
                prog = progfile.read()
    else:
        print('Brainfuck program:')
        prog = sys.stdin.readline()

    results = brainfuck_fuck.fuck(prog)

    if '--stats' in args:
        print()
        print('Space used:', len(results[0]), 'cells')
        print('Length of parsed program:', len(results[1]))
        print('Time used:', results[2], 'seconds')
