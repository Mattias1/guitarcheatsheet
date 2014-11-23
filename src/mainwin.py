from .win import *
from .key import *
from .colors import *


class MainWin(Win):
    """
    The main window class
    This is the main window for the guitar theory thingy.
    """

    def __init__(self, settings, app):
        Win.__init__(self, settings, app)

        self.key = Key('C')
        self.highlightSet = set()

    def draw(self):
        """Draw the main window"""
        st = self.settings
        cl = self.colors
        w, h = st.sqsize.t

        self.fullClear()

        # Draw valid tones
        for y in range(st.necksize.h):
            for x in range(st.necksize.w):
                nr = self.baseNote(y) + x + 1
                idx = self.key.getIndex(nr)
                highLight = False
                if idx > -1:
                    self.drawRect(cl.selectionbg, st.offset + (x * w, y * h), st.sqsize)
                    highLight = True
                if nr % 12 in self.highlightSet:
                    self.drawRect(cl.highlightbg, st.offset + (x * w, y * h), st.sqsize)
                    highLight = True
                if highLight:
                    s = Key.note2str(nr % 12) if st.displayNotes else str(idx)
                    if s != '-1':
                        self.drawString(s, cl.text, st.offset + (x * w, y * h) + (w // 2, h // 2), "center")

        # Draw string names
        sqWidth = 14
        fadeWidth = 19
        for i in range(st.necksize.h):
            nr = st.tuning[i]
            clr = cl.highlightbg if nr in self.highlightSet else cl.selectionbg
            idx = self.key.getIndex(nr)
            if idx > -1: # TODO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                self.drawRect(clr, st.offset + (-sqWidth, i * h), Size(sqWidth, st.sqsize.h))
                for j in range(fadeWidth):
                    c = cl.hexlerp(cl.bg, clr, 1 - j / fadeWidth)
                    self.drawRect(c, st.offset + (-sqWidth - j, i * h), Size(1, st.sqsize.h))
            self.drawString(Key.note2str(nr), cl.text, st.offset + (-9, i * h + h // 2), "e")

        # Draw guitar neck
        for i in range(st.necksize.h + 1): # Horizontal lines
            self.drawLine(cl.text, st.offset + (-3, i * h), st.offset + (st.necksize.w * w, i * h))
        for i in range(st.necksize.w + 1): # Vertical lines
            self.drawLine(cl.text, st.offset + (i * w, 0), st.offset + (i * w, st.necksize.h * h))
        self.drawLine(cl.text, st.offset + (-3, 0), st.offset + (-3, st.necksize.h * h))
        for i in [5, 7, 10, 12]: # Mark some fret numbers
            self.drawString(str(i), cl.text, st.offset + (i * w - w // 2, st.necksize.h * h + 3), "n")

    def change(self, key, scale, necksize, tuning, highlightSet, displayNotes):
        """Call this function to update some settings"""
        self.settings.necksize = necksize
        self.settings.tuning = tuning
        self.settings.displayNotes = displayNotes
        self.key = Key(key, scale)
        self.highlightSet = highlightSet

        self.draw()

    def resize(self, s=None, draw=True):
        """Override the resize window"""
        Win.resize(self, s, False)

        if draw:
            self.draw()

    def onKeyDown(self, c):
        if c == 'Esc':
            self.app.quit()

    def baseNote(self, y):
        """Get the base tone of a string"""
        return self.settings.tuning[y]

