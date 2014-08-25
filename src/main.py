from tkinter import *
from tkinter.ttk import *
from mattycontrols.MattyControls import *
from .mainwin import MainWin
from .settings import Settings, Pos, Size


class Application(Frame):
    def __init__(self, settings, master=None):
        """The constructor"""
        Frame.__init__(self, master)
        master.title("Guitar theory helper")

        self.ctrl, self.shift, self.alt, self.superkey = False, False, False, False

        self.canvas = Cnvs(master, bd=-2)
        self.canvas.bind("<Button>", self.onMouseDown)
        self.canvas.bind("<Motion>", self.onMouseMove)
        self.canvas.bind("<ButtonRelease>", self.onMouseUp)
        self.master.bind("<Key>", self.onKeyDown)
        self.master.bind("<KeyRelease>", self.onKeyUp)
        self.resize_bind_id = self.master.bind("<Configure>", self.onResizeOrMove)
        self.canvas.highlightthickness = 0
        self.canvas.width = settings.size.w
        self.canvas.height = settings.canvasheight
        self.canvas.locateInside(self, d=0)

        self.mainWindow = MainWin(settings, self)
        self.mainWindow.draw()

        self.settings = settings

        self.master.after(int(self.settings.fps_inv * 1000), self.loop)

    def onMouseDown(self, event):
        self.mainWindow.onMouseDown(Pos(event.x, event.y), event.num)

    def onMouseMove(self, event):
        self.mainWindow.onMouseMove(Pos(event.x, event.y), event.num)

    def onMouseUp(self, event):
        self.mainWindow.onMouseUp(Pos(event.x, event.y), event.num)

    def onKeyDown(self, event):
        if self.setModifyKeys(event, True):
            self.mainWindow.onKeyDown(self.getchar(event))

    def onKeyUp(self, event):
        self.setModifyKeys(event, False)

    def setModifyKeys(self, event, value):
        # Set the modify keys and return whether or not something has to be done still.
        if event.keysym_num in {65505, 65506}:
            self.shift = value
        elif event.keysym_num in {65507, 65508}:
            self.ctrl = value
        elif event.keysym_num in {65513, 65514}:
            self.alt = value
        elif event.keysym_num in {65371, 65372, 65515, 65516}:
            self.superkey = value
        else:
            return True
        return False

    def onResizeOrMove(self, event):
        # s = Size(event.width, event.height)
        # if s != self.settings.size:
        #     self.settings.size = s
        #     self.canvas.width, self.canvas.height = s.w, self.settings.canvasheight
        #     self.mainWindow.resize(Size(s.w, self.settings.canvasheight))
        pass

    def loop(self):
        """Private method to manage the loop method"""
        self.mainWindow.loop()
        self.master.after(int(self.settings.fps_inv * 1000), self.loop)

    def getchar(self, e):
        """Convert a tkinter event (given these three different representations of the same char)"""
        # Get prefixes
        prefix = ('Ctrl-' if self.ctrl else '') + ('Alt-' if self.alt else '') + ('Super-' if self.superkey else '')

        # Some basic key mapping
        num = e.keysym_num
        name = e.keysym
        if 31 < num < 256:
            c = chr(num)
        else:
            c = name

        # Some exceptopns
        if num == 65307: c = 'Esc'
        elif num == 65288: c = '\b'
        elif num == 65293: c = '\n'
        elif num == 65289: c = 'Backtab' if self.shift else '\t'

        return prefix + c


def main():
    """The main entrypoint for this application"""
    root = Tk()
    settings = Settings()
    root.configure(bg=settings.colors.bg)
    root.geometry("{}x{}".format(settings.size.w, settings.size.h))
    app = Application(settings, master=root)
    app.mainloop()

