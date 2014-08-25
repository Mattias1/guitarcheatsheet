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
                if idx > -1:
                   self.drawRect(cl.selectionbg, st.offset + (x * w, y * h), st.sqsize)
                   self.drawString(str(idx), cl.text, st.offset + (x * w, y * h) + (w // 2, h // 2), "center")

        # Draw guitar neck
        for i in range(st.necksize.h + 1): # Horizontal lines
            self.drawLine(cl.text, st.offset + (-3, i * h), st.offset + (st.necksize.w * w, i * h))
            if i < st.necksize.h:
                self.drawString(Key.note2str(st.tuning[i]), cl.text, st.offset + (-9, i * h + h // 2), "e")
        for i in range(st.necksize.w + 1): # Vertical lines
            self.drawLine(cl.text, st.offset + (i * w, 0), st.offset + (i * w, st.necksize.h * h))
        self.drawLine(cl.text, st.offset + (-3, 0), st.offset + (-3, st.necksize.h * h))
        for i in [5, 7, 10, 12]:
            self.drawString(str(i), cl.text, st.offset + (i * w - w // 2, st.necksize.h * h + 3), "n")

    def change(self, key, scale, necksize, tuning):
        """Call this function to update some settings"""
        self.settings.necksize = necksize
        self.settings.tuning = tuning
        self.key = Key(key, scale)

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

