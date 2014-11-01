from .key import *
from . import colors
import tkinter.font


class Settings():
    """The settings class"""

    def __init__(self):
        self.size = Size(1111, 470)
        self.canvasheight = 300
        self.offset = Pos(40, 20)
        self.necksize = Size(14, 6)
        self.sqsize = Size(75, 40)
        self.tuning = []
        self.displayNotes = True
        self.font = ('Consolas', 16)
        self.colors = colors.Colors()
        self.fps_inv = 1/30                       # seconds per frame
        self.calcFontWidths()

    def calcFontWidths(self):
        fonts = [tkinter.font.Font(family=fam, size=pt) for fam, pt in [self.font]]
        self.fontsize = Size(fonts[0].measure('a'), fonts[0].metrics("linespace"))

    def load(self):
        """Load all the settings from json file"""
        pass

    def save(self):
        """Write the settings to a json file"""
        pass


class Pos():
    """A position class just to make things a bit easier."""
    def __init__(self, x, y=None):
        if y == None:
            self.x, self.y = x
        else:
            self.x, self.y = x, y

    @property
    def t(self):
        return (self.x, self.y)

    def __getitem__(self, i):
        if i==0:
            return self.x
        return self.y

    def __add__(self, other):
        return Pos(self.x + other[0], self.y + other[1])
    def __radd__(self, other):
        return other + self
    def __sub__(self, other):
        return self + (-other[0], -other[1])

    def __eq__(self, other):
        if other is None:
            return False
        return self.x == other[0] and self.y == other[1]
    def __neq__(self, other):
        return not self == other


class Size():
    """A size class just to make things a bit easier."""
    def __init__(self, w, h=None):
        if h == None:
            self.w, self.h = w
        else:
            self.w, self.h = w, h

    @property
    def t(self):
        return (self.w, self.h)

    def __getitem__(self, i):
        if i==0:
            return self.w
        return self.h

    def __add__(self, other):
        return Size(self.w + other[0], self.h + other[1])
    def __radd__(self, other):
        return other + self
    def __sub__(self, other):
        return self + (-other[0], -other[1])

    def __eq__(self, other):
        if other is None:
            return False
        return self.w == other[0] and self.h == other[1]
    def __neq__(self, other):
        return not a == other

