from tkinter import *
from tkinter.ttk import *
from mattycontrols.MattyControls import *
from .mainwin import MainWin
from .key import Key, Scale
from .settings import Settings, Pos, Size


class Application(Frame):
    def __init__(self, settings, master=None):
        """The constructor"""
        frame_init(self, master)
        master.title('Guitar cheat sheet')

        self.ctrl, self.shift, self.alt, self.superkey = False, False, False, False

        self.canvas = Cnvs(master, bd=-2)
        self.canvas.bind('<Button>', self.onMouseDown)
        self.canvas.bind('<Motion>', self.onMouseMove)
        self.canvas.bind('<ButtonRelease>', self.onMouseUp)
        self.master.bind('<Key>', self.onKeyDown)
        self.master.bind('<KeyRelease>', self.onKeyUp)
        self.resize_bind_id = self.master.bind('<Configure>', self.onResizeOrMove)
        self.canvas.highlightthickness = 0
        self.canvas.width = settings.size.w
        self.canvas.height = settings.canvasheight
        self.canvas.locateInside(self, d=0)

        self.dbKey = Db(self, [Key.note2str(i) for i in range(12)], 3)
        self.dbKey.locateFrom(self.canvas, H_COPY_LEFT, V_BOTTOM)
        self.dbKey.x = 10
        self.dbKey.addLabel('Key: ')
        self.dbKey.onChange = lambda *args: self.onChangeAnything()

        self.dbScale = Db(self, ['default', 'pentatonic'], 0)
        self.dbScale.locateFrom(self.dbKey.label, H_COPY_LEFT, V_BOTTOM)
        self.dbScale.addLabel('Scale: ')
        self.dbScale.onChange = lambda *args: self.onChangeAnything()

        self.dbPreset = Db(self, ['guitar', 'soprano ukelele', 'tenor ukelele'], 0)
        self.dbPreset.locateFrom(self.dbScale.label, H_COPY_LEFT, V_BOTTOM)
        self.dbPreset.addLabel('Preset: ')
        self.dbPreset.onChange = lambda *args: self.onChangeAnything()

        self.cbNotes = Cb(self, text='Display notes')
        self.cbNotes.locateFrom(self.canvas, H_COPY_RIGHT, V_BOTTOM)
        self.cbNotes.onChange = lambda *args: self.onChangeAnything()

        self.btnQuit = Btn(self, text='Quit', command=self.quit)
        self.btnQuit.locateInside(self, H_RIGHT, V_BOTTOM)

        self.settings = settings

        self.mainWindow = MainWin(settings, self)
        self.onChangeAnything()

        self.master.after(int(self.settings.fps_inv * 1000), self.loop)

    def onChangeAnything(self):
        """This method is called whenever a control changed value"""
        scale = Scale.default
        if self.dbScale.selectedValue == 'pentatonic':
            scale = Scale.pentatonic
        necksize = Size(14, 6)
        tuning = ['E','B','G','D','A','E']
        if self.dbPreset.selectedValue == 'soprano ukelele':
            necksize = Size(12, 4)
            tuning = ['A','E','C','G']
        elif self.dbPreset.selectedValue == 'tenor ukelele':
            necksize = Size(14, 4)
            tuning = ['G#', 'Eb', 'B', 'F#']
        displayNotes = self.cbNotes.checked
        self.mainWindow.change(self.dbKey.selectedValue, scale, necksize, [Key.str2note(c) for c in tuning], displayNotes)

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
    root.geometry('{}x{}'.format(settings.size.w, settings.size.h))
    app = Application(settings, master=root)
    app.mainloop()

