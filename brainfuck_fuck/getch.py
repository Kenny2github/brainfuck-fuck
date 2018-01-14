"""
Module for universally getting a character from standard input.
Taken from http://code.activestate.com/recipes/134892/
"""
import sys

class _Getch(object):
    """Gets a single character from standard input.
    Does not echo to the screen.
    """
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self):
        return self.impl()

class _GetchUnix(object):
    """Get a character from Unix-style input."""
    def __init__(self):
        import tty
        self.tty = tty
    def __call__(self):
        import termios
        tty = self.tty
        fileno = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fileno)
        try:
            tty.setraw(sys.stdin.fileno())
            char = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fileno, termios.TCSADRAIN, old_settings)
        return char

class _GetchWindows(object):
    """Get a character from Windows-style input."""
    def __init__(self):
        import msvcrt
        self.msvcrt = msvcrt

    def __call__(self):
        return self.msvcrt.getch()

_GETCH = _Getch()

def getch():
    """Do the thing."""
    return _GETCH()
